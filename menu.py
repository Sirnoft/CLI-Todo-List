from login import Authentication,Session
from time import sleep
from datetime import date
from tasks import TaskHandling,Task


clear = lambda: print("\033c", end="", flush=True) #clears the CLI

class AuthenticationMenus:
    """Contains all login menu and signup menu methods"""

    def startMenu() -> None:
        #Allows the user to pick what operation to do

        print("Welcome to TDL, a place to track all your tasks and to-dos!\n")
        choice = int(input("Please enter a number.\n 1. Login\n 2. Signup\n 3. Quit\n"))

        
        if choice == 1:
            clear()
            AuthenticationMenus.loginMenu()
        elif choice == 2:
            clear()
            AuthenticationMenus.signupMenu()
        elif choice == 3:
            clear() 
            quit()
        else:
            clear()
            AuthenticationMenus.startMenu()
        
    def loginMenu() -> None:
        print("Please Input Your Details:")
        username = input("Username: ").strip()
        password = input("Password: ").strip()

        #Checks to make to sure details are not empty and the password is longer than 4 chars
        if username != "" and password != "" and len(password) >= 4:
            session = Authentication.login(username,password) #checks if the details entered are correct

            if session.getStatus():
                clear()
                TaskMenus.showTasks(session) #Shows the users tasks if successful
            else:
                while True: # Allows the user to try again or sign-up if their details are incorrect
                    print("Details are incorrect or could not be found. Please try again by entering 1 or go to the signup page by entering 2.")
                    choice = input()

                    if choice == "1":
                        clear()
                        AuthenticationMenus.loginMenu()
                        break
                    elif choice == "2":
                        clear()
                        AuthenticationMenus.signupMenu()
                        break
                    else:
                        clear()
                        continue
            
        else:
            clear()
            print("Your details are empty or your password is too short(5 characters). Please try again.")
            sleep(2)
            AuthenticationMenus.loginMenu()


    def signupMenu():
        print("Welcome to the signup Menu. Please Enter Your Details:")
        username = str(input("Username: ").strip())
        password = str(input("Password: ").strip())

        #Validates the input
        if username != "" and password != "" and len(password) >= 4:
            if Authentication.signup(username,password) == 1:
                print("Successfully signed up. Please Login now.")
                sleep(1)
                clear()
                AuthenticationMenus.loginMenu() #Lets the user login once signed up

            elif Authentication.signup(username,password) == 2:
                print("A account with that Username already exists! Please use a different username or login.")
                sleep(2)
                clear()
                AuthenticationMenus.startMenu()
            else:
                print("Something went wrong. Please try again.") #If there is a sys error, this runs
                sleep(2)
                clear()
                AuthenticationMenus.signupMenu()
        else:
            clear() # Makes sure the input is not erroneous
            print("Your details are empty or your password is too short(5 characters). Please try again.")
            sleep(2)
            clear()
            AuthenticationMenus.signupMenu()


class TaskMenus: 
    """Contains the methods to show the tasks of the user/ do operations on tasks"""


    def showTasks(session:Session) -> None: #Takes the users session object to get their user ID
        session = session
        userID = session.getID()
        tasks = TaskHandling.getTasks(userID) #Gets all the user's tasks in the form of Task objects


        print("Your Tasks are:\n")

        if len(tasks) == 0: #If no tasks exist, this is shown to tell the user to create one
           print("No Tasks currently. Please Add One")
        

        for i,j in enumerate(tasks): # Shows all tasks
            p = f"{i}: Title: {j.title} | Date: {j.dateCreated}"
            print(p)

        print("\n//////////////////////////////////////////")

        print("\n1. Look at a task's description\n2. Add a task\n3. Delete a task\n4. Quit")
        choice = input("") #Input to do a chosen operation on a task

        if choice == "1":
            chosenTask = input("Please enter a task number: ")
            try:
                chosenTask = tasks[int(chosenTask)] #casts the type to int and sees if the index exists
                TaskMenus.showDescription(session,chosenTask)
            
            except: #runs if the above tasks[] index doesn't exist
                clear()
                print("You have entered a non-existent task number. Please try again.")
                sleep(1)
                clear()
                TaskMenus.showTasks(session)

        elif choice == "2":
            TaskMenus.addTask(session)
        
        elif choice == "3":
            chosenTask = input("Please enter a task number: ")
            try:
                chosenTask = tasks[int(chosenTask)] #same thing as the choice == "1" statement
                TaskMenus.deleteTask(session,chosenTask)
            except IndexError:
                clear()
                print("You have entered a non-existent task number. Please try again.")
                sleep(1)
                clear()
                TaskMenus.showTasks(session)

        elif choice == "4":
            exit()
        else:
            clear()
            TaskMenus.showTasks(session) #recalls the showTask() if the input was not identified

    
    def showDescription(session:Session,task:Task) -> None:
        session = session
        clear()
        title = task.title  #unpacking the given Task() object
        description = task.description
        dateCreated = task.dateCreated

        print(f"Title: {title} | Date Created: {dateCreated}\n") #displays the given task
        print(f"Description:\n{description}")

        input("\n\n\n\n") 
        clear()
        TaskMenus.showTasks(session)

    def addTask(session:Session) -> None:
        session = session
        clear()

        title = str(input("Title: "))
        description = str(input("Description: "))
        dateCreated = date.today().strftime("%d/%m/%Y") #formats the time to DAY/MONTH/YEAR
        userID = session.getID()

        if title != "" and description != "":
            task = Task(title,description,dateCreated,userID)
            retr = TaskHandling.makeTask(task) #makes the task on the TASKS table

            if retr == False:
                print("A task with that title already exists. Please enter a different title!")
                sleep(1.5)
                clear()
                TaskMenus.addTask(session)
            else:
                clear()
                TaskMenus.showTasks(session)
        
        else:
            print("The title or description cannot be empty!\n")
            sleep(1)
            clear()
            TaskMenus.addTask(session)
        

    def deleteTask(session:Session,task:Task) -> None:
        session = session
        task = task
        clear()
        
        retr = TaskHandling.deleteTask(task)
        if retr ==True:
            TaskMenus.showTasks(session)
        else:
            print("No Such Task Exists!\n")
            sleep(1.5)
            clear()
            TaskMenus.showTasks(session)

