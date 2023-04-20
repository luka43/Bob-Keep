import hashlib
import json
import os
from getpass import getpass
from decimal import Decimal

x053 = '0x53d6316bd7b9044e6bb5deaa87fe8316c2fde3938b78f8448875b08e551ccc95'

def addNewClient(name):
    unpaid_list[name] = {
        "item":[],
        "price":[],
        "sum":0
    }
    return unpaid_list

def addNewItem(name, items, prices):
    n = 0
    for item in items:
        unpaid_list[name]["item"].append(item)
        n = n + 1
    n = 0
    for price in prices:
        unpaid_list[name]["price"].append(price)
        n = n + 1

def deleteClient(name):
    unpaid_list.pop(name)

def deleteItem(name):
    unpaid_list[name]["item"].clear()
    unpaid_list[name]["price"].clear()

def loadDatabase():
    if os.path.isfile("db.json") == True:

        with open("db.json","r") as file:
            unpaid_list = json.load(file)

    elif os.path.isfile("db.json") == False:
        with open("db.json","w") as file:
            unpaid_list = {}
            file.write(json.dumps(unpaid_list))

    return unpaid_list

def saveDatabase(list):
    with open("db.json","w") as file:
        file.write(json.dumps(list))

def autoSave(list):
    with open("autosave.json","w") as file:
        file.write(json.dumps(list))

def mainMenu():
    os.system("cls")
    print("-" * 100 + "\n\n" +
          "\t\tBOB KEEPER v1.0.1 - Developed by Luka43 \n\n" +
          "-" * 100
    )
    print("\n\t\tChoose Option: \n\n" +
        "\t\t\t(1) Add new client.\n" +
        "\t\t\t(2) Add new item.\n\n" +
        "\t\t\t(3) Delete client.\n" +
        "\t\t\t(4) Delete item.\n\n" +
        "\t\t\t(L) See list.\n\n" +
        "\t\t\t(?) About.\n" +
        "\t\t\t(x) Exit.\n\n" +
        "-" * 100
    )

    if unpaid_list == {}:
        print("Nema dužnika...")
    else:
        n = 0
        for name in unpaid_list:
            if n == 12:
                n = 0
                print("")
            print(name, end=", ")
            n = n + 1

    print("")
    print("-" * 100)

def printList(list):
    for name in list:
        sum = Decimal(0)
        print(f"Name: \t{name}")
        print("Items: \t", end="")

        for item in list[name]['item']:
            print(item, end=", ")

        print("\nPrice: \t", end="")

        for price in list[name]['price']:
            print(price, end="€, ")
            sum = sum + Decimal(price)

        unpaid_list[name]["sum"] = str(sum)

        print(
            "\n"+
            "Sum:\t\x1b[92m" + str(sum)[:4] + "€\x1b[0m"
            "\n"
            )

def printAbout():
    os.system("cls")

    print("-" * 100 + "\n" +
        "\t\tBOB KEEPER v1.0.1 - Developed by Luka43 \n" +
        "-" * 100 +
        "\n"
    )
    print(
        "\t\t This program was made for my dear friend who \n" +
        "\t\t doesn't have time to be both a waiter and \n" +
        "\t\t an accountant at the same time. A bunch of drunk \n" +
        "\t\t people, everyone drinks on credit, and only one \n" +
        "\t\t person is employed, the waiter, who is not an accountant. \n" +
        "\t\t I hope this program will save you time in writing \n" +
        "\t\t down the names of the drunks. And that you'll forget \n" +
        "\t\t to write down a few beers for me :)\n\n" +
        "\t\t I wish you good luck and careless drinking...\n\n" +
        "\t\t There is autosave coded in the program so it saves \n" +
        "\t\t every change made with database in case program crashes \n" +
        "\t\t in a file named 'autosave.json'. If program quit via menu\n" +
        "\t\t it will automatically delete 'autosave.db' and save it \n" +
        "\t\t in a 'database.json' \n\n" +
        "\t\t 'Delete item' option deletes only the last item for \n" +
        "\t\t given client name.\n\n" +
        "-" * 100
    )

    getpass("Press ENTER to continue... ")



######### Main thread #############
while True:
    os.system("cls")
    inp = getpass("\x1b[93m L O G I N : \x1b[0m")

    # encode input, add '1y' to begining and compare it to stored password remove '0x' and add '1y'
    if "1y" + hashlib.sha256(inp.encode('utf-8')).hexdigest() == "1y" + x053[2:]:
        break

    else:
        print("Wrong password!! Try again..")

n = 0
unpaid_list = loadDatabase()
client_name = str
item_name = str
price = Decimal

while True:
    mainMenu()
    menu_choice = input(" >: \x1b[93m")
    print("\x1b[0m")

    for client_name in unpaid_list:
        if client_name == menu_choice:
            client_name == menu_choice.split
            item_name = input("Item: \x1b[93m").split(" ")
            print("\x1b[0m", end="")
            price = input("Price: \x1b[92m").split(" ")
            print("\x1b[0m", end="")
            addNewItem(client_name, item_name, price)
            autoSave(unpaid_list)
        else:
            pass

    if menu_choice == "1":
        client_name = input(" New client name: \x1b[93m").split(" ")
        print("\x1b[0m")
        try:
            not unpaid_list[client_name[0]]
        except:
            unpaid_client = addNewClient(client_name[0])
        else:
            print("USER ALREADY EXISTS!!")
            os.system("pause")

    elif menu_choice == "2":
        client_name = input("Client name: \x1b[93m").split(" ")
        print("\x1b[0m", end="")
        item_name = input("Item: \x1b[93m").split(" ")
        print("\x1b[0m", end="")
        price = input("Price: \x1b[92m").split(" ")
        print("\x1b[0m", end="")
        addNewItem(client_name[0], item_name, price)
        autoSave(unpaid_list)

    elif menu_choice == "3":
        client_name = input("Delete client named: ")
        areyousure = input("Are you sure u want to delete {client_name} and all debts? ")

        if areyousure.lower() == "y":
            deleteClient(client_name)
        else:
            pass

    elif menu_choice == "4":
        client_name = input("Client name: ")
        deleteItem(client_name)

    elif menu_choice.lower() == "l" or menu_choice.lower() == "list":
        os.system("cls")
        printList(unpaid_list)
        getpass("Press ENTER to continue... ")

    elif menu_choice == "?" or menu_choice.lower() == "help" or menu_choice.lower() == "h":
        printAbout()

    elif menu_choice.lower() == "x" or menu_choice.lower() == "q" or menu_choice.lower() == "exit" or menu_choice.lower() == "quit":
        os.system("cls")
        print("\x1b[91m W A R N I N G ! ! !\x1b[0m")
        exit_choice = input(" Are you sure you want to exit and save the database? \x1b[92m")
        print("\x1b[0m")

        if exit_choice.lower() == "y" or exit_choice.lower() == "ye" or exit_choice.lower() == "yes":
            saveDatabase(unpaid_list)
            try:
                os.remove("autosave.json")
                exit()
            except:
                pass
            break
        else:
            continue
    else:
        pass