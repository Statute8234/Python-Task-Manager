from tkinter import *
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import psutil
import pygetwindow as gw

def button_action():
    print("Button pressed!")

# Get all network connections
def list_process_network_info(process_name):
    connections = psutil.net_connections(kind='inet')
    connection_details = []
    # First, find the PIDs associated with the given process name
    target_pids = {p.pid for p in psutil.process_iter(['pid', 'name']) if p.info['name'] == process_name}

    # Now filter and collect details of connections that belong to these PIDs
    for conn in connections:
        if conn.pid in target_pids:
            local_address = f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else "N/A"
            remote_address = f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "N/A"
            connection_details.append({
                'Status': conn.status
            })
    return connection_details if connection_details else f"N/A"
        
app_names = set()
def list_background_processes():
    for process in psutil.process_iter(['pid', 'name', 'username']):
        try:
            with process.oneshot():
                pid = process.pid
                name = process.name()
                #cpu_usage = process.cpu_percent(interval=1.0)
                memory_info = process.memory_full_info()
                memory_usage = memory_info.uss
                memory_usage = memory_info.uss
                memory_usage_final = memory_usage / 1024 ** 2
                Network = list_process_network_info(name)
                app_names.add((name,1,str(memory_usage_final) + " MB",str(Network)))
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
list_background_processes()

def setup_treeview():
    # Define columns
    columns = ('Name', 'CPU', 'Disk','Network')
    tree['columns'] = columns
    tree.heading('#0', text='ID', anchor=W)

    for col in columns:
        tree.heading(col, text=col.capitalize(), anchor=W)
        tree.column(col, width=100, anchor=W)  # Column headers

    # Define column widths and alignments
    tree.column('#0', width=40, anchor=W)  # The first column for IDs
    tree.column('Name', width=100, anchor=W)
    tree.column('CPU', width=100, anchor=W)
    tree.column('Disk', width=100, anchor=W)
    tree.column('Network', width=100, anchor=W)

    # Insert data
    data = []
    for rows in app_names:
        data.append(rows)

    for idx, (Name, CPU, Disk, Network) in enumerate(data, 1):
        tree.insert("", 'end', iid=str(idx), text=str(idx), values=(Name, CPU, Disk, Network))


window = Tk()
window.title("Python Task Manager")
window.geometry("700x700")
window.configure(bg="black")

side_panel = Frame(window, bg='gray', width=100, height=300, borderwidth=2, relief=SUNKEN)
side_panel.pack(side=LEFT, fill=Y)
Processes = Button(side_panel, text="Processes", command=button_action)
Processes.pack(pady=10, padx=10, fill=X)
Performance = Button(side_panel, text="Performance", command=button_action)
Performance.pack(pady=10, padx=10, fill=X)
History = Button(side_panel, text="App History", command=button_action)
History.pack(pady=10, padx=10, fill=X)
Startup = Button(side_panel, text="Startup Apps", command=button_action)
Startup.pack(pady=10, padx=10, fill=X)
Users = Button(side_panel, text="Users", command=button_action)
Users.pack(pady=10, padx=10, fill=X)
Details = Button(side_panel, text="Details", command=button_action)
Details.pack(pady=10, padx=10, fill=X)
Services = Button(side_panel, text="Services", command=button_action)
Services.pack(pady=10, padx=10, fill=X)

Font_tuple = ("Comic Sans", 10, "bold")
label = Label(window, text="Python Task Manager")
label.configure(font = Font_tuple, bg="black", fg="white")
label.pack()

tree = ttk.Treeview(window)
setup_treeview()
tree.pack(padx=10, pady=10, fill=BOTH, expand=True)
window.mainloop()
window.mainloop()