import os
import time
import stat 

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

