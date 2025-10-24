# Python v3.13.9 + tkinter

import subprocess
import sys, threading
from tkinter import Tk
from tkinter import Label, Entry, Button
from tkinter import messagebox

# === GUI Setup ===
root = Tk()
root.title("Python Libraries un-install")
root.geometry("335x100")
root.resizable(False, False)
#root.resizable(True, True)

python_path = sys.executable

def update_buttons(*args):
    button_install.config(state="normal" if entry_install.get().strip() else "disabled")
    button_uninstall.config(state="normal" if entry_uninstall.get().strip() else "disabled")

def run_pip(python_exe, action, package, target=None):
    cmd = [python_exe, "-m", "pip", action, package]
    if action == "uninstall":
        cmd.append("-y")
    if target:
        cmd += ["--target", target]
    subprocess.run(cmd, check=True)

# === Install Section ===
def install_package():
    package = entry_install.get().strip()
    if not package:
        return
    button_install.config(state="disabled")
    button_uninstall.config(state="disabled")

    def worker():
        try:
            run_pip(sys.executable, "install", package)
            messagebox.showinfo("Installation Complete", f"'{package}' was installed successfully.")

        except Exception as e:
            messagebox.showerror("Error", f"Installation failed:\n{str(e)}")
            
        finally:
            button_install.config(state="normal")
            button_uninstall.config(state="normal")
            
    threading.Thread(target=worker).start()

# === Install Layout ===
label_install = Label(text="pip install")
label_install.grid(row=0, column=0, padx=10, pady=10)

entry_install = Entry()
entry_install.grid(row=0, column=1, padx=10, pady=10)
entry_install.bind("<KeyRelease>", update_buttons)

button_install = Button(text="install", command=install_package, state="disabled")
button_install.grid(row=0, column=2, padx=10, pady=10)

# === Uninstall Section ===
def uninstall_package():
    package = entry_uninstall.get().strip()
    if not package:
        return

    button_install.config(state="disabled")
    button_uninstall.config(state="disabled")

    def worker():
        try:
            run_pip(sys.executable, "uninstall", package)
            messagebox.showinfo("Uninstallation Complete", f"'{package}' was uninstalled successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Uninstallation failed:\n{str(e)}")
        finally:
            button_install.config(state="normal")
            button_uninstall.config(state="normal")

    threading.Thread(target=worker).start()

# === Uninstall Layout ===
label_uninstall = Label(text="pip uninstall")
label_uninstall.grid(row=1, column=0, padx=10, pady=10)

entry_uninstall = Entry()
entry_uninstall.grid(row=1, column=1, padx=10, pady=10)
entry_uninstall.bind("<KeyRelease>", update_buttons)

button_uninstall = Button(text="uninstall", command=uninstall_package, state="disabled")
button_uninstall.grid(row=1, column=2, padx=10, pady=10)

root.mainloop()
