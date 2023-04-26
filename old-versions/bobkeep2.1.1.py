import hashlib, json, os, sys
import tkinter
from datetime import datetime
from decimal import Decimal
from tkinter import ttk, filedialog, messagebox
from tkinter.scrolledtext import ScrolledText

def resource_path(relative_path):
    # Copy pasted a code to get correct path for icon.ico
    # when compiling with pyinstaller
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
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
    # Read log file and return data
    def read():
        with open("log","r") as file:
            return file.read()
class database():

    # isfile = True/False
    # filepath = path to file
    def __init__(self, filepath) -> None:
        self.isfile = os.path.isfile(filepath)
        self.filepath = filepath

    # Open database if exist if not create new one if init == 1
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

    # Save data to filepath.json
    def save(self, data):
        with open(self.filepath, "w") as file:
            file.write(json.dumps(data))

    def exists(self):
        return self.isfile
class MainWindow(tkinter.Tk):

    def __init__(self):
        super().__init__()
        log.write("Loading main window...")

        self.withdraw()
        self.loggedInAs = 0
        self.logoutValue = 0
        self.changedData = 0
        # Setup memory for database
        self.unpaid_list = {}
        self.name_list = []
        self.item_list = []
        self.db_filepath = resource_path("database.json")

        # ------------------------------------------------- Set Main Window ------------------------------------------------- #
        self.iconphoto(False, tkinter.PhotoImage(file=resource_path("icon.ico")))
        self.geometry("650x750+50+50")
        self.title("Bar Owers Book Keep")
        #Will use this later when I optimize all functions
        #self.attributes("-fullscreen", True)
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", lambda: self.exit(1))

        # ------------------------------------------------- Menu Bar Setup -------------------------------------------------- #
        self.menubar = tkinter.Menu(self)

        # File Menu Bar Options
        self.filemenu = tkinter.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        self.filemenu.add_command(label="New database", command=lambda: self.createNewDatabase())
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Open", command=lambda: self.openDatabaseFile())
        self.filemenu.add_command(label="Save", command=lambda: self.save(0))
        self.filemenu.add_command(label="Save As", command=lambda: self.save(1))
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Log out", command=lambda: self.logout())
        self.filemenu.add_command(label="Exit", command=lambda: self.exit(1))

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

        # ------------------------------------------------- Top input frame setup ------------------------------------------- #
        self.top_frame = tkinter.Frame(self)
        self.top_frame.columnconfigure(0, weight=1)
        self.top_frame.columnconfigure(1, weight=2)
        self.top_frame.columnconfigure(2, weight=20)

        # LABEL - Name
        self.nameLabel = tkinter.Label(self.top_frame, text="Name: ")
        self.nameLabel.grid(row=0, column=0,  pady=3, sticky="w")
        # INPUT - Name
        self.nameInput = tkinter.Entry(self.top_frame, width=46, font=('Arial', 11))
        self.nameInput.grid(row=0, column=1, sticky="w", pady=0)
        self.nameInput.bind("<Return>", self.addNewDebt)
        self.nameInput.bind("<FocusIn>", self.focusOnNameInput)

        # DROPDOWN - Names
        self.addClientList = [""]
        self.addClientCliked = tkinter.StringVar()
        self.addClientListDropDown = tkinter.OptionMenu(self.top_frame, self.addClientCliked, *self.addClientList)
        self.addClientListDropDown.config(width=25)
        self.addClientListDropDown.grid(row=0, column=3, sticky="W")

        # LABEL - Item
        self.itemLabel = tkinter.Label(self.top_frame, text="Item:  ")
        self.itemLabel.grid(row=1, column=0,  pady=3, sticky="w")

        # INPUT - Item
        self.itemInput = tkinter.Entry(self.top_frame, width=30, font=('Arial', 11))
        self.itemInput.grid(row=1, column=1, sticky="w", pady=0, padx=(0, 2))
        self.itemInput.bind("<Return>", self.addNewDebt)
        self.itemInput.bind("<FocusIn>", self.focusOnItemInput)

        # LABEL - Kol
        self.amountLabel = tkinter.Label(self.top_frame, text="Kol: ")
        self.amountLabel.grid(row=1, column=1,  pady=3, padx=(225, 0))
        # INPUT - kol
        self.amountInput = tkinter.Entry(self.top_frame, width=4, font=('Arial', 11))
        self.amountInput.grid(row=1, column=1, sticky="e")
        self.amountInput.bind("<Return>", self.addNewDebt)
        self.amountInput.bind("<FocusIn>", self.focusOnKolInput)

        # DROPDOWN - Item
        self.itemsClicked = tkinter.StringVar()
        self.itemsClicked.set("Items")
        self.itemsDropDown = tkinter.OptionMenu(self.top_frame, self.itemsClicked, *self.addClientList)
        self.itemsDropDown.config(width=25)
        self.itemsDropDown.grid(row=1, column=3, sticky="W")

        # LABEL - Price
        self.priceLabel = tkinter.Label(self.top_frame, text="Price: ")
        self.priceLabel.grid(row=2, column=0,  pady=3, sticky="w")

        # INPUT - Price
        self.priceInput = tkinter.Entry(self.top_frame, width=46, font=('Arial', 11))
        self.priceInput.grid(row=2, column=1, sticky="w")
        self.priceInput.bind("<Return>", self.addNewDebt)
        self.priceInput.bind("<FocusIn>", self.focusOnPriceInput)

        # BUTTON - Reset
        self.addClientButton = ttk.Button(self.top_frame, text="Reset", width=12, command=self.resetInputFields)
        self.addClientButton.grid(row=2, column=3, sticky="w")
        # BUTTON - Add
        self.resetButton = ttk.Button(self.top_frame, text="Add", width=17, command=self.addNewDebt)
        self.resetButton.grid(row=2, column=3, sticky="e")

        self.top_frame.pack(fill='x', pady=(10, 5), padx=10)

        # SEPARATOR
        self.separator_top = ttk.Separator(self, orient='horizontal')
        self.separator_top.pack(fill="x", pady=2, padx=10)

        # -------------------------------------------- Frame for Treeview of unpaid items -------------------------------------- #
        self.treeViewFrame = tkinter.Frame(self)
        self.treeViewFrame.pack(expand=True, fill="both", padx=10)

        # Scrollbar
        self.treeViewScrollBar = tkinter.Scrollbar(self.treeViewFrame)
        self.treeViewScrollBar.pack(side="right", fill="y")

        # Tree view
        self.debtsTreeView = ttk.Treeview(self.treeViewFrame,yscrollcommand=self.treeViewScrollBar.set)
        self.treeViewScrollBar.config(command=self.debtsTreeView.yview)

        self.debtsTreeView.tag_configure('name', background='#eaf1fb', font=("Montserrat",10))
        self.debtsTreeView.tag_configure('even', background='#FFFFFF', font=("Montserrat",10))
        self.debtsTreeView.tag_configure('odd', background='#f5f9f9', font=("Montserrat",10))

        # Setup Columns
        self.debtsTreeView['columns'] = ('clientName', 'item','amount', 'price','sum')

        # Format Columns
        self.debtsTreeView.column("#0", width=20, stretch="no")
        self.debtsTreeView.column("clientName",anchor="center", width=80, stretch="no")
        self.debtsTreeView.column("item",anchor="w",width=100, stretch="no")
        self.debtsTreeView.column("amount",anchor="center",width=30, stretch="no")
        self.debtsTreeView.column("price",anchor="w")
        self.debtsTreeView.column("sum",anchor="e",width=50, stretch="no")

        # Create Headings
        self.debtsTreeView.heading("#0",text="",anchor="center")
        self.debtsTreeView.heading("clientName",text="Name",anchor="center")
        self.debtsTreeView.heading("item",text="Item",anchor="center")
        self.debtsTreeView.heading("amount",text="x",anchor="center")
        self.debtsTreeView.heading("price",text="Price",anchor="center")
        self.debtsTreeView.heading("sum",text="Sum",anchor="center")

        self.debtsTreeView.pack(expand=True, fill="both")

        # FRAME - Log textbox
        self.logFrame = tkinter.Frame(self)
        self.logFrame.pack(fill='x', padx=10)
        self.logLabel = tkinter.Label(self.logFrame, text="Log: ")
        self.logLabel.pack(side="left", fill=tkinter.BOTH)


        # TEXTBOX - Log textbox
        self.logTextBox = ScrolledText(self, font=('Arial', 10), height=0.5, state="disabled")
        self.logTextBox.pack(fill="x", pady=5, padx=10)

        # SEPARATOR
        self.separator_bot = ttk.Separator(self, orient='horizontal')
        self.separator_bot.pack(fill="x", pady=2, padx=5)

        #Set bottom frame
        self.bottomFrame = tkinter.Frame(self)
        self.bottomFrame.columnconfigure(0, weight=1)
        self.bottomFrame.columnconfigure(1, weight=2)
        self.bottomFrame.columnconfigure(2, weight=3)
        self.bottomFrame.columnconfigure(3, weight=4)

        # DROPDOWN - Names
        self.delClientList = ["Names"]
        self.delClientListClicked = tkinter.StringVar(self)
        self.delClientListClicked.set("Names")
        self.delClientListDropDown = tkinter.OptionMenu(self.bottomFrame, self.delClientListClicked, *self.delClientList)
        self.delClientListDropDown.config(width=25)
        self.delClientListDropDown.grid(row=0, column=0)

        # DROPDOWN - Items
        self.delItems = ["Items"]
        self.delItemsClicked = tkinter.StringVar(self)
        self.delItemsClicked.set("Items")
        self.delItemsDropDown = tkinter.OptionMenu(self.bottomFrame, self.delItemsClicked, *self.delItems)
        self.delItemsDropDown.config(width=25)
        self.delItemsDropDown.grid(row=0, column=1)

        self.delAmount = [0]
        self.delAmountClicked = tkinter.StringVar(self)
        self.delAmountClicked.set(0)
        self.delAmountDropDown = tkinter.OptionMenu(self.bottomFrame, self.delAmountClicked, *self.delAmount)
        self.delAmountDropDown.config(width=3)
        self.delAmountDropDown.grid(row=0, column=2)
        # BUTTON - Delete
        self.deleteButton = ttk.Button(self.bottomFrame, text="Delete", width=26, padding=4, command=self.deleteSelectedItem)
        self.deleteButton.grid(row=0, column=3)

        self.bottomFrame.pack(fill='x', pady=(10, 5), padx=10)

        # SEPARATOR - Footer
        self.separator_bot2 = ttk.Separator(self, orient='horizontal')
        self.separator_bot2.pack(fill="x", pady=(5,0))
        self.footerFrame = tkinter.Frame(self)

        # LABEL - Footer - User (X) Logged in
        self.bottomLabel = tkinter.Label(self, text=f"User: None")
        self.bottomLabel.pack(padx=5, pady=(0.10), side="left")

        self.databaseFilepathLabel = tkinter.Label(self, text=resource_path(self.db_filepath))
        self.databaseFilepathLabel.pack(padx=5, side="right")

        self.addClientCliked.trace("w", self.updateNameInputField)
        self.itemsClicked.trace("w", self.updateItemInputField)

        self.delClientListClicked.trace('w', self.updateDeleteItemDropDown)
        self.delItemsClicked.trace("w", self.updateDeleteAmountDropDown)
        # ------------------------------------------------- Set Login Window ------------------------------------------------- #

        self.loginWindow = tkinter.Toplevel(self)
        #self.loginWindow.eval("tk::PlaceWindow . center")
        self.loginWindow.withdraw()
        self.loginWindow.iconphoto(False, tkinter.PhotoImage(file=resource_path("icon.ico")))
        self.loginWindow.geometry("400x120+250+250")
        self.loginWindow.title("BOB Keep - Login")

        self.loginWindow.resizable(False, False)
        self.loginWindow.protocol("WM_DELETE_WINDOW", lambda: self.exit(0))
        #self.attributes("-toolwindow", True)

        # LABEL - Password
        self.passwordLabel = tkinter.Label(self.loginWindow, font=("Arial", 12), text="Password:")
        self.passwordLabel.pack(pady=5)

        # INPUT - Password
        self.passwordEntry = tkinter.Entry(self.loginWindow, show="●", font=("Arial", 12), justify="center",borderwidth=3, relief=tkinter.FLAT)
        self.passwordEntry.bind("<Return>", self.tryLogin)
        self.passwordEntry.pack(pady=5)

        # BUTTON - Login
        self.loginButton = ttk.Button(self.loginWindow, text="Login", command=self.tryLogin, padding=2)
        self.loginButton.pack(pady=5)

        # Focus on Password - INPUT
        self.loginWindow.deiconify()
        self.passwordEntry.focus_set()

        log.write("Login window initiated.")

    def tryLogin(self, *args):

        log.write(f"Login attempt.[{args}]")
        # sha256(SuperUserPassword1234!)
        x01 = "0bbcf80bf633d612763b178703ad4b129d37f8ea2f11017d57c6ed14870992ee"
        # (random 10 char string) + sha256(admin0000)
        x02 = "53d6316bd7b9044e6bb5deaa87fe8316c2fde3938b78f8448875b08e551ccc95"
        password = self.passwordEntry.get()

        if hashlib.sha256(password.encode('utf-8')).hexdigest() == x01:

            log.write("Password for SuperUser correct! ")
            self.passwordEntry.delete(0, "end")
            self.loggedInAs = 1
            self.editmenu.entryconfigure(3, state="normal")
            self.bottomLabel.config(text="User: Super User")
            self.loginWindow.withdraw()
            self.deiconify()
            if self.logoutValue == 0:
                self.loadInitialDatabase()
                self.updateEverything()

        elif hashlib.sha256(password.encode('utf-8')).hexdigest() == x02:
            log.write("Password for Admin correct! ")
            self.passwordEntry.delete(0, "end")
            self.loggedInAs = 2
            self.bottomLabel.config(text="User: Admin")
            self.loginWindow.withdraw()
            self.deiconify()
            if self.logoutValue == 0:
                self.loadInitialDatabase()
                self.updateEverything()

        else:
            log.write("Wrong password!!!")
            pass

    def loadInitialDatabase(self):
        # Check if database.json exist and load it, if not create new
        try:
            self.unpaid_list = database(self.db_filepath).open(1)
            log.write(f"Names: {self.name_list}")
            print(self.unpaid_list)
        except:
            database(self.db_filepath).save(self.unpaid_list)
            log.write("Can't read database, database deleted")

    def exit(self, window):
        if window == 0:
            self.destroy()
            sys.exit(0)
        elif window == 1:
            if self.changedData == 0:
                log.write("Database unchanged.")
                self.destroy()
                sys.exit(0)

            else:
                yesnocancel = self.saveUnchangedData()
                print(yesnocancel)
                if yesnocancel == True:
                    self.save(0)
                    log.write("EXIT")
                    self.destroy()
                    sys.exit(0)

                elif yesnocancel == False:
                    log.write("EXIT")
                    self.destroy()
                    sys.exit(0)

                elif yesnocancel == None:
                    pass
                    self.updateLogBox()

    def saveUnchangedData(self):
                yesnocancel = messagebox.askyesnocancel("Save database?", f"Do you want to save changes to the {self.db_filepath}", default='yes')
                if yesnocancel == True:
                    self.save(0)
                elif yesnocancel == False:
                    pass
                elif yesnocancel == None:
                    pass
                return yesnocancel
    # ------------------------------------------------ Menu bar Funcions ------------------------------------------------ #
    def createNewDatabase(self):
        filename = None

        if self.changedData == 1:

            yesnocancel = self.saveUnchangedData()

            if yesnocancel == True or yesnocancel == False:
                filename = filedialog.asksaveasfilename(initialdir=".", defaultextension=".json", filetypes=(("JSON Database", "*.json"),("All Files", "*.*") ))
                if filename == "":
                    pass

                else:
                    self.unpaid_list = {}
                    database(filename).save(self.unpaid_list)
                    self.db_filepath = filename
                    log.write(f"Created new database on path: {filename}")
                    self.changedData = 0

                    self.updateEverything()

            elif yesnocancel == None:
                pass
        else:
            filename = filedialog.asksaveasfilename(initialdir=".", defaultextension=".json", filetypes=(("JSON Database", "*.json"),("All Files", "*.*") ))
            if filename == "":
                pass

            else:
                self.unpaid_list = {}
                database(filename).save(1)
                self.db_filepath = filename
                log.write(f"Created new database on path: {filename}")
                self.changedData = 0

                self.updateEverything()

    def openDatabaseFile(self):
        filename = None

        if self.changedData == 1:

            yesnocancel = self.saveUnchangedData()

            if yesnocancel == True or yesnocancel == False:

                filename = filedialog.askopenfilename(initialdir=".", defaultextension=".json", filetypes=(("JSON Database", "*.json"),("All Files", "*.*") ))
                if filename == "":
                    pass
                else:
                    try:
                        self.unpaid_list = database(filename).open(0)
                        self.db_filepath = filename
                        self.changedData = 0
                        log.write(f"Database loaded on path : {filename}")
                        self.updateEverything()
                    except:
                        log.write(f"Error wihle trying to load database : {filename}")
                        self.updateLogBox()

            else:
                pass
        else:
            filename = filedialog.askopenfilename(initialdir=".", defaultextension=".json", filetypes=(("JSON Database", "*.json"),("All Files", "*.*") ))
            if filename == "":
                pass
            else:
                try:
                    self.unpaid_list = database(filename).open(0)
                    self.db_filepath = filename
                    self.changedData = 0
                    log.write(f"Database loaded on path : {filename}")
                    self.updateEverything()
                except:
                    log.write(f"Error wihle trying to load database : {filename}")
                    self.updateLogBox()

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
        self.updateLogBox()
        self.changedData = 0

    def logout(self):
        log.write("Logout from session...")
        self.logoutValue = 1
        self.loggedInAs = 0
        self.withdraw()
        self.loginWindow.deiconify()

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
            "Version: 2.1.1\n" +
            "Date of release: 26/4/2023"
            )
    # ------------------------------------------------ Function functions ------------------------------------------------ #
    def addNewDebt(self, *args):
        new_name_created = False
        # Get Input fields and correct them
        input_name = self.nameInput.get().lower()
        item = self.itemInput.get().lower()
        if input_name == "":
            pass

        else:
            ## Corect little non alphabet mistakes in input string
            ## Check for words and try to remove non alphabetical mishapess
            name = ""
            firstletter = 0

            for character in input_name:
                if firstletter == 0:
                    if character.isalpha() == False:
                        pass
                    else:
                        firstletter = 1
                        name = name + character

                elif firstletter == 1:
                    if character.isalpha() == True:
                        name = name + character

                    else:
                        firstletter = 0
                        name = name + " "

            # Delete last character in output string if is not alphabetical character
            if name[-1].isalpha() == False:
                name = name[0:-1]

            try:
                amount = int(self.amountInput.get())
            except:
                amount = 0

            # If amount is set to 0, pass and set amount to 1
            if amount == 0:
                self.amountInput.delete(0, "end")
                self.amountInput.insert("end", 1)

            else:
                try:
                    price = Decimal(self.priceInput.get())
                    price = str(price)
                except:
                    price = "0.00"
                    self.priceInput.delete(0, "end")
                    self.priceInput.insert("end", price)

                n = 0

                if name not in self.unpaid_list:
                    self.unpaid_list[name] = {}
                    new_name_created = True
                    log.write(f"Add new Client named: {name}")

                while n < amount:
                    if item not in self.unpaid_list[name]:
                        self.unpaid_list[name][item] = [price]
                    else:
                        self.unpaid_list[name][item].append(price)

                    n = n + 1

                log.write(f"Added new item to {name}: ", (f"{item}, " * n))
                self.changedData = 1

                self.updateGlobalItemsList()
                self.updateGlobalNameList()
                self.updateMainTreeView()
                if new_name_created == True:
                    self.updateAddItemDropDown()
                self.updateDeleteNamesDropDown(0)
                self.updateDeleteItemDropDown(0)
                self.updateLogBox()

    def deleteSelectedItem(self):
        dropdown_position_reset = False
        name = self.delClientListClicked.get().lower()
        item = self.delItemsClicked.get().lower()
        amount = self.delAmountClicked.get().lower()

        if item == "-":
            self.unpaid_list.pop(name)

        else:
            if item:
                if self.unpaid_list[name][item]:
                    if amount == "0":
                        self.unpaid_list[name].pop(item)
                    n = 0
                    while n < int(amount):
                        price = self.unpaid_list[name][item][-1]
                        self.unpaid_list[name][item].pop(-1)
                        log.write(f"Deleted {item} with price {price} from {name}")
                        n = n + 1
                else:
                    self.unpaid_list[name].pop(item)
            else:
                self.unpaid_list.pop(name)
                dropdown_position_reset = True
                log.write(f"List of items empty. Delete client: {name}")

        self.changedData = 1
        self.updateGlobalNameList()
        self.updateGlobalItemsList()
        self.updateMainTreeView()
        self.updateAddItemDropDown()
        if dropdown_position_reset == True:
            self.updateDeleteNamesDropDown(1)
        self.updateDeleteNamesDropDown(0)
        self.updateDeleteItemDropDown()
        self.updateLogBox()
    # ------------------------------------------------- Update functions ------------------------------------------------- #
    def updateGlobalNameList(self):
        self.name_list.clear()
        for name in self.unpaid_list:
            if name not in self.name_list:
                self.name_list.append(name)
        self.name_list.sort()

    def updateGlobalItemsList(self):

        self.item_list.clear()
        for name in self.unpaid_list:
            for item in self.unpaid_list[name]:
                if item not in self.item_list:
                    self.item_list.append(item)
        self.item_list.sort()

    def updateNameInputField(self, *args):
        name = self.addClientCliked.get()
        self.nameInput.delete(0, 'end')
        self.nameInput.insert("end", name.title())

    def updateItemInputField(self, *args):
        item = self.itemsClicked.get()
        self.itemInput.delete(0, 'end')
        self.itemInput.insert("end", item.capitalize())

    def updateAddItemDropDown(self):

        self.addClientList.clear()
        self.addClientListDropDown['menu'].delete(0, 'end')
        try:
            for name in self.name_list:
                self.addClientList.append(name)
                self.addClientListDropDown['menu'].add_command(label=name.title() + "                 ", command=lambda value=name.title(): self.addClientCliked.set(value))

            self.itemsDropDown['menu'].delete(0, 'end')
            for item in self.item_list:
                self.itemsDropDown['menu'].add_command(label=item.capitalize() + "                 ", command=lambda value=item.capitalize(): self.itemsClicked.set(value))
            self.addClientCliked.set(self.addClientList[0])
        except:
            log.write("Error can't read items list or empty")

    def updateMainTreeView(self):
        n=1
        n2=1

        # Delete entries in Tree View
        for item in self.debtsTreeView.get_children():
            self.debtsTreeView.delete(item)

        # Go trough name and item list in memory and append everything to tree view
        # Calculate sum for every item and every name(client)
        for name in self.name_list:
            self.debtsTreeView.insert("",'end',iid=n,open=True,text='',values=(name.title(),"","",""), tags = ('name',))
            even=0
            client_sum = 0

            for item in self.unpaid_list[name]:
                prices = ""
                amount = 0
                item_sum = 0

                for price in self.unpaid_list[name][item]:
                    amount = amount + 1
                    prices = f"{prices + price},   "
                    item_sum = Decimal(price) + item_sum

                client_sum = item_sum + client_sum

                if even == 0:
                    self.debtsTreeView.insert(parent=n,index='end',iid=f"n{n2}",text='', values=("",item.capitalize(),amount,prices,f"{str(item_sum)} €"),tags = ('odd'))
                    even = 1
                    n2=n2+1

                elif even == 1:
                    self.debtsTreeView.insert(parent=n,index='end',text=(n+1), values=("",item.capitalize(),amount,prices,f"{str(item_sum)} €"),tags = ('even'))
                    even = 0
                    n2=n2+1

            self.debtsTreeView.set(n,4,f"{client_sum} €")
            n=n+1

    def updateDeleteNamesDropDown(self, position_reset):
        self.addClientList.clear()
        self.delClientList.clear()
        self.delClientListDropDown['menu'].delete(0, 'end')
        for name in self.name_list:
            self.addClientList.append(name.title())
            self.delClientListDropDown['menu'].add_command(label=name.title()+"                 ", command=lambda value=name.title(): self.delClientListClicked.set(value))
        if position_reset == 1:
            try:
                self.delClientListClicked.set(self.addClientList[0])
            except:
                self.delClientListClicked.set("")

    def updateDeleteItemDropDown(self, *args):

        name_selected = self.delClientListClicked.get()
        self.delItems.clear()
        self.delItemsDropDown["menu"].delete(0, "end")
        self.delItemsDropDown["menu"].add_command(label=" - ", command=lambda value="-": self.delItemsClicked.set(value))
        for name in self.unpaid_list:
            if name == name_selected.lower():
                for item in self.unpaid_list[name]:
                    self.delItems.append(item.capitalize())
                    self.delItemsDropDown["menu"].add_command(label=item.capitalize()+"                 ", command=lambda value=item.capitalize(): self.delItemsClicked.set(value))
        try:
            self.delItemsClicked.set(self.delItems[0])
        except:
            self.delItemsClicked.set("")

    def updateDeleteAmountDropDown(self, *args):
        name_selected = self.delClientListClicked.get().lower()
        item_selected = self.delItemsClicked.get().lower()
        self.delAmount.clear()
        self.delAmountDropDown["menu"].delete(0, "end")
        amount = 0
        self.delAmount.append(str(amount))
        self.delAmountDropDown['menu'].add_command(label=str(amount), command=lambda value=str(amount): self.delAmountClicked.set(value))
        for name in self.unpaid_list:
            if name == name_selected:
                for item in self.unpaid_list[name]:
                    if item == item_selected:
                        for price in self.unpaid_list[name][item]:
                            amount = amount + 1
                            self.delAmount.append(str(amount))
                            self.delAmountDropDown['menu'].add_command(label=str(amount), command=lambda value=str(amount): self.delAmountClicked.set(value))
        try:
            self.delAmountClicked.set(self.delAmount[1])
        except:
            self.delAmountClicked.set("")

    def resetInputFields(self):
        for item in self.debtsTreeView.get_children():
            self.debtsTreeView.delete(item)
        self.nameInput.delete(0, 'end')
        self.itemInput.delete(0, 'end')
        self.amountInput.delete(0, 'end')
        self.amountInput.insert("end", "1")
        self.priceInput.delete(0, "end")
        self.priceInput.insert("end", "0.00")

    def updateLogBox(self):
        self.logTextBox.config(state="normal")
        self.logTextBox.delete(0.0, "end")
        self.logTextBox.insert("end", log.read())
        self.logTextBox.config(state="disabled")

    def updateDatabaseFilepathLabel(self):
        self.databaseFilepathLabel.config(text=resource_path(self.db_filepath))

    def updateEverything(self):
        # UPDATE EVERYTHING
        self.updateGlobalNameList()
        self.updateGlobalItemsList()
        self.resetInputFields()
        self.updateMainTreeView()
        self.updateAddItemDropDown()
        self.updateDeleteNamesDropDown(1)
        self.focusOnItemInput()
        self.updateLogBox()
        self.updateDatabaseFilepathLabel()

    # ------------------------------------------------- Focus functions ---------------------------------------------------- #
    def focusOnNameInput(self, *args):
        self.nameInput.selection_range(0, "end")

    def focusOnItemInput(self, *args):
        self.itemInput.selection_range(0, "end")

    def focusOnKolInput(self, *args):
        self.amountInput.selection_range(0, "end")

    def focusOnPriceInput(self, *args):
        self.priceInput.selection_range(0, "end")

log.write("-"*100)
log.write("Program executed.")
MainWindow().mainloop()