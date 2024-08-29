import os
import sys
import yaml
import subprocess
import time
sys.path.insert(1, f'{os.getcwd()}/src')
from setup import PhishSetup # type: ignore
from colorama import init, Fore
init()
GREEN = Fore.GREEN
RED   = Fore.RED
BLUE   = Fore.BLUE
RESET = Fore.RESET

os.system("clear")
error_raise = 0
def banner():
    print(f"{RED}         Welcome to Beef-Hacks         {RESET}")
    print(f"""{RED}
     ______ _   _     _    _            _        
    |  ____| | | |   | |  | |          | |       
    | |__  | |_| |__ | |__| | __ _  ___| | _____ {RESET}{BLUE}
    |  __| | __| '_ \|  __  |/ _` |/ __| |/ / __|
    | |____| |_| | | | |  | | (_| | (__|   <\___ {RESET}{GREEN}
    |______|\__|_| |_|_|  |_|\__,_|\___|_|\_\___|
        {RESET}""")
    print("\n")
    print("----------------------------------------------------------------------------")

banner()
result = subprocess.run("apaches2 -help", shell=True, capture_output=True, text=True)
if "not found" in result.stderr and "apache2" in result.stderr:
    print("[-] Apache2 is not installed. Installing apache2: -----")
    result = subprocess.run("apt install apache2 -y", shell=True, capture_output=True, text=True)
    result = subprocess.run("apache2 -help", shell=True, capture_output=True, text=True)
    if "not found" in result.stderr and "apache2" in result.stderr:
        print("[-] Could not install apache2: Install it manaully -----")
        error_raise += 1
    else:
        print("[+] Apache2 is successfully installed!!!!")
else:
    print("[+] Apache2 is already installed!!!!")


original_dir = os.getcwd()
try:
    os.chdir("src/beef-master/")
    with open("beef-status.txt", 'r') as file:
        content = file.read()
    print("[!] Checking beef dependencies installation..........")
    if "Install=1" not in content:
        print("[-] Beef dependencies are not installed. Installing dependencies which make take minutes. WAIT......")
        process = subprocess.Popen(['./install'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                if "This script will install BeEF and its required dependencies (including operating system packages)." in output:
                    process.stdin.write('y\n')
                    process.stdin.flush()
                if "Install completed successfully!" in output:
                    print("[+] Beef dependencies Installed Successfully!!!!!!!")
                    with open("beef-status.txt", 'a') as file:
                        file.write("Install=1\n")
        return_code = process.poll()
    else:
        print("[+] Beef dependencies are already installed!!!!!!!!")
    print("[!] Checking for beef password setup......")
    if "pass-set=1" not in content:
        with open('config.yaml', 'r') as file:
            config = yaml.safe_load(file)
        while True:
            beef_password = input("\n[?] Provide the password for beef panel (It will be used to login to beef panel) --> ")
            if beef_password == "" or beef_password == " ":
                pass
            else:
                config['beef']['credentials']['passwd'] = beef_password
                with open('config.yaml', 'w') as file:
                    yaml.dump(config, file)
                print("[+] Beef password is set Successfully!!!!!!!")
                with open("beef-status.txt", 'a') as file:
                        file.write("pass-set=1\n")
                break
    else:
        print("[+] Beef password is already set!!!!!!!!")
        
except FileNotFoundError:
    print("[-] Beef dependencies are not installed. Installing dependencies which make take minutes. WAIT......")
    process = subprocess.Popen(['./install'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            process.stdin.write('y\n')
            process.stdin.flush()
            if "Install completed successfully!" in output:
                print("[+] Beef dependencies Installed Successfully!!!!!!!")
                with open("beef-status.txt", 'a') as file:
                    file.write("Install=1\n")
    return_code = process.poll()
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    while True:
        beef_password = input("\n[?] Provide the password for beef panel (It will be used to login to beef panel) --> ")
        if beef_password == "" or beef_password == " ":
            pass
        else:
            config['beef']['credentials']['passwd'] = beef_password
            with open('config.yaml', 'w') as file:
                yaml.dump(config, file)
            print("[+] Beef password is set Successfully!!!!!!!")
            with open("beef-status.txt", 'a') as file:
                    file.write("pass-set=1\n")
            break
finally:
    os.chdir(original_dir)
    


time.sleep(2)
if error_raise == 0:
    ON = True
    
    while ON:
        os.system("clear")
        banner()
        print(f"{GREEN}0. Hook targets using beef within the network.")
        print("1. Hook targets using beef within/outside the network using ROUTER PORT FORWARDING.")
        print("2. Hook targets using beef within/outside th network using localhost.run (SSH TUNNELING).")
        print("3. Hook targets using beef within/outside th network using ngrok")
        print("4. Hook targets using beef within/outside th network using serveo.net")
        print("5. Exit.")
        option = input(f"[?] Select the option by typing corresponding index number -->{RESET}")
        if option == "5" or option == "exit" or option == "Exit" or option == "EXIT":
            ON = False
        elif option == "0":
            os.system("clear")
            PhishSetup().setup_within_network()
        elif option == "1":
            os.system("clear")
            PhishSetup().setup_with_port_forwarding()
        elif option == "2":
            os.system("clear")
            PhishSetup().setup_with_localhost_run()
        elif option == "3":
            os.system("clear")
            PhishSetup().setup_with_ngrok()
        elif option == "4":
            os.system("clear")
            PhishSetup().setup_with_serveo()

        

else:
    print("\n\n[--] Apache2 could not be installed. Install it manually and then run this program.")
        
