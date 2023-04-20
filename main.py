import hashlib
import json
import os
import sys
import tkinter
import time
from datetime import datetime
from decimal import Decimal
from tkinter import ttk, filedialog, messagebox
from tkinter.scrolledtext import ScrolledText

class log():
    # Does log file exists? If not, create one
    if os.path.isfile("log") == False:
            with open("log","w") as file:
                file.write("[" + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "] " + "-" * 100)
    else:
        pass
    # Write "input_string" to log file
    def write(*input_string):
        string = ""
        for word in input_string:
            string = string + word
        output_string = "[" + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "] " + string + "\n"
        with open("log","r+") as file:
            old = file.read()
            file.seek(0, 0)
            file.write(output_string + old)
    def read():
        with open("log","r") as file:
            return file.read()
class database():
    # isfile = True/False
    # filepath = path to file
    def __init__(self, filepath) -> None:
        self.isfile = os.path.isfile(filepath)
        self.filepath = filepath

    def open(self, init):
        if self.isfile == True:
            with open(self.filepath, "r") as file:
                return json.load(file)
        elif self.isfile == False and init==1:
            data = {}
            with open(self.filepath, "w") as file:
                file.write(json.dumps(data))
                return data
        elif self.isfile == False and not init:
            return False
    # Open, Sort and Return values from database (complete data, name liist, price list)
    def load(self, init):
        if self.isfile == True:
            with open(self.filepath, "r") as file:
                data = json.load(file)
            self.name_list = []
            self.item_list = []
            price_list = []

            for name in data:
                self.name_list.append(name)
                self.name_list.sort()

            self.item_list.sort()
            return data, self.name_list, self.item_list

        elif self.isfile == False and init == 1:
            data = {}
            with open(self.filepath, "w") as file:
                file.write(json.dumps(data))
            return {}, [], []
    # Save data to filepath.json
    def save(self, data):
        with open(self.filepath, "w") as file:
            file.write(json.dumps(data))

    def exists(self):
        return self.isfile
class LoginWindow(tkinter.Tk):

    def __init__(self):
        super().__init__()
        self.withdraw()
        global x

        # Set Window
        #self.iconphoto(False, tkinter.PhotoImage(file="icon.ico"))   ---- strugling with icons and pyinstaller (figured it out but saved this for future exam)
        self.iconphoto(False, tkinter.PhotoImage(file=resource_path("icon.ico")))
        self.geometry("400x120")
        self.eval("tk::PlaceWindow . center")
        self.title("BOB Keep - Login")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.exit)
        #self.attributes("-toolwindow", True)

        # LABEL - Password
        self.passwordLabel = tkinter.Label(self, font=("Arial", 12), text="Password:")
        self.passwordLabel.pack(pady=5)

        # INPUT - Password
        self.passwordEntry = tkinter.Entry(self, show="●", font=("Arial", 12), justify="center",borderwidth=3, relief=tkinter.FLAT)
        self.passwordEntry.bind("<Return>", self.tryLogin)
        self.passwordEntry.pack(pady=5)

        # BUTTON - Login
        self.loginButton = ttk.Button(self, text="Login", command=self.tryLogin, padding=2)
        self.loginButton.pack(pady=5)

        # Focus on Password - INPUT
        self.deiconify()
        self.passwordEntry.focus_set()

        log.write("Login window initiated.")

    def tryLogin(self, *args):
        global x

        # (random 10 char string) + sha256(SuperUserPassword1234!)
        x01 = "NAUsmfUrbW0bbcf80bf633d612763b178703ad4b129d37f8ea2f11017d57c6ed14870992ee"
        # (random 10 char string) + sha256(admin0000)
        x02 = "PYvxTKpLrO53d6316bd7b9044e6bb5deaa87fe8316c2fde3938b78f8448875b08e551ccc95"
        log.write(f"Login attempt.[{args}]")
        password = self.passwordEntry.get()

        if hashlib.sha256(password.encode('utf-8')).hexdigest() == x01[10:]:
            log.write("Password correct! ")
            x = 1
            self.destroy()

        elif hashlib.sha256(password.encode('utf-8')).hexdigest() == x02[10:]:
            log.write("Password correct! ")
            x = 2
            self.destroy()

        else:
            log.write("Wrong password!!!")
            pass
    def exit(self):
        global logout_value
        logout_value = 0
        self.destroy()
        sys.exit(0)
class MainWindow(tkinter.Tk):

    def __init__(self):
        super().__init__()
        log.write("Loading main window...")
        self.withdraw()
        self.unpaid_list = {}
        self.name_list = []
        self.item_list = []
        self.db_filepath = "database.json"

        # ------------------------------------------------- Set Main Window ------------------------------------------------- #
        self.iconphoto(False, tkinter.PhotoImage(file=resource_path("icon.ico")))
        self.geometry("650x705+10+10")
        self.title("Bar Owers Book Keep")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", lambda: self.exit())


        # --------------------------------------------------- MENU BAR ------------------------------------------------------ #
        self.menubar = tkinter.Menu(self)

        # File Menu Bar Options
        self.filemenu = tkinter.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=self.filemenu)

        self.filemenu.add_command(label="New database", command=lambda: self.createNewDatabase())
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Load", command=lambda: self.loadDatabase())
        self.filemenu.add_command(label="Save", command=lambda: self.save(0))
        self.filemenu.add_command(label="Save As", command=lambda: self.save(1))
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Log out", command=lambda: self.logout())
        self.filemenu.add_command(label="Exit", command=lambda: self.exit())

        # Edit Menu Bar Options
        self.editmenu = tkinter.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Edit", menu=self.editmenu)
        self.editmenu.add_command(label="Add Items", state="disabled")
        self.editmenu.add_command(label="Delete Items", state="disabled")
        self.editmenu.add_separator()
        self.editmenu.add_command(label="Manage Users", state="disabled")

        # Help Menu Bar Optionts
        self.helpmenu = tkinter.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Help", menu=self.helpmenu)
        self.helpmenu.add_command(label="About", command=lambda: self.showAbout())
        self.config(menu=self.menubar)
        # SEPARATOR
        self.menuBarSeparator = ttk.Separator(self, orient='horizontal')
        self.menuBarSeparator.pack(fill="x")

        #Set top frame
        self.top_frame = tkinter.Frame(self)
        self.top_frame.columnconfigure(0, weight=1)
        self.top_frame.columnconfigure(1, weight=2)
        self.top_frame.columnconfigure(2, weight=20)

        # LABEL - Name
        nameLabel = tkinter.Label(self.top_frame, text="Name: ")
        nameLabel.grid(row=0, column=0,  pady=3, sticky="w")
        # INPUT - Name
        self.nameInput = tkinter.Entry(self.top_frame, width=46, font=('Arial', 11))
        self.nameInput.grid(row=0, column=1, sticky="w", pady=0)
        self.nameInput.bind("<Return>", self.addNewDebt)
        self.nameInput.bind("<FocusIn>", self.focusOnNameInput)

        # DROPDOWN - Names
        self.addClientList = [""]
        self.addNameCliked = tkinter.StringVar()
        self.addClientListDropDown = tkinter.OptionMenu(self.top_frame, self.addNameCliked, *self.addClientList)
        self.addClientListDropDown.config(width=25)
        self.addClientListDropDown.grid(row=0, column=3, sticky="W")

        # LABEL - Item
        itemLabel = tkinter.Label(self.top_frame, text="Item:  ")
        itemLabel.grid(row=1, column=0,  pady=3, sticky="w")
        # INPUT - Item
        self.itemInput = tkinter.Entry(self.top_frame, width=30, font=('Arial', 11))
        self.itemInput.grid(row=1, column=1, sticky="w", pady=0, padx=(0, 2))
        self.itemInput.bind("<Return>", self.addNewDebt)
        self.itemInput.bind("<FocusIn>", self.focusOnItemInput)

        # LABEL - Kol
        kolLabel = tkinter.Label(self.top_frame, text="Kol: ")
        kolLabel.grid(row=1, column=1,  pady=3, padx=(225, 0))
        # INPUT - kol
        self.kolInput = tkinter.Entry(self.top_frame, width=4, font=('Arial', 11))
        self.kolInput.grid(row=1, column=1, sticky="e")
        self.kolInput.bind("<Return>", self.addNewDebt)
        self.kolInput.bind("<FocusIn>", self.focusOnKolInput)

        # DROPDOWN - Item
        self.itemsClicked = tkinter.StringVar()
        self.itemsClicked.set("Items")
        self.itemsDropDown = tkinter.OptionMenu(self.top_frame, self.itemsClicked, *self.addClientList)
        self.itemsDropDown.config(width=25)
        self.itemsDropDown.grid(row=1, column=3, sticky="W")

        # LABEL - Price
        kolLabel = tkinter.Label(self.top_frame, text="Price: ")
        kolLabel.grid(row=2, column=0,  pady=3, sticky="w")
        # INPUT - Price
        self.priceInput = tkinter.Entry(self.top_frame, width=46, font=('Arial', 11))
        self.priceInput.grid(row=2, column=1, sticky="w")
        self.priceInput.bind("<Return>", self.addNewDebt)
        self.priceInput.bind("<FocusIn>", self.focusOnPriceInput)

        # BUTTON - Reset
        addButton = ttk.Button(self.top_frame, text="Reset", width=12, command=self.resetInputFields)
        addButton.grid(row=2, column=3, sticky="w")
        # BUTTON - Add
        resetButton = ttk.Button(self.top_frame, text="Add", width=17, command=self.addNewDebt)
        resetButton.grid(row=2, column=3, sticky="e")

        self.top_frame.pack(fill='x', pady=(10, 5), padx=10)

        # SEPARATOR
        separator_top = ttk.Separator(self, orient='horizontal')
        separator_top.pack(fill="x", pady=2, padx=10)

        # TEXTBOX - List
        self.listTextBox = ScrolledText(self, font=('Arial', 10))
        self.listTextBox.pack(fill=tkinter.BOTH, pady=5, padx=10)

        logFrame = tkinter.Frame(self)
        logLabel = tkinter.Label(logFrame, text="Log: ")
        logLabel.pack(side="left", fill="x")

        logFrame.pack(fill='x', padx=10)

        # TEXTBOX - Log
        self.logTextBox = ScrolledText(self, font=('Arial', 10), height=0.5, state="disabled")
        self.logTextBox.pack(fill="x", pady=5, padx=10)

        # SEPARATOR
        separator_bot = ttk.Separator(self, orient='horizontal')
        separator_bot.pack(fill="x", pady=2, padx=5)

        #Set bottom frame
        bot_frame = tkinter.Frame(self)
        bot_frame.columnconfigure(0, weight=1)
        bot_frame.columnconfigure(1, weight=2)
        bot_frame.columnconfigure(2, weight=3)

        # DROPDOWN - Names
        self.delClientList = ["Names"]
        self.delClientListClicked = tkinter.StringVar(self)
        self.delClientListClicked.set("Names")
        self.delClientListDropDown = tkinter.OptionMenu(bot_frame, self.delClientListClicked, *self.delClientList)
        self.delClientListDropDown.config(width=30)
        self.delClientListDropDown.grid(row=0, column=0)

        # DROPDOWN - Items
        self.delItems = ["Items"]
        self.delItemsClicked = tkinter.StringVar(self)
        self.delItemsClicked.set("Items")
        self.delItemsDropDown = tkinter.OptionMenu(bot_frame, self.delItemsClicked, *self.delItems)
        self.delItemsDropDown.config(width=30)
        self.delItemsDropDown.grid(row=0, column=1)

        # BUTTON - Delete
        deleteButton = ttk.Button(bot_frame, text="Delete", width=26, padding=4, command=self.deleteSelectedItem)
        deleteButton.grid(row=0, column=2)

        bot_frame.pack(fill='x', pady=(10, 5), padx=10)

        # SEPARATOR
        separator_bot2 = ttk.Separator(self, orient='horizontal')
        separator_bot2.pack(fill="x", pady=(5,0))

        bottomLabel = tkinter.Label(self, text=f"User: {user}")
        bottomLabel.pack(padx=5, side="left")

        if x == 1:
            self.editmenu.entryconfigure(3, state="normal")
    # ------------------------------------------- End of Main Window Setup -------------------------------------------- #

        self.delClientListClicked.trace('w', self.updateDeleteItemDropDown)
        self.addNameCliked.trace("w", self.updateNameInputField)
        self.itemsClicked.trace("w", self.updateItemInputField)

        log.write("Done")
        # Check if database.json exist and load it
        log.write(f"Checking if {self.db_filepath} exist...")
        if database(self.db_filepath).exists() == True:
            log.write("It does.. Loading data from database.json...")
            self.unpaid_list, self.name_list, self.item_list = database("database.json").load(1)
        log.write("Loading and sorting data...")
        self.updateGlobalItemsList()
        log.write(f"Names: {self.name_list}")
        self.resetInputFields()
        self.updateMainTextBox()
        self.updateAddItemDropDown()
        self.updateDeleteNamesDropDown(1)
        self.focusOnItemInput()
        log.write("Done")
        self.updateLogTextBox()
        self.deiconify()

    # ------------------------------------------------ Menu Bar methods ------------------------------------------------ #

    def createNewDatabase(self):
        filename = filedialog.asksaveasfilename(initialdir=".", defaultextension=".json", filetypes=(("JSON Database", "*.json"),("All Files", "*.*") ))
        if filename == "":
            pass
        else:
            self.unpaid_list, self.name_list, self.item_list= database(filename).load(1)
            log.write(f"Created new database on path: {filename}")
            self.updateGlobalNameList()
            self.updateGlobalItemsList()
            self.resetInputFields()
            self.updateMainTextBox()
            self.updateAddItemDropDown()
            self.updateDeleteNamesDropDown(1)
            self.focusOnItemInput()
            self.updateLogTextBox()

    def loadDatabase(self):
        try:
            filename = filedialog.askopenfilename(initialdir=".", defaultextension=".json", filetypes=(("JSON Database", "*.json"),("All Files", "*.*") ))
            self.unpaid_list, self.name_list, self.item_list = database(filename).load(0)
            log.write(f"Database loaded on path : {filename}")
            self.updateMainTextBox()
            self.updateAddItemDropDown()
            self.updateDeleteNamesDropDown()
        except Exception:
            log.write(f"Error wihle trying to load database : {filename}")
        self.updateLogTextBox()

    def save(self, saveAs):
        if saveAs == 0:
            database(self.db_filepath).save(self.unpaid_list)
            log.write(f"Save : {self.db_filepath}")
        elif saveAs == 1:
            filename = filedialog.asksaveasfilename(initialdir=".", defaultextension=".json", filetypes=(("JSON Database", "*.json"),("All Files", "*.*") ))
            if filename == "":
                pass
            else:
                database(filename).save(self.unpaid_list)
                log.write(f"Save database at : {filename}")
        self.updateLogTextBox()

    def exit(self):
        global logout_value
        if self.unpaid_list == database(self.db_filepath).open(0):
            log.write("Database unchanged at exit.")
            self.destroy()
            sys.exit(0)
        else:
            yesnocancel = messagebox.askyesnocancel("Save before exit", "Do you want to save changes to the database before exiting", default='yes')
            log.write(f"Save on exit {yesnocancel}")
            if yesnocancel == True:
                self.save(0)
                log.write("EXIT")
                self.destroy()
                sys.exit(0)
            elif yesnocancel == False:
                log.write("EXIT")
                logout_value = 0
                self.destroy()
                sys.exit(0)
            elif yesnocancel == None:
                pass
        self.updateLogTextBox()

    def showAbout(self):
        messagebox.showinfo(
            "About",
            "This program was made for my dear friend who \n" +
            "doesn't have time to be both a waiter and \n" +
            "an accountant at the same time. A bunch of drunk \n" +
            "people, everyone drinks on credit, and only one \n" +
            "person is employed, the waiter, who is not an accountant. \n" +
            "I hope this program will save you time in writing \n" +
            "down the names of the drunks. And that you'll forget \n" +
            "to write down a few beers for me :)\n\n" +
            "I wish you good luck and careless drinking...\n\n" +
            "Log out function just added, it doesn't save changes\n" +
            "to the file. Be careful!\n" +
            "Will add autosave, items database with item prices\n" +
            "and items manager to add/remove/change items\n\n" +
            "Version: 2.0.3\n" +
            "Date of release: 20/4/2023"
            )

    def logout(self):
        self.destroy()
    # ------------------------------------------------ Function methods ------------------------------------------------ #

    def addNewDebt(self, *args):
        new_name_created = False
        name = self.nameInput.get()
        item = self.itemInput.get()
        kol = int(self.kolInput.get())
        price = self.priceInput.get()
        n = 0
        if name not in self.unpaid_list:
            self.unpaid_list[name] = {
                    "item":[],
                    "price":[],
                    "sum": "0"
                }
            new_name_created = True
            log.write(f"Add new Client named: {name}")

        while n < kol:

            self.unpaid_list[name]["item"].append(item)
            self.unpaid_list[name]["price"].append(price)
            sum = Decimal(self.unpaid_list[name]["sum"]) + Decimal(price)
            self.unpaid_list[name]["sum"] = str(sum)
            n = n + 1

        log.write(f"Added new item to {name}: ", (f"{item}, " * n))

        self.updateGlobalItemsList()
        self.updateGlobalNameList()
        self.updateMainTextBox()
        if new_name_created == True:
            self.updateAddItemDropDown()
        self.updateDeleteNamesDropDown(0)
        self.updateDeleteItemDropDown(0)
        self.updateLogTextBox()

    def deleteSelectedItem(self):
        dropdown_position_reset = False
        name = self.delClientListClicked.get()
        item = self.delItemsClicked.get()
        if item:
            priceindex = self.unpaid_list[name]["item"].index(item)
            price = self.unpaid_list[name]["price"][priceindex]
            sum = Decimal(self.unpaid_list[name]["sum"]) - Decimal(price)
            self.unpaid_list[name]["item"].remove(item)
            self.unpaid_list[name]["price"].remove(price)
            self.unpaid_list[name]["sum"] = str(sum)
            log.write(f"Deleted {item} with price {price} from {name}")
        else:
            self.unpaid_list.pop(name)
            dropdown_position_reset = True
            log.write(f"List of items empty. Delete client: {name}")

        self.updateGlobalNameList()
        self.updateGlobalItemsList()
        self.updateMainTextBox()
        self.updateAddItemDropDown()
        if dropdown_position_reset == True:
            self.updateDeleteNamesDropDown(1)
        self.updateDeleteNamesDropDown(0)
        self.updateDeleteItemDropDown()
        self.updateLogTextBox()
    # ------------------------------------------------- Update methods ------------------------------------------------- #

    def updateGlobalItemsList(self):
        self.item_list.clear()
        for name in self.unpaid_list:
            for item in self.unpaid_list[name]["item"]:
                if item not in self.item_list:
                    self.item_list.append(item)
        self.item_list.sort()

    def updateGlobalNameList(self):
        self.name_list.clear()
        for name in self.unpaid_list:
            if name not in self.name_list:
                self.name_list.append(name)
        self.name_list.sort()

    def updateNameInputField(self, *args):
        name = self.addNameCliked.get()
        self.nameInput.delete(0, 'end')
        self.nameInput.insert("end", name)

    def updateItemInputField(self, *args):
        item = self.itemsClicked.get()
        self.itemInput.delete(0, 'end')
        self.itemInput.insert("end", item)

    def updateMainTextBox(self):
        self.listTextBox.config(state="normal")
        self.listTextBox.delete(1.0, tkinter.END)

        for name in self.name_list:
            sum = Decimal(0)
            self.listTextBox.insert(tkinter.END, f"{name}\n")
            #self.listTextBox.insert(tkinter.END, "Items: \t")

            for item in self.unpaid_list[name]['item']:
                self.listTextBox.insert(tkinter.END, f"{item}\t")
            self.listTextBox.insert('end', "\n")
            #self.listTextBox.insert(tkinter.END, "\nPrice: \t")

            for price in self.unpaid_list[name]['price']:

                self.listTextBox.insert(tkinter.END, f"{price}€\t")
                sum = sum + Decimal(price)

            self.unpaid_list[name]["sum"] = str(sum)
            self.listTextBox.insert("end", f"\n{sum}")
            self.listTextBox.insert('end', "\n")
            #self.listTextBox.insert(tkinter.END, f"\nSum: \t{str(sum)[:4]} €\n")
            self.listTextBox.insert(tkinter.END, "-"*120+"\n")

        self.listTextBox.config(state="disabled")

    def updateAddItemDropDown(self):

        self.addClientList.clear()
        self.addClientListDropDown['menu'].delete(0, 'end')
        try:
            for name in self.name_list:
                self.addClientList.append(name)
                self.addClientListDropDown['menu'].add_command(label=name+"                 ", command=lambda value=name: self.addNameCliked.set(value))

            self.itemsDropDown['menu'].delete(0, 'end')
            for item in self.item_list:
                self.itemsDropDown['menu'].add_command(label=item+"                 ", command=lambda value=item: self.itemsClicked.set(value))
            self.addNameCliked.set(self.addClientList[0])
        except:
            log.write("Error can't read items list or empty")

    def updateDeleteNamesDropDown(self, position_reset):
        self.addClientList.clear()
        self.delClientList.clear()
        self.delClientListDropDown['menu'].delete(0, 'end')
        for name in self.name_list:
            self.addClientList.append(name)
            self.delClientListDropDown['menu'].add_command(label=name+"                 ", command=lambda value=name: self.delClientListClicked.set(value))
        if position_reset == 1:
            try:
                self.delClientListClicked.set(self.addClientList[0])
            except:
                self.delClientListClicked.set("")

    def updateDeleteItemDropDown(self, *args):

        name_selected = self.delClientListClicked.get()
        self.delItems.clear()
        self.delItemsDropDown['menu'].delete(0, "end")
        for name in self.unpaid_list:
            if name == name_selected:
                for item in self.unpaid_list[name]['item']:

                    self.delItems.append(item)
                    self.delItemsDropDown['menu'].add_command(label=item+"                 ", command=lambda value=item: self.delItemsClicked.set(value))
        try:
            self.delItemsClicked.set(self.delItems[0])
        except:
            self.delItemsClicked.set("")

    def resetInputFields(self):
        self.nameInput.delete(0, 'end')
        self.itemInput.delete(0, 'end')
        self.kolInput.delete(0, 'end')
        self.kolInput.insert("end", "1")
        self.priceInput.delete(0, "end")
        self.priceInput.insert("end", "0.00")

    def updateLogTextBox(self):
        self.logTextBox.config(state="normal")
        self.logTextBox.delete(0.0, "end")
        self.logTextBox.insert("end", log.read())
        self.logTextBox.config(state="disabled")
    # ------------------------------------------------- Focus methods ------------------------------------------------- #

    def focusOnNameInput(self, *args):
        self.nameInput.selection_range(0, "end")

    def focusOnItemInput(self, *args):
        self.itemInput.selection_range(0, "end")

    def focusOnKolInput(self, *args):
        self.kolInput.selection_range(0, "end")

    def focusOnPriceInput(self, *args):
        self.priceInput.selection_range(0, "end")

    # --------------------------------------------------- Main Loop ---------------------------------------------------- #
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
logout_value = 1
#x = 1
log.write("-"*100)
log.write("Program executed.")
while logout_value == 1:
    log.write("Initiate login window...")
    LoginWindow().mainloop()
    log.write(f"Login window closed")
    if x == 1:
        user = "Super User"
        log.write(f"Login successful. Logged as: {user}")
        MainWindow().mainloop()
    elif x == 2:
        user = "Admin"
        log.write(f"Login successful. Logged as: {user}")
        MainWindow().mainloop()
    else:
        log.write("Login unsuccessful. Exiting program...")
    time.sleep(0.3)