import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import os

# importing helper functions
from filesystem import *
from process import *
from usage_monitor import *
from protectedFile import *

#creating the window with title and size 
root = tk.Tk()
root.title("File Explorer & Monitor")
root.geometry("900x600")

##getting the folders/file/lock
folder_icon = tk.PhotoImage(file="icons/folder.png")
file_icon   = tk.PhotoImage(file="icons/file.png")

##making tree view to view the files nicely
file_view_frame = tk.LabelFrame(root, text="File View", padx=5, pady=5)
file_view_frame.config(width=600, height=200)
file_view_frame.pack_propagate(False)  ##preventing the frame from fitting the children
file_view_frame.pack(padx=10, pady=5) 


#creating the path frame
path_frame = tk.LabelFrame(root, text="Path Navigation", padx=10, pady=10)
path_frame.pack(fill="x", padx=10, pady=5)

#Adding label for the path 
tk.Label(path_frame, text="Current Path:").grid(row=0, column=0, sticky="w")

path_entry = tk.Entry(path_frame, width=70)
path_entry.grid(row=0, column=1, padx=5)

##setting the current path as the defualt path 
path_entry.insert(0, os.getcwd())



##function used to display the output on the output frame
def write_output(text):
    output.delete("1.0", tk.END)
    output.insert(tk.END, text)
   
#list files gui
def list_files_gui():
    path = path_entry.get()
    ##removes existing items from the tree before adding new ones
    tree.delete(*tree.get_children()) 

    try:
         for item in get_directory_items(path):
            #if the item is a directory 
            if item["is_dir"]:
                 #insert the file/folder with extra hidden info
                 tree.insert("", "end", text=item["name"], image=folder_icon, values=(item["path"], "dir"))
            else:
                 tree.insert("", "end", text=item["name"], image=file_icon, values=(item["path"], "file"))
    except Exception as e:
        messagebox.showerror("Error", str(e))


##the list files button 
tk.Button(path_frame, text="List Files", width=12, command=list_files_gui).grid(row=0, column=2, padx=5)

##function to go back
def go_back():
    current_path = path_entry.get()

    parent_path = os.path.dirname(current_path)

    if parent_path and parent_path != current_path:
        path_entry.delete(0, tk.END)
        path_entry.insert(0, parent_path)
        list_files_gui()   # refresh file view
    else:
        write_output("Already at root directory.")

top_bar = tk.Frame(file_view_frame)
top_bar.pack(fill="x")

##button to go back
btn_back = tk.Button(file_view_frame, text="⬅ Back",command=go_back,width=10)
btn_back.pack(side="left",  anchor="nw", padx=5, pady=5)

tree = ttk.Treeview(file_view_frame)
tree.pack(fill="both", expand=True)

##function used to show file info
def file_info_gui():
    path = path_entry.get()
    try:
        info = show_file_info(path) 
        write_output(info)
    except Exception as e:
        messagebox.showerror("Error", str(e))
    show_output()

#File Info Button
tk.Button(path_frame, text="File/Folder Info", width=12, command=file_info_gui).grid(row=0, column=3, padx=5)


##output frame only appears when this function is called
def show_output():
    output_frame.pack(fill="both", expand=True, padx=10, pady=10) 

##creating file with the gui
def create_file_gui():
    directory = path_entry.get()          # current folder
    file_name = file_name_entry.get()     # new file name

    if not file_name:
        write_output("Please enter a file name.")
        return

    full_path = os.path.join(directory, file_name)
    result = create_file(full_path)       # call your helper
    write_output(result)
    show_output()



##reading a file
def read_file_gui():
    directory = path_entry.get()
    file_name = file_name_entry.get()

    if not file_name:
        write_output("Please enter a file name.")
        return

    full_path = os.path.join(directory, file_name)

    if not os.path.exists(full_path):
        write_output("File does not exist.")
        return

    #  protected file then get password
    if is_protected_file(full_path):
        prompt_password_and_read(full_path)
    else:
       
        result = read_file(full_path)
        write_output(result)
    show_output()

##this function asks for password to read a protected file
def prompt_password_and_read(path):
    pw_win = tk.Toplevel(root)
    pw_win.title("Protected File")
    pw_win.geometry("400x200")

    tk.Label(pw_win, text="Enter Password:", font=("Arial", 10)).pack(pady=10)
    pw_entry = tk.Entry(pw_win, show="*", font=("Arial", 8), width=30)
    pw_entry.pack(pady=10)

    ##verify the password
    def verify():
        password = pw_entry.get()
        result = read_protected_file(path, password)
        write_output(result)
        pw_win.destroy()

    tk.Button(pw_win, text="Unlock & Read", font=("Arial", 8), command=verify).pack(pady=15)



# Delete function gui
def delete_file_gui():
    directory = path_entry.get()
    file_name = file_name_entry.get()
    if not file_name:
        write_output("Please enter a file name.")
        return
    full_path = os.path.join(directory, file_name)
    result = delete_path(full_path)  # make sure delete_path returns string
    write_output(result)
    show_output()

# Function to save a file
def save_file_gui():
        directory = path_entry.get()
        file_name = file_name_entry.get()
        if not file_name:
            write_output("Please enter a file name.")
            return
        full_path = os.path.join(directory, file_name)

        if is_protected_file(full_path):
         write_output("Cannot save/edit: File is password protected.")
    
        else:
            content = output.get("1.0", tk.END).strip()
            result = save_file(full_path, content)  # ensure save_file returns string
            write_output(result)
        
        show_output()


##gui function to create protected file
def create_protected_file_gui():
    directory = path_entry.get()
    file_name = file_name_entry.get()

    if not directory or not file_name:
        write_output("Please enter directory and file name.")
        return

    # Get content from text editor
    content = output.get("1.0", "end-1c")

    if not content.strip():
        write_output("File content is empty.")
        return

    # Ask for password ONLY when button is pressed
    password = simpledialog.askstring(
        "Password Required",
        "Enter password to protect this file:",
        show="*"
    )

    if not password:
        write_output("Operation cancelled.")
        return

    full_path = os.path.join(directory, file_name)
    result = create_protected_file(full_path, password, content)
    write_output(result)
    show_output()


##creating file frame
file_frame = tk.LabelFrame(root, text="File Operations", padx=10, pady=10)
file_frame.pack(fill="x", padx=10, pady=5)

tk.Label(file_frame, text="File Name:").grid(row=0, column=0, sticky="w")

file_name_entry = tk.Entry(file_frame, width=25)
file_name_entry.grid(row=0, column=1, padx=5)


##creating buttons which use this frame
#Create button
tk.Button(file_frame, text="Create", width=12, command=create_file_gui).grid(row=1, column=0, pady=5)

#Read button
tk.Button(file_frame, text="Read", width=12, command=read_file_gui).grid(row=1, column=1, pady=5)

#Edit/Save button
tk.Button(file_frame, text="Edit / Save", width=12, command=save_file_gui).grid(row=1, column=2, padx=20)

#Delete button
tk.Button(file_frame, text="Delete", width=12, command=delete_file_gui).grid(row=1, column=3, padx=20)


#Create Protected button
tk.Button(file_frame, text="Create Protected", width=15, command=create_protected_file_gui).grid(row=1, column=4, padx=20)


#gui function to output all the processes
def show_processes_gui():
    output = show_all_processes()
    write_output(output)
    show_output()

#gui function to display usage of the processes
def show_usage_gui():
    output = show_process_usage()
    write_output(output)
    show_output()


##gui function to monitor usage 
def monitor_usage_gui():
    write_output("Monitoring app usage...\nPlease wait...")

    root.update()  # force GUI refresh

    result = monitor_and_analyze(duration=15, cpu_threshold=20, time_threshold_minutes=30)
    write_output(result)
    show_output()

##seperate frame for processes
proc_frame = tk.LabelFrame(root, text="Process & Usage Monitor", padx=10, pady=10)
proc_frame.pack(fill="x", padx=10, pady=5)

#button to view all processes 
tk.Button(proc_frame, text="All Processes", width=15,command=show_processes_gui).grid(row=0, column=0, padx=5)

#button to view CPU/Memory usage of processes
tk.Button(proc_frame, text="CPU / Memory", width=15,command=show_usage_gui).grid(row=0, column=1, padx=5)

#button to view App Usage Alert
tk.Button(proc_frame, text="App Usage Alert", width=15,command=monitor_usage_gui).grid(row=0, column=2, padx=5)




##can click on files
def on_file_select(event):
    selected = tree.focus()
    if not selected:
        return

    # "dir" or "file" -> retrieving that info from the values
    file_type = tree.item(selected, "values")[1]  
    full_path = tree.item(selected, "values")[0]

    #if its a file then that file is put in the file entry
    if file_type == "file":
        file_name_entry.delete(0, tk.END)
        file_name = os.path.basename(full_path)
        file_name_entry.delete(0, tk.END)
        file_name_entry.insert(0, file_name)

    # if its a folder then update the path to include the folder
    elif file_type == "dir":
        current_path = path_entry.get()
        new_path = os.path.join(current_path, tree.item(selected, "text"))
        path_entry.delete(0, tk.END)
        path_entry.insert(0, new_path)
        
        # Auto refresh tree view
        list_files_gui()

tree.bind("<<TreeviewSelect>>", on_file_select)

##display output (creating output frame)
output_frame = tk.LabelFrame(root, text="Output / File Content", padx=5, pady=5)
#output_frame.pack(fill="both", expand=True, padx=10, pady=10)

##making the output frame scrollable
scrollbar = tk.Scrollbar(output_frame)
scrollbar.pack(side="right", fill="y")

output = tk.Text(output_frame, wrap="word", yscrollcommand=scrollbar.set)
output.pack(fill="both", expand=True)

scrollbar.config(command=output.yview)


##calls the gui to run
root.mainloop()


