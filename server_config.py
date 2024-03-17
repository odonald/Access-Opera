import tkinter as tk
from tkinter import simpledialog
import threading
import iso639
import socket
import webbrowser

def start_server_thread(start):
    global server_running  # Declare server_running as a global variable
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True  # Allow the thread to exit when the main program exits
    server_thread.start()
    if start:
        server_thread = threading.Thread(target=run_server, daemon=True)
        server_thread.start()
        server_running = True
        if local_ip == "127.0.0.1":
            server_status_label.configure(text=f"LOCAL - No network detected")
            server_indicator.configure(bg="red")
        else:
            server_status_label.configure(text=f"Live\n http://{local_ip}:{port_number}")
            server_indicator.configure(bg="green")
    else:
        server_running = False
        server_status_label.configure(text=f"Idle")
        server_indicator.configure(bg="red")

local_ip = socket.gethostbyname(socket.gethostname())

port_number = 7832
def change_port():
    global port_number, server_running
    reserved_ports = [80, 443, 8080, 8443]  # List of reserved ports

    # Stop the existing server if it's running
    if server_running:
        start_server_thread(start=False)
        server_running = False
        server_status_label.configure(text=f"Idle")
        server_indicator.configure(bg="red")

    while True:
        new_port = simpledialog.askstring("Change Port", "Enter new port number between 1024 and 65535:", parent=root)
        if new_port:
            try:
                port_int = int(new_port)
                if 1024 <= port_int <= 65535 and port_int not in reserved_ports:
                    port_number = port_int
                    url = f"http://{local_ip}:{port_number}/stream/push"  # Update the url variable

                    # Start a new server with the updated port
                    server_thread = threading.Thread(target=run_server, daemon=True)
                    server_thread.start()
                    server_running = True
                    if local_ip == "127.0.0.1":
                        server_status_label.configure(text=f"LOCAL - No network detected")
                        server_indicator.configure(bg="red")
                    else:
                        server_status_label.configure(text=f"Live\n http://{local_ip}:{port_number}")
                        server_indicator.configure(bg="green")
                    break
                else:
                    tk.messagebox.showerror("Invalid Port", "The selected port is already reserved or invalid.")
            except ValueError:
                tk.messagebox.showerror("Invalid Port", "Please enter a valid port number.")
        else:
            break

url = f"http://{local_ip}:{port_number}/stream/push"

original_file = None
translation_file = None
original_lines = []
translation_lines = []
additional_languages = {}
combined_lines = []
current_line = 0
imported_languages_label = []

if original_lines:
    combined_lines.extend(original_lines)

if translation_lines:
    combined_lines.extend(translation_lines)

current_line = 0 if combined_lines else None

# Create a dictionary of all available languages using the iso639 package
available_languages = {lang.name: lang.alpha2 for lang in iso639.languages}


def open_url_in_browser(local_ip, port_number):
    url = f"http://{local_ip}:{port_number}"
    webbrowser.open(url)
