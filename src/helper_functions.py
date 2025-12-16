import os
import stat
import time
import psutil

##created helper functions
##the list_directory function will allow to list the files/directories if its called with a path specified
def list_directory(path):
    try:
        ##listdir used to get all the files/directories in the root directory
        entries = os.listdir(path)
        for e in entries:
            full_path = os.path.join(path, e)
            if os.path.isdir(full_path):
                print(f"[DIR]  {e}")  ##used to print the directory name
            else:
                print(f"[FILE] {e}")  ##used to print the file name if no directory
    except Exception as ex:
        print("Error:", ex)

##used to get the info of a file
def show_file_info(path):
    if not os.path.exists(path):
        print("File does not exist")
        return
    info = os.stat(path)
    ##get all relevant info of a file
    print(f"File: {path}")
    print(f"Size: {info.st_size} bytes")
    print(f"Permissions: {stat.filemode(info.st_mode)}")
    print(f"Owner UID: {info.st_uid}, GID: {info.st_gid}")
    print(f"Inode: {info.st_ino}")
    print(f"Last accessed: {time.ctime(info.st_atime)}")
    print(f"Last modified: {time.ctime(info.st_mtime)}")



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

##creating a file
def create_file(path):
    try:
        if os.path.exists(path):
            print("File already exists.")
            return

        with open(path, 'w') as f:  #open file in write mode
            pass  # creates empty file

        print("File created successfully.")
    except Exception as e:
        print("Error creating file:", e)

#appending to a file
def append_to_file(path, content):
    try:
        if not os.path.exists(path):
            print("File does not exist.")
            return

        ##opening a file in append mode
        with open(path, 'a') as f:
            f.write(content + "\n")  ##appending to the file

        print("Content appended.")
    except Exception as e:
        print("Error appending to file:", e)

##reading a file
def read_file(path):
    try:
        ##check if file exists
        if not os.path.exists(path):
            print("File does not exist.")
            return

        with open(path, 'r') as f:
            print(f.read())
    except Exception as e:
        print("Error reading file:", e)

##deleting a file
def delete_path(path):
    try:
        if not os.path.exists(path):
            print("Path does not exist.")
            return
        ##if file then delete file
        if os.path.isfile(path):
            os.remove(path)
            print("File deleted.")

        ##if directory then delete directory 
        elif os.path.isdir(path):
            os.rmdir(path)
            print("Directory deleted.")

    ##exceptions handled
    except OSError:
        print("Directory not empty or permission denied.")
    except Exception as e:
        print("Error deleting:", e)

##used to memory/CPU usage 
def show_process_usage():
    for proc in psutil.process_iter(['pid', 'name', 'memory_percent', 'cpu_percent']):
        try:
            print(f"PID: {proc.info['pid']}, Name: {proc.info['name']}, Memory: {proc.info['memory_percent']:.2f}%, CPU: {proc.info['cpu_percent']:.2f}%")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

##function to show recent files /directory in current dir
def show_recent_files(path, top=5):
   all_files = []

   for root, dirs, files in os.walk(path):
        for name in files:
            try:
                full_path = os.path.join(root, name)
                mtime = os.stat(full_path).st_mtime
                all_files.append((full_path, mtime))
            except (PermissionError, FileNotFoundError):
                continue  # skip protected files
 
   if not all_files:
        print("No files found.")
        return

   all_files.sort(key=lambda x: x[1], reverse=True)

   print(f"Top {top} recent files under {path}:\n")
   for f, t in all_files[:top]:
        print(f"{f} — Last modified: {time.ctime(t)}")


##function to monitor app usage
def monitor_app_usage(duration=30):
    start_time = time.time()
    usage_stats = {}

    psutil.cpu_percent(interval=None)  # prime CPU stats

    while time.time() - start_time < duration:
        for proc in psutil.process_iter(['pid', 'name', 'memory_percent']):
            try:
                name = proc.info['name']
                cpu = proc.cpu_percent(interval=None)
                mem = proc.info['memory_percent']

                if name:
                    if name not in usage_stats:
                        usage_stats[name] = {'cpu': 0, 'mem': 0, 'samples': 0}

                    usage_stats[name]['cpu'] += cpu
                    usage_stats[name]['mem'] += mem
                    usage_stats[name]['samples'] += 1

            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        time.sleep(1)

    return usage_stats

##currently hard coded apps
SOCIAL_APPS = ["chrome.exe", "msedge.exe", "firefox.exe", "discord.exe"]

def analyze_usage(usage_stats, cpu_threshold=20):
    for app, stats in usage_stats.items():
        avg_cpu = stats['cpu'] / stats['samples']

        if app.lower() in SOCIAL_APPS and avg_cpu > cpu_threshold:
            print(f"⚠ ALERT: High usage detected for {app} (Avg CPU: {avg_cpu:.2f}%)")

