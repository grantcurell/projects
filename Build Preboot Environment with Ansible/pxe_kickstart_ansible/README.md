
Update inventory/inventory.yml

```bash
sudo dnf install epel-release -y
sudo dnf install ansible -y
sudo dnf install -y python3-netaddr
ansible-galaxy collection install containers.podman
ansible-playbook playbooks/site.yml
```