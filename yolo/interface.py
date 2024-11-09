import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import shutil
import os
from pathlib import Path

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

    def start_internal_camera():
        cam_window.destroy()
        run_yolo_command("python detect.py --weights weights/exp_19.pt --img 640 --conf 0.4 --source 0")

    def start_external_camera():
        cam_window.destroy()
        run_yolo_command("python detect.py --weights weights/exp_19.pt --img 640 --conf 0.4 --source 1")

    btn_internal = tk.Button(cam_window, text="Use Internal Camera", command=start_internal_camera)
    btn_internal.pack(pady=10)

    btn_external = tk.Button(cam_window, text="Use External Camera", command=start_external_camera)
    btn_external.pack(pady=10)

def select_directory():
    dir_path = filedialog.askdirectory()
    if dir_path:
        run_yolo_command(f"python detect.py --weights weights/exp_19.pt --img 640 --conf 0.4 --source {dir_path}")

def zip_latest_results():
    results_base_dir = "runs/detect"
    if os.path.exists(results_base_dir):
        result_dirs = [os.path.join(results_base_dir, d) for d in os.listdir(results_base_dir) if d.startswith("exp")]
        latest_dir = max(result_dirs, key=os.path.getmtime)

        zip_filename = os.path.join(downloads_path, "yolo_latest_results.zip")
        shutil.make_archive(zip_filename.replace(".zip", ""), 'zip', latest_dir)
        print(f"Latest results saved to {zip_filename}!")
    else:
        print("No results found to be zipped!")

def close_application():
    global process
    if process and process.poll() is None:
        process.terminate()
        process = None
    zip_latest_results()
    root.destroy()

root = tk.Tk()
root.title("Cashew Quality Detection Application")

btn_camera = tk.Button(root, text="Use Camera", command=select_camera)
btn_camera.pack(pady=20)

btn_directory = tk.Button(root, text="Use Existing Image or Video", command=select_directory)
btn_directory.pack(pady=20)

btn_close = tk.Button(root, text="Close Application", command=close_application)
btn_close.pack(pady=20)

root.mainloop()
        