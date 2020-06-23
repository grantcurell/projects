This is the first problem: https://github.com/open-switch/opx-tools/issues/27

He says the code should be somewhere here: https://github.com/open-switch/opx-base-model/blob/master/yang-models/dell-base-hash.yang

![https://github.com/open-switch/opx-docs/wiki/NAS-L2](images/nas_l2.png)

![https://github.com/open-switch/opx-docs/raw/master/images/opx_architecture.png](images/opx_architecture.png)

[Helpful docs on how yang is processed](https://github.com/open-switch/opx-base-model)

### Installing header files for OPX base

Run `apt install -y libopx-base-model-dev`. The headers will be in `/usr/include/opx`. The metadata files are in `ls /usr/lib/x86_64-linux-gnu/`
