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

def get_cpu_affinity(tid):
    try:
        with open(f"/proc/{tid}/status", 'r') as file:
            for line in file:
                if line.startswith("Cpus_allowed_list"):
                    return line.strip().split(":")[1].strip()
    except FileNotFoundError:
        print(f"File not found for TID: {tid}")
    except Exception as e:
        print(f"Error reading CPU affinity for TID: {tid}: {str(e)}")
    return "N/A"

def print_threads(process, core_to_node):
    print(f"PID: {process.pid}, Name: {process.name()}, Threads:")
    header = f"{'Thread ID':<10} {'CPU Time':<10} {'CPU Affinity':<15} {'NUMA Node(s)':<15}"
    print(header)
    print('-' * len(header))
    try:
        for thread in process.threads():
            cpu_time = thread.user_time + thread.system_time
            affinity = get_cpu_affinity(thread.id)
            numa_nodes = {core_to_node.get(int(cpu), 'Unknown') for cpu in affinity.split('-')}
            numa_nodes_str = ', '.join(map(str, numa_nodes))
            print(f"{thread.id:<10} {cpu_time:<10.2f} {affinity:<15} {numa_nodes_str:<15}")
    except psutil.AccessDenied:
        print("Access denied when trying to access threads.")

def find_and_print_process_with_threads(process_name, core_to_node):
    for proc in psutil.process_iter(attrs=['name', 'pid']):
        if proc.info['name'] == process_name:
            print_threads(proc, core_to_node)
            print()  # Add a newline for separation between processes

def print_system_cpu_usage(core_to_node):
    cpu_usage_per_core = psutil.cpu_percent(interval=1, percpu=True)
    print("\nCPU Usage Per Core (NUMA Node):")
    header = f"{'Core ID':<10} {'Usage %':<10} {'NUMA Node':<10}"
    print(header)
    print('-' * len(header))
    for core_id, usage in enumerate(cpu_usage_per_core):
        numa_node = core_to_node.get(core_id, "Unknown")
        print(f"{core_id:<10} {usage:<10.2f} {numa_node:<10}")

# Main execution starts here
process_name = 'xhpl_intel64_dynamic'
core_to_node = get_numa_node_info()

find_and_print_process_with_threads(process_name, core_to_node)
