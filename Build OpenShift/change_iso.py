import requests
import json
import urllib3

# Suppress SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# vCenter server details
vc_host = "YOUR_VCENTER_DNS_NAME"
username = "YOUR_ADMIN_USER"
password = "YOUR_PASSWORD"

# Target VMs and the new ISO path
vm_names = ["openshift1", "openshift2", "openshift3", "openshift4", "openshift5", "openshift6"]
#vm_names = ["openshift5"]
iso_path = "[datastore1] agent5.iso"


# Login to vCenter
def login():
    url = f"https://{vc_host}/rest/com/vmware/cis/session"
    response = requests.post(url, auth=(username, password), verify=False)
    if response.status_code == 200:
        return response.json()['value']
    else:
        print(f"Failed to login: {response.status_code}, {response.text}")
        return None


# Get VM ID by name
def get_vm_id(session_id, vm_name):
    url = f"https://{vc_host}/rest/vcenter/vm?filter.names={vm_name}"
    headers = {'vmware-api-session-id': session_id}
    response = requests.get(url, headers=headers, verify=False)
    if response.status_code == 200:
        vms = response.json().get('value', [])
        if vms:
            return vms[0]['vm']
        else:
            print(f"VM {vm_name} not found")
    else:
        print(f"Failed to get VM ID: {response.status_code}, {response.text}")
    return None


# Shutdown VM
def shutdown_vm(session_id, vm_id):
    url = f"https://{vc_host}/rest/vcenter/vm/{vm_id}/power/stop"
    headers = {'vmware-api-session-id': session_id}
    response = requests.post(url, headers=headers, verify=False)
    if response.status_code == 200:
        print(f"VM {vm_id} shutdown successfully")
    else:
        print(f"Failed to shutdown VM {vm_id}: {response.status_code}, {response.text}")


# Change ISO
def change_iso(session_id, vm_id, iso_path):
    url = f"https://{vc_host}/rest/vcenter/vm/{vm_id}/hardware/cdrom"
    headers = {'vmware-api-session-id': session_id}
    cdrom_response = requests.get(url, headers=headers, verify=False)
    if cdrom_response.status_code == 200:
        cdroms = cdrom_response.json().get('value', [])
        if cdroms:
            cdrom_id = cdroms[0]['cdrom']
            iso_config = {
                "spec": {
                    "backing": {
                        "type": "ISO_FILE",
                        "iso_file": iso_path
                    },
                    "start_connected": True,
                    "allow_guest_control": True
                }
            }
            url = f"https://{vc_host}/rest/vcenter/vm/{vm_id}/hardware/cdrom/{cdrom_id}"
            update_response = requests.patch(url, headers=headers, json=iso_config, verify=False)
            if update_response.status_code == 200:
                print(f"ISO changed successfully for VM {vm_id}")
            else:
                print(f"Failed to change ISO for VM {vm_id}: {update_response.status_code}, {update_response.text}")
        else:
            print(f"No CD-ROM found for VM {vm_id}")
    else:
        print(f"Failed to get CD-ROM details for VM {vm_id}: {cdrom_response.status_code}, {cdrom_response.text}")


# Enter BIOS boot menu
def enter_bios(session_id, vm_id):
    url = f"https://{vc_host}/rest/vcenter/vm/{vm_id}/power/reset"
    headers = {'vmware-api-session-id': session_id}
    bios_config = {
        "spec": {
            "enter_setup_mode": True
        }
    }
    config_url = f"https://{vc_host}/rest/vcenter/vm/{vm_id}/hardware/boot"
    config_response = requests.patch(config_url, headers=headers, json=bios_config, verify=False)
    if config_response.status_code == 200:
        response = requests.post(url, headers=headers, verify=False)
        if response.status_code == 200:
            print(f"VM {vm_id} entered BIOS setup")
        else:
            print(f"Failed to enter BIOS for VM {vm_id}: {response.status_code}, {response.text}")
    else:
        print(f"Failed to configure BIOS setup for VM {vm_id}: {config_response.status_code}, {config_response.text}")


# Power on VM
def power_on_vm(session_id, vm_id):
    url = f"https://{vc_host}/rest/vcenter/vm/{vm_id}/power/start"
    headers = {'vmware-api-session-id': session_id}
    response = requests.post(url, headers=headers, verify=False)
    if response.status_code == 200:
        print(f"VM {vm_id} powered on successfully")
    else:
        print(f"Failed to power on VM {vm_id}: {response.status_code}, {response.text}")


# Main script
def main():
    session_id = login()
    if not session_id:
        return

    for vm_name in vm_names:
        vm_id = get_vm_id(session_id, vm_name)
        if vm_id:
            shutdown_vm(session_id, vm_id)
            change_iso(session_id, vm_id, iso_path)
            enter_bios(session_id, vm_id)
            power_on_vm(session_id, vm_id)


if __name__ == "__main__":
    main()