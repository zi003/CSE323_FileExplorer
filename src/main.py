import os
from filesystem import *
from process import *
from usage_monitor import *



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

        ##user can get help with the available commands
        elif cmd[0] == "help":
            print("Available commands: ls, cd <dir>, info <file>, touch, write, rd, del, exit")

        ##user can use 'touch' to create a file
        elif cmd[0] == "touch" and len(cmd) > 1:
            create_file(os.path.join(current_path, cmd[1]))

        ##user can use 'write' to write to a file
        elif cmd[0] == "write" and len(cmd) > 2:
             path = os.path.join(current_path, cmd[1])
             content = " ".join(cmd[2:])
             append_to_file(path, content)

        ##user can use rd to read a file
        elif cmd[0] == "rd" and len(cmd) > 1:
             read_file(os.path.join(current_path, cmd[1]))

        ##user can use del to delete a file
        elif cmd[0] == "del" and len(cmd) > 1:
            delete_path(os.path.join(current_path, cmd[1]))

        ##user can see memory usage
        elif cmd[0] == "check_mem":
            show_process_usage()

        ##user can see recent files
        elif cmd[0] == "recent_files":
            show_recent_files(current_path)

        elif cmd[0] == "monitor":
            print("Monitoring application usage...")
            stats = monitor_app_usage(30)
            analyze_usage(stats)

        ##if first word is exit then we leave the file explorer
        elif cmd[0] == "exit":
            print("Exiting File Explorer...")
            break

        else:
            ##showing the approporiate commands
            print("Commands: ls, cd <dir>, info <file>, touch, write, rd, del, exit")

##only calls main if file run directly
if __name__ == "__main__":
    main()