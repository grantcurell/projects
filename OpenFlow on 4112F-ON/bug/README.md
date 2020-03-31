# Bug in Dell OS10 Openflow Implementation

## Overview

### Problem

OS10 does not correctly follow [the specification](https://www.opennetworking.org/wp-content/uploads/2014/10/openflow-spec-v1.3.0.pdf)
with regards to datapath_id. See page 52 for the definition of *struct ofp_switch_features*.
The datapath_id should be 64 bits long, however, I discovered while using Ryu
that OS10 returns a 60 bit integer instead.

### Suggested Fix

Suggest zero padding the datapath_id to 64 bits.

I found the problem while testing [this Ryu example](https://osrg.github.io/ryu-book/en/html/rest_api.html#implementing-simpleswitchrest13-class).

## Reproducing

### My Configuration

- Controller is running on Windows in PyCharm
- Controller: Ryu
- Switch: 4112F-ON

#### Switch Version Info

    Dell EMC Networking OS10 Enterprise
    Copyright (c) 1999-2020 by Dell Inc. All Rights Reserved.
    OS Version: 10.5.1.0
    Build Version: 10.5.1.0.124
    Build Time: 2020-02-12T09:05:20+0000
    System Type: S4112F-ON
    Architecture: x86_64
    Up Time: 4 days 09:16:43

### Setup

#### Enable OpenFlow on the Switch

On the switch run:

    OS10# configure terminal
    OS10(config)# openflow
    OS10(config-openflow)# mode openflow-only
    Configurations not relevant to openflow mode will be removed from the startup-configuration and system will be rebooted. Do you want to proceed? [confirm yes/no]:yes

#### Configure OpenFlow

    OS10# configure terminal
    OS10(config)# openflow
    OS10(config-openflow)# switch of-switch-1
    OS10(config-openflow-switch)# controller ipv4 <YOUR_CONTROLLER_IP> port 6633
    OS10(config-openflow-switch)# no shutdown

See [the switch config](./switch_configuration) for details.

### Run the Code

Run `pip install ryu` to install Ryu and its dependencies.

I have included my Ryu app as it currently was when I found the bug in the file
`main.py`.

I used PyCharm to perform debugging which required me to adjust the debug configuration
to the below:

![](images/debug_configuration.PNG)

This will allow you to use PyCharm's debugger.

Alternatively, you can delete everything after line 358 in main.py and use `ryu-manager`
to run the application.

To run the code there is an application called `ryu-manager`. To run the code 
you have to run `ryu-manager main.py`.

## Proof of Concept

Running the code in debug mode produces the below:
![](images/poc.PNG)
You can see that the switch ID 150013889525632 which is only 15 characters instead
of the required 16. 

### Consequences

This causes code following the spec to fail. In my case, Ryu's WSGI application fails
because it is using dlib:

    @route('/simpleswitch', url, methods=['PUT'], requirements={'dpid': dpid_lib.DPID_PATTERN})

and dlib requires all 16 digits to be present. You can see this by reverse engineering
the WSGI call until you find the regex produced from the above line.

![](images/regex.jpg)

This will lead you to the dlib library where you see:

    _DPID_LEN = 16
    _DPID_FMT = '%0{0}x'.format(_DPID_LEN)
    DPID_PATTERN = r'[0-9a-f]{%d}' % _DPID_LEN

This is in no way relevant to the bug, I just wanted another programmer to appreciate
how much of a pain in the ass this was to find hahahahaha