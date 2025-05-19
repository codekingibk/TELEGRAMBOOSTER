# Telegram Member Adder
# Developed by EDWARD
# Contact: +2347019706826

from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
from telethon.tl.functions.channels import InviteToChannelRequest
import os
import sys
import configparser
import csv
import time
import random
import traceback
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

{Fore.YELLOW}Telegram Member Adder v1.0
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

def load_members(filename="members.csv"):
    members = []
    try:
        with open(filename, encoding='UTF-8') as f:
            reader = csv.reader(f, delimiter=",", lineterminator="\n")
            next(reader, None)  # Skip header
            for row in reader:
                if len(row) >= 4:  # Ensure row has enough columns
                    members.append({
                        'username': row[0],
                        'id': int(row[1]),
                        'access_hash': int(row[2]),
                        'name': row[3]
                    })
        return members
    except FileNotFoundError:
        print(f"{Fore.RED}[!] Members file not found! Run scraper.py first.{Style.RESET_ALL}")
        sys.exit(1)

def main():
    display_banner()
    config = load_config()
    members = load_members()
    
    print(f"{Fore.YELLOW}Important Notes:{Style.RESET_ALL}")
    print(f"{Fore.CYAN}1. Telegram limits adding members to ~200 per day per account")
    print("2. Add no more than 30-50 members at a time")
    print("3. Wait 15-30 minutes between adding sessions")
    print("4. Ensure your group allows adding members")
    print(f"5. Respect privacy - don't spam{Style.RESET_ALL}")
    
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
        
        print(f"{Fore.GREEN}[+] Select target group:{Style.RESET_ALL}")
        for i, group in enumerate(groups):
            print(f"{Fore.CYAN}[{i}] {group.title}{Style.RESET_ALL}")
        
        try:
            group_index = int(input(f"{Fore.GREEN}[+] Enter group number: {Fore.RED}"))
            target_group = groups[group_index]
            target_entity = InputPeerChannel(target_group.id, target_group.access_hash)
            
            print(f"{Fore.GREEN}[+] Select add method:{Style.RESET_ALL}")
            print(f"{Fore.CYAN}[1] By username")
            print("[2] By user ID")
            mode = int(input(f"{Fore.GREEN}[+] Enter method (1/2): {Fore.RED}"))
            
            added_count = 0
            for i, user in enumerate(members):
                try:
                    print(f"{Fore.YELLOW}[+] Adding {user.get('name', 'user')} ({i+1}/{len(members)}){Style.RESET_ALL}")
                    
                    if mode == 1 and user['username']:
                        user_to_add = client.get_input_entity(user['username'])
                    elif mode == 2:
                        user_to_add = InputPeerUser(user['id'], user['access_hash'])
                    else:
                        continue
                    
                    client(InviteToChannelRequest(target_entity, [user_to_add]))
                    added_count += 1
                    
                    # Random delay between 5-15 seconds
                    delay = random.randint(5, 15)
                    print(f"{Fore.GREEN}[+] Added. Waiting {delay} seconds...{Style.RESET_ALL}")
                    time.sleep(delay)
                    
                    # Every 20 users, take a longer break
                    if added_count % 20 == 0:
                        long_delay = random.randint(60, 120)
                        print(f"{Fore.YELLOW}[+] Taking a longer break of {long_delay} seconds...{Style.RESET_ALL}")
                        time.sleep(long_delay)
                
                except PeerFloodError:
                    print(f"{Fore.RED}[!] Flood error detected. Stopping for 1 hour.{Style.RESET_ALL}")
                    time.sleep(3600)
                except UserPrivacyRestrictedError:
                    print(f"{Fore.RED}[!] User privacy restrictions - skipped.{Style.RESET_ALL}")
                except Exception as e:
                    print(f"{Fore.RED}[!] Error: {e}{Style.RESET_ALL}")
                    traceback.print_exc()
                    time.sleep(10)
            
            print(f"{Fore.GREEN}[+] Done! Added {added_count} members.{Style.RESET_ALL}")
        
        except Exception as e:
            print(f"{Fore.RED}[!] Error: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
