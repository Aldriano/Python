import sys
import subprocess as sp

from utilTello import sendData,sendStop

def get_menu_choice():
    def print_menu():     
        print(30 * "-", "DRONE MENU", 30 * "-")
        print("1. Decolar ")
        print("2. Pousar")        
        print("3. Vire a direita ")
        print("4. Vire a esquerda ")
        print("5. Sair Menu ")
        print(73 * "-")

    loop = True

    while loop:         
        sp.call('cls', shell=True)
        print_menu()   
        choice = input("Enter your choice [1-5]: ")

        if choice == '1': # Decolar
            sendData("command")
            sendData("takeoff")
        elif choice == '2': # Pousar
            sendData("command")
            sendData("land")
        elif choice == '3': # Vire a direita 
            sendData("command")
            sendData("up 33")
        elif choice == '4': # Vire a esquerda
            sendData("command")
            sendData("down 33")        
        elif choice == '5':
             sendStop()
             loop = False
    return [choice]


get_menu_choice()