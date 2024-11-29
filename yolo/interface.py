import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import subprocess
import shutil
import os
import time
from pathlib import Path
import threading
import psutil
from datetime import datetime

process = None
downloads_path = str(Path.home() / "Downloads")

def run_yolo_command(command):
    global process
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    if process.returncode == 0:
        print("Command Executed Successfully!")
        zip_latest_results()  # Automatically zip results after the command finishes
    else:
        print("Error Occurred:", error.decode())

def select_camera():
    cam_window = tk.Toplevel(root)
    cam_window.title("Select Camera")
    cam_window.geometry("300x200")

    def start_internal_camera():
        cam_window.destroy()
        start_camera_detection("python detect.py --weights weights/exp26.pt --img 640 --conf 0.4 --source 0")

    def start_external_camera():
        cam_window.destroy()
        start_camera_detection("python detect.py --weights weights/exp26.pt --img 640 --conf 0.4 --source 1")

    tk.Label(cam_window, text="Choose Camera Source", font=("Arial", 12)).pack(pady=10)
    btn_internal = tk.Button(cam_window, text="Use Internal Camera", command=start_internal_camera, width=25, height=2)
    btn_internal.pack(pady=5)
    btn_external = tk.Button(cam_window, text="Use External Camera", command=start_external_camera, width=25, height=2)
    btn_external.pack(pady=5)

def start_camera_detection(command):
    global process
    if process and process.poll() is None:
        process.terminate()
    process = subprocess.Popen(command, shell=True)

def stop_detection():
    global process
    if process and process.poll() is None:  # Check if the process is still running
        try:
            process.terminate()  # Try terminating the process

            # Wait for process to terminate gracefully
            process.wait(timeout=2)

        except subprocess.TimeoutExpired:
            process.kill()  # Force kill if the process didn't terminate in time

        # Now check if there are any other related Python processes (e.g., 'python detect.py' processes)
        try:
            # Look for Python processes (camera app, detect.py, etc.)
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                if 'python' in proc.info['name'] and 'detect.py' in " ".join(proc.info['cmdline']):
                    proc.terminate()  # Try to terminate it
                    proc.wait(timeout=2)  # Wait for it to terminate gracefully

                    if proc.is_running():
                        proc.kill()  # Force kill if it didn't terminate in time

        except Exception as e:
            print(f"Error killing related processes: {e}")

        # Zip the latest detection folder
        zip_latest_results()
    else:
        messagebox.showinfo("Camera Stopped", "No camera detection process running.")

def zip_latest_results():
    results_base_dir = "runs/detect"
    if os.path.exists(results_base_dir):
        result_dirs = [os.path.join(results_base_dir, d) for d in os.listdir(results_base_dir) if d.startswith("exp")]
        latest_dir = max(result_dirs, key=os.path.getmtime)  # Get the most recent 'exp' directory

        # Generate a unique name for the zip file using a timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        zip_filename = os.path.join(downloads_path, f"yolo_results_{timestamp}.zip")

        progress_label.config(text="Zipping latest results...")
        progress_bar["value"] = 0
        root.update_idletasks()

        # Update progress bar while zipping
        for i in range(1, 11):
            time.sleep(0.1)
            progress_bar["value"] += 10
            root.update_idletasks()

        # Create a zip file from the latest detection folder
        shutil.make_archive(zip_filename.replace(".zip", ""), 'zip', latest_dir)
        progress_label.config(text=f"Latest results saved to {zip_filename}!")
        messagebox.showinfo("Zipping Complete", "Results stored successfully in Downloads.")
    else:
        messagebox.showinfo("Error", "No detection results found.")

def select_directory():
    dir_path = filedialog.askdirectory()
    if dir_path:
        threading.Thread(target=run_yolo_command, args=(f"python detect.py --weights weights/exp_19.pt --img 640 --conf 0.4 --source {dir_path}",)).start()

def close_application():
    global process
    if process and process.poll() is None:  # Check if process is still running
        process.terminate()
        try:
            process.wait(timeout=1)  # Give it a second to close gracefully
        except subprocess.TimeoutExpired:
            process.kill()  # Force kill if it didn't terminate in time

    root.quit()  # Stop the Tkinter main loop
    root.destroy()  # Destroy the window
    os._exit(0)  # Ensure all threads and processes are killed


root = tk.Tk()
root.title("Cashew Quality Detection Application")
root.geometry("640x640")
root.resizable(False, False)

title_label = tk.Label(root, text="Cashew Quality Detection", font=("Arial", 18, "bold"), fg="dark green")
title_label.pack(pady=20)

instructions = tk.Label(root, text="Select an input source for detection:", font=("Arial", 12))
instructions.pack(pady=10)

frame = tk.Frame(root)
frame.pack(pady=20)

btn_camera = tk.Button(frame, text="Use Camera", font=("Arial", 12), command=select_camera, width=25, height=2)
btn_camera.grid(row=0, column=0, padx=10, pady=10)

btn_directory = tk.Button(frame, text="Use Existing Image or Video", font=("Arial", 12), command=select_directory, width=25, height=2)
btn_directory.grid(row=1, column=0, padx=10, pady=10)

progress_bar = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
progress_bar.pack(pady=20)

progress_label = tk.Label(root, text="", font=("Arial", 10))
progress_label.pack()

btn_stop = tk.Button(root, text="Stop Detection", font=("Arial", 12), command=stop_detection, width=25, height=2)
btn_stop.pack(pady=10)

btn_close = tk.Button(root, text="Close Application", font=("Arial", 12), command=close_application, width=25, height=2)
btn_close.pack(pady=20)

footer = tk.Label(root, text="Latest results will be saved in Downloads", font=("Arial", 10), fg="gray")
footer.pack(side="bottom", pady=10)

root.mainloop()
