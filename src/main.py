#!/usr/bin/env python
# -*- coding: utf-8 -*-
#title           :menu.py
#description     :This program displays an interactive menu on CLI for our program
#author          :Beatriz Costa
#date            :07/05/2021
#version         :1.0
#usage           :python3 menu.py
#notes           :
#python_version  :3.8.2
#=======================================================================

# Import the modules needed to run the script.
import sys, os


#
from login import login, register
from hashed import adicionarDesafioH, listarDesafiosH, responderDesafioHash
from cypher import adicionarDesafioC, listarDesafiosC, responderDesafio

# Main definition - constants
menu_actions  = {}  

# =======================
#     MENUS FUNCTIONS
# =======================

# Main menu
def main_menu():
    os.system('clear')
    banner.printbanner()
    print ("Welcome! \n")
    print ("Please choose an option to start with:")
    print ("1. Login")
    print ("2. Create Account")
    print ("3. Help")
    print ("\n0. Quit")
    choice = input(" >>  ")
    exec_menu(choice)

    return

# =======================

# Execute main menu
def exec_menu(choice):
    os.system('clear')
    ch = choice.lower()
    if ch == '':
        menu_actions['main_menu']()
    else:
        try:
            menu_actions[ch]()
        except KeyError:
            print ("Invalid selection, please try again.\n")
            menu_actions['main_menu']()
    return

# =======================

# Execute login menu
def exec_menulogin(choice):
    os.system('clear')
    ch = choice.lower()
    if ch == '':
        submenulogin_actions['']()
    else:
        try:
            submenulogin_actions[ch]()
        except KeyError:
            print ("Invalid selection, please try again.\n")
            submenulogin_actions['menulogin']()
    return

# =======================

# Execute register menu
def exec_menureg(choice):
    os.system('clear')
    ch = choice.lower()
    if ch == '':
        submenuregister_actions['']()
    else:
        try:
            submenuregister_actions[ch]()
        except KeyError:
            print ("Invalid selection, please try again.\n")
            submenuregister_actions['menuregister']()
    return

# =======================

# Execute help menu
def exec_menuhelp(choice):
    os.system('clear')
    ch = choice.lower()
    if ch == '':
        submenuhelp_actions['']()
    else:
        try:
            submenuhelp_actions[ch]()
        except KeyError:
            print ("Invalid selection, please try again.\n")
            submenuhelp_actions['menuhelp']()
    return

# =======================

# Execute homepage
def exec_menuhome(choice):
    os.system('clear')
    ch = choice.lower()
    if ch == '':
        submenuhome_actions['']()
    else:
        try:
            submenuhome_actions[ch]()
        except KeyError:
            print ("Invalid selection, please try again.\n")
            submenuhome_actions['menuhome']()
    return

# =======================

# Execute challenges menu
def exec_menuc(choice):
    os.system('clear')
    ch = choice.lower()
    if ch == '':
        submenuc_actions['']()
    else:
        try:
            submenuc_actions[ch]()
        except KeyError:
            print ("Invalid selection, please try again.\n")
            submenuc_actions['menuchallenges']()
    return

# =======================

# Execute new challenge menu
def exec_menunc(choice):
    os.system('clear')
    ch = choice.lower()
    if ch == '':
        submenunewc_actions['']()
    else:
        try:
            submenunewc_actions[ch]()
        except KeyError:
            print ("Invalid selection, please try again.\n")
            submenunewc_actions['menunewchallenge']()
    return

# =======================

# Execute message decipher challenge menu
def exec_menunc1(choice):
    os.system('clear')
    ch = choice.lower()
    if ch == '':
        submenunewc1_actions['']()
    else:
        try:
            submenunewc1_actions[ch]()
        except KeyError:
            print ("Invalid selection, please try again.\n")
            submenunewc1_actions['menunewctype1']()
    return

# =======================

# Execute hash challenge menu
def exec_menunc2(choice):
    os.system('clear')
    ch = choice.lower()
    if ch == '':
        submenunewc2_actions['']()
    else:
        try:
            submenunewc2_actions[ch]()
        except KeyError:
            print ("Invalid selection, please try again.\n")
            submenunewc2_actions['menunewctype2']()
    return

# =======================

def exec_menusubmitc(choice):
    os.system('clear')
    ch = choice.lower()
    if ch == '':
        submenusubmitc_actions['']()
    else:
        try:
            submenusubmitc_actions[ch]()
        except KeyError:
            print ("Invalid selection, please try again.\n")
            submenusubmitc_actions['submit']()
    return

# =======================

def exec_menusubmith(choice):
    os.system('clear')
    ch = choice.lower()
    if ch == '':
        submenusubmith_actions['']()
    else:
        try:
            submenusubmith_actions[ch]()
        except KeyError:
            print ("Invalid selection, please try again.\n")
            submenusubmith_actions['submit']()
    return

# =======================

# Execute scoreboard menu
def exec_menuscore(choice):
    os.system('clear')
    ch = choice.lower()
    if ch == '':
        submenuscore_actions['']()
    else:
        try:
            submenuscore_actions[ch]()
        except KeyError:
            print ("Invalid selection, please try again.\n")
            submenuscore_actions['scoreboard']()
    return

def exec_menusettings(choice):
    os.system('clear')
    ch = choice.lower()
    if ch == '':
        submenusettings_actions['']()
    else:
        try:
            submenusettings_actions[ch]()
        except KeyError:
            print ("Invalid selection, please try again.\n")
            submenusettings_actions['settings']()
    return

# =======================

# Login Menu
def menulogin():
    if (login.loginUser()): 
        exec_menulogin("1")
    else:
        exec_menulogin("")
    return

# =======================

# Register Menu
def menuregister():
    if (register.registerUser()): 
        exec_menureg("1")
    else:
        exec_menureg("0")
    return

# =======================

# Help Menu
def menuhelp():
    print ("Help me!\n")
    print ("Por informacoes todas bonitinhas")
    print ("9. Back")
    print ("0. Quit")
    choice = input(" >>  ")
    exec_menuhelp(choice)
    return

# =======================

# Homepage
def menuhome():
    print ("Welcome User:\n") #colocar username da pessoa para mais personalização
    print ("HOMEPAGE\n")
    print ("1. List of challenges available")
    print ("2. Submit new challenge") 
    print ("3. Scoreboard")
    print ("4. Settings")
    print ("5. Help")
    print ("0. Logout") 
    choice = input(" >>  ")
    exec_menuhome(choice)
    return

# =======================

# Menu List of Challenges
def menuchallenges():
    print ("CHALLENGES AVAILABLE\n") #colocar lista de challenges available por numero
    print ("1. AES CYPHER CHALLENGES")
    print ("2. HASH CHALLENGES")
    print ("9. Back")
    print ("0. Quit") 
    choice = input(" >>  ")
    exec_menuc(choice)
    return

# =======================

# Menu List of Challenges Cypher
def menuchallengesc():
    print ("CHALLENGES AVAILABLE\n") #colocar lista de challenges available por numero
    listarDesafiosC.listarDesafios()
    print ("Insert number of challenge you want to answer:\n")
    global idc
    idc = input(" >>  ")
    print ("1. Submit solution")
    print ("9. Back")
    print ("0. Quit") 
    choice = input(" >>  ")
    exec_menusubmitc(choice)
    return

# =======================

# Menu List of Challenges Hash
def menuchallengesh():
    print ("CHALLENGES AVAILABLE\n") #colocar lista de challenges available por numero
    listarDesafiosH.listarDesafios()
    print ("Insert number of challenge you want to answer:\n")
    global idc
    idc = input(" >>  ")
    print ("1. Submit solution")
    print ("9. Back")
    print ("0. Quit") 
    choice = input(" >>  ")
    exec_menusubmith(choice)
    return

# =======================

# Menu New Challenge
def menunewchallenge():
    print ("NEW CHALLENGE\n")
    print ("1. Decipher Challenge Type") # decifra de mensagens
    print ("2. Hash Challenge Type") # calcular hash de mensagem
    print ("9. Back")
    print ("0. Quit") 
    choice = input(" >>  ")
    exec_menunc(choice)
    return

# =======================

# Menu New Decipher Challenge
def menunewctype1():
    choice = str(adicionarDesafioC.adicionarDesafioCypher())
    if (choice == "1"):
        print("Your challenge was submitted - Let the challenges begin!")
    exec_menunc1(choice)
    return

# =======================

# Menu New Challenge Hash
def menunewctype2():
    choice = str(adicionarDesafioH.adicionarDesafioHash())
    if (choice == "1"):
        print("Your challenge was submitted - Let the challenges begin!")
    exec_menunc2(choice)
    return

# =======================

# Menu Submit Challenge Hash
def submitchallengeh(): #colocar mensagem de sucesso ou insucesso e no tipo de desafios de mensagem, colocar a mensagem decifrada
    responderDesafioHash.responderDesafioHash(idc)
    print ("9. Back")
    print ("0. Quit") 
    choice = input(" >>  ")
    exec_menusubmith(choice)
    return

# =======================

# Menu Submit Challenge Hash
def submitchallengec(): #colocar mensagem de sucesso ou insucesso e no tipo de desafios de mensagem, colocar a mensagem decifrada
    #responderDesafio(id_desafio_cifras)
    print ("9. Back")
    print ("0. Quit") 
    choice = input(" >>  ")
    exec_menusubmitc(choice)
    return

# =======================

# Menu Scoreboard
def scoreboard(): #scoreboard dos users
    print ("SCOREBOARD\n")
    print ("9. Back")
    print ("0. Quit") 
    choice = input(" >>  ")
    exec_menuscore(choice)
    return

# =======================

# Menu Definições
def settings(): #definicoes do sistema
    print ("SETTINGS\n")
    print ("9. Back")
    print ("0. Quit") 
    choice = input(" >>  ")
    exec_menusettings(choice)
    return

# =======================

# Back to main menu
def back():
    menu_actions['main_menu']()

# Back to homepage 
def backhome():
    submenuhome_actions['menuhome']()

# Exit program
def exit():
    sys.exit()

# =======================
#    MENUS DEFINITIONS
# =======================

# Main Menu definition
menu_actions = {
    'main_menu': main_menu,
    '1': menulogin,
    '2': menuregister,
    '3': menuhelp,
    '9': back,
    '0': exit,
}

# Login Menu definition
submenulogin_actions = {
    'menulogin': menulogin,
    '9': back,
    '1': menuhome,
    '0': exit,
}

# Register Menu definition
submenuregister_actions = {
    'menuregister': menuregister,
    '0': back,
    '1': menulogin,
}

# Help Menu definition
submenuhelp_actions = {
    'menuhelp': menuhelp,
    '9': back,
    '0': exit,
}

# Homepage Menu definition
submenuhome_actions = {
    'menuhome': menuhome,
    '1': menuchallenges,
    '2': menunewchallenge,
    '3': scoreboard,
    '4': settings,
    '5': menuhelp,
    '0': exit,
}

# Challenges Menu definition
submenuc_actions = {
    'menuchallenges': menuchallenges,
    '1': menuchallengesc,
    '2': menuchallengesh,
    '9': backhome,
    '0': exit,
}

# New Challenge Menu definition
submenunewc_actions = {
    'menunewchallenge': menunewchallenge,
    '1': menunewctype1,
    '2': menunewctype2,
    '9': backhome,
    '0': exit,
}

# Message Decipher Challenge Menu definition
submenunewc1_actions = {
    'menunewctype1': menunewctype1,
    '1': menuchallenges,
    '9': backhome,
    '0': exit,
}

# Hash Challenge Menu definition
submenunewc2_actions = {
    'menunewctype2': menunewctype2,
    '1': menuchallenges,
    '9': backhome,
    '0': exit,
}

# Submit Hash Solution Menu definition
submenusubmith_actions = {
    '1': submitchallengeh,
    '9': menuchallenges,
    '0': exit,
}

# Submit Cypher Solution Menu definition
submenusubmitc_actions = {
    '1': submitchallengec,
    '9': menuchallenges,
    '0': exit,
}

# Scoreboard Menu definition
submenuscore_actions = {
    'scoreboard': scoreboard,
    '9': backhome,
    '0': exit,
}

# Settings Menu definition
submenusettings_actions = {
    'settings': settings,
    '9': backhome,
    '0': exit,
}

# =======================
#      MAIN PROGRAM
# =======================

# Main Program
if __name__ == "__main__":
    # Launch main menu
    main_menu()