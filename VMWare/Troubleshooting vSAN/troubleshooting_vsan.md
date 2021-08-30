# Troubleshooting vSAN

## vSAN Support Insight



## Overall Approach

vSAN observer
vSAN health test
Time/resource permitting vSAN HCI benchmark
I'll also do a general network survey to make sure I understand the physical and logical layout paying particular attention to the various VLANs

https://core.vmware.com/resource/troubleshooting-vsan-performance

1. Identify and quantify.  This step helps to clearly define the issue.  Clarifying questions can help properly qualify the problem statement, which will allow for a more targeted approach to addressing.  This process helps sort out real versus perceived issues, and focuses on the end result and supporting symptoms, without implying the cause of the issue.
2. Discovery/Review - Environment.  This step takes a review of the current configuration.  This will help eliminate previously unnoticed basic configuration or topology issues that might be plaguing the environment.
3. Discovery/Review - Workload.  This step will help the reader review the applications and workflows.  This will help a virtualization administrator better understand what the application is attempting to perform, and why. 
4. Performance Metrics - Insight.  This step will review some of the key performance metrics to view, and how to interpret some of the findings the reader may see when observing their workloads.  It clarifies what the performance metrics means, and how they relate to each other..
5. Mitigation - Options in potential software and hardware changes.  This step will help the reader step through the potential actions for mitigation.

## Technical Approach

Potential Bottlenecks: https://core.vmware.com/blog/understanding-performance-bottlenecks

### Identify

1. Kick off vSAN Observer. See [Using vSAN Observer](#using-vsan-observer). Details on using vSAN observer available in [this PDF](./Monitoring-with-VSAN-Observer-v1.2.pdf)
   1. Check the latency as seen by a guest VM running the application of interest (check on the VMs tab)
      1. VM Home - This is where the VM's configuration file, log files, and other VM related small files are stored. The RAID tree subsection shows the different component owners for VM Home.
      2. Virtual Disk - This shows the different virtual disks attached to the VM. Each disk displas stats specific to that disk. You can drill down to individual virtual disks. The VSCSI layer shows the aggregate latency, IOPS and throughput numbers for a particular virtual disk of a VM.
   2. Check for high outstanding IOPs (vSAN client tab and vSAN disks). On the vSAN disks tab make sure that outstanding IO is well balanced across the hosts
   3. Check for high latencies (time it takes to complete on I/O operation from application viewpoint). (vSAN client tab and vSAN disk tab)
      1. Make sure that what we see on the vSAN client tab correspondings to what is on the vSAN disk tabs
      2. Common causes of high latency:
         1. Large average I/O sizes, which leads to increased latencies
         2. Large number of writes
         3. Large number of I/Os
         4. Slow SSD that isn't keeping up
         5. Too many random reads causing cache misses in the SSD.
      3. Latency formula: outstanding IOs / drive max write or I/O = x ms
      4. If we kick off a lot of read ops on something we generally expect there to a spike in latency followed by a drop as things are cached (assuming the same thing is being read)
      5. The standard deviation graph is telling you the frequency you are outside a single standard deviation
   4. Check bandwidth utilization
      1. Lots of small I/Os could cause you to hit I/O ceiling before bandwidth
      2. Large I/Os may exhaust bandwidth
   5. Check buffer utilization. You can see this on the client and disk tabs. On the deep dive tab you can check RC hit rate for the various hosts
   6. Check PCPU utilization. It isn't uncommon to see 30-50% utilization when under I/O load. Sustained high CPU utilization could indicate a problem.
   7. Check memory consumption paying specific attention to congestion
   8. Check distribution of [components](../Notes%20on%20VSAN/README.md#components). The line should be uniform indicating roughly equal distribution of components

![](images/2021-08-29-20-59-39.png)
![](images/2021-08-29-21-02-43.png)

1. Check cluster health with `esxcli vsan health cluster list`


## Ideas

### Check for high outstanding

## Using vSAN Observer

SSH to vCenter and then run `rvc administrator@vsphere.lan@localhost`
`vsan.observer /localhost/datacenter/computers/vSAN\ Cluster/ --run-webserver --force`
Go to https://vcenter.lan:8010/ (it must be https)

### Running from a remote machine

Install Ruby: https://rubyinstaller.org/downloads/
Install Ruby vSphere Console: https://rubydoc.info/gems/rvc/1.6.0 `gem install rvc`

## Helpful Commands

esxcli network ip interface list
esxcli network ip interface ipv4 get
esxcli network ip  neighbor list (view ARP table)