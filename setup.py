#!/usr/bin/env python3
# Telegram Member Tool Setup
# Developed by EDWARD
# Contact: +2347019706826

import os
import sys
import configparser
from colorama import Fore, Style

def display_banner():
    os.system('clear')
    print(f"""
{Fore.RED}╔═╗{Fore.CYAN}┌─┐┌┬┐┬ ┬┌─┐
{Fore.RED}╚═╗{Fore.CYAN}├┤  │ │ │├─┘
{Fore.RED}╚═╝{Fore.CYAN}└─┘ ┴ └─┘┴

{Fore.YELLOW}Telegram Member Tool v2.0
{Fore.RED}Developed by EDWARD
{Fore.CYAN}Contact: +2347019706826
{Style.RESET_ALL}""")

def main():
    display_banner()
    print(f"{Fore.GREEN}[+] Installing requirements...{Style.RESET_ALL}")
    os.system('pip install telethon colorama')
    
    display_banner()
    config = configparser.RawConfigParser()
    config.add_section('cred')
    
    print(f"{Fore.GREEN}[+] Telegram API Setup{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Note: Get API ID and Hash from https://my.telegram.org{Style.RESET_ALL}")
    
    config.set('cred', 'id', input(f"{Fore.GREEN}[+] Enter API ID: {Fore.RED}"))
    config.set('cred', 'hash', input(f"{Fore.GREEN}[+] Enter API Hash: {Fore.RED}"))
    config.set('cred', 'phone', input(f"{Fore.GREEN}[+] Enter phone number (with country code): {Fore.RED}"))
    
    with open('config.data', 'w') as configfile:
        config.write(configfile)
    
    print(f"\n{Fore.GREEN}[+] Setup complete!")
    print(f"{Fore.GREEN}[+] You can now run scraper.py or adder.py")
    print(f"{Fore.YELLOW}Important: Respect Telegram's limits to avoid account restrictions.{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
