----------health_check.py----------
A script meant to be run via cron daily, monitoring the health of the computer running it. it can check:
- CPU usage, less and more detailed
- Disk usage (checks the main disk, and a mounted one)
- Uptime
It then evaluates that data, and sends an email to the person monitoring the machine with the data set as contents, and with a title simply
saying wether the machine is ok or not.

------------backuper.py------------
Another script meant to be run via cron, but weekly. Its purpose is to backup health_check.py, itself, and most importantly: hlog.log. Features:
- It renames the files to be backuped so that they also contain the date they were backuped
- Backups them in separate folders
- Deletes the oldest item(s) from backup_logs or/and backup_scripts if there are more than 30, so that there are exactly 30 left.
