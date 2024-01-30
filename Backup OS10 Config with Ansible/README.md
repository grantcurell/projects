# Backup OS10 Config with Ansible

## Overview

The following describes how to both backup and deploy a config to OS10 using Ansible.

### Prerequisites

- [Install Ansible](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html) on your device.
- Ensure that the Ansible server has IP connectivity to the management interface of all OS10 devices.

### Backup a Config

On your Ansible server, copy the following Ansible playbook to a file called `backup_config.yaml`.

    ---
    - name: Setting up localhost for saving config
      hosts: localhost
      gather_facts: yes
      tasks:
        - block:
            - name: Generating backup folder name in localhost
              set_fact:
                 target_folder: "{{ backup_folder }}/{{ ansible_date_time.iso8601 }}"
            - name: Create config_backup folder
              file:
                path: "{{ target_folder }}"
                state: directory
            - debug:
                msg: "Config files are to be backed up at {{target_folder}}"
          delegate_to: localhost
          run_once: True
    - name: Backup os10 running configurations
      hosts: os10
      gather_facts: False
      connection: network_cli
      tasks:
        - name: Fetch OS10 running configuration
          dellos10_command:
            commands: show running
          register: sh_runn
        - name: Save config to file
          copy:
            content: "{{ sh_runn.stdout | replace('\\n', '\n') }}"
            dest: "{{hostvars.localhost.target_folder}}/{{inventory_hostname}}_os10_show_run"
          delegate_to: localhost
        - debug:
            msg: "Config files are to be backed up at {{hostvars.localhost.target_folder}}"
          run_once: true

Next, create a separate file called `inventory.yaml` with the following contents:

    all:
      vars:
        backup_folder: "/root/backup"
      children:
        os10:
          hosts:
            192.168.1.169:
              ansible_become: 'yes'
              ansible_become_method: enable
              ansible_command_timeout: 120
              ansible_connection: ansible.netcommon.network_cli
              ansible_network_os: dellemc.os10.os10
              ansible_password: admin
              ansible_user: admin
            192.168.1.170:
              ansible_become: 'yes'
              ansible_become_method: enable
              ansible_command_timeout: 120
              ansible_connection: ansible.netcommon.network_cli
              ansible_network_os: dellemc.os10.os10
              ansible_password: admin
              ansible_user: admin

Replace the IPs, backup_folder, ansible_password, and ansible_user variables above with the variables for your hosts. I am demoing the most simplistic configuration above. There are ways to use more generally scoped variables so that the password doesn't have to repeated, use SSH keys instead of cleartext passwords, place passwords in a vault, etc, but I do not demo that here. See [the module parameter provider](https://docs.ansible.com/ansible/latest/collections/dellemc/os10/os10_config_module.html#parameters) for details on this.

Finally, to run the backup run `ansible-playbook -i inventory.yaml backup_config.yaml`. A clean run will look like this:

    ansible-playbook -i inventory.yaml backup_config.yaml

    PLAY [Setting up localhost for saving config] **********************************************************************************************************************************************************

    TASK [Gathering Facts] *********************************************************************************************************************************************************************************
    ok: [localhost]

    TASK [Generating backup folder name in localhost] ******************************************************************************************************************************************************
    ok: [localhost -> localhost]

    TASK [Create config_backup folder] *********************************************************************************************************************************************************************
    changed: [localhost -> localhost]

    TASK [debug] *******************************************************************************************************************************************************************************************
    ok: [localhost -> localhost] => {
        "msg": "Config files are to be backed up at /root/backup/2022-09-07T20:06:17Z"
    }

    PLAY [Backup os10 running configurations] **************************************************************************************************************************************************************

    TASK [Fetch OS10 running configuration] ****************************************************************************************************************************************************************
    [DEPRECATION WARNING]: Distribution fedora 35 on host 192.168.1.169 should use /usr/bin/python3, but is using /usr/bin/python for backward compatibility with prior Ansible releases. A future Ansible
    release will default to using the discovered platform python for this host. See https://docs.ansible.com/ansible/2.9/reference_appendices/interpreter_discovery.html for more information. This feature
     will be removed in version 2.12. Deprecation warnings can be disabled by setting deprecation_warnings=False in ansible.cfg.
    ok: [192.168.1.169]

    TASK [Save config to file] *****************************************************************************************************************************************************************************
    changed: [192.168.1.169 -> localhost]

    TASK [debug] *******************************************************************************************************************************************************************************************
    ok: [192.168.1.169] => {
        "msg": "Config files are to be backed up at /root/backup/2022-09-07T20:06:17Z"
    }

    PLAY RECAP *********************************************************************************************************************************************************************************************
    192.168.1.169              : ok=3    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
    localhost                  : ok=4    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

The results will appear, in my configuration, in the folder `/root/backup/2022-09-07T20:06:17Z`.

    [root@fedora ~]# ls -al /root/backup/2022-09-07T20:06:17Z
    total 4
    drwxr-xr-x 1 root root   54 Sep  7 16:06 .
    drwxr-xr-x 1 root root  240 Sep  7 16:06 ..
    -rw-r--r-- 1 root root 2169 Sep  7 16:06 192.168.1.169_os10_show_run
