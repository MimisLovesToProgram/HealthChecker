import os
import datetime
import re

user = "abs_path_to_user"
logpath = "abs_path_to_log"

# Moving the current hlog to it's new position at 'backup_logs' with the movement day appended in the end of it's name, and creating a new one.
os.system(f"mv {user}path_to_hlog.log {user}path_to_backup_logs/hlog{datetime.date.today()}.log")
os.system(f"touch {user}path_to_hlog.log")

# Copying the files 'health_check.py' and 'backuper.py' to backup_scripts, with their movement dates appended in the end of their names.
os.system(f"cp {user}path_to_health_check.py {user}path_to_backup_scripts/health_check{datetime.date.today()}.py")
os.system(f"cp {user}path_to_backuper.py {user}path_to_backup_scripts/backuper{datetime.date.today()}.py")

# When this folder has more than 30 logs backuped, the program will remove the oldest log.
if len(os.listdir(user + "path_to_backup_logs")) > 30:
    today = re.search(r"([0-9]+)-([0-9]+)-([0-9]+)", str(datetime.datetime.today())).groups()
    oldest = {"name": "example", "year": int(today[0]), "month": int(today[1]), "day": int(today[2])}
    for file in os.listdir(user + "path_to_backup_logs"):
        # Getting the date the file was backuped using Regex, and then comparing it with the current oldest's one.
        date = re.search(r"hlog([0-9]+)-([0-9]+)-([0-9]+).log", file)
        year = int(date.group(1))
        month = int(date.group(2))
        day = int(date.group(3))
        # If any of the ifs is executed, the current oldest file is replaced.
        if year < oldest["year"]:
            oldest = {"name": file, "year": year, "month": month, "day": day}
        elif year == oldest["year"] and month < oldest["month"]:
            oldest = {"name": file, "year": year, "month": month, "day": day}
        elif year == oldest["year"] and month == oldest["month"] and day < oldest["day"]:
            oldest = {"name": file, "year": year, "month": month, "day": day}
    os.remove(user + "path_to_backup_logs/" + oldest["name"])

# Everything here works the exact same way as the above if, but this one is for backuped scripts, not logs, and we remove a second item based on the first removed item's date
if len(os.listdir(user + "path_to_backup_scripts")) > 30:
    today = re.search(r"([0-9]+)-([0-9]+)-([0-9]+)", str(datetime.datetime.today())).groups()
    oldest = {"name": "example", "year": int(today[0]), "month": int(today[1]), "day": int(today[2])}
    for file in os.listdir(user + "path_to_backup_scripts"):
        date = re.search(r"[^0-9]+([0-9]+)-([0-9]+)-([0-9]+).py", file)
        year = int(date.group(1))
        month = int(date.group(2))
        day = int(date.group(3))
        if year < oldest["year"]:
            oldest = {"name": file, "year": year, "month": month, "day": day}
        elif year == oldest["year"] and month < oldest["month"]:
            oldest = {"name": file, "year": year, "month": month, "day": day}
        elif year == oldest["year"] and month == oldest["month"] and day < oldest["day"]:
            oldest = {"name": file, "year": year, "month": month, "day": day}
    os.remove(user + "path_to_backup_scripts/" + oldest["name"])
    # Append a zero at the end of the oldest months and days if they are below 10, because this is how such months and days get treated in our filenames
    if oldest["month"] < 10:
        oldest["month"] = "0" + str(oldest["month"])
    if oldest["day"] < 10:
        oldest["day"] = "0" + str(oldest["day"])
    # Identify the first deleted file, and delete the second one accordingly.
    if "backuper" in oldest["name"]:
        os.remove(f"path_to_backup_scripts/health_check{oldest['year']}-{oldest['month']}-{oldest['day']}.py")
    else:
        os.remove(f"path_to_backup_scripts/backuper{oldest['year']}-{oldest['month']}-{oldest['day']}.py")

# Finally, writing to the new log that the program has finished.
with open(logpath, "a") as log:
    log.write(f"INFO: Successfully finished running backuper.py. Time: {datetime.datetime.now()}\n")
