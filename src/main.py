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



def main():
    # Start in the current working directory

    current_path = os.getcwd() 

    print("Welcome to OS-Insight File Explorer!")
    print("Type 'help' for available commands.\n")


    #used to create an infinite loop so that users can keep typing commands
    while True:
        #creating a list out of the path
        cmd = input(f"{current_path}> ").strip().split()
        if not cmd:
            continue  # Skip if user presses enter without typing anything

        ##if the user's command starts with 'ls' then list_directory is called
        if cmd[0] == "ls":
            list_directory(current_path)

        ##if the user's command starts with 'cd' 
        elif cmd[0] == "cd" and len(cmd) > 1:
            new_path = os.path.join(current_path, cmd[1])
            if os.path.isdir(new_path):
                current_path = os.path.abspath(new_path) ##changing the directory 
            else:
                print("Directory does not exist") 

        elif cmd[0] == "info" and len(cmd) > 1:
            ##showing the file info calling the show file info function
            show_file_info(os.path.join(current_path, cmd[1])) 

        elif cmd[0] == "procs":
            ##shows the processes running
            #processes_using_file(os.path.join(current_path, cmd[1]))
            show_all_processes()

        elif cmd[0] == "help":
            print("Available commands: ls, cd <dir>, info <file>, procs [limit], exit")

        elif cmd[0] == "exit":
            ##if first word is exit then we leave the file explorer
            print("Exiting File Explorer...")
            break




        else:
            ##showing the approporiate commands
            print("Commands: ls, cd <dir>, info <file>, exit")

##only calls main if file run directly
if __name__ == "__main__":
    main()