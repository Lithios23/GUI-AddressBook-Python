import sys
from os import path
from tkinter import messagebox
import sqlite3

if getattr(sys, 'frozen', False):
    folder = path.dirname(sys.executable)
elif __file__:
    folder = path.dirname(__file__)

conection = sqlite3.connect(folder+'\\contactos.db')
cursor = conection.cursor()

def update():
    cursor.execute('Select * from contactos')
    return cursor.fetchall()

class contact:

    def __init__(self, name='', phone='', email='', clr='', id=''):
        
        self.name = name
        self.phone = phone
        self.email = email
        self.clr = clr
        self.id = id

    def add(self):   
        
        error = ''
        if len(self.name) == 0: error += 'Invalid name\n'
        if not self.phone.isdigit(): error += 'Invalid phone\n'
        if '@' not in self.email: error += 'Invalid email'
        
        if error != '': messagebox.showerror(title='Invalid details', message=error)
        else:
            sql = f"Insert into contactos values (null, '{self.name}', {int(self.phone)}, '{self.email}', {self.clr})"
            cursor.execute(sql)
            conection.commit()
            return True
        return False
    
    def update(self):
        error = ''
        if len(self.name) == 0: error += 'Invalid name\n'
        if not self.phone.isdigit(): error += 'Invalid phone\n'
        if '@' not in self.email: error += 'Invalid email'
        
        if error != '': messagebox.showerror(title='Invalid details', message=error)
        else:
            sql = (f"Update contactos set name='{self.name}', phone={self.phone}, email='{self.email}', clr={self.clr} where id = {self.id}")
            cursor.execute(sql)
            conection.commit()
            return True
        return False
        
    def delete(self):
        
        sql = f"delete from contactos where id = {self.id}"
        cursor.execute(sql)
        conection.commit()     