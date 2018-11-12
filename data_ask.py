#This is the accompanying module to 'db_connect.py'
import sqlite3
import time
import sys

conn = sqlite3.connect('info_base.db')
cur = conn.cursor()

#Use this to introduce the program and return the user's choice
def welcome():
    print("Welcome to info-base, where you'll be able to store your information and later access it.\n")
    choice = input("If you'd like to create a new file, enter 'c'. If you'd like to view a file, enter 'v'.\n").lower()

    while choice != 'c' and choice != 'v':
        choice = input("Ensure you're using the correct input -- use 'c' to create a file and 'v' to view an existing one.\n")

    if choice == 'c':
        print("Got it! We'll be creating a new file!")
    else:
        print("Ok, let's view an existing file!")

    return choice

#Use this function to collect information regarding a new user
def create():
    print("Ok, let's get started with your file. Answer the questions that come up as you would like them to appear on your file.\n")
    userName = input("Choose a username for your log-in. Remember it - it cannot be reset!\n")

    cur.execute("SELECT rowid FROM userInfo WHERE username = (?)", (userName,))
    data = cur.fetchall()

    # Ensure that the user is NOT registered with info-base
    if len(data) != 0:
        print(f'The following errors found... @{userName} is already registered with info-base!\n Goodbye!')
        time.sleep(5)
        sys.exit()

    userPass = input(f"Enter a password for the account: {userName}")
    passConfirm = input("Re-enter the password to confirm...\n")

    while userPass != passConfirm:
        print("The passwords don't match!\n")
        userPass = input(f"Enter a password for the account: {userName}. Remember it - it cannot be reset!")
        passConfirm = input("Re-enter the password to confirm...")

    print(f"Got it! @{userName} - let's continue with the rest of your information!\n")
    firstName = input("What is your first name?")
    lastName = input("What is your last name?\n")

    eMail = input("What is your e-mail address?\n")

    while '@' not in list(eMail) or '.' not in list(eMail):
        eMail = input("Hmm... That doesn't look right.\n What is your e-mail address?\n")

    phoneNo = input("What is your phone number? Integers only - no dashes or spaces!\n")

    while True:
        try:
            int(phoneNo)
        except ValueError:
            print ("This is not a phone number!\n")
            phoneNo = input("What is your phone number?")
        else:
            break

    age = input("What is your age?\n")

    while True:
        try:
            int(age)
        except ValueError:
            print ("This is not an age!\n")
            age = input("What is your age?")
        else:
            break

    faceBook = '@' + input("What is your faceBook username?\n")
    twitter = '@' + input("What is your Twitter username?\n")
    gitHub = '@' + input("What is your gitHub username?\n")

    return (userName, userPass, firstName, lastName, eMail, phoneNo, age, faceBook, twitter, gitHub)


