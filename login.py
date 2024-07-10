from hashlib import md5 #md5 hashing function
import sqlite3

"""
Database Tables Info:
USERS(ID INTEGER PRIMARY KEY AUTOINCREMENT,NAME TEXT NOT NULL, PASSWORD TEXT NOT NULL)
TASKS(TITLE TEXT NOT NULL, DESCRIPTION TEXT, DATE_CREATED TEXT, ID TEXT NOT NULL, FOREIGN KEY(ID) REFERENCES USERS(ID)
"""

class Session:

    def __init__(self,session_status:bool,status_code:int,session_id:int) -> None:
        self.session = session_status
        self.status_code = status_code
        self.session_id = session_id

    def getStatus(self) -> bool: # Returns the current sessions status
        return self.session
    def getCode(self) -> int: # Retuns the current sessions status code
        return self.status_code
    def getID(self) -> int: # Returns the current sessions ID 
        return self.session_id

class Authentication:
    """All Authentication related methods"""
   
    def login(username:str,password:str) -> Session|None:
        """
        Returns a Session object with a session status and status code and ID\n
        Session(False,0,None) -> Details do not match, failed to log in\n
        Session(True,1,matches[0]) -> Details match, logged in \n
        Session(False,2,None) -> No such details on the database, failed to login\n
        """


        username = username.upper()
        passwordBytes = bytes(password,'utf-8')
        hash = Authentication._hashPassword(passwordBytes) #hashes the bytes and gets the hash

        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

        #if the returned list is 1, then the user exists and then we check if the hashes are the same
        matches = cursor.execute("SELECT * FROM USERS WHERE NAME = ?",(username,)).fetchall()
        
        cursor.close()
        connection.close()

        if len(matches) == 1: 
            matches = matches[0]

            if hash == matches[2]: #checks if the hashes are the same
                return Session(True,1,matches[0]) #Returns the session object with the users id in the db
            else: 
                return Session(False,0,None) #failed to login
            
        elif len(matches) <= 0:
            return Session(False,2,None)    #No such user exists, signup

    def signup(username:str,password:str) -> int:
        """
        Return 0 -> Adding details failed (sys failure), failed to sign up\n
        Return 1 -> Details logged, signed up\n
        Return 2 -> Details on the database already, failed to sign up\n
        """


        username = username.upper()
        passwordBytes = bytes(password,'utf-8')
        hash = Authentication._hashPassword(passwordBytes)

        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        
        database = cursor.execute("SELECT * FROM USERS WHERE NAME = ?",(username,)).fetchall()
        
        if len(database) <= 0: #if no user with that usrname exists, we make the user
            try:
                cursor.execute("INSERT INTO USERS(NAME,PASSWORD) VALUES(?,?)",(username,hash,))
                connection.commit()

                cursor.close()
                connection.close()

                return 1    #successfully signed up
            except:
                cursor.close()
                connection.close()

                return 0    #system error
        else:
            cursor.close()
            connection.close()

            return 2 #user with that username already exists
        
    def _hashPassword(passwordBytes:bytes) -> str:
        """Hashes a given set of bytes(passwords in this case) with a salt and returns their md5 hash"""

        m = md5()
        secret_salt = b"ewrtkiuytre3wsdcvbnhji8uytrew"
        
        m.update(secret_salt)
        m.update(passwordBytes)
        hash = m.hexdigest() #gets the actual md5 hash
        return hash
    

