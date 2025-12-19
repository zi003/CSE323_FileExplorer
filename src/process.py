import psutil

##showing processes
def show_all_processes():
    result = []
    ##adjusted column width to make it look nice
    result.append(f"{'PID':<8}{'USER':<25}{'PROCESS NAME'}")
    
    for process in psutil.process_iter(['pid', 'name', 'username']):
        try:
            pid = process.info['pid']
            name = process.info['name'] or ""
            user = process.info['username'] or ""
            result.append(f"{pid:<8}{user:<25}{name}")


        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    return "\n".join(result)


##used to see memory/CPU usage 
def show_process_usage():
    result = []
    result.append("PID\tCPU%\tMEM%\tPROCESS")

    for proc in psutil.process_iter(['pid', 'name', 'memory_percent', 'cpu_percent']):
        try:
            result.append( f"{proc.info['pid']}\t" f"{proc.info['cpu_percent']:.2f}\t" f"{proc.info['memory_percent']:.2f}\t" f"{proc.info['name']}")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    return "\n".join(result)