
## Good Job

```bash
grant    988748 988748 988730  0 11:36 ?        00:00:00 bash runme_intel64_dynamic                                                                                                       
grant    988798 988798 988748  0 11:36 ?        00:00:00 /bin/sh /home/modules/core/apps/oneapi/2023.0.0/mpi/2021.8.0/bin/mpirun -perhost 2 -np 8 ./runme_intel64_prv -n 117120 -b 384 -p 2 -q 4                                                                  
grant    988803 988803 988798  0 11:36 ?        00:00:00 mpiexec.hydra -perhost 2 -np 8 ./runme_intel64_prv -n 117120 -b 384 -p 2 -q 4
grant    988804 988804 988803  0 11:36 ?        00:00:00 /cm/shared/apps/slurm/current/bin/srun -N 2 -n 2 --ntasks-per-node 1 --nodelist z5-01,z5-02 --input none /home/modules/core/apps/oneapi/2023.0.0/mpi/2021.8.0/bin//hydra_bstrap_proxy --upstream-host z5-01.cm.cluster --upstream-port 34921 --pgid 0 --launcher slurm --launcher-number 1 --base-path /home/modules/core/apps/oneapi/2023.0.0/mpi/2021.8.0/bin/ --tree-width 16 --tree-level 1 --time-left -1 --launch-type 0 /home/modules/core/apps/oneapi/2023.0.0/mpi/2021.8.0/bin//hydra_pmi_proxy --usize -1 --auto-cleanup 1 --abort-signal 9
grant    988804 988806 988803  0 11:36 ?        00:00:00 /cm/shared/apps/slurm/current/bin/srun -N 2 -n 2 --ntasks-per-node 1 --nodelist z5-01,z5-02 --input none /home/modules/core/apps/oneapi/2023.0.0/mpi/2021.8.0/bin//hydra_bstrap_proxy --upstream-host z5-01.cm.cluster --upstream-port 34921 --pgid 0 --launcher slurm --launcher-number 1 --base-path /home/modules/core/apps/oneapi/2023.0.0/mpi/2021.8.0/bin/ --tree-width 16 --tree-level 1 --time-left -1 --launch-type 0 /home/modules/core/apps/oneapi/2023.0.0/mpi/2021.8.0/bin//hydra_pmi_proxy --usize -1 --auto-cleanup 1 --abort-signal 9
grant    988804 988807 988803  0 11:36 ?        00:00:00 /cm/shared/apps/slurm/current/bin/srun -N 2 -n 2 --ntasks-per-node 1 --nodelist z5-01,z5-02 --input none /home/modules/core/apps/oneapi/2023.0.0/mpi/2021.8.0/bin//hydra_bstrap_proxy --upstream-host z5-01.cm.cluster --upstream-port 34921 --pgid 0 --launcher slurm --launcher-number 1 --base-path /home/modules/core/apps/oneapi/2023.0.0/mpi/2021.8.0/bin/ --tree-width 16 --tree-level 1 --time-left -1 --launch-type 0 /home/modules/core/apps/oneapi/2023.0.0/mpi/2021.8.0/bin//hydra_pmi_proxy --usize -1 --auto-cleanup 1 --abort-signal 9
grant    988804 988808 988803  0 11:36 ?        00:00:00 /cm/shared/apps/slurm/current/bin/srun -N 2 -n 2 --ntasks-per-node 1 --nodelist z5-01,z5-02 --input none /home/modules/core/apps/oneapi/2023.0.0/mpi/2021.8.0/bin//hydra_bstrap_proxy --upstream-host z5-01.cm.cluster --upstream-port 34921 --pgid 0 --launcher slurm --launcher-number 1 --base-path /home/modules/core/apps/oneapi/2023.0.0/mpi/2021.8.0/bin/ --tree-width 16 --tree-level 1 --time-left -1 --launch-type 0 /home/modules/core/apps/oneapi/2023.0.0/mpi/2021.8.0/bin//hydra_pmi_proxy --usize -1 --auto-cleanup 1 --abort-signal 9
grant    988805 988805 988804  0 11:36 ?        00:00:00 /cm/shared/apps/slurm/current/bin/srun -N 2 -n 2 --ntasks-per-node 1 --nodelist z5-01,z5-02 --input none /home/modules/core/apps/oneapi/2023.0.0/mpi/2021.8.0/bin//hydra_bstrap_proxy --upstream-host z5-01.cm.cluster --upstream-port 34921 --pgid 0 --launcher slurm --launcher-number 1 --base-path /home/modules/core/apps/oneapi/2023.0.0/mpi/2021.8.0/bin/ --tree-width 16 --tree-level 1 --time-left -1 --launch-type 0 /home/modules/core/apps/oneapi/2023.0.0/mpi/2021.8.0/bin//hydra_pmi_proxy --usize -1 --auto-cleanup 1 --abort-signal 9
root     988813 988813      1  0 11:36 ?        00:00:00 slurmstepd: [251336.0]
root     988813 988814      1  0 11:36 ?        00:00:00 slurmstepd: [251336.0]
root     988813 988815      1  0 11:36 ?        00:00:00 slurmstepd: [251336.0]
root     988813 988816      1  0 11:36 ?        00:00:00 slurmstepd: [251336.0]
root     988813 988817      1  0 11:36 ?        00:00:00 slurmstepd: [251336.0]
grant    988818 988818 988813  0 11:36 ?        00:00:00 /home/modules/core/apps/oneapi/2023.0.0/mpi/2021.8.0/bin//hydra_pmi_proxy --usize -1 --auto-cleanup 1 --abort-signal 9
grant    988821 988821 988818  0 11:36 ?        00:00:00 /bin/bash ./runme_intel64_prv -n 117120 -b 384 -p 2 -q 4
grant    988822 988822 988818  0 11:36 ?        00:00:00 /bin/bash ./runme_intel64_prv -n 117120 -b 384 -p 2 -q 4
grant    988823 988823 988818  0 11:36 ?        00:00:00 /bin/bash ./runme_intel64_prv -n 117120 -b 384 -p 2 -q 4
grant    988824 988824 988818  0 11:36 ?        00:00:00 /bin/bash ./runme_intel64_prv -n 117120 -b 384 -p 2 -q 4
grant    988825 988825 988822 97 11:36 ?        00:02:28 /home/grant/mp_linpack/xhpl_intel64_dynamic
grant    988825 988832 988822  0 11:36 ?        00:00:00 /home/grant/mp_linpack/xhpl_intel64_dynamic
grant    988825 988836 988822 91 11:36 ?        00:02:18 /home/grant/mp_linpack/xhpl_intel64_dynamic
grant    988825 988837 988822 91 11:36 ?        00:02:18 /home/grant/mp_linpack/xhpl_intel64_dynamic
grant    988825 988843 988822 91 11:36 ?        00:02:18 /home/grant/mp_linpack/xhpl_intel64_dynamic
grant    988825 988847 988822 91 11:36 ?        00:02:18 /home/grant/mp_linpack/xhpl_intel64_dynamic
grant    988825 988852 988822 91 11:36 ?        00:02:18 /home/grant/mp_linpack/xhpl_intel64_dynamic
grant    988825 988854 988822 91 11:36 ?        00:02:18 /home/grant/mp_linpack/xhpl_intel64_dynamic
grant    988825 988856 988822 91 11:36 ?        00:02:18 /home/grant/mp_linpack/xhpl_intel64_dynamic
grant    988825 988858 988822 91 11:36 ?        00:02:18 /home/grant/mp_linpack/xhpl_intel64_dynamic
grant    988825 988861 988822 91 11:36 ?        00:02:18 /home/grant/mp_linpack/xhpl_intel64_dynamic
grant    988825 988862 988822 91 11:36 ?        00:02:18 /home/grant/mp_linpack/xhpl_intel64_dynamic
grant    988825 988865 988822 91 11:36 ?        00:02:18 /home/grant/mp_linpack/xhpl_intel64_dynamic
grant    988825 988869 988822 91 11:36 ?        00:02:18 /home/grant/mp_linpack/xhpl_intel64_dynamic
grant    988825 988882 988822 97 11:36 ?        00:02:28 /home/grant/mp_linpack/xhpl_intel64_dynamic
grant    988826 988826 988821 97 11:36 ?        00:02:28 /home/grant/mp_linpack/xhpl_intel64_dynamic
grant    988826 988830 988821  0 11:36 ?        00:00:00 /home/grant/mp_linpack/xhpl_intel64_dynamic
grant    988826 988834 988821 91 11:36 ?        00:02:18 /home/grant/mp_linpack/xhpl_intel64_dynamic
grant    988826 988835 988821 91 11:36 ?        00:02:18 /home/grant/mp_linpack/xhpl_intel64_dynamic
grant    988826 988842 988821 91 11:36 ?        00:02:18 /home/grant/mp_linpack/xhpl_intel64_dynamic
grant    988826 988846 988821 91 11:36 ?        00:02:18 /home/grant/mp_linpack/xhpl_intel64_dynamic
grant    988826 988850 988821 91 11:36 ?        00:02:18 /home/grant/mp_linpack/xhpl_intel64_dynamic
grant    988826 988851 988821 91 11:36 ?        00:02:18 /home/grant/mp_linpack/xhpl_intel64_dynamic
grant    988826 988853 988821 91 11:36 ?        00:02:18 /home/grant/mp_linpack/xhpl_intel64_dynamic
grant    988826 988855 988821 91 11:36 ?        00:02:18 /home/grant/mp_linpack/xhpl_intel64_dynamic
grant    988826 988857 988821 91 11:36 ?        00:02:18 /home/grant/mp_linpack/xhpl_intel64_dynamic
grant    988826 988860 988821 91 11:36 ?        00:02:18 /home/grant/mp_linpack/xhpl_intel64_dynamic
grant    988826 988863 988821 91 11:36 ?        00:02:18 /home/grant/mp_linpack/xhpl_intel64_dynamic
grant    988826 988867 988821 91 11:36 ?        00:02:18 /home/grant/mp_linpack/xhpl_intel64_dynamic
grant    988826 988884 988821 97 11:36 ?        00:02:28 /home/grant/mp_linpack/xhpl_intel64_dynamic
grant    988827 988827 988824 97 11:36 ?        00:02:28 /home/grant/mp_linpack/xhpl_intel64_dynamic
grant    988827 988833 988824  0 11:36 ?        00:00:00 /home/grant/mp_linpack/xhpl_intel64_dynamic
grant    988827 988840 988824 90 11:36 ?        00:02:18 /home/grant/mp_linpack/xhpl_intel64_dynamic
grant    988827 988841 988824 90 11:36 ?        00:02:18 /home/grant/mp_linpack/xhpl_intel64_dynamic
grant    988827 988845 988824 90 11:36 ?        00:02:18 /home/grant/mp_linpack/xhpl_intel64_dynamic
grant    988827 988849 988824 90 11:36 ?        00:02:18 /home/grant/mp_linpack/xhpl_intel64_dynamic
grant    988827 988866 988824 90 11:36 ?        00:02:18 /home/grant/mp_linpack/xhpl_intel64_dynamic
grant    988827 988871 988824 90 11:36 ?        00:02:18 /home/grant/mp_linpack/xhpl_intel64_dynamic
grant    988827 988872 988824 90 11:36 ?        00:02:18 /home/grant/mp_linpack/xhpl_intel64_dynamic
grant    988827 988874 988824 90 11:36 ?        00:02:18 /home/grant/mp_linpack/xhpl_intel64_dynamic
grant    988827 988876 988824 90 11:36 ?        00:02:18 /home/grant/mp_linpack/xhpl_intel64_dynamic
grant    988827 988878 988824 90 11:36 ?        00:02:18 /home/grant/mp_linpack/xhpl_intel64_dynamic
grant    988827 988880 988824 90 11:36 ?        00:02:18 /home/grant/mp_linpack/xhpl_intel64_dynamic
grant    988827 988881 988824 90 11:36 ?        00:02:18 /home/grant/mp_linpack/xhpl_intel64_dynamic
grant    988827 988883 988824 97 11:36 ?        00:02:28 /home/grant/mp_linpack/xhpl_intel64_dynamic
grant    988828 988828 988823 97 11:36 ?        00:02:28 /home/grant/mp_linpack/xhpl_intel64_dynamic
grant    988828 988831 988823  0 11:36 ?        00:00:00 /home/grant/mp_linpack/xhpl_intel64_dynamic
grant    988828 988838 988823 90 11:36 ?        00:02:18 /home/grant/mp_linpack/xhpl_intel64_dynamic
grant    988828 988839 988823 91 11:36 ?        00:02:18 /home/grant/mp_linpack/xhpl_intel64_dynamic
grant    988828 988844 988823 91 11:36 ?        00:02:18 /home/grant/mp_linpack/xhpl_intel64_dynamic
grant    988828 988848 988823 91 11:36 ?        00:02:18 /home/grant/mp_linpack/xhpl_intel64_dynamic
grant    988828 988859 988823 91 11:36 ?        00:02:18 /home/grant/mp_linpack/xhpl_intel64_dynamic
grant    988828 988864 988823 91 11:36 ?        00:02:18 /home/grant/mp_linpack/xhpl_intel64_dynamic
grant    988828 988868 988823 90 11:36 ?        00:02:18 /home/grant/mp_linpack/xhpl_intel64_dynamic
grant    988828 988870 988823 91 11:36 ?        00:02:18 /home/grant/mp_linpack/xhpl_intel64_dynamic
grant    988828 988873 988823 91 11:36 ?        00:02:18 /home/grant/mp_linpack/xhpl_intel64_dynamic
grant    988828 988875 988823 91 11:36 ?        00:02:18 /home/grant/mp_linpack/xhpl_intel64_dynamic
grant    988828 988877 988823 91 11:36 ?        00:02:18 /home/grant/mp_linpack/xhpl_intel64_dynamic
grant    988828 988879 988823 90 11:36 ?        00:02:18 /home/grant/mp_linpack/xhpl_intel64_dynamic
grant    988828 988885 988823 97 11:36 ?        00:02:28 /home/grant/mp_linpack/xhpl_intel64_dynamic
```

## Bad Job - NUMA_PER_MPI set to 4

```bash
grant    924288 924288 917096  0 11:30 pts/1    00:00:00 /bin/bash ./runme_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924295 924295 924288  0 11:30 pts/1    00:00:00 /bin/sh /home/modules/core/apps/oneapi/2024.1.0/mpi/2021.12/bin/mpirun -hostfile hosts -perhost 2 -np 8 ./runme_intel64_prv -n 117
grant    924296 924296 924288  0 11:30 pts/1    00:00:00 tee -a xhpl_intel64_dynamic_outputs.txt
grant    924301 924301 924295  0 11:30 pts/1    00:00:00 mpiexec.hydra -hostfile hosts -perhost 2 -np 8 ./runme_intel64_prv -n 117120 -b 384 -p 2 -q 4
grant    924302 924302 924301  0 11:30 pts/1    00:00:00 /usr/bin/ssh -q -x grant@z1-33 /home/modules/core/apps/oneapi/2024.1.0/mpi/2021.12/bin//hydra_bstrap_proxy --upstream-host z1-33 -
grant    924303 924303 924301  0 11:30 pts/1    00:00:00 /usr/bin/ssh -q -x grant@z1-34 /home/modules/core/apps/oneapi/2024.1.0/mpi/2021.12/bin//hydra_bstrap_proxy --upstream-host z1-33 -
root     924304 924304  10338  0 11:30 ?        00:00:00 sshd: grant [priv]
grant    924306 924306 924304  0 11:30 ?        00:00:00 sshd: grant@notty
grant    924307 924307 924306  0 11:30 ?        00:00:00 /home/modules/core/apps/oneapi/2024.1.0/mpi/2021.12/bin//hydra_pmi_proxy --usize -1 --auto-cleanup 1 --abort-signal 9
grant    924367 924367 924307  0 11:30 ?        00:00:00 /bin/bash ./runme_intel64_prv -n 117120 -b 384 -p 2 -q 4
grant    924368 924368 924307  0 11:30 ?        00:00:00 /bin/bash ./runme_intel64_prv -n 117120 -b 384 -p 2 -q 4
grant    924369 924369 924307  0 11:30 ?        00:00:00 /bin/bash ./runme_intel64_prv -n 117120 -b 384 -p 2 -q 4
grant    924370 924370 924307  0 11:30 ?        00:00:00 /bin/bash ./runme_intel64_prv -n 117120 -b 384 -p 2 -q 4
grant    924371 924371 924367 49 11:30 ?        00:05:56 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924371 924377 924367  0 11:30 ?        00:00:00 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924371 924380 924367 24 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924371 924381 924367 24 11:30 ?        00:02:52 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924371 924382 924367 24 11:30 ?        00:02:52 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924371 924383 924367 24 11:30 ?        00:02:52 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924371 924384 924367 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924371 924385 924367 24 11:30 ?        00:02:52 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924371 924386 924367 24 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924371 924387 924367 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924371 924388 924367 24 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924371 924389 924367 24 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924371 924390 924367 24 11:30 ?        00:02:52 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924371 924391 924367 24 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924371 924392 924367 24 11:30 ?        00:02:52 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924371 924393 924367 24 11:30 ?        00:02:52 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924371 924394 924367 24 11:30 ?        00:02:52 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924371 924395 924367 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924371 924396 924367 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924371 924397 924367 24 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924371 924398 924367 24 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924371 924399 924367 24 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924371 924400 924367 24 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924371 924401 924367 24 11:30 ?        00:02:52 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924371 924402 924367 24 11:30 ?        00:02:52 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924371 924403 924367 24 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924371 924404 924367 24 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924371 924405 924367 24 11:30 ?        00:02:52 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924371 924406 924367 24 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924371 924407 924367 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924371 924408 924367 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924371 924409 924367 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924371 924410 924367 24 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924371 924411 924367 24 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924371 924412 924367 24 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924371 924413 924367 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924371 924414 924367 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924371 924415 924367 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924371 924416 924367 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924371 924417 924367 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924371 924418 924367 24 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924371 924419 924367 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924371 924420 924367 24 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924371 924421 924367 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924371 924422 924367 24 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924371 924423 924367 24 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924371 924424 924367 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924371 924425 924367 24 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924371 924426 924367 24 11:30 ?        00:02:52 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924371 924427 924367 24 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924371 924428 924367 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924371 924429 924367 24 11:30 ?        00:02:52 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924371 924430 924367 24 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924371 924431 924367 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924371 924432 924367 24 11:30 ?        00:02:52 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924371 924433 924367 24 11:30 ?        00:02:52 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924371 924597 924367 49 11:30 ?        00:05:56 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924372 924372 924368 49 11:30 ?        00:05:56 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924372 924379 924368  0 11:30 ?        00:00:00 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924372 924434 924368 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924372 924435 924368 24 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924372 924436 924368 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924372 924437 924368 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924372 924440 924368 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924372 924442 924368 24 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924372 924444 924368 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924372 924446 924368 24 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924372 924447 924368 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924372 924448 924368 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924372 924449 924368 24 11:30 ?        00:02:52 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924372 924451 924368 24 11:30 ?        00:02:52 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924372 924452 924368 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924372 924453 924368 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924372 924454 924368 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924372 924455 924368 24 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924372 924456 924368 24 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924372 924457 924368 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924372 924458 924368 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924372 924459 924368 24 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924372 924460 924368 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924372 924461 924368 24 11:30 ?        00:02:52 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924372 924462 924368 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924372 924463 924368 23 11:30 ?        00:02:50 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924372 924465 924368 23 11:30 ?        00:02:50 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924372 924466 924368 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924372 924467 924368 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924372 924468 924368 23 11:30 ?        00:02:50 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924372 924469 924368 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924372 924470 924368 24 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924372 924471 924368 24 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924372 924472 924368 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924372 924473 924368 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924372 924474 924368 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924372 924475 924368 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924372 924476 924368 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924372 924477 924368 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924372 924478 924368 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924372 924480 924368 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924372 924481 924368 24 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924372 924483 924368 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924372 924485 924368 24 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924372 924488 924368 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924372 924490 924368 24 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924372 924492 924368 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924372 924494 924368 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924372 924496 924368 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924372 924498 924368 24 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924372 924500 924368 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924372 924502 924368 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924372 924504 924368 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924372 924506 924368 24 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924372 924508 924368 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924372 924510 924368 24 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924372 924596 924368 49 11:30 ?        00:05:55 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924373 924373 924369 49 11:30 ?        00:05:56 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924373 924378 924369  0 11:30 ?        00:00:00 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924373 924438 924369 24 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924373 924439 924369 24 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924373 924441 924369 24 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924373 924443 924369 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924373 924445 924369 24 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924373 924450 924369 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924373 924464 924369 24 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924373 924479 924369 24 11:30 ?        00:02:52 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924373 924482 924369 24 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924373 924484 924369 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924373 924486 924369 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924373 924487 924369 24 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924373 924489 924369 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924373 924491 924369 23 11:30 ?        00:02:50 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924373 924493 924369 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924373 924495 924369 24 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924373 924497 924369 24 11:30 ?        00:02:52 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924373 924499 924369 24 11:30 ?        00:02:52 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924373 924501 924369 24 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924373 924503 924369 24 11:30 ?        00:02:52 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924373 924505 924369 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924373 924507 924369 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924373 924509 924369 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924373 924511 924369 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924373 924512 924369 24 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924373 924513 924369 24 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924373 924514 924369 24 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924373 924515 924369 24 11:30 ?        00:02:52 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924373 924516 924369 24 11:30 ?        00:02:52 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924373 924517 924369 24 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924373 924518 924369 24 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924373 924519 924369 24 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924373 924520 924369 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924373 924521 924369 24 11:30 ?        00:02:52 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924373 924522 924369 24 11:30 ?        00:02:52 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924373 924523 924369 24 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924373 924524 924369 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924373 924525 924369 24 11:30 ?        00:02:52 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924373 924526 924369 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924373 924527 924369 24 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924373 924528 924369 24 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924373 924529 924369 24 11:30 ?        00:02:52 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924373 924530 924369 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924373 924531 924369 24 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924373 924532 924369 24 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924373 924533 924369 24 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924373 924534 924369 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924373 924535 924369 24 11:30 ?        00:02:52 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924373 924536 924369 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924373 924537 924369 24 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924373 924538 924369 24 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924373 924539 924369 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924373 924540 924369 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924373 924541 924369 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924373 924599 924369 49 11:30 ?        00:05:56 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924374 924374 924370 49 11:30 ?        00:05:56 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924374 924376 924370  0 11:30 ?        00:00:00 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924374 924542 924370 24 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924374 924543 924370 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924374 924544 924370 24 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924374 924545 924370 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924374 924546 924370 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924374 924547 924370 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924374 924548 924370 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924374 924549 924370 23 11:30 ?        00:02:50 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924374 924550 924370 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924374 924551 924370 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924374 924552 924370 23 11:30 ?        00:02:50 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924374 924553 924370 23 11:30 ?        00:02:50 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924374 924554 924370 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924374 924555 924370 23 11:30 ?        00:02:50 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924374 924556 924370 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924374 924557 924370 23 11:30 ?        00:02:50 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924374 924558 924370 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924374 924559 924370 23 11:30 ?        00:02:50 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924374 924560 924370 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924374 924561 924370 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924374 924562 924370 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924374 924563 924370 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924374 924564 924370 23 11:30 ?        00:02:50 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924374 924565 924370 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924374 924566 924370 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924374 924567 924370 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924374 924568 924370 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924374 924569 924370 24 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924374 924570 924370 24 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924374 924571 924370 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924374 924572 924370 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924374 924573 924370 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924374 924574 924370 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924374 924575 924370 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924374 924576 924370 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924374 924577 924370 24 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924374 924578 924370 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924374 924579 924370 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924374 924580 924370 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924374 924581 924370 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924374 924582 924370 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924374 924583 924370 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924374 924584 924370 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924374 924585 924370 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924374 924586 924370 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924374 924587 924370 24 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924374 924588 924370 23 11:30 ?        00:02:50 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924374 924589 924370 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924374 924590 924370 23 11:30 ?        00:02:50 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924374 924591 924370 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924374 924592 924370 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924374 924593 924370 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924374 924594 924370 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924374 924595 924370 23 11:30 ?        00:02:51 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    924374 924598 924370 49 11:30 ?        00:05:55 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
```

## Bad Job - NUMA_PER_MPI set to 1

```bash
[grant@z1-33 ~]$ ps -eTf | grep xhpl | wc -l
62

grant    926850 926850 917096  0 11:54 pts/1    00:00:00 /bin/bash ./runme_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    926857 926857 926850  0 11:54 pts/1    00:00:00 /bin/sh /home/modules/core/apps/oneapi/2024.1.0/mpi/2021.12/bin/mpirun -hostfile hosts -perhost 2 -np 8 ./runme_intel64_prv -n 117
grant    926858 926858 926850  0 11:54 pts/1    00:00:00 tee -a xhpl_intel64_dynamic_outputs.txt
grant    926863 926863 926857  0 11:54 pts/1    00:00:00 mpiexec.hydra -hostfile hosts -perhost 2 -np 8 ./runme_intel64_prv -n 117120 -b 384 -p 2 -q 4
grant    926864 926864 926863  0 11:54 pts/1    00:00:00 /usr/bin/ssh -q -x grant@z1-33 /home/modules/core/apps/oneapi/2024.1.0/mpi/2021.12/bin//hydra_bstrap_proxy --upstream-host z1-33 -
grant    926865 926865 926863  0 11:54 pts/1    00:00:00 /usr/bin/ssh -q -x grant@z1-34 /home/modules/core/apps/oneapi/2024.1.0/mpi/2021.12/bin//hydra_bstrap_proxy --upstream-host z1-33 -
root     926866 926866  10338  0 11:54 ?        00:00:00 sshd: grant [priv]
root     926870 926870      1  0 11:54 ?        00:00:00 /usr/libexec/sssd/sssd_kcm --uid 0 --gid 0 --logger=files
root     926871 926871      2  0 11:54 ?        00:00:00 [kworker/55:2]
grant    926872 926872 926866  0 11:54 ?        00:00:00 sshd: grant@notty
grant    926873 926873 926872  0 11:54 ?        00:00:00 /home/modules/core/apps/oneapi/2024.1.0/mpi/2021.12/bin//hydra_pmi_proxy --usize -1 --auto-cleanup 1 --abort-signal 9
grant    926933 926933 926873  0 11:54 ?        00:00:00 /bin/bash ./runme_intel64_prv -n 117120 -b 384 -p 2 -q 4
grant    926934 926934 926873  0 11:54 ?        00:00:00 /bin/bash ./runme_intel64_prv -n 117120 -b 384 -p 2 -q 4
grant    926935 926935 926873  0 11:54 ?        00:00:00 /bin/bash ./runme_intel64_prv -n 117120 -b 384 -p 2 -q 4
grant    926936 926936 926873  0 11:54 ?        00:00:00 /bin/bash ./runme_intel64_prv -n 117120 -b 384 -p 2 -q 4
grant    926937 926937 926933 48 11:54 ?        00:00:11 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    926937 926942 926933  0 11:54 ?        00:00:00 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    926937 926948 926933 19 11:54 ?        00:00:04 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    926937 926949 926933 19 11:54 ?        00:00:04 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    926937 926951 926933 19 11:54 ?        00:00:04 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    926937 926953 926933 18 11:54 ?        00:00:04 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    926937 926959 926933 19 11:54 ?        00:00:04 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    926937 926961 926933 18 11:54 ?        00:00:04 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    926937 926963 926933 19 11:54 ?        00:00:04 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    926937 926965 926933 18 11:54 ?        00:00:04 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    926937 926966 926933 19 11:54 ?        00:00:04 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    926937 926967 926933 18 11:54 ?        00:00:04 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    926937 926968 926933 18 11:54 ?        00:00:04 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    926937 926969 926933 18 11:54 ?        00:00:04 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    926937 926994 926933 48 11:54 ?        00:00:11 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    926938 926938 926936 48 11:54 ?        00:00:11 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    926938 926945 926936  0 11:54 ?        00:00:00 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    926938 926970 926936 18 11:54 ?        00:00:04 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    926938 926972 926936 18 11:54 ?        00:00:04 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    926938 926974 926936 18 11:54 ?        00:00:04 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    926938 926976 926936 18 11:54 ?        00:00:04 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    926938 926978 926936 18 11:54 ?        00:00:04 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    926938 926980 926936 18 11:54 ?        00:00:04 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    926938 926982 926936 18 11:54 ?        00:00:04 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    926938 926984 926936 18 11:54 ?        00:00:04 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    926938 926986 926936 18 11:54 ?        00:00:04 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    926938 926988 926936 18 11:54 ?        00:00:04 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    926938 926990 926936 18 11:54 ?        00:00:04 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    926938 926991 926936 18 11:54 ?        00:00:04 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    926938 926996 926936 48 11:54 ?        00:00:11 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    926939 926939 926934 48 11:54 ?        00:00:11 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    926939 926944 926934  0 11:54 ?        00:00:00 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    926939 926946 926934 19 11:54 ?        00:00:04 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    926939 926947 926934 18 11:54 ?        00:00:04 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    926939 926950 926934 19 11:54 ?        00:00:04 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    926939 926952 926934 18 11:54 ?        00:00:04 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    926939 926954 926934 18 11:54 ?        00:00:04 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    926939 926955 926934 19 11:54 ?        00:00:04 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    926939 926956 926934 18 11:54 ?        00:00:04 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    926939 926957 926934 19 11:54 ?        00:00:04 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    926939 926958 926934 18 11:54 ?        00:00:04 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    926939 926960 926934 18 11:54 ?        00:00:04 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    926939 926962 926934 18 11:54 ?        00:00:04 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    926939 926964 926934 19 11:54 ?        00:00:04 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    926939 926995 926934 48 11:54 ?        00:00:11 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    926940 926940 926935 48 11:54 ?        00:00:11 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    926940 926943 926935  0 11:54 ?        00:00:00 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    926940 926971 926935 18 11:54 ?        00:00:04 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    926940 926973 926935 18 11:54 ?        00:00:04 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    926940 926975 926935 17 11:54 ?        00:00:04 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    926940 926977 926935 18 11:54 ?        00:00:04 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    926940 926979 926935 18 11:54 ?        00:00:04 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    926940 926981 926935 18 11:54 ?        00:00:04 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    926940 926983 926935 18 11:54 ?        00:00:04 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    926940 926985 926935 18 11:54 ?        00:00:04 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    926940 926987 926935 18 11:54 ?        00:00:04 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    926940 926989 926935 18 11:54 ?        00:00:04 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    926940 926992 926935 18 11:54 ?        00:00:04 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    926940 926993 926935 18 11:54 ?        00:00:04 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
grant    926940 926997 926935 48 11:54 ?        00:00:11 ./xhpl_intel64_dynamic -n 117120 -b 384 -p 2 -q 4
```