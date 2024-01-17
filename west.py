import winrm

def gather_system_info(ip_address, user, password):
    """Gathers system information from the given remote host."""

    try:
        with winrm.Session(ip_address, auth=(user, password)) as session:
            commands = [
                ("ipconfig /all", "IP Configuration:"),
                ("net user", "Users:"),
                ("net localgroup", "Groups:"),
                ("tasklist /svc", "Tasks:"),
                ("net start", "Services:"),
                ("schtasks", "Task Scheduler:"),
                ("reg query HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run", "Registry Control:"),
                ("netstat -ano", "Active TCP & UDP ports:"),
                ("net view", "File sharing:"),
                ("forfiles /D -10 /S /M *.exe /C \"cmd /c echo @ext @fname @fdate\"", "Files:"),
                ("netsh firewall show config", "Firewall Config:"),
                ("net use", "Sessions with other Systems:"),
                ("net session", "Open Sessions:"),
                ("wevtutil qe security", "Log Entries:")
            ]

            for command, label in commands:
                print(label)
                try:
                    result = session.run_cmd(command)
                    for line in result.std_out.decode('ascii').splitlines():
                        print(line)
                except Exception as e:
                    print(f"Error executing command '{command}': {e}")

    except Exception as e:
        print(f"Failed to connect to {ip_address}: {e}")

with open('cred_list.txt') as f:
    for line in f:
        ip_address, user, password = line.strip().split("|")
        print(f"Gathering information for {ip_address}...")
        gather_system_info(ip_address, user, password)
        print("-" * 40)
