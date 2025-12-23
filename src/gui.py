import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import os

# importing functions in the filesystem
from filesystem import *
from process import *
from usage_monitor import *
from protectedFile import *

#creating the window with title and size 
root = tk.Tk()
root.title("OS File Explorer & Monitor")
root.geometry("900x600")

#creating the labels 
path_label = tk.Label(root, text="Current Path:")
path_label.pack(anchor="w", padx=10)


path_entry = tk.Entry(root, width=80)
path_entry.pack(padx=10)
path_entry.insert(0, os.getcwd()) ##current directory set in the current path

##creating space to display results
# Frame to hold Text + Scrollbar
output_frame = tk.Frame(root)
output_frame.pack(fill="both", expand=True, padx=10, pady=10)

# Scrollbar
scrollbar = tk.Scrollbar(output_frame)
scrollbar.pack(side="right", fill="y")

# Text widget
output = tk.Text(output_frame, height=25, yscrollcommand=scrollbar.set)
output.pack(side="left", fill="both", expand=True)

# Link scrollbar to text widget
scrollbar.config(command=output.yview)

# Initial text
output.insert("1.0", "Type here to append to a file if you choose edit file..\n")


##frame for the buttons
btn_frame = tk.Frame(root)
btn_frame.pack(pady=10, padx=10, fill="x")  # container for buttons

##function used to display the output
def write_output(text):
    output.delete("1.0", tk.END)
    output.insert(tk.END, text)

#list files gui
def list_files_gui():
    path = path_entry.get()

    try:
        files = list_directory(path)   # helper function
        write_output(files)
    except Exception as e:
        messagebox.showerror("Error", str(e))

##this button provokes the list_files_gui function which calls the helper function
btn_ls = tk.Button(btn_frame, text="List Files", command=list_files_gui, width=15)
btn_ls.grid(row=0, column=0, padx=5, pady=5)



##function used to show file info
def file_info_gui():
    path = path_entry.get()
    try:
        info = show_file_info(path) 
        write_output(info)
    except Exception as e:
        messagebox.showerror("Error", str(e))

##button used to display the file info which calls the file_info_gui function
btn_ls = tk.Button(btn_frame, text="File Info (Inode)", command=file_info_gui, width=15)
btn_ls.grid(row=0, column=1, padx=5, pady=5)


file_frame = tk.Frame(root)
file_frame.pack(pady=10, padx=10, fill="x")

# Label
file_label = tk.Label(file_frame, text="File Name:")
file_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

# Entry
file_name_entry = tk.Entry(file_frame, width=40)
file_name_entry.grid(row=0, column=1, padx=5, pady=5)

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


#Button under the file
file_btn_frame = tk.Frame(file_frame)
file_btn_frame.grid(row=1, column=0, columnspan=2, pady=5)

# Create button
btn_create = tk.Button(file_btn_frame, text="Create", command=create_file_gui, width=12)
btn_create.pack(side="left", padx=5)



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

def prompt_password_and_read(path):
    pw_win = tk.Toplevel(root)
    pw_win.title("Protected File")

    tk.Label(pw_win, text="Enter Password:").pack(pady=5)
    pw_entry = tk.Entry(pw_win, show="*")
    pw_entry.pack(pady=5)

    def verify():
        password = pw_entry.get()
        result = read_protected_file(path, password)
        write_output(result)
        pw_win.destroy()

    tk.Button(pw_win, text="Unlock & Read", command=verify).pack(pady=10)

btn_read = tk.Button(file_btn_frame, text="Read", command=read_file_gui, width=12)
btn_read.pack(side="left", padx=5)



# Delete button
def delete_file_gui():
    directory = path_entry.get()
    file_name = file_name_entry.get()
    if not file_name:
        write_output("Please enter a file name.")
        return
    full_path = os.path.join(directory, file_name)
    result = delete_path(full_path)  # make sure delete_path returns string
    write_output(result)

btn_delete = tk.Button(file_btn_frame, text="Delete", command=delete_file_gui, width=12)
btn_delete.pack(side="left", padx=5)

##append to a file
def append_file_gui():

    
    directory = path_entry.get()
    file_name = file_name_entry.get()
    content = output.get("1.0", tk.END).strip()  # get all text from Text widget

    if not file_name:
        write_output("Please enter a file name.")
        return
    if not content:
        write_output("Text area is empty.")
        return

    full_path = os.path.join(directory, file_name)

    if is_protected_file(full_path):
         write_output("Cannot append: File is password protected.")
    
    else:
     result = append_to_file(full_path, content)  # helper function
     write_output(result)
     ##to clear the text area after appending will show success message for 1.5 seconds before clearing
     root.after(1500, lambda: output.delete("1.0", tk.END))

##append button
btn_append = tk.Button(file_btn_frame, text="Append", command=append_file_gui, width=12)
btn_append.pack(side="left", padx=5)


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

##button to save/edit
btn_save = tk.Button(file_btn_frame, text="Save/Edit", command=save_file_gui, width=12)
btn_save.pack(side="left", padx=5)

#gui function to output all the processes
def show_processes_gui():
    output = show_all_processes()
    write_output(output)

#gui function to display usage of the processes
def show_usage_gui():
    output = show_process_usage()
    write_output(output)

#buttons to view all processes/usage
tk.Button(btn_frame, text="All Processes", command=show_processes_gui, width=15).grid(row=0, column=2, padx=5, pady=5)
tk.Button(btn_frame, text="CPU / Memory", command=show_usage_gui, width=15).grid(row=0, column=3, padx=5, pady=5)


##gui function to monitor usage 
def monitor_usage_gui():
    write_output("Monitoring app usage...\nPlease wait...")

    root.update()  # force GUI refresh

    result = monitor_and_analyze(duration=15, cpu_threshold=20)
    write_output(result)

tk.Button(btn_frame, text="Monitor App Usage", command=monitor_usage_gui, width=18).grid(row=0, column=4, padx=5, pady=5)

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

##Button used to create a protected file
protected_button = tk.Button(file_btn_frame, text="Create Protected",command=create_protected_file_gui)
protected_button.pack(side="left", padx=5)



##calls the gui to run
root.mainloop()


