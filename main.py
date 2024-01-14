


import sys
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QDialog, QApplication, QLineEdit, QTableWidget, QTableWidgetItem, QListWidgetItem
from PyQt6.uic import loadUi
from pymongo import MongoClient
import hashlib



class DatabaseManager:
    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['UserInfo']
        self.users_collection = self.db['_id_password']


    def create_user(self, username, password):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        user_data = {'_id': username, 'password': hashed_password, 'pets': []}
        self.users_collection.insert_one(user_data)

    def validate_user(self, username, password):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        user_data = self.users_collection.find_one({'_id': username, 'password': hashed_password})
        return user_data is not None

    def add_pet(self, username, pet_name):
        pet_data = {'name': pet_name}
        self.users_collection.update_one({'_id': username}, {'$push': {'pets': pet_data}})

    def get_user_pets(self, username):
        user_data = self.users_collection.find_one({"_id": username})
        return user_data.get('pets', [])
    def add_task(self,username,task_name):
        task_data= {'task': task_name}
        self.users_collection.update_one({'_id':username},{'$push':{'tasks':task_data}})
    def get_user_tasks(self,username):
        user_data = self.users_collection.find_one({'_id':username})
        return  user_data.get('tasks',[])


class Petlist(QDialog):
    def __init__(self, database_manager):
        super(Petlist, self).__init__()
        loadUi("Petlist.ui", self)
        self.database_manager = database_manager
        self.current_username = ""  # Başlangıçta boş bir kullanıcı adı
        self.gotomenubutton.clicked.connect(self.gotomenu)

    def gotomenu(self):
        widget.setCurrentWidget(choicepage)

    def addtolistPet(self, username=None):
        if username is not None:
            self.current_username = username

        # Clear existing items in the PetListTableWidget
        self.PetlistWidget.clearContents()
        self.PetlistWidget.setRowCount(0)  # Reset row count

        if self.current_username:  # Eğer geçerli bir kullanıcı adı varsa
            # Assuming this method adds pets to the TableWidget based on the username
            pets = self.database_manager.get_user_pets(self.current_username)

            # Add pets to the PetListTableWidget
            for row, pet in enumerate(pets):
                self.PetlistWidget.insertRow(row)
                for col, (key, value) in enumerate(pet.items()):
                    item = QTableWidgetItem(str(value))
                    self.PetlistWidget.setItem(row, col, item)

class Login(QDialog):
    def __init__(self, database_manager):
        super(Login, self).__init__()
        loadUi("Login.ui", self)
        self.database_manager = database_manager

        # Connect buttons to their respective methods
        self.loginbutton.clicked.connect(self.gotochoice)
        self.createaccountbutton.clicked.connect(self.create_account)

    def gotochoice(self):
        # Get entered username and password from the input fields
        self.username = self.Usernameinput.text()
        password = self.Passwordinput.text()

        # Check if the entered credentials are correct
        if self.database_manager.validate_user(self.username, password):
            petlistspage.addtolistPet(self.username)
            tasklist.addtolistTask(self.username)
            widget.setCurrentIndex(1)
        else:
            # Display an error message or take appropriate action for incorrect credentials
            print("Incorrect username or password")

    def create_account(self):
        # Switch to the account creation page
        widget.setCurrentIndex(2)

        # You can further implement the account creation logic in the CreateAccount class

class Choice(QDialog):
    def __init__(self, database_manager):
        super(Choice, self).__init__()
        loadUi("Choice.ui", self)
        self.database_manager = database_manager

        # Connect buttons to their respective methods
        self.addPetButton.clicked.connect(self.gotoaddpet)
        self.MyPetsButton.clicked.connect(self.gotomypets)
        self.gototasklistbutton.clicked.connect(self.gototasklist)

    def gotoaddpet(self):
        # Switch to the add pet page
        widget.setCurrentIndex(3)

    def gotomypets(self):
        widget.setCurrentIndex(4)

    def gototasklist(self):
        widget.setCurrentIndex(5)

class PetAdd(QDialog):
    def __init__(self, database_manager):
        super(PetAdd, self).__init__()
        loadUi("PetAdd.ui", self)
        self.database_manager = database_manager

        # Connect button to the add_pet method
        self.petAddButton.clicked.connect(self.add_pet)

    def add_pet(self):
        # Get entered username and pet name from the input fields
        username = self.UsernamePet.text()
        pet_name = self.PetNamePet.text()

        # Check if the pet name is provided
        if not pet_name:
            print("Please enter a name for your pet.")
            return

        # Add a new pet for the user in the database
        self.database_manager.add_pet(username, pet_name)

        # Switch back to the choice page
        widget.setCurrentIndex(1)

class CreateAccount(QDialog):
    def __init__(self, database_manager):
        super(CreateAccount, self).__init__()
        loadUi("CreateAccount.ui", self)
        self.database_manager = database_manager

        # Connect button to the create_account method
        self.createaccountbutton2.clicked.connect(self.create_account)

    def create_account(self):
        # Get entered username and password from the input fields
        username = self.CreateUsername.text()
        password = self.CreatePassword.text()

        # Create a new user in the database
        self.database_manager.create_user(username, password)

        # Switch back to the login page
        widget.setCurrentIndex(0)

class TaskList(QDialog):
    def __init__(self,database_manager):
        super(TaskList,self).__init__()
        loadUi("TaskList.ui",self)
        self.current_username = ""  # Başlangıçta boş bir kullanıcı adı
        self.database_manager = database_manager
        self.GotoMenuButton.clicked.connect(self.gotomenu)
        self.gototaskbutton.clicked.connect(self.gotoaddtask)
        self.RemoveTask.clicked.connect(self.remove_task)

    def addtolistTask(self, username=None):
        if username is not None:
            self.current_username = username


        self.listWidgetTaskList.clearContents()
        self.listWidgetTaskList.setRowCount(0)  # Reset row count

        if self.current_username:
            tasks = self.database_manager.get_user_tasks(self.current_username)


            for row, task in enumerate(tasks):
                self.listWidgetTaskList.insertRow(row)
                for col, (key, value) in enumerate(task.items()):
                    item = QTableWidgetItem(str(value))
                    self.listWidgetTaskList.setItem(row, col, item)

    def remove_task(self):
        # Get the selected item from the listWidgetTaskList
        selected_item = self.listWidgetTaskList.currentItem()

        if selected_item:
            # Find the row of the selected item
            row = self.listWidgetTaskList.row(selected_item)

            # Remove the selected task from the listWidgetTaskList
            self.listWidgetTaskList.removeRow(row)

            # You may also want to remove the task from the database
            # Get the task name from the selected item
            task_name = selected_item.text()

            # Remove the task from the database
            # (Assuming you have a method in your DatabaseManager to remove a task)
            self.database_manager.remove_task(self.current_username, task_name)
    def gotomenu(self):
        widget.setCurrentIndex(1)
    def gotoaddtask(self):
        widget.setCurrentIndex(6)



class AddTaskPage(QDialog):
    def __init__(self,database_manager):
        super(AddTaskPage,self).__init__()
        loadUi("AddTaskPage.ui",self)
        self.database_manager= database_manager
        self.returntasklistbutton.clicked.connect(self.returntotasklist)
        self.gototasklistbutton.clicked.connect(self.add_tasks)

    def add_tasks(self):
        # Get entered username and pet name from the input fields
        username = self.taskusername.text()
        task_name = self.taskname.text()

        # Check if the pet name is provided
        if not task_name:
            print("Please enter a task")
            return

        # Add a new pet for the user in the database
        self.database_manager.add_task(username, task_name)

        # Switch back to the choice page
        widget.setCurrentIndex(5)

    def returntotasklist(self):
        widget.setCurrentIndex(5)





# Initialize the database manager
database_manager = DatabaseManager()

app = QApplication(sys.argv)

mainwindow = Login(database_manager)
choicepage = Choice(database_manager)
createaccountpage = CreateAccount(database_manager)
addpetpage = PetAdd(database_manager)
petlistspage = Petlist(database_manager)
tasklist = TaskList(database_manager)
addtaskpage = AddTaskPage(database_manager)

widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.addWidget(choicepage)
widget.addWidget(createaccountpage)
widget.addWidget(addpetpage)
widget.addWidget(petlistspage)
widget.addWidget(tasklist)
widget.addWidget(addtaskpage)
widget.setFixedWidth(500)
widget.setFixedHeight(500)

# Set echo mode for Passwordinput and CreatePassword to Password
mainwindow.Passwordinput.setEchoMode(QLineEdit.EchoMode.Password)
createaccountpage.CreatePassword.setEchoMode(QLineEdit.EchoMode.Password)
QtWidgets.QApplication.processEvents()

widget.show()
sys.exit(app.exec())
