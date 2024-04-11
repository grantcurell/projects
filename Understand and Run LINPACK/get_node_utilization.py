import subprocess
import psutil

def get_numa_node_info():
    try:
        lscpu_output = subprocess.check_output(["lscpu", "-p=CPU,NODE"], universal_newlines=True)
        core_to_node = {}
        for line in lscpu_output.splitlines():
            if not line.startswith("#"):
                core_id, node_id = line.split(',')
                core_to_node[int(core_id)] = int(node_id)
        return core_to_node
    except subprocess.CalledProcessError:
        print("Failed to execute lscpu command.")
        return {}

def print_affinity_and_check_numa(process_or_thread):
    try:
        affinity = process_or_thread.cpu_affinity()
        print(f"        CPU Affinity: {affinity}")
    except AttributeError:
        print("        CPU Affinity: Not available for threads")
    except psutil.AccessDenied:
        print("        Access Denied when trying to access CPU affinity.")

def print_threads(process):
    try:
        print(f"PID: {process.pid}, Name: {process.name()}, Threads:")
        for thread in process.threads():
            cpu_time = thread.user_time + thread.system_time
            print(f"    Thread ID: {thread.id}, CPU Time: {cpu_time}")
            print_affinity_and_check_numa(process)
    except psutil.AccessDenied:
        print("Access denied when trying to access threads.")

def find_and_print_process_with_threads(process_name):
    for proc in psutil.process_iter(attrs=['name', 'pid', 'cpu_affinity']):
        if proc.info['name'] == process_name:
            print(f"Process: {proc.info['name']} (PID: {proc.info['pid']})")
            print_affinity_and_check_numa(proc)
            print_threads(proc)

def print_system_cpu_usage(core_to_node):
    cpu_usage_per_core = psutil.cpu_percent(interval=1, percpu=True)
    numa_usage = {}
    active_cores = 0

    print("\nCPU Usage Per Core (NUMA Node):")
    for core_id, usage in enumerate(cpu_usage_per_core):
        numa_node = core_to_node.get(core_id, "Unknown")
        print(f"Core {core_id} (NUMA Node {numa_node}): {usage}%")
        
        if usage > 0.0:
            active_cores += 1
            numa_usage[numa_node] = numa_usage.get(numa_node, 0) + 1

    print(f"\nActive NUMA Nodes (with non-zero CPU usage): {len(numa_usage)}")
    print(f"Total Active Cores (non-zero CPU usage): {active_cores}")
    print(f"NUMA Node Utilization Summary: {numa_usage}")

# Main execution starts here
process_name = 'xhpl_intel64_dynamic'
core_to_node = get_numa_node_info()

find_and_print_process_with_threads(process_name)
print_system_cpu_usage(core_to_node)
