import psutil
import email
import smtplib
import subprocess
import re
import datetime
import os

# Absolute paths to all files used here.
bodypath = "abs_path_to_body.txt"
smart_temppath = "abs_path_to_SMART_tempmon.log"
cpu_temppath = "abs_path_to_CPU_temp.log"
contentpath = "abs_path_to_content.txt"

# Returns: whether the CPU's usage is above 85%, and the usage.
def check_cpu():
    usage = psutil.cpu_percent()
    return [usage > 85, usage]

# Checks 2 disks and returns: whether one of the two disks' usage is above 80%, and the output of a command (stored at the body.txt file) showing the detailed usage of both disks.
def check_disks() -> list[bool, str]:
    # Running the command showing the detailed usage of our two disks, then storing it's output at the body.txt file.
    os.system("df -H | grep '/dev/root\|abs_path_to_second_drive\|Filesystem' > abs_path_to_body.txt")
    disks = []
    with open(bodypath) as f:
        # Checking body.txt to get each disk's usage
        for line in f.readlines():
            line.strip()
            # Using Regex to take the desired data, if any.
            disk = re.search(r"([^ ]+) +([^A-Z]+[A-Z] +){3}([0-9]+)%", line)
            if disk != None:
                # Creating a dictionary with the valuable data and storing it in a list.
                disks.append({"name": disk.group(1), "percentage": int(disk.group(3))})
        # Finally returning what has been described at the comment above this function.
        return [disks[0]["percentage"] > 80 or disks[1]["percentage"] > 80, f.readlines()]

# Returns: the machine's uptime.
def find_uptime() -> str:
    # Getting uptime info, then getting the actual uptime from the command with Regex, then returning it.
    uptime = subprocess.run(["uptime"], capture_output = True, text = True)
    time = re.search(r"up *([^,]+)", uptime.stdout)
    time = time.group(1)
    return time

# Sends an email to whoever is monitoring the machine, containing: the machine's uptime, CPU info, HDD info, Disk info, and the machine's RAM usage. Takes a parameter 'subject' saying whether the machine is OK or not.
def send_email(subject : str):
    with open(bodypath) as f:
        # Taking info about the CPU (less and more detailed respectively), and the RAM.
        cpu_temp = subprocess.run(["tail", "-1", cpu_temppath], capture_output = True, text = True)
        smart_cpu = subprocess.run(["tail", "-1", smart_temppath], capture_output = True, text = True)
        overall_ram = subprocess.run(["free"], capture_output = True, text = True)
        gline = ""
        # Capturing the line containing the desired info, which is the only one starting with 'M'. Also, 'gline' stands for 'good line'.
        for line in overall_ram.stdout.split('\n'):
            if line[0] == "M":
                gline = line
                break
        # Processing the desired line using Regex (getting the 'total' and 'used' sectors of the 'free' command seperately), ending up with the string 'ram_final'.
        ram_total = int(re.search(r"Mem: +([0-9]+)", gline).group(1))
        ram_used = int(re.search(r"Mem: +[0-9]+ +([0-9]+)", gline).group(1))
        ram_percent = round(ram_used / ram_total * 100)
        ram_final = f"{ram_percent}%"
        with open(contentpath, "w") as content:
            # Writing the machine's uptime, the content of the 'body.txt' file, CPU info retreived above, HDD info retreived above, and the RAM usage to the 'content.txt' file
            content.write(f"Uptime: {find_uptime()}\n\n{f.read()}\n\nCPU: {cpu_temp.stdout}\nHDD: {smart_cpu.stdout}\n\nRAM: {ram_final}")
            # Starting to compose the email, adding the contents of the 'content.txt' file as content to the email.
            To = "recipient"
            mail = email.message.EmailMessage()
            mail["From"] = "myemail@example.com"
            mail["To"] = To
            mail["Subject"] = subject
        with open(contentpath) as content:
            mail.set_content(content.read())

        # Sending the email via outlook.
        server = smtplib.SMTP("smtp-mail.outlook.com", port=587)
        server.starttls()
        password = "MyPass"
        server.login(mail["From"], password)
        server.send_message(mail)
        server.quit()

# Getting the CPU's usage and our two disks' usages, packed with two booleans.
OK = True
cpu = check_cpu()
disks = check_disks()

# Opening a log, and checking if everything is alright.
with open("abs_path_to_hlog.log", "a") as log:
    # Used in case something is wrong, to give vital info to the one monitoring the machine.
    with open(contentpath) as con:
        # In case any of these ifs are executed, something is wrong. The program will send an email with an easily visible title among others, and some error info. Also, writing the machine's info on the log.
        if cpu[0]:
            subject = "!!! PI WARNING-ERROR !!!"
            send_email(subject)
            log.write(con.read())
            OK = False
        elif disks[0]:
            subject = "!!! PI WARNING-ERROR !!!"
            send_email(subject)
            log.write(con.read())
            OK = False

        # In case nothing is wrong, the program will send an email saying everything is alright, and info about how it is going.
        if OK:
            subject = "*** PI : OK ***"
            send_email(subject)

    # Finally, writing that the script has successfully finished to the log.
    log.write(f"INFO: Successfully finished running health_check.py. Time: {datetime.datetime.now()}\n")
