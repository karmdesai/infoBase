import sqlite3
import sys
import time

conn = sqlite3.connect('info_base.db')
cur = conn.cursor()

# Create the table
cur.execute('''CREATE TABLE IF NOT EXISTS userInfo (username, password, first name, last name, 
            email, phone number, age, FaceBook, Twitter, GitHub)''')
conn.commit()

# Welcome the user, find out what they what they want to do with info-base
def welcome():
    global choice

    print("Welcome to info-base, where you'll be able to store your information and later access it.\n")
    choice = input("If you'd like to create a new file, enter 'c'. If you'd like to view a file, enter 'v'.\n").lower()

    while choice != 'c' and choice != 'v':
        choice = input("Ensure you're using the correct input -- use 'c' to create a file and 'v' to view an existing one.\n")

    if choice == 'c':
        print("Got it! We'll be creating a new file!")
    else:
        print("Ok, let's view an existing file!")

# Use this function to collect information regarding a new user
def collect():
    print('''Ok, let's get started with your file. Answer the questions that come up as you would like them to appear 
        on your file. \nEnter 'N/A' if you don't want to answer the question.\n''')

    userName = input("Choose a username for your log-in. Remember it - it cannot be reset!\n")

    cur.execute("SELECT rowid FROM userInfo WHERE username = (?)", (userName,))
    data = cur.fetchall()

    # Ensure that the user is NOT registered with info-base
    if len(data) != 0:
        print(f'The following errors found... @{userName} is already registered with info-base!\n Goodbye!')
        time.sleep(5)
        sys.exit()

    # Ask for a password from the user and ask them to also confirm it
    userPass = input(f"Enter a password for the account: {userName}")
    passConfirm = input("Re-enter the password to confirm...\n")

    while userPass != passConfirm:
        print("The passwords don't match!\n")
        userPass = input(f"Enter a password for the account: {userName}. Remember it - it cannot be reset!")
        passConfirm = input("Re-enter the password to confirm...")

    # Asks for and stores all required input
    print(f"Got it! @{userName} - let's continue with the rest of your information!\n")
    firstName = input("What is your first name?")
    lastName = input("What is your last name?\n")

    eMail = input("What is your e-mail address?\n")

    while ('@' not in list(eMail) or '.' not in list(eMail)) and eMail != 'N/A':
        eMail = input("Hmm... That doesn't look right.\n What is your e-mail address?\n")

    phoneNo = input("What is your phone number? Integers only - no dashes or spaces!\n")

    while phoneNo != 'N/A':
        try:
            int(phoneNo)
        except ValueError:
            print ("This is not a phone number!\n")
            phoneNo = input("What is your phone number?")
        else:
            break

    age = input("What is your age?\n")

    while age != 'N/A':
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

    print("I've created your file. Thanks for using info-base!")

    return (userName, userPass, firstName, lastName, eMail, phoneNo, age, faceBook, twitter, gitHub)

# Use this function to gather an existing user's data
def gather ():
    global userQuery, queryData

    userQuery = input('Enter your username to find your data...\n')

    cur.execute('SELECT rowid FROM userInfo WHERE username = (?)', (userQuery,))
    data = cur.fetchall()

    # Ensure that the user is registered with info-base
    if len(data) == 0:
        print(f'The username @{userQuery} does not exist in info-base!\n Goodbye!')
        time.sleep(3)
        sys.exit()

    # Ask for the user's password and ensure that it is correct
    tryPass = input(f'Enter the password for the user: @{userQuery}...\n')

    cur.execute('SELECT password FROM userInfo WHERE username = (?)', (userQuery,))
    data = cur.fetchall()

    while data != [(tryPass,)]:
        print('Incorrect Password...\n')
        tryPass = input(f'Enter the password for the user: @{userQuery}...\n')

    cur.execute('''SELECT first name, last name, email, phone number, age, FaceBook, Twitter, GitHub 
                FROM userInfo WHERE username = (?)''', (userQuery,))

    queryData = cur.fetchall()

# Create a user using the tuple returned by the ask.create() function
def create_user():
    cur.execute('INSERT INTO userInfo VALUES (?,?,?,?,?,?,?,?,?,?)', collect())
    conn.commit()

def show_data():
    gather()

    # Display all the user's data, line by line
    print(f'Displaying your data, ...@{userQuery}\n')
    time.sleep(1)

    print('Your first name is: ', queryData[0][0])
    print('Your last name is: ', queryData[0][1])
    print('Your e-mail address is: ', queryData[0][2])
    print('Your phone number is: ', queryData[0][3])
    print(f'You are {queryData[0][4]} years old.')
    print('Your faceBook username is: ', queryData[0][5])
    print('Your Twitter username is: ', queryData[0][6])
    print(f'Your gitHub username is: ', queryData[0][7])

welcome()

if choice == 'c':
    create_user()

elif choice == 'v':
    show_data()

else:
    print('An unknown error occurred... \nAbort...')
    time.sleep(3)
    sys.exit()
