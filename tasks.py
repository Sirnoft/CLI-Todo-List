"""
Each Task has 5 attributes:
Title -> The name of the task
Description -> The Description of the task
Date Created -> The Day It was created
ID -> The ID of the user who created it

The ID field means different users have different tasks to do and these tasks are not shared.

"""

import sqlite3


class Task: #Every Task is an instance of this class
    def __init__(self,title:str,description:str,dateCreated:str,id:int) -> None:
        self.title = title
        self.description = description
        self.dateCreated = dateCreated
        self.id = id

    
    def __str__(self) -> str:   #returns a list of the instances details
        return [self.title,self.description,self.dateCreated,self.id]
    
    def getDescription(self) -> str: #returns the instances description
        return self.description

class TaskHandling:
    """All methods to operate on tasks"""

    def makeTask(task:Task) -> bool:
        task = task.__str__() #gets all the task's details

        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

        matches = cursor.execute("SELECT * FROM TASKS WHERE ID = ? AND title = ?",(task[3],task[0],)).fetchall()
        #checks if the task given already exists for that user

        if len(matches) > 0:
            return False # Already exists
        if len(matches) == 0:
            try:
                cursor.execute("INSERT INTO TASKS VALUES(?,?,?,?)",(task[0],task[1],task[2],task[3],))
                connection.commit()

                cursor.close()
                connection.close()
                return True #inserts the task into the db and commits it
            except:
                raise sqlite3.DatabaseError # sys error
    
    def deleteTask(task:Task) -> bool:
        task = task.__str__()
        _id = task[3] #gets the user ID

        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

        matches = cursor.execute("SELECT * FROM TASKS WHERE ID = ? AND TITLE = ?",(_id,task[0],)).fetchall()
        #checks if the task exists

        if len(matches) == 0:
            return False #task doesnt exist
        else:
            cursor.execute("DELETE FROM TASKS WHERE ID = ? AND TITLE = ?",(_id,task[0],)) #deletes the task from db
            connection.commit()

            cursor.close(), connection.close()
            return True

    def getTasks(userID:int) -> list:
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

        tasks = cursor.execute("SELECT * FROM TASKS WHERE ID = ? ORDER BY DATE_CREATED",(userID,)).fetchall()
        #gets the tasks of the user

        if tasks == []:
            return [] #user has no tasks

        task_objects = []

        for i in range(len(tasks)):
            obj = Task(tasks[i][0],tasks[i][1],tasks[i][2],tasks[i][3]) #makes a task object for each entry
            task_objects.append(obj)

        return task_objects #makes it easier to deal with operations as we already have the tasks

