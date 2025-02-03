# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 08:56:50 2025

@author: DiMartino
"""

import getpass

def welcome_user():
    username = getpass.getuser()
    print(f"Ciao, {username}! Avvio subito il programma per te.")
        
def welcome_user_anfia():
    username = getpass.getuser()
    
    if "sala" in username.casefold():
        print("Ciao Miriam! Avvio subito il programma per te.")
    elif "irene" in username.casefold():
        print("Ciao Alessio! Avvio subito il programma per te.")
    elif "dimartino" in username.casefold():
        print("Ciao Cosimo! Avvio subito il programma per te.")
        
    else:
        print(f"Ciao {username}! Avvio subito il programma per te.")
