#!/bin/sh

numjobs="4"
iodepth="128"

for i in `seq 0 1 11`
do
	if [[ $i -le 5 ]]
	then
		numa_str="--numa_mem_policy=bind:3 --numa_cpu_nodes=2"
	else
		numa_str="--numa_mem_policy=bind:4 --numa_cpu_nodes=3"
	fi
	fio --filename=/dev/nvme${i}n1 --ioengine=libaio --iodepth=$iodepth \
	    --direct=1 --ramp_time=10s --time_based --runtime=1m --rw=read \
	    --name=foo --numjobs=$numjobs --bs=1m $numa_str &
done 
