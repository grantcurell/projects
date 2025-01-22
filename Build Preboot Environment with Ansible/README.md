# Build Preboot Environment with Ansible

## Test

**Objective:**  

Your task is to create a series of Ansible playbooks which configure a blank Rocky Linux or RHEL server as a PXE/Kickstart server. The resulting PXE server should perform automated installations of Rocky Linux or RHEL on client machines. The choice between the two is up to you.

Personally, I used RHEL for my own testing.

### Requirements:

Your Ansible playbooks must meet the following requirements

- Install and configure a DHCP server to provide IP addresses to PXE clients and direct them to the TFTP server.
   - The interface used for DHCP **must** be dynamically selected. IE: If the correct interface is ens160 with IP 192.168.35.133, you cannot hardcode these values. You must write code that dynamically identifies the correct interface based on a target subnet. Ex: if the target subnet is 192.168.35.0/24 then your code should intelligently select ens160.
- Configure an HTTP server within a Podman container to serve the Kickstart file and any necessary installation resources.
   - You must use Podman specifically to run the HTTP server. You can choose to run other things with Podman, but at a minimum, the HTTP server must leverage Podman to host the files.
   - You must use Must use https://docs.ansible.com/ansible/latest/collections/containers/podman/podman_container_module.html#ansible-collections-containers-podman-podman-container-module
   - The kickstart files you host must use static IP addresses matched to specific MAC addresses. This means each must boot during PXE with that IP address and the host must use that IP address after installation.
- Set up and configure a TFTP server to host PXE boot files.
  - The TFTP server must correctly serve separate files dependent on the host MAC address
- All playbooks must correctly employ tags so that roles may be run in a modular fashion
- The totality of the code must be idempotent
- There may be no magic values hardcoded into playbooks. Everything must be appropriately placed in variable files. As mentioned above, the interface to be used on the PXE server cannot be hardcoded. You must calculate it dynamically in the code based off of the desired subnet.
- You cannot disable firewalld or SELinux

### Deliverables:

- Your code on a publicly hosted GitHub
- A README describing how to run it. The test will be my taking your code and running at on VMWare workstation against VMs.
  - Your instructions need to specify whether I should run the VMs as UEFI or BIOS.

### Evaluation Criteria:

- **Completeness:** Does the playbook cover all required services and configurations on the PXE server.
- **Code Quality:** Is the Ansible playbook well-structured, modular, and documented?
- **Efficiency:** Are the tasks optimized for idempotency and reliability, ensuring that the PXE server is robust and maintainable?

Partially compliant solutions will be evaluated on a case by case basis.
