import psutil

##showing processes
def show_all_processes():
    for process in psutil.process_iter(['pid', 'name', 'username']):
        try:
            pid = process.info['pid']
            name = process.info['name']
            user = process.info['username']
            print(f"PID: {pid}, Name: {name}, User: {user}")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue


##used to see memory/CPU usage 
def show_process_usage():
    for proc in psutil.process_iter(['pid', 'name', 'memory_percent', 'cpu_percent']):
        try:
            print(f"PID: {proc.info['pid']}, Name: {proc.info['name']}, Memory: {proc.info['memory_percent']:.2f}%, CPU: {proc.info['cpu_percent']:.2f}%")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue