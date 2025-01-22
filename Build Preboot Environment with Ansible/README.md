# Build Preboot Environment with Ansible

**Objective:**  
 
Your task is to create a series of Ansible playbooks which configure a blank Rocky Linux or RHEL host as a PXE/Kickstart server. The resulting PXE server should perform automated installations of Rocky Linux or RHEL via Kickstart against targeted devices via their MAC addresses. The choice between the two operating systems is up to you. Personally, I used RHEL on VMWare Workstation for my own testing.

### Requirements:

Your Ansible playbooks must meet the following requirements

- Install and configure a DHCP server to provide IP addresses to PXE clients and direct them to the TFTP server.
   - The interface used for DHCP must be dynamically selected. IE: If the correct interface is ens160 with IP 192.168.35.133, you cannot hardcode these values. You must write code that dynamically identifies the correct interface based on a target subnet. Ex: if the target subnet provided by the user is 192.168.35.0/24 then your code should intelligently select ens160.
- Configure httpd within a Podman container to serve the Kickstart files
   - You must use Podman specifically to run the HTTP server. You can choose to run other things with Podman, but at a minimum, the httpd server must leverage Podman to host the kickstart files
   - You must use https://docs.ansible.com/ansible/latest/collections/containers/podman/podman_container_module.html#ansible-collections-containers-podman-podman-container-module [docs.ansible.com]
   - The kickstart files you host must use static IP addresses matched to specific MAC addresses. If you want, you can use DHCP in the preboot environment, but the end result is that each host must boot RHEL/Rocky with the correct static IP address.
- Set up and configure a TFTP server to host PXE boot files.
  - I suggest setting up TFTP to serve different files based on the target host MAC addresses
 - You may use UEFI or BIOS
- All playbooks must correctly employ tags so that roles may be run in a modular fashion
- The totality of the code must be idempotent
  - I do not care if things get marked as changed, only that it does not crash on rerun
- Magic values hardcoded into playbooks or templates will count heavily against you. Everything must be appropriately placed in variable files per best practice. As mentioned above, the interface to be used on the PXE server should not be hardcoded. You must calculate it dynamically in the code based off of the desired subnet.
- You cannot disable firewalld or SELinux

You may violate these requirements, but the solution will not be considered complete.

### What It Should Look Like

Some version of the user specifying the MAC addresses of the servers they are targeting along with pertinent network information in an inventory file. Running your playbooks against some target server should turn that server into a PXE boot server meeting all the above requirements. The user should then be able to use the PXE boot server to PXE boot the aforementioned servers and the end result should be working RHEL or Rocky boxes with the specified static IP addresses.

### Deliverables:

- Your code on a publicly hosted GitHub or delivered via a ZIP in git repo format
- A README describing how to run it. The test will be my taking your code and running at on VMWare workstation against VMs. I will run your code myself per your README prior to the interview. The interview itself will vast majority consist of my asking you about your solution.
  - Your instructions need to specify whether I should run the VMs as UEFI or BIOS.

### Evaluation Criteria:

- **Completeness:** Does the playbook cover all required services and configurations on the PXE server.
- **Code Quality:** Is the Ansible playbook well-structured, modular, and documented?
- **Efficiency:** Are the tasks optimized for idempotency and reliability, ensuring that the PXE server is robust and maintainable?

A complete solution means exceedingly high odds you get the job. Partially complete answers will be evaluated on a case-by-case basis. Any questions text 9374780551. To move on to an interview you must at a minimum have a working kickstart solution that results in a booted RHEL or Rocky box.