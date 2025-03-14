#!/usr/bin/python3 -Wignore

# Usage: host pdu1_host pdu1_port pdu2_host pdu2_port

import requests
import base64
import json
import time
import sys

fail = False
host = sys.argv[1]
pdu_1_data = {"host":sys.argv[2], "port":sys.argv[3]}
pdu_2_data = {"host":sys.argv[4], "port":sys.argv[5]}

def pdu_port_status(session_obj,session_hdr,pduhost,pduport):
    try:
        portinfo = session_obj.get("https://"+pduhost+"/redfish/v1/PowerEquipment/RackPDUs/1/Outlets/OUTLET"+pduport, headers=session_hdr, verify=False, stream=False)
        portdict = portinfo.json()
        return portdict['PowerState']
    except Exception as err:
        print(f"FAILED\nAn unexpected error occurred: {err}")
        sys.exit(2)

def drac_psu_status(session_obj,session_hdr,psu):
    try:
        psuinfo = session_obj.get("https://"+host+"-drac/redfish/v1/Chassis/System.Embedded.1/Power/Oem/Dell/DellPowerSupplyInventory/PSU.Slot."+str(psu), headers=session_hdr, verify=False, stream=False)
        psudict = psuinfo.json()
        return psudict['DetailedState']
    except Exception as err:
        print(f"FAILED\nAn unexpected error occurred: {err}")
        sys.exit(3)

def drac_syspwr_status(session_obj,session_hdr):
    try:
        syspwrinfo = session_obj.get("https://"+host+"-drac/redfish/v1/Chassis/System.Embedded.1/", headers=session_hdr, verify=False, stream=False)
        syspwrdict = syspwrinfo.json()
        return syspwrdict['PowerState']
    except Exception as err:
        print(f"FAILED\nAn unexpected error occurred: {err}")
        sys.exit(4)

def pdu_setstate(session_obj,session_hdr,pduhost,pduport,state):
    global fail

    # Define request json
    power_dict = {"OutletNumber":int(pduport),"StartupState":"on","Outletname":"OUTLET"+str(pduport),"OnDelay":0,"OffDelay":0,"RebootDelay":5,"OutletStatus":state}
    power_json = json.dumps(power_dict, indent=2)

    action_header = {"Content-type":"application/json","X-Auth-Token":session_hdr['X-Auth-Token']}

    # Perform power action
    try:
        pwraction = session_obj.post("https://"+pduhost+"/redfish/v1/PowerEquipment/RackPDUs/1/Outlets/OUTLET"+str(pduport)+"/Outlet.PowerControl",data=power_json, verify=False, headers=action_header, stream=False)

        # Check for success
        if pwraction.json()['OutletStatus'] == state:
            print(pduhost+" port "+pduport+" powered "+state+" successfully.")
        else:
            print(pduhost+" port "+pduport+" powered "+state+" FAILED.")
            fail = True

        time.sleep(30)
    except Exception as err:
        print(f"FAILED\nAn unexpected error occurred: {err}")
        sys.exit(5)

def show_status(test=0,desstate=0):
    global fail

    pdu1_status = pdu_port_status(pdu_1_session,pdu_1_header,pdu_1_data['host'],pdu_1_data['port'])
    pdu2_status = pdu_port_status(pdu_2_session,pdu_2_header,pdu_2_data['host'],pdu_2_data['port'])

    psu1_status = drac_psu_status(drac_session,drac_headers,1)
    psu2_status = drac_psu_status(drac_session,drac_headers,2)

    host_status = drac_syspwr_status(drac_session,drac_headers)

    print("PSU1: "+psu1_status+" "+pdu_1_data['host']+" Port "+pdu_1_data['port']+": "+pdu1_status)
    print("PSU2: "+psu2_status+" "+pdu_2_data['host']+" Port "+pdu_2_data['port']+": "+pdu2_status)
    print("Server Power: "+host_status)

    if host_status == "Off":
        print("FAILED: Expected host in On state, instead got Off")
        fail = True

    if test == 1:
        if desstate == 0:
            if "Input lost (AC)" not in psu1_status:
                print("FAILED: Expected PSU1 in Input lost state, instead got "+psu1_status)
                fail = True
            if "Off" not in pdu1_status:
                print("FAILED: Expected "+pdu_1_data['host']+" port "+pdu_1_data['port']+" in state Off, instead got "+pdu1_status)
                fail = True
        elif desstate == 1:
            if "Input lost (AC)" in psu1_status:
                print("FAILED: Expected PSU1 in Presence Detected state, instead got "+psu1_status)
                fail = True
            if "On" not in pdu1_status:
                print("FAILED: Expected "+pdu_1_data['host']+" port "+pdu_1_data['port']+" in state On, instead got "+pdu1_status)
                fail = True
    elif test == 2:
        if desstate == 0:
            if "Input lost (AC)" not in psu2_status:
                print("FAILED: Expected PSU2 in Input lost state, instead got "+psu2_status)
                fail = True
            if "Off" not in pdu2_status:
                print("FAILED: Expected "+pdu_2_data['host']+" port "+pdu_2_data['port']+" in state Off, instead got "+pdu2_status)
                fail = True
        elif desstate == 1:
            if "Input lost (AC)" in psu2_status:
                print("FAILED: Expected PSU2 in Presence Detected state, instead got "+psu2_status)
                fail = True
            if "On" not in pdu2_status:
                print("FAILED: Expected "+pdu_2_data['host']+" port "+pdu_2_data['port']+" in state On, instead got "+pdu2_status)
                fail =True

# Generate authentication data for the PDU. The APC PDUs require http basic auth + the expected json auth to create the session, so we have to generate both to be sent.
l_username = "admin"
l_password = "HPC1234!@#$"
l_combined = l_username + ":" + l_password
l_base64_bytes = base64.b64encode(l_combined.encode('utf-8'))
l_base64_str = l_base64_bytes.decode('utf-8')
l_auth_header = "Basic " + l_base64_str

pdu_authdata = {"username":l_username ,"password":l_password}
pdu_authdata_json = json.dumps(pdu_authdata)
pdu_header = {"Content-type":"application/json","Authorization":l_auth_header}

# Generate authentication data for iDRAC
drac_authdata = {"UserName":"root","Password":"calvin"}
drac_authdata_json = json.dumps(drac_authdata)
drac_auth_header = {"Content-type":"application/json"}

try:
    # Start PDU session for PDU1 host
    pdu_1_session = requests.Session()
    pdu_1_login = pdu_1_session.post("https://"+pdu_1_data['host']+"/redfish/v1/SessionService/Sessions", data=pdu_authdata_json, verify=False, headers=pdu_header, stream=False)
    pdu_1_auth_token = pdu_1_login.headers['X-Auth-Token']
    pdu_1_header = {"X-Auth-Token":pdu_1_auth_token}

    # Start PDU session for PDU2 host
    pdu_2_session = requests.Session()
    pdu_2_login = pdu_2_session.post("https://"+pdu_2_data['host']+"/redfish/v1/SessionService/Sessions", data=pdu_authdata_json, verify=False, headers=pdu_header, stream=False)
    pdu_2_auth_token = pdu_2_login.headers['X-Auth-Token']
    pdu_2_header = {"X-Auth-Token":pdu_2_auth_token}

    # Start iDRAC session for system host
    drac_session = requests.Session()
    drac_login = drac_session.post("https://"+host+"-drac/redfish/v1/SessionService/Sessions", data=drac_authdata_json, headers=drac_auth_header, verify=False, stream=False)
    drac_session_Id = json.loads(drac_login.content)['Id']
    drac_auth_token = drac_login.headers['X-Auth-Token']
    drac_headers = {"X-Auth-Token":drac_auth_token}

    # Make sure both target outlets are energized before running testing
    pdu_setstate(pdu_1_session,pdu_1_header,pdu_1_data['host'],pdu_1_data['port'],"on")
    pdu_setstate(pdu_2_session,pdu_2_header,pdu_2_data['host'],pdu_2_data['port'],"on")

    # Perform PDU Test. Check starting port/PDU state, de energize each port, check respective PDU status and system up status, then power port back on and test again.
    print("Host: "+host+", PSU1: "+pdu_1_data['host']+" Port "+pdu_1_data['port']+", PSU2: "+pdu_2_data['host']+" Port "+pdu_2_data['port'])
    print("=============================================")
    print("Initial State:")
    # Get Initial PSU/PDU power states
    show_status()
    print("---------------------------------------------")
    # Power off PSU1 PDU port
    pdu_setstate(pdu_1_session,pdu_1_header,pdu_1_data['host'],pdu_1_data['port'],"off")
    # Report power states
    show_status(1,0)
    # Power on PSU1 PDU Port
    pdu_setstate(pdu_1_session,pdu_1_header,pdu_1_data['host'],pdu_1_data['port'],"on")
    # Report power states
    show_status(1,1)
    print("---------------------------------------------")
    # Power off PSU2 PDU port - all need to be modified for PROD
    pdu_setstate(pdu_2_session,pdu_2_header,pdu_2_data['host'],pdu_2_data['port'],"off")
    # Report power states
    show_status(2,0)
    # Power on PSU2 PDU Port
    pdu_setstate(pdu_2_session,pdu_2_header,pdu_2_data['host'],pdu_2_data['port'],"on")
    # Report power states
    show_status(2,1)
    if fail == True:
        print("FAIL: Review test output for errors.")
    else:
        print("PASSED: All port tests completed successfully.")

    # Make sure both target outlets are energized after running testing
    pdu_setstate(pdu_1_session,pdu_1_header,pdu_1_data['host'],pdu_1_data['port'],"on")
    pdu_setstate(pdu_2_session,pdu_2_header,pdu_2_data['host'],pdu_2_data['port'],"on")

    # Log out from PDU Sessions
    pdu_1_session.delete("https://"+pdu_1_data['host']+"/redfish/v1/SessionService/Sessions/"+pdu_1_auth_token, verify=False, headers=pdu_1_header, stream=False)
    pdu_2_session.delete("https://"+pdu_2_data['host']+"/redfish/v1/SessionService/Sessions/"+pdu_2_auth_token, verify=False, headers=pdu_2_header, stream=False)
    pdu_1_session.close()
    pdu_2_session.close()
    # Log out from DRAC session
    drac_session.delete("https://"+host+"-drac//redfish/v1/SessionService/Sessions/"+drac_session_Id, verify=False, headers=drac_headers, stream=False)
    drac_session.close()
except Exception as err:
    print(f"FAILED\nAn unexpected error occurred: {err}")
    sys.exit(1)
