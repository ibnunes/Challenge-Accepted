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
import time


#
from login import login, register
from hashed import adicionarDesafioH, listarDesafiosH, responderDesafioHash
from cypher import adicionarDesafioC, listarDesafiosC, responderDesafioC
from banner import BANNER
from TUI import Menu, Item

# Main definition - constants
menu_actions  = {}  

# =======================
#     MENUS FUNCTIONS
# =======================


# =======================

# # Execute main menu
# def exec_menu(choice):
#     os.system('clear')
#     ch = choice.lower()
#     if ch == '':
#         menu_actions['main_menu']()
#     else:
#         try:
#             menu_actions[ch]()
#         except KeyError:
#             print ("Invalid selection, please try again.\n")
#             menu_actions['main_menu']()
#     return

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

# =======================

# Main menu
def mainMenu() -> None:
    Title = BANNER + "Welcome! \n"
    Menu(
        Title,
        "Please choose an option to start with:",
        [Item("Login", menuLogin),
         Item("Create Account", menuRegister),
         Item("Help", menuHelp),
         Item("Back", back),
         Item("Quit", exit)]
    )

# =======================

# Login Menu
def menuLogin():
    if (login.loginUser()): 
        exec_menulogin("1")
    else:
        exec_menulogin("")

# =======================

# Register Menu
def menuRegister():
    if (register.registerUser()): 
        exec_menureg("1")
    else:
        exec_menureg("0")

# =======================

# Help Menu
def menuHelp():
    Menu(
        "About",
        "Informações",
        [Item("Back", None),
         Item("Quit", exit)]
    )

# =======================

# Homepage
def menuHome():
    Menu(
        "Welcome User:",
        "HOMEPAGE",
        [Item("List challenges available", ),
         Item("Submit new challenge", ),
         Item("Scoreboard", ),
         Item("Settings", ),
         Item("Help", menuHelp),
         Item("Logout", )]
    )

# =======================

# Menu List of Challenges
def menuChallenges():
    Menu(
        "CHALLENGES AVAILABLE",
        "",
        [Item("AES CYPHER CHALLENGES", ),
         Item("HASH CHALLENGES", ),
         Item("Back", None),
         Item("Quit", exit)]
    )


# =======================

def menuChallengesC():
    """Menu List of Challenges Cypher"""
    print ("CHALLENGES AVAILABLE\n") # colocar lista de challenges available por numero
    listarDesafiosC.listarDesafios()
    print ("Insert number of challenge you want to answer:\n")
    global idc
    idc = input(" >>  ")
    print ("1. Submit solution")
    print ("9. Back")
    print ("0. Quit") 
    choice = input(" >>  ")
    exec_menusubmitc(choice)

# =======================

# Menu List of Challenges Hash
def menuChallengesH():
    print ("CHALLENGES AVAILABLE\n") # colocar lista de challenges available por numero
    listarDesafiosH.listarDesafios()
    print ("Insert number of challenge you want to answer:\n")
    global idc
    idc = input(" >>  ")
    print ("1. Submit solution")
    print ("9. Back")
    print ("0. Quit") 
    choice = input(" >>  ")
    exec_menusubmith(choice)

# =======================

# Menu New Challenge
def menuNewChallenge():
    Menu(
        "NEW CHALLENGE",
        "",
        [Item("Decipher Challenge Type", ), 
         Item("Hash Challenge Type", ), 
         Item("Back", None),
         Item("Quit", exit)]
    )

# =======================

# Menu New Decipher Challenge
def menuNewCType1():
    choice = str(adicionarDesafioC.adicionarDesafioCypher())
    if (choice == "1"):
        print("Your challenge was submitted - Let the challenges begin!")
    exec_menunc1(choice)

# =======================

# Menu New Challenge Hash
def menuNewCType2():
    choice = str(adicionarDesafioH.adicionarDesafioHash())
    if (choice == "1"):
        print("Your challenge was submitted - Let the challenges begin!")
    exec_menunc2(choice)

# =======================

# Menu Submit Challenge Hash
def submitChallengeH(): #colocar mensagem de sucesso ou insucesso e no tipo de desafios de mensagem, colocar a mensagem decifrada
    responderDesafioHash.responderDesafioHash(idc)
    Menu(
        "",
        "",
        [Item("Back", None),
         Item("Quit", exit)]
    )

# =======================

# Menu Submit Challenge Hash
def submitChallengeC(): #colocar mensagem de sucesso ou insucesso e no tipo de desafios de mensagem, colocar a mensagem decifrada
    responderDesafioC.responderDesafioCrypto(idc)
    Menu(
        "",
        "",
        [Item("Back", None),
         Item("Quit", exit)]
    )

# =======================

# Menu Scoreboard
def scoreboard(): #scoreboard dos users
    Menu(
        "SCOREBOARD",
        "",
        [Item("Back", None),
         Item("Quit", exit)]
    )

# =======================

# Menu Definições
def settings(): #definicoes do sistema
    Menu(
        "SETTINGS",
        "",
        [Item("Back", None),
         Item("Quit", exit)]
    )

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
# menu_actions = {
#     'main_menu': main_menu,
#     '1': menulogin,
#     '2': menuregister,
#     '3': menuhelp,
#     '9': back,
#     '0': exit,
# }

# Login Menu definition
submenulogin_actions = {
    'menulogin': menuLogin,
    '9': back,
    '1': menuHome,
    '0': exit,
}

# Register Menu definition
submenuregister_actions = {
    'menuregister': menuRegister,
    '0': back,
    '1': menuLogin,
}

# Help Menu definition
submenuhelp_actions = {
    'menuhelp': menuHelp,
    '9': back,
    '0': exit,
}

# Homepage Menu definition
submenuhome_actions = {
    'menuhome': menuHome,
    '1': menuChallenges,
    '2': menuNewChallenge,
    '3': scoreboard,
    '4': settings,
    '5': menuHelp,
    '0': exit,
}

# Challenges Menu definition
submenuc_actions = {
    'menuchallenges': menuChallenges,
    '1': menuChallengesC,
    '2': menuChallengesH,
    '9': backhome,
    '0': exit,
}

# New Challenge Menu definition
submenunewc_actions = {
    'menunewchallenge': menuNewChallenge,
    '1': menuNewCType1,
    '2': menuNewCType2,
    '9': backhome,
    '0': exit,
}

# Message Decipher Challenge Menu definition
submenunewc1_actions = {
    'menunewctype1': menuNewCType1,
    '1': menuChallenges,
    '9': backhome,
    '0': exit,
}

# Hash Challenge Menu definition
submenunewc2_actions = {
    'menunewctype2': menuNewCType2,
    '1': menuChallenges,
    '9': backhome,
    '0': exit,
}

# Submit Hash Solution Menu definition
submenusubmith_actions = {
    '1': submitChallengeH,
    '9': menuChallenges,
    '0': exit,
}

# Submit Cypher Solution Menu definition
submenusubmitc_actions = {
    '1': submitChallengeC,
    '9': menuChallenges,
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
    mainMenu()
