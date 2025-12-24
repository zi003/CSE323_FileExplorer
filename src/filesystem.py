import os
import time
import stat 

##function to get directory
def get_directory_items(path):
    items = []
    for name in os.listdir(path):
        full_path = os.path.join(path, name)
        items.append({
            "name": name,
            "path": full_path,
            "is_dir": os.path.isdir(full_path)
        })
    return items



##the list_directory function will allow to list the files/directories if its called with a path specified
def list_directory(path):
    try:
        ##listdir used to get all the files/directories in the root directory
        entries = os.listdir(path)
        result = []  #to store the list of results
        for e in entries:
            full_path = os.path.join(path, e)
            if os.path.isdir(full_path):
                result.append(f"[DIR]  {e}")  ##used to print the directory name
            else:
                result.append(f"[FILE] {e}")  ##used to print the file name if no directory

        return "\n".join(result)
    except Exception as ex:

         return f"Error: {ex}"

##used to get the info of a file
def show_file_info(path):
    if not os.path.exists(path):
        return "File does not exist" ##returning a string for the GUI
        
    info = os.stat(path)
    ##get all relevant info of a file
    result = f"File: {path} \n"
    result += f"Size: {info.st_size} bytes \n"
    result += f"Permissions: {stat.filemode(info.st_mode)} \n"
    result += f"Owner UID: {info.st_uid}, GID: {info.st_gid} \n"
    result += f"Inode: {info.st_ino} \n"
    result += f"Last accessed: {time.ctime(info.st_atime)} \n"
    result += f"Last modified: {time.ctime(info.st_mtime)} \n"

    return result


##creating a file
def create_file(path):
    try:
        if os.path.exists(path):
            return "File already exists."

        with open(path, 'w') as f:  #open file in write mode
            pass  # creates empty file

        return "File created successfully."
    except Exception as e:
        return f"Error creating file: {e}"

#appending to a file
def append_to_file(path, content):
    try:
        if not os.path.exists(path):
            return "File does not exist."
           

        ##opening a file in append mode
        with open(path, 'a') as f:
            f.write(content + "\n")  ##appending to the file

        return "Content appended Successfully!"
    except Exception as e:
        return f"Error appending to file:, {e}"

##reading a file
def read_file(path):
    try:
        ##check if file exists
        if not os.path.exists(path):
            return "File does not exist."
            

        with open(path, 'r') as f:
            return f.read()
    except Exception as e:
       return f"Error reading file:, {e}"

##deleting a file
def delete_path(path):
    try:
        if not os.path.exists(path):
            return "Path does not exist."
            
        ##if file then delete file
        if os.path.isfile(path):
            os.remove(path)
            return "File deleted."

        ##if directory then delete directory 
        elif os.path.isdir(path):
            os.rmdir(path)
            return "Directory deleted."

    ##exceptions handled
    except OSError:
        return "Directory not empty or permission denied."
    except Exception as e:
       return f"Error deleting:, {e}"

##helper function to save a file 
def save_file(path, content):
    try:
        if not os.path.exists(path):
            return "File does not exist."
        with open(path, 'w') as f:  # overwrite file
            f.write(content)
        return "File saved successfully."
    except Exception as e:
        return f"Error saving file: {e}"


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
        return "No files found."

   all_files.sort(key=lambda x: x[1], reverse=True)
   result = []
   result.append(f"Top {top} recent files under {path}:\n")

   for f, t in all_files[:top]:
        result.append(f"{f} — Last modified: {time.ctime(t)}")


   return "\n".join(result)