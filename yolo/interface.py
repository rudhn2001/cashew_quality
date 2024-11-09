import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import subprocess
import shutil
import os
import time
from pathlib import Path
import threading

process = None
downloads_path = str(Path.home() / "Downloads")

def run_yolo_command(command):
    global process
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    if process.returncode == 0:
        print("Command Executed Successfully!")
    else:
        print("Error Occurred:", error.decode())

def select_camera():
    cam_window = tk.Toplevel(root)
    cam_window.title("Select Camera")
    cam_window.geometry("300x200")

    def start_internal_camera():
        cam_window.destroy()
        run_yolo_command("python detect.py --weights weights/exp_19.pt --img 640 --conf 0.4 --source 0")

    def start_external_camera():
        cam_window.destroy()
        run_yolo_command("python detect.py --weights weights/exp_19.pt --img 640 --conf 0.4 --source 1")

    tk.Label(cam_window, text="Choose Camera Source", font=("Arial", 12)).pack(pady=10)
    btn_internal = tk.Button(cam_window, text="Use Internal Camera", command=start_internal_camera, width=25, height=2)
    btn_internal.pack(pady=5)
    btn_external = tk.Button(cam_window, text="Use External Camera", command=start_external_camera, width=25, height=2)
    btn_external.pack(pady=5)

def select_directory():
    dir_path = filedialog.askdirectory()
    if dir_path:
        # Run YOLO command in a separate thread
        threading.Thread(target=run_yolo_command, args=(f"python detect.py --weights weights/exp_19.pt --img 640 --conf 0.4 --source {dir_path}",)).start()

def zip_latest_results():
    results_base_dir = "runs/detect"
    if os.path.exists(results_base_dir):
        result_dirs = [os.path.join(results_base_dir, d) for d in os.listdir(results_base_dir) if d.startswith("exp")]
        latest_dir = max(result_dirs, key=os.path.getmtime)

        zip_filename = os.path.join(downloads_path, "yolo_latest_results.zip")

        # Update the progress bar incrementally
        progress_label.config(text="Zipping latest results...")
        progress_bar["value"] = 0
        root.update_idletasks()

        # Simulate progress with gradual updates
        for i in range(1, 11):
            time.sleep(0.1)  # Simulating work in increments
            progress_bar["value"] += 10
            root.update_idletasks()

        # Actually create the zip file (in one go)
        shutil.make_archive(zip_filename.replace(".zip", ""), 'zip', latest_dir)
        progress_label.config(text=f"Latest results saved to {zip_filename}!")
    else:
        progress_label.config(text="No results found to be zipped!")

def start_zipping_thread():
    # Start the zipping process in a separate thread
    threading.Thread(target=zip_latest_results).start()

def close_application():
    global process
    if process and process.poll() is None:
        process.terminate()
        process = None
    start_zipping_thread()
    root.destroy()

root = tk.Tk()
root.title("Cashew Quality Detection Application")
root.geometry("640x640")
root.resizable(False, False)  # Fix the window size to 640x640

# Title Label
title_label = tk.Label(root, text="Cashew Quality Detection", font=("Arial", 18, "bold"), fg="dark green")
title_label.pack(pady=20)

# Instructions Label
instructions = tk.Label(root, text="Select an input source for detection:", font=("Arial", 12))
instructions.pack(pady=10)

# Frame for Camera and Directory Selection
frame = tk.Frame(root)
frame.pack(pady=20)

btn_camera = tk.Button(frame, text="Use Camera", font=("Arial", 12), command=select_camera, width=25, height=2)
btn_camera.grid(row=0, column=0, padx=10, pady=10)

btn_directory = tk.Button(frame, text="Use Existing Image or Video", font=("Arial", 12), command=select_directory, width=25, height=2)
btn_directory.grid(row=1, column=0, padx=10, pady=10)

# Progress Bar for Zipping Process
progress_bar = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
progress_bar.pack(pady=20)

progress_label = tk.Label(root, text="", font=("Arial", 10))
progress_label.pack()

# Close Button
btn_close = tk.Button(root, text="Close Application", font=("Arial", 12), command=close_application, width=25, height=2)
btn_close.pack(pady=20)

# Footer
footer = tk.Label(root, text="Latest results will be saved in Downloads", font=("Arial", 10), fg="gray")
footer.pack(side="bottom", pady=10)

root.mainloop()
