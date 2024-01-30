# Understanding PERC Interrupts

- [Testing PERC Interrupts](#testing-perc-interrupts)
	- [Hardware](#hardware)
	- [How Affinity Works](#how-affinity-works)
	- [Initial State](#initial-state)
	- [Testing](#testing)
	- [Understanding Interrupts](#understanding-interrupts)
	- [How Interrupts Are Structured](#how-interrupts-are-structured)
		- [Understanding the Interrupt Table](#understanding-the-interrupt-table)
		- [What is a Trigger Mode and What Does Edge Triggered Mean?](#what-is-a-trigger-mode-and-what-does-edge-triggered-mean)
		- [What is an MSI-X Vector?](#what-is-an-msi-x-vector)
	- [Reverse Engineering the LSI Driver](#reverse-engineering-the-lsi-driver)
	- [Reverse Engineering the MPI Driver](#reverse-engineering-the-mpi-driver)
	- [Helpful Commands](#helpful-commands)
		- [View all Interrupts](#view-all-interrupts)
	- [Investigating Hardware Noise](#investigating-hardware-noise)

## Hardware

I used a Dell R7525 (Rome) for testing.

## How Affinity Works

Here is the provided text converted to Markdown:

1. Driver loads.
2. When the driver loads, it checks the affinity flags and gets the current value as seen in proc. 
   1. The value is defined by PCI_IRQ_AFFINITY (see [PCI_IRQ_AFFINITY documentation](https://www.kernel.org/doc/Documentation/PCI/MSI-HOWTO.txt)).
   2. In the code, that's `irq_flags |= PCI_IRQ_AFFINITY | PCI_IRQ_ALL_TYPES;`
3. The driver then checks how many MSI-X vectors the device can support (a property of the PCIe device itself, and the value is stored in PCIe config space).
4. Driver calls `pci_alloc_irq_vectors_affinity` with `retval = pci_alloc_irq_vectors_affinity(mrioc->pdev, min_vec, max_vectors, irq_flags, &desc)`. See [pci_alloc_irq_vectors_affinity documentation](https://archive.kernel.org/oldlinux/htmldocs/kernel-api/API-pci-alloc-irq-vectors-affinity.html).
5. Based on that call, when the MSI-X vectors get set up, the OS then knows whether to apply affinity rules to them.
6. The OS owns it from there and does the actual allocating of cores.


## Initial State

This was what was present when I logged into the system. I had been doing testing with FIO and interrupt `megasas12-msix120: 18429` had the following:

| IRQ   |   CPU0  |   CPU1  |   CPU2  |   CPU3  |   ...   |   Device                    |
|-------|---------|---------|---------|---------|---------|-----------------------------|
|  379  |   16101 |    0    |    0    |    0    |   ...   | IR-PCI-MSI 101187704-edge  |

I also went ahead and checked the CPU affinity:

```bash
cat /sys/module/megaraid_sas/parameters/smp_affinity_enable
1
```

Check performance mode:

```bash
[grant@r7525 ~]$ cat /sys/module/megaraid_sas/parameters/perf_mode
-1
```

As explained in [the reverse engineering section](#reverse-engineering-the-lsi-driver) the -1 corresponds to the mode being ignored.

Make sure that affinity is enabled for the system as a whole:

```bash
cat /proc/irq/default_smp_affinity
ffffffff,ffffffff,ffffffff,ffffffff
```

Check CPU affinity for observed interrupts?

```bash
cat /proc/irq/379/affinity_hint
00000000,00000000,00000000,00000000
```

## Testing

I used [this script I have previously written](../Using%20FIO/fio_test.py) with:

```bash
sudo python3 fio_test.py -s 1TB /dev/sda
```

Interrupts increased as expected:

```bash
awk '/megasas/ { printf "%s: %s\n", $NF, $2 }' /proc/interrupts
...SNIP...
```

## Understanding Interrupts

I wanted to know more about how the driver functioned so I pulled up my model:

```bash
[grant@r7525 ~]$ lspci | grep -i raid
01:00.0 RAID bus controller: Broadcom / LSI MegaRAID 12GSAS/PCIe Secure SAS39xx
```

which is listed on [the Linux Hardware Page](https://linux-hardware.org/?id=pci:1000-10e2-1028-2176)

## How Interrupts Are Structured

### Understanding the Interrupt Table

`megasas12-msix120` in `/proc/interrupts` is likely an MSI-X (Message Signaled Interrupts Extended) vector used by the MegaRAID SAS driver for a specific RAID controller function. In the Linux kernel, drivers for devices like RAID controllers map their interrupt handling routines to MSI-X vectors. Each vector represents a specific interrupt line that the hardware can trigger. The driver, upon receiving an interrupt on this vector, executes the corresponding interrupt service routine. The naming convention (`megasas12-msix120`) typically includes the driver name (`megasas`) and a unique identifier for the interrupt vector (`msix120`), which helps in identifying the source of the interrupt.

### What is a Trigger Mode and What Does Edge Triggered Mean?

In computing, a trigger mode for an interrupt signals how the processor identifies the presence of an interrupt. "Edge-triggered" means the interrupt is triggered by a change of state or an edge of a signal – specifically, the transition from low voltage to high (rising edge) or high voltage to low (falling edge). Edge-triggered interrupts are activated once per edge event, making them suitable for devices that need to signal a change of state rather than a continuous condition.

### What is an MSI-X Vector?

An MSI-X (Message Signaled Interrupts Extended) vector is a mechanism used in modern computer systems to improve interrupt handling efficiency. It is an extension of MSI, which stands for Message Signaled Interrupts. Both MSI and MSI-X are techniques used to manage interrupts in a more scalable and efficient way compared to traditional interrupt mechanisms like IRQs (Interrupt Request Lines).

In the context of MSI-X:

1. **Message Signaled Interrupts (MSI)**: MSI allows devices to send interrupt signals directly to the CPU(s) without going through a specific interrupt controller chip. Each interrupt is associated with a unique data message and a target CPU or set of CPUs. This reduces interrupt handling overhead and can lead to better performance in multi-core/multi-processor systems.

2. **Message Signaled Interrupts Extended (MSI-X)**: MSI-X is an extension of MSI that provides more flexibility and scalability. It allows a device to have multiple interrupt vectors (or "vectors") associated with it, each pointing to a different interrupt handler. This means that a single device can generate multiple interrupts, each with its own associated handler, which can improve the handling of diverse events or multiple queues in devices like network cards, storage controllers, and more.

## Reverse Engineering the LSI Driver

The driver itself is available on [the official Linux GitHub page](https://github.com/torvalds/linux/tree/master/drivers/scsi/megaraid)

- We can see the irq vectors are registered in [megaraid_sas_base.c](./MegaRAID%20Driver/megaraid_sas_base.c) with [megasas_alloc_irq_vectors(struct megasas_instance *instance)](./MegaRAID%20Driver/megaraid_sas_base.c#L5945)


```c
/**
 * megasas_alloc_irq_vectors -	Allocate IRQ vectors/enable MSI-x vectors
 * @instance:			Adapter soft state
 * return:			void
 */
static void
megasas_alloc_irq_vectors(struct megasas_instance *instance)
{
	int i;
	unsigned int num_msix_req;

	instance->iopoll_q_count = 0;
	if ((instance->adapter_type != MFI_SERIES) &&
		poll_queues) {

		instance->perf_mode = MR_LATENCY_PERF_MODE;
		instance->low_latency_index_start = 1;

		/* reserve for default and non-mananged pre-vector. */
		if (instance->msix_vectors > (poll_queues + 2))
			instance->iopoll_q_count = poll_queues;
		else
			instance->iopoll_q_count = 0;

		num_msix_req = num_online_cpus() + instance->low_latency_index_start;
		instance->msix_vectors = min(num_msix_req,
				instance->msix_vectors);

	}

	i = __megasas_alloc_irq_vectors(instance);

	if (((instance->perf_mode == MR_BALANCED_PERF_MODE)
		|| instance->iopoll_q_count) &&
	    (i != (instance->msix_vectors - instance->iopoll_q_count))) {
		if (instance->msix_vectors)
			pci_free_irq_vectors(instance->pdev);
		/* Disable Balanced IOPS mode and try realloc vectors */
		instance->perf_mode = MR_LATENCY_PERF_MODE;
		instance->low_latency_index_start = 1;
		num_msix_req = num_online_cpus() + instance->low_latency_index_start;

		instance->msix_vectors = min(num_msix_req,
				instance->msix_vectors);

		instance->iopoll_q_count = 0;
		i = __megasas_alloc_irq_vectors(instance);

	}

	dev_info(&instance->pdev->dev,
		"requested/available msix %d/%d poll_queue %d\n",
			instance->msix_vectors - instance->iopoll_q_count,
			i, instance->iopoll_q_count);

	if (i > 0)
		instance->msix_vectors = i;
	else
		instance->msix_vectors = 0;

	if (instance->smp_affinity_enable)
		megasas_set_high_iops_queue_affinity_and_hint(instance);
}
```

- Of particular note here are `MR_BALANCED_PERF_MODE ` AND `MR_LATENCY_PERF_MODE`. It seems these are associated with Aero adapters per the below comment. Moreover the value must be between 0-2 for it to do anything other wise it is ignored.

> "Performance mode (only for Aero adapters), options:
>     0 - balanced: High iops and low latency queues are allocated &
>     interrupt coalescing is enabled only on high iops queues
>     1 - iops: High iops queues are not allocated &
>     interrupt coalescing is enabled on all queues
>     2 - latency: High iops queues are not allocated &
>     interrupt coalescing is disabled on all queues
>     default mode is 'balanced'"

```c
/*
    * Performance mode settings provided through module parameter-perf_mode will
    * take affect only for:
    * 1. Aero family of adapters.
    * 2. When user sets module parameter- perf_mode in range of 0-2.
    */
if ((perf_mode >= MR_BALANCED_PERF_MODE) &&
    (perf_mode <= MR_LATENCY_PERF_MODE))
    instance->perf_mode = perf_mode;
```

- You can check your device model by inspecting the output from `lspci -nn | grep RAID` and then checking it against [the device IDs](./MegaRAID%20Driver/megaraid_sas.h#L34). You can see from the output below I have `[1000:10e2]` which corresponds to `PCI_DEVICE_ID_LSI_AERO_10E2` so I do have an aero-type RAID controller and could change the performance modes if I wanted to.

```bash
[grant@r7525 ~]$ lspci -nn | grep RAID
01:00.0 RAID bus controller [0104]: Broadcom / LSI MegaRAID 12GSAS/PCIe Secure SAS39xx [1000:10e2]
```

```c
/*
 * Device IDs
 */
#define	PCI_DEVICE_ID_LSI_SAS1078R		0x0060
#define	PCI_DEVICE_ID_LSI_SAS1078DE		0x007C
#define	PCI_DEVICE_ID_LSI_VERDE_ZCR		0x0413
#define	PCI_DEVICE_ID_LSI_SAS1078GEN2		0x0078
#define	PCI_DEVICE_ID_LSI_SAS0079GEN2		0x0079
#define	PCI_DEVICE_ID_LSI_SAS0073SKINNY		0x0073
#define	PCI_DEVICE_ID_LSI_SAS0071SKINNY		0x0071
#define	PCI_DEVICE_ID_LSI_FUSION		0x005b
#define PCI_DEVICE_ID_LSI_PLASMA		0x002f
#define PCI_DEVICE_ID_LSI_INVADER		0x005d
#define PCI_DEVICE_ID_LSI_FURY			0x005f
#define PCI_DEVICE_ID_LSI_INTRUDER		0x00ce
#define PCI_DEVICE_ID_LSI_INTRUDER_24		0x00cf
#define PCI_DEVICE_ID_LSI_CUTLASS_52		0x0052
#define PCI_DEVICE_ID_LSI_CUTLASS_53		0x0053
#define PCI_DEVICE_ID_LSI_VENTURA		    0x0014
#define PCI_DEVICE_ID_LSI_CRUSADER		    0x0015
#define PCI_DEVICE_ID_LSI_HARPOON		    0x0016
#define PCI_DEVICE_ID_LSI_TOMCAT		    0x0017
#define PCI_DEVICE_ID_LSI_VENTURA_4PORT		0x001B
#define PCI_DEVICE_ID_LSI_CRUSADER_4PORT	0x001C
#define PCI_DEVICE_ID_LSI_AERO_10E1		0x10e1
#define PCI_DEVICE_ID_LSI_AERO_10E2		0x10e2
#define PCI_DEVICE_ID_LSI_AERO_10E5		0x10e5
#define PCI_DEVICE_ID_LSI_AERO_10E6		0x10e6
#define PCI_DEVICE_ID_LSI_AERO_10E0		0x10e0
#define PCI_DEVICE_ID_LSI_AERO_10E3		0x10e3
#define PCI_DEVICE_ID_LSI_AERO_10E4		0x10e4
#define PCI_DEVICE_ID_LSI_AERO_10E7		0x10e7

/*
 * Intel HBA SSDIDs
 */
#define MEGARAID_INTEL_RS3DC080_SSDID		0x9360
#define MEGARAID_INTEL_RS3DC040_SSDID		0x9362
#define MEGARAID_INTEL_RS3SC008_SSDID		0x9380
#define MEGARAID_INTEL_RS3MC044_SSDID		0x9381
#define MEGARAID_INTEL_RS3WC080_SSDID		0x9341
#define MEGARAID_INTEL_RS3WC040_SSDID		0x9343
#define MEGARAID_INTEL_RMS3BC160_SSDID		0x352B

/*
 * Intruder HBA SSDIDs
 */
#define MEGARAID_INTRUDER_SSDID1		0x9371
#define MEGARAID_INTRUDER_SSDID2		0x9390
#define MEGARAID_INTRUDER_SSDID3		0x9370
```

- We see that CPU affinity is handled in the function [__megasas_alloc_irq_vectors](./MegaRAID%20Driver/megaraid_sas_base.c#L5916). Specifically there appears to be a flag as part of the PERC instance which defines whether SMP (symmetric multi-processing) affinity is enabled `if (instance->smp_affinity_enable)`. You can check this with `cat /sys/module/megaraid_sas/parameters/smp_affinity_enable`

```c
static int
__megasas_alloc_irq_vectors(struct megasas_instance *instance)
{
	int i, irq_flags;
	struct irq_affinity desc = { .pre_vectors = instance->low_latency_index_start };
	struct irq_affinity *descp = &desc;

	irq_flags = PCI_IRQ_MSIX;

	if (instance->smp_affinity_enable)
		irq_flags |= PCI_IRQ_AFFINITY | PCI_IRQ_ALL_TYPES;
	else
		descp = NULL;

	/* Do not allocate msix vectors for poll_queues.
	 * msix_vectors is always within a range of FW supported reply queue.
	 */
	i = pci_alloc_irq_vectors_affinity(instance->pdev,
		instance->low_latency_index_start,
		instance->msix_vectors - instance->iopoll_q_count, irq_flags, descp);

	return i;
}
```

- The variable is defined in [megaraid_sas.h](./MegaRAID%20Driver/megaraid_sas.h#L2334) and we can see that by default it is enabled [`static int smp_affinity_enable = 1;`](./MegaRAID%20Driver/megaraid_sas_base.c#L81).
- We can also conclude from this that the number of vectors is variable and in some way based on the machine's available count of MSI-X vectors as defined by [`MODULE_PARM_DESC(msix_vectors, "MSI-X max vector count. Default: Set by FW");`](./MegaRAID%20Driver/megaraid_sas_base.c#L66):
- We can see the handlers themselves are registered in [`megasas_setup_irqs_ioapic`](./MegaRAID%20Driver/megaraid_sas_base.c#L5671) and [`megasas_setup_irqs_msix`](./MegaRAID%20Driver/megaraid_sas_base.c#L5703)

```c
/*
 * megasas_setup_irqs_ioapic -		register legacy interrupts.
 * @instance:				Adapter soft state
 *
 * Do not enable interrupt, only setup ISRs.
 *
 * Return 0 on success.
 */
static int
megasas_setup_irqs_ioapic(struct megasas_instance *instance)
{
	struct pci_dev *pdev;

	pdev = instance->pdev;
	instance->irq_context[0].instance = instance;
	instance->irq_context[0].MSIxIndex = 0;
	snprintf(instance->irq_context->name, MEGASAS_MSIX_NAME_LEN, "%s%u",
		"megasas", instance->host->host_no);
	if (request_irq(pci_irq_vector(pdev, 0),
			instance->instancet->service_isr, IRQF_SHARED,
			instance->irq_context->name, &instance->irq_context[0])) {
		dev_err(&instance->pdev->dev,
				"Failed to register IRQ from %s %d\n",
				__func__, __LINE__);
		return -1;
	}
	instance->perf_mode = MR_LATENCY_PERF_MODE;
	instance->low_latency_index_start = 0;
	return 0;
}

/**
 * megasas_setup_irqs_msix -		register MSI-x interrupts.
 * @instance:				Adapter soft state
 * @is_probe:				Driver probe check
 *
 * Do not enable interrupt, only setup ISRs.
 *
 * Return 0 on success.
 */
static int
megasas_setup_irqs_msix(struct megasas_instance *instance, u8 is_probe)
{
	int i, j;
	struct pci_dev *pdev;

	pdev = instance->pdev;

	/* Try MSI-x */
	for (i = 0; i < instance->msix_vectors; i++) {
		instance->irq_context[i].instance = instance;
		instance->irq_context[i].MSIxIndex = i;
		snprintf(instance->irq_context[i].name, MEGASAS_MSIX_NAME_LEN, "%s%u-msix%u",
			"megasas", instance->host->host_no, i);
		if (request_irq(pci_irq_vector(pdev, i),
			instance->instancet->service_isr, 0, instance->irq_context[i].name,
			&instance->irq_context[i])) {
			dev_err(&instance->pdev->dev,
				"Failed to register IRQ for vector %d.\n", i);
			for (j = 0; j < i; j++) {
				if (j < instance->low_latency_index_start)
					irq_update_affinity_hint(
						pci_irq_vector(pdev, j), NULL);
				free_irq(pci_irq_vector(pdev, j),
					 &instance->irq_context[j]);
			}
			/* Retry irq register for IO_APIC*/
			instance->msix_vectors = 0;
			instance->msix_load_balance = false;
			if (is_probe) {
				pci_free_irq_vectors(instance->pdev);
				return megasas_setup_irqs_ioapic(instance);
			} else {
				return -1;
			}
		}
	}

	return 0;
}
```

- From this we can see that the interrupt handler is defined as `service_isr`. This in turn corresponds to `megasas_isr`. There are different structs for different megasas devices but they all use the same interrupt handler.

```c
static struct megasas_instance_template megasas_instance_template_xscale = {

	.fire_cmd = megasas_fire_cmd_xscale,
	.enable_intr = megasas_enable_intr_xscale,
	.disable_intr = megasas_disable_intr_xscale,
	.clear_intr = megasas_clear_intr_xscale,
	.read_fw_status_reg = megasas_read_fw_status_reg_xscale,
	.adp_reset = megasas_adp_reset_xscale,
	.check_reset = megasas_check_reset_xscale,
	.service_isr = megasas_isr,
	.tasklet = megasas_complete_cmd_dpc,
	.init_adapter = megasas_init_adapter_mfi,
	.build_and_issue_cmd = megasas_build_and_issue_cmd,
	.issue_dcmd = megasas_issue_dcmd,
};
```

- This takes us to the actual interrupt handler entry point [`megasas_isr`](./MegaRAID%20Driver/megaraid_sas_base.c#L4085). We can see that the function checks to make sure that a firmware reset isn't in progress and if it isn't then it acquires a spinlock and runs the function `megasas_deplete_reply_queue`.

```c
/**
 * megasas_isr - isr entry point
 * @irq:	IRQ number
 * @devp:	IRQ context address
 */
static irqreturn_t megasas_isr(int irq, void *devp)
{
	struct megasas_irq_context *irq_context = devp;
	struct megasas_instance *instance = irq_context->instance;
	unsigned long flags;
	irqreturn_t rc;

	if (atomic_read(&instance->fw_reset_no_pci_access))
		return IRQ_HANDLED;

	spin_lock_irqsave(&instance->hba_lock, flags);
	rc = megasas_deplete_reply_queue(instance, DID_OK);
	spin_unlock_irqrestore(&instance->hba_lock, flags);

	return rc;
}
```

- [`megasas_deplete_reply_queue`](./MegaRAID%20Driver/megaraid_sas_base.c#L4014) is defined below. It processes completed commands from the RAID controller. The function first checks for a reset condition and then clears any pending interrupts. If certain conditions are met, such as a firmware state change or a fault state, it handles these scenarios appropriately, which might include logging the state, managing internal data structures, or scheduling further tasks. The use of tasklet_schedule suggests it defers some processing to a tasklet, a type of bottom half handler in the Linux kernel, for handling tasks that don't need to be processed immediately in the interrupt context.

```c
/**
 * megasas_deplete_reply_queue -	Processes all completed commands
 * @instance:				Adapter soft state
 * @alt_status:				Alternate status to be returned to
 *					SCSI mid-layer instead of the status
 *					returned by the FW
 * Note: this must be called with hba lock held
 */
static int
megasas_deplete_reply_queue(struct megasas_instance *instance,
					u8 alt_status)
{
	u32 mfiStatus;
	u32 fw_state;

	if (instance->instancet->check_reset(instance, instance->reg_set) == 1)
		return IRQ_HANDLED;

	mfiStatus = instance->instancet->clear_intr(instance);
	if (mfiStatus == 0) {
		/* Hardware may not set outbound_intr_status in MSI-X mode */
		if (!instance->msix_vectors)
			return IRQ_NONE;
	}

	instance->mfiStatus = mfiStatus;

	if ((mfiStatus & MFI_INTR_FLAG_FIRMWARE_STATE_CHANGE)) {
		fw_state = instance->instancet->read_fw_status_reg(
				instance) & MFI_STATE_MASK;

		if (fw_state != MFI_STATE_FAULT) {
			dev_notice(&instance->pdev->dev, "fw state:%x\n",
						fw_state);
		}

		if ((fw_state == MFI_STATE_FAULT) &&
				(instance->disableOnlineCtrlReset == 0)) {
			dev_notice(&instance->pdev->dev, "wait adp restart\n");

			if ((instance->pdev->device ==
					PCI_DEVICE_ID_LSI_SAS1064R) ||
				(instance->pdev->device ==
					PCI_DEVICE_ID_DELL_PERC5) ||
				(instance->pdev->device ==
					PCI_DEVICE_ID_LSI_VERDE_ZCR)) {

				*instance->consumer =
					cpu_to_le32(MEGASAS_ADPRESET_INPROG_SIGN);
			}


			instance->instancet->disable_intr(instance);
			atomic_set(&instance->adprecovery, MEGASAS_ADPRESET_SM_INFAULT);
			instance->issuepend_done = 0;

			atomic_set(&instance->fw_outstanding, 0);
			megasas_internal_reset_defer_cmds(instance);

			dev_notice(&instance->pdev->dev, "fwState=%x, stage:%d\n",
					fw_state, atomic_read(&instance->adprecovery));

			schedule_work(&instance->work_init);
			return IRQ_HANDLED;

		} else {
			dev_notice(&instance->pdev->dev, "fwstate:%x, dis_OCR=%x\n",
				fw_state, instance->disableOnlineCtrlReset);
		}
	}

	tasklet_schedule(&instance->isr_tasklet);
	return IRQ_HANDLED;
}
```

- After all this, what I found entertaining is that I learned that modern drivers completely ignore the IRQ number. So in my case the IRQ 379 basically does nothing. What matters is just the state of the device. You can see in `megasas_isr` that the IRQ number comes in as an input and is quite literally, dropped on the floor. Ultimately the request handler just makes sure that the RAID controller is in the appropriate state.

## Reverse Engineering the MPI Driver

- [IRQ setup](./MPI%20Driver/mpi3mr_fw.c#L780). We see that the IRQ affinity is identical.
  - See [the docs](https://archive.kernel.org/oldlinux/htmldocs/kernel-api/API-pci-alloc-irq-vectors-affinity.html) for pci_alloc_irq_vectors_affinityy

```c
irq_flags |= PCI_IRQ_AFFINITY | PCI_IRQ_ALL_TYPES;

retval = pci_alloc_irq_vectors_affinity(mrioc->pdev,
	min_vec, max_vectors, irq_flags, &desc);
```

```c
/**
 * mpi3mr_setup_isr - Setup ISR for the controller
 * @mrioc: Adapter instance reference
 * @setup_one: Request one IRQ or more
 *
 * Allocate IRQ vectors and call mpi3mr_request_irq to setup ISR
 *
 * Return: 0 on success and non zero on failures.
 */
static int mpi3mr_setup_isr(struct mpi3mr_ioc *mrioc, u8 setup_one)
{
	unsigned int irq_flags = PCI_IRQ_MSIX;
	int max_vectors, min_vec;
	int retval;
	int i;
	struct irq_affinity desc = { .pre_vectors =  1, .post_vectors = 1 };

	if (mrioc->is_intr_info_set)
		return 0;

	mpi3mr_cleanup_isr(mrioc);

	if (setup_one || reset_devices) {
		max_vectors = 1;
		retval = pci_alloc_irq_vectors(mrioc->pdev,
		    1, max_vectors, irq_flags);
		if (retval < 0) {
			ioc_err(mrioc, "cannot allocate irq vectors, ret %d\n",
			    retval);
			goto out_failed;
		}
	} else {
		max_vectors =
		    min_t(int, mrioc->cpu_count + 1 +
			mrioc->requested_poll_qcount, mrioc->msix_count);

		mpi3mr_calc_poll_queues(mrioc, max_vectors);

		ioc_info(mrioc,
		    "MSI-X vectors supported: %d, no of cores: %d,",
		    mrioc->msix_count, mrioc->cpu_count);
		ioc_info(mrioc,
		    "MSI-x vectors requested: %d poll_queues %d\n",
		    max_vectors, mrioc->requested_poll_qcount);

		desc.post_vectors = mrioc->requested_poll_qcount;
		min_vec = desc.pre_vectors + desc.post_vectors;
		irq_flags |= PCI_IRQ_AFFINITY | PCI_IRQ_ALL_TYPES;

		retval = pci_alloc_irq_vectors_affinity(mrioc->pdev,
			min_vec, max_vectors, irq_flags, &desc);

		if (retval < 0) {
			ioc_err(mrioc, "cannot allocate irq vectors, ret %d\n",
			    retval);
			goto out_failed;
		}


		/*
		 * If only one MSI-x is allocated, then MSI-x 0 will be shared
		 * between Admin queue and operational queue
		 */
		if (retval == min_vec)
			mrioc->op_reply_q_offset = 0;
		else if (retval != (max_vectors)) {
			ioc_info(mrioc,
			    "allocated vectors (%d) are less than configured (%d)\n",
			    retval, max_vectors);
		}

		max_vectors = retval;
		mrioc->op_reply_q_offset = (max_vectors > 1) ? 1 : 0;

		mpi3mr_calc_poll_queues(mrioc, max_vectors);

	}

	mrioc->intr_info = kzalloc(sizeof(struct mpi3mr_intr_info) * max_vectors,
	    GFP_KERNEL);
	if (!mrioc->intr_info) {
		retval = -ENOMEM;
		pci_free_irq_vectors(mrioc->pdev);
		goto out_failed;
	}
	for (i = 0; i < max_vectors; i++) {
		retval = mpi3mr_request_irq(mrioc, i);
		if (retval) {
			mrioc->intr_info_count = i;
			goto out_failed;
		}
	}
	if (reset_devices || !setup_one)
		mrioc->is_intr_info_set = true;
	mrioc->intr_info_count = max_vectors;
	mpi3mr_ioc_enable_intr(mrioc);
	return 0;

out_failed:
	mpi3mr_cleanup_isr(mrioc);

	return retval;
}
```


## Helpful Commands

### View all Interrupts

```bash
awk '/megasas/ { printf "%s: %s\n", $NF, $2 }' /proc/interrupts
```

## Investigating Hardware Noise

