# Telegram Member Scraper
# Developed by EDWARD
# Contact: +2347019706826

from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
import os
import sys
import configparser
import csv
import time
from colorama import Fore, Style

def display_banner():
    os.system('clear')
    print(f"""
Fore.RED}███████╗██████╗ ██╗    ██╗ █████╗ ██████╗ ██████╗ 
{Fore.CYAN}██╔════╝██╔══██╗██║    ██║██╔══██╗██╔══██╗██╔══██╗
{Fore.GREEN}█████╗  ██║  ██║██║ █╗ ██║███████║██████╔╝██║  ██║
{Fore.YELLOW}██╔══╝  ██║  ██║██║███╗██║██╔══██║██╔══██╗██║  ██║
{Fore.MAGENTA}███████╗██████╔╝╚███╔███╔╝██║  ██║██║  ██║██████╔╝
{Fore.BLUE}╚══════╝╚═════╝  ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ 

{Fore.YELLOW}Telegram Member Scraper v1.0
{Fore.RED}Developed by EDWARD
{Fore.CYAN}Contact: +2347019706826
{Style.RESET_ALL}""")

def load_config():
    config = configparser.RawConfigParser()
    config.read('config.data')
    try:
        return {
            'api_id': config['cred']['id'],
            'api_hash': config['cred']['hash'],
            'phone': config['cred']['phone']
        }
    except KeyError:
        print(f"{Fore.RED}[!] Run setup.py first!{Style.RESET_ALL}")
        sys.exit(1)

def main():
    display_banner()
    config = load_config()
    
    with TelegramClient(config['phone'], config['api_id'], config['api_hash']) as client:
        if not client.is_user_authorized():
            client.send_code_request(config['phone'])
            client.sign_in(config['phone'], input(f"{Fore.GREEN}[+] Enter verification code: {Fore.RED}"))
        
        display_banner()
        print(f"{Fore.GREEN}[+] Fetching your groups...{Style.RESET_ALL}")
        
        groups = []
        result = client(GetDialogsRequest(
            offset_date=None,
            offset_id=0,
            offset_peer=InputPeerEmpty(),
            limit=200,
            hash=0
        ))
        
        for chat in result.chats:
            try:
                if chat.megagroup:
                    groups.append(chat)
            except:
                continue
        
        print(f"{Fore.GREEN}[+] Select a group to scrape:{Style.RESET_ALL}")
        for i, group in enumerate(groups):
            print(f"{Fore.CYAN}[{i}] {group.title}{Style.RESET_ALL}")
        
        try:
            group_index = int(input(f"{Fore.GREEN}[+] Enter group number: {Fore.RED}"))
            target_group = groups[group_index]
            
            print(f"{Fore.GREEN}[+] Scraping members from {target_group.title}...{Style.RESET_ALL}")
            members = client.get_participants(target_group, aggressive=True)
            
            filename = f"members_{target_group.id}.csv"
            with open(filename, 'w', encoding='UTF-8') as f:
                writer = csv.writer(f, delimiter=',', lineterminator='\n')
                writer.writerow(['username', 'user_id', 'access_hash', 'name', 'group', 'group_id'])
                
                for user in members:
                    username = user.username or ""
                    name = (user.first_name or "") + " " + (user.last_name or "")
                    writer.writerow([
                        username,
                        user.id,
                        user.access_hash,
                        name.strip(),
                        target_group.title,
                        target_group.id
                    ])
            
            print(f"{Fore.GREEN}[+] Success! Saved {len(members)} members to {filename}{Style.RESET_ALL}")
            
        except Exception as e:
            print(f"{Fore.RED}[!] Error: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
