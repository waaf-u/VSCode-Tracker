# Welcome to my project, this project will track the time used on VSCode
import psutil
import time
from datetime import datetime
from plyer import notification
import platform

# This checks the platform the user is using
def get_vscode_process_name():
    system = platform.system()
    if system == 'Windows':
        return 'Code.exe'
    elif system == 'Darwin':  # macOS
        return 'Visual Studio Code'
    else:  # Linux and others
        return 'code'

# This is a checker to see if VSCode is up and running when launched on the users device
def vscode_checker():
    vscode_process_name = get_vscode_process_name()
    for process in psutil.process_iter(['name']):
        if process.info['name'] == vscode_process_name:
            return True
    return False

# This function tracks when the user opens or closes VSCode and writes the events to a text file.
def log_event(event, timestamp):
    with open("vscode_usage_log.txt", "a") as log_file:
        log_file.write(f"VSCode {event} at {timestamp}\n")
    notification.notify(
        title="VSCode Tracker",
        message=f"VSCode {event} at {timestamp}",
        timeout=5
    )
    print(f"VSCode {event} at {timestamp}")

# Automatic state of running VSCode is off by default
vscode_running = False

# Checks to see if VSCode is running and prints it if true
while True:
    if vscode_checker():
        if not vscode_running:
            log_event("opened", datetime.now())
            vscode_running = True
    else:
        if vscode_running:
            log_event("closed", datetime.now())
            vscode_running = False
    time.sleep(0.1)
