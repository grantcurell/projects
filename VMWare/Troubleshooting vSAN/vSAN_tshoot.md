esxcli vsan health cluster list

## Ruby Console

Install Ruby: https://rubyinstaller.org/downloads/
Install Ruby vSphere Console: https://rubydoc.info/gems/rvc/1.6.0 `gem install rvc`

### Using vSAN Observer

SSH to vCenter and then run `rvc administrator@vsphere.lan@localhost`
`vsan.observer /localhost/datacenter/computers/vSAN\ Cluster/ --run-webserver --force`
Go to https://vcenter.lan:8010/ (it must be https)