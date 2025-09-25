# Latitude 7455 – Enabling the WWAN Modem via Device Tree

This is the process I followed to get the Dell Latitude 7455’s cellular modem working under Linux by enabling the PCIe5 controller and wiring up its power and sideband signals in the device tree.

The Latitude 7455 uses **device tree**, not ACPI. If the PCIe5 controller is disabled or incorrectly wired, the modem will never enumerate. Everything here is specifically about getting the modem visible on PCIe domain 0005.

---

## 1. PCIe5 Root Port Changes

First, I enabled the PCIe5 root complex in the device tree and wired up the power rail, GPIOs, and reset delays. Without these, the modem stays dark.

Here’s the full node I edited under `/soc@0/pci@1c00000`:

```dts
status = "okay";                         // Enable PCIe5 controller so the kernel probes it.

vpcie3v3-supply = <0x1a3>;               // 3.3V rail for the WWAN slot. This powers the modem card.

pinctrl-names = "default";               // Tell the kernel to apply the default pin configuration at probe.
pinctrl-0 = <0x300>;                     // Reference to the pin group defined below for PERST#, CLKREQ#, and WAKE#.

perst-gpios = <0x60 0x9b 0x01>;          // PERST# reset signal on TLMM GPIO155 (active high in DT encoding).
clkreq-gpios = <0x60 0x9c 0x01>;         // CLKREQ# signal on TLMM GPIO156, used for ASPM and clock management.
wake-gpios   = <0x60 0x9d 0x01>;         // WAKE# signal on TLMM GPIO157, used for waking the system from low power.

perst-delay-us  = <0x2710>;              // 10ms delay before releasing PERST# after power-up.
resume-delay-us = <0x2710>;              // 10ms delay after resume before link training.

max-link-speed = <0x03>;                 // Cap the PCIe link at Gen3 for stability with the modem.
```

### Why each piece matters

* `status = "okay"`: Without this, PCIe5 is never even probed.
* `vpcie3v3-supply`: Powers the slot; no 3.3V, no modem.
* `perst-gpios`: Allows the host to reset and release the modem.
* `clkreq-gpios`: Enables ASPM and clock request signaling so the link stays stable and power efficient.
* `wake-gpios`: Lets the modem signal the host to wake up for things like SMS or paging.
* `*delay-us`: Some modems need extra time to boot internally before link training.
* `max-link-speed`: Prevents negotiation issues at higher speeds.

---

## 2. Pinmux Group for PCIe5 Signals

Next, I defined the pinmux group that configures those three GPIOs (PERST#, CLKREQ#, WAKE#). Without this, the pins won’t be mapped correctly to the PCIe5 controller.

This goes under `/soc@0/pinctrl@f100000`:

```dts
pcie5-default-state {
    phandle = <0x300>;                   // Referenced by pinctrl-0 above.

    perst-n-pins {
        pins = "gpio155";                // PERST# on GPIO155.
        function = "gpio";               // Standard GPIO output.
        drive-strength = <0x02>;         // 2mA drive is enough for reset.
        bias-disable;                    // No internal pull resistor.
    };

    clkreq-n-pins {
        pins = "gpio156";                // CLKREQ# on GPIO156.
        function = "pcie5_clk";          // Dedicated CLKREQ# function for PCIe5.
        drive-strength = <0x02>;         // Keep low drive strength.
        bias-pull-up;                    // Pull-up so it defaults to inactive when idle.
    };

    wake-n-pins {
        pins = "gpio157";                // WAKE# on GPIO157.
        function = "gpio";               // Input GPIO for wake events.
        drive-strength = <0x02>;         // Minimal drive.
        bias-pull-up;                    // Pull-up so it's inactive unless driven by the modem.
    };
};
```

### Why this is needed

* The SoC has multiplexed pins. This block tells it:

  * Use GPIO155 as a standard output for reset.
  * Use GPIO156 as a special PCIe5 clock request pin.
  * Use GPIO157 as a wake interrupt.
* If this isn’t set, the sideband pins either float or do nothing, and the card never initializes properly.

---

## 3. Make the Group Discoverable

I added an alias so other nodes and debugging tools can reference the group by path:

```dts
pcie5_default = "/soc@0/pinctrl@f100000/pcie5-default-state";
```

---

## 4. Verifying After Boot

Once these changes are in place and the device tree is loaded, I check that everything came up:

1. Verify that PCIe5 shows as enabled in the live device tree:

```bash
cat /proc/device-tree/soc@0/pci@1c00000/status
# Expected: okay
```

2. Check for domain `0005` in `lspci`:

```bash
sudo lspci -Dnn | grep '^0005:'
```

Expected output:

```
0005:00:00.0 PCI bridge [0604]: Qualcomm Technologies, Inc Device [17cb:0111]
0005:01:00.0 Network controller [0280]: Qualcomm Technologies, Inc Device [105b:???]
```

3. Confirm the PCIe5 controller probed:

```bash
dmesg -T | grep -i 'qcom.*pcie.*1c00000\|segment.*5'
```

You should see logs showing the controller powered up and trained the link.

