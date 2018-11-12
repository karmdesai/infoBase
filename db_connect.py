import sqlite3
import sys
import time
import data_ask as ask

conn = sqlite3.connect('info_base.db')
cur = conn.cursor()

#Create the table
cur.execute('CREATE TABLE IF NOT EXISTS userInfo (username, password, first name, last name, email, phone number, age, FaceBook, Twitter, GitHub)')
conn.commit()

#Create a user using the tuple returned by the ask.create() function
def create_user():
    cur.execute('INSERT INTO userInfo VALUES (?,?,?,?,?,?,?,?,?,?)', ask.create())
    conn.commit()

def find_user():
    userQuery = input('Enter your username to find your data...\n')

    cur.execute('SELECT rowid FROM userInfo WHERE username = (?)', (userQuery,))
    data = cur.fetchall()

#Ensure that the user is registered with info-base
    if len(data) == 0:
        print(f'The username @{userQuery} does not exist in info-base!\n Goodbye!')
        time.sleep(3)
        sys.exit()

    tryPass = input(f'Enter the password for the user: @{userQuery}...\n')

    cur.execute('SELECT password FROM userInfo WHERE username = (?)', (userQuery,))
    data = cur.fetchall()

    while data != [(tryPass,)]:
        print('Incorrect Password...\n')
        tryPass = input(f'Enter the password for the user: @{userQuery}...\n')

if ask.welcome() == 'c':
    create_user()

elif ask.welcome() == 'v':
    find_user()

else:
    print('An unknown error occurred... \nAbort...')
    time.sleep(3)
    sys.exit()

























