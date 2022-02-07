import time
import sqlite3
import pandas as pd
import random
from random import randint
import matplotlib.pyplot as plt
import warnings
from cryptography.fernet import Fernet

class Login():

    def encryption(self, password):
        key = Fernet.generate_key()
        
        fernet = Fernet(key)
        encrypt = fernet.encrypt(password.encode())
        return encrypt
    
    def decryption(self, password):
        key = Fernet.generate_key()
    
        fernet = Fernet(key)
        decrypt = fernet.decrypt(password)
        return decrypt

    def new_user(self, username, password):

        run = True
        while run:

            sure = input("Are you sure that you want your username and password to be that? ")
                   
            if sure == 'yes':              
                
                conn = sqlite3.connect("Real.db")
                cur = conn.cursor()
                cur.execute("SELECT * FROM UserPass WHERE Username = '" + username + "';")
                exist = cur.fetchone()
                if exist is None:
                    #Login.encryption(self, password)
                    cur.execute("INSERT INTO UserPass (Username, Password) VALUES  ('" + username + "', '" + password  + "');")
                    cur.execute('COMMIT')
                    cur.close()
                    run = False
                else:
                    print("\nUnfortunately this account already exists, please choose a different username ")
                    m = Menu()
                    m.menu()
                    
                    
     
                
    def existing_user(self, username, password):
            
        run = True
        while run:
            #Login.decryption(password)
            conn = sqlite3.connect("Real.db")
            cur = conn.cursor()
            cur.execute("SELECT * FROM UserPass WHERE Username = '" + username + "' AND Password = '" + password + "';")
            exist = cur.fetchone()
            if exist is None:
                print("\nYour account does not exist ")
                print("\nPlease either re-enter your login or register a new account ")
                m = Menu()
                m.menu()
                    
            else:
               print("\nYou have logged in with Username:", username)
               run = False
                    

         
class Game():

    def __init__(self):
        self.answerl = ['A', 'B', 'C', 'D', 'Correct']
        self.answerd = {}# store the 4 options plus the corret answer
        self.reward = ['£0','£100','£200','£300','£500','£1000','£2000','£4000','£8000','£16000','£32000','£64000','£125000','£250000','£500000','£1000000']
        #self.reward is used to store every reward that is possible
        self.question = 1 #keeps count on what question number the user is on
        self.ask = Questions()
        self.lst = []#stores the question, possible answers and correct answer
        self.lb = Leaderboard()
        

    
    def start_game_new(self, username):
        input("\nWelcome " + username + " to Who Wants To Be a Millionaire! Press enter to get started ")
        print("\n")
         
             
        q = 0
        lcount = 0
        run = True
        while run and self.question < 16:
            #run will = True as long as the user answers correctly
            #if self.question reaches 16 it means that the user has answered all questions correctly and the game will end 
            r = random.randint(0, 9)
            #using the random library to get a number between 0 and 9 
            self.lst = self.ask.qs(q, r)
            #the questions and answwers from the questions class are appended to the list
            #q will increment each time the user answers correctly, r is a random number 
            print("\nQuestion:", str(self.question), "for", str(self.reward[self.question]))
            ret0 = self.lst[0]
             
            ret1 = "\nA. " + self.lst[1]
            ret2 = "\nB. " + self.lst[2] #list indexing is used to append the question (index 0), answers (index 1,2,3,4)                     
            ret3 = "\nC. " + self.lst[3] #and the correct answer (index 5)
            ret4 = "\nD. " + self.lst[4]
            correct = self.lst[5]            
            print()
            print(ret0)
            print("====================================")
            print("\nThe possible answers are:")
            print("\n")
            print(ret1)
            time.sleep(1)
            print(ret2)
            time.sleep(1)
            print(ret3)
            time.sleep(1)
            print(ret4)
            print()
            #print(self.lst[5])
            self.answerd['A'] = self.lst[1]
            self.answerd['B'] = self.lst[2] #the list indexes are appended in the same order to the answerd dictionary
            self.answerd['C'] = self.lst[3]
            self.answerd['D'] = self.lst[4]
            self.answerd['Correct'] = self.lst[5]

            play = True
            while play:
                if lcount < 3:
                    life = input("\nWould you like to use a lifeline? ")
                    if life == 'yes':
                        line = input("\nWhat lifeline would you like to use? (50/50, call a friend) ")
                   
                        if line == 'call' or 'friend' or 'call a friend':#asks what lifeline the user wants to use
                            print("\n *  Calling...")
                            print()                 #the lifelines are also included in the lists in the questions class
                            print(self.lst[6])      #they are appened to self.lst and have an index of 6
                            lcount = lcount + 1
                            play = False
                        elif line == '50/50' or '50':
                            #fifty_fifty(self)
                            play = False
                        else:
                            print("Please enter a valid input ")#error checking on the user input
                    elif life == 'no':
                        play = False

                else:
                    print("\nSorry you dont have any lifelines remaining ")#once the user has used 3 lifelines they cant use anymore
                    play = False
                
            yes = True
            while yes:
                user = input("\nPlease select your answer ")
                user = user.upper()     #the users answer is turned into caps so it can be matched to a key in the dictionary
                if user in self.answerd:#otherwise it will ask the user to input a valid option
                    pass
                else:
                    print("\nPlease enter a valid input")
                    continue
                    
                choice = input("\nIs that your final answer? ")
                if choice == 'yes':
                    yes = False         #validation checking on the users answer
                elif choice == 'no':
                    continue
                else:
                    print("Please enter a valid input ")

            if user in ret1 or ret2 or ret3 or ret4: #user is the variable that takes the users answer
                                                     #this if statement checks if the answer is in the possible answers
                if self.answerd[user] == self.answerd['Correct']:
                    if self.question == 15:
                        print("\nYou have won a million pounds! £1000000 is yours.")
                        print("\nThat is the end of the game")
                        conn = sqlite3.connect("Real.db")
                        cur = conn.cursor()
                        cur.execute("""SELECT Username FROM Leaderboard WHERE Username=?;""",
                                            (username,))
                        chck = cur.fetchone()
                        if chck is None:
                        
                            cur.execute("""INSERT INTO Leaderboard (Username, Score, MoneyWon) VALUES (?, ?, ?);""",
                                    (username, self.question-1, self.reward[self.question-1]))
                            cur.execute("""INSERT INTO Lifelines (Username, LifelinesUsed, Score) VALUES (?, ?, ?);""",
                                    (username, lcount, self.question))#the users scores, lifelines and moneywon are all stored in the database
                            cur.execute('COMMIT')
                            cur.close()
                            self.question = self.question + 1
                            q = q + 1
                        else:
                            cur.execute("""UPDATE Leaderboard SET Score=?, MoneyWon=? WHERE Username=?;""",
                                                (self.question-1, self.reward[self.question-1], username))
                            cur.execute("""UPDATE Lifelines SET LifelinesUsed=?, Score =? WHERE Username=?;""",
                                                (lcount, self.question-1, username))
                            cur.execute('COMMIT')
                            cur.close()
                            self.question = self.question + 1
                            q = q + 1
                    else:
                    #if the users choice matches the 'correct' answer in the dictionary then they are correct
                        print("\nThe answer is," , str(self.answerd['Correct']))#prints the correct answer
                        print("\nYou chose the right answer!")
                        print("You win", self.reward[self.question])#shows the user how much they won after that round
                        self.question = self.question + 1
                        q = q + 1
                    #question and q are incremented 
                       
                elif self.question == 15:#if question 14 is reached then it means the user has won the ultimate prize
                    print("\nYou have won a million pounds! £1000000 is yours.")
                    print("\nThat is the end of the game")
                    conn = sqlite3.connect("Real.db")
                    cur = conn.cursor()
                    cur.execute("""SELECT Username FROM Leaderboard WHERE Username=?;""",
                                            (username,))
                    chck = cur.fetchone()
                    if chck is None:
                        
                        cur.execute("""INSERT INTO Leaderboard (Username, Score, MoneyWon) VALUES (?, ?, ?);""",
                                (username, self.question-1, self.reward[self.question-1]))
                        cur.execute("""INSERT INTO Lifelines (Username, LifelinesUsed, Score) VALUES (?, ?, ?);""",
                                (username, lcount, self.question))#the users scores, lifelines and moneywon are all stored in the database
                        cur.execute('COMMIT')
                        cur.close()
                    else:
                        cur.execute("""UPDATE Leaderboard SET Score=?, MoneyWon=? WHERE Username=?;""",
                                            (self.question-1, self.reward[self.question-1], username))
                        cur.execute("""UPDATE Lifelines SET LifelinesUsed=?, Score =? WHERE Username=?;""",
                                            (lcount, self.question-1, username))
                        cur.execute('COMMIT')
                        cur.close()
                    try:
                        a = input("\nWould you like to see your name on the leaderboard?")
                        if a == 'yes':
                            self.lb.leader()#the leaderboard is shown if the user wants to see it
                        elif a == 'no':
                            run = False#the game is ended
                        
                    except:
                        print("Please enter a valid input ")#try and except used to validate the response
                        
                elif user in ret1 or ret2 or ret3 or ret4:#checks if the users answer is in the possible answers

                    if self.answerd[user] != self.answerd['Correct']:#checks if the users answer matches the correct one
                        print("The answer is, ", str(self.answerd['Correct']))#shows the right answer
                        print("\nUnfortunately you chose the wrong answer")
                        print("That means you walk away with, ", self.reward[self.question-1])#shows how much money the user won
                        conn = sqlite3.connect("Real.db")
                        cur = conn.cursor()
                        cur.execute("""SELECT Username FROM Leaderboard WHERE Username=?;""",
                                            (username,))#SELECT statement to see if the user has a previous score or not
                        chck = cur.fetchone()
                        if chck == None:
                            #if there is no previous score in the leaderboard then this result is added to the leaderboard
                            cur.execute("""INSERT INTO Leaderboard (Username, Score, MoneyWon) VALUES (?, ?, ?);""",
                                    (username, self.question-1, self.reward[self.question-1]))
                            cur.execute("""INSERT INTO Lifelines (Username, LifelinesUsed, Score) VALUES (?, ?, ?);""",
                                    (username, lcount, self.question-1))#username, score and money won are all added
                            cur.execute('COMMIT')
                            cur.close()
        
                        else:
                            qus = input("Would you like to update your previous score")
                            if qus == 'yes':#if a previous score is detected then the user is asked if they wish to update that score 
                                cur.execute("""UPDATE Leaderboard SET Score=?, MoneyWon=? WHERE Username=?;""",
                                            (self.question-1, self.reward[self.question-1], username))
                                cur.execute("""UPDATE Lifelines SET LifelinesUsed=?, Score =? WHERE Username=?;""",
                                            (lcount, self.question-1, username))
                                cur.execute('COMMIT')#if the user wants to updte their score then a UPDATE statement is used
                                cur.close()          #username, score and money won are all updated
                            elif qus == 'no':
                                pass
                            else:
                                print("\nPlease enter a valid input ")#validation check for the input
                        run = False
                        play = False
                        self.question = 16#the whole game loop is ended as self.question = 16 and run = False
                        b = input("Would you like to see your name on the leaderboard? ")
                        if b == 'yes':
                            self.lb.leader()#leaderboard is displayed if the user wants to see it 
                        elif b == 'no':
                            run = False
                            
                        else:
                            run = False
                                               
               
                else:

                    print("Please enter a valid input")#if user is not in ret then the user is asked for a valid input
                    continue#continues the loop if the user enters and invalid input
        m = Menu()
        m.menu()#calls the menu class once the loop has completley finished 
            

            
        

    def fifty_fifty(self):

    
        count = 0
        
        while count <= 2:#only 2 options should be removed so loop goes until 2
            d = random.randint(1,4)
            if self.answerd[d] == self.answerd['Correct']:#if the random number chosen is the correct answer
                pass                                 #the loop should pass and go again as we want to keep the correct answer
            else:
                self.answerd.remove(d)#the random answer is appended to the list
         
        print()
        if self.answerd['A'] is None:
            pass
        else:
            print (self.answerd['A'])
        if self.answerd['B'] is None:
            pass
        else:
            print (self.answerd['B'])
        if self.answerd['C'] is None:
            pass                        #these IF statements check what has been removed from the dictionary
        else:                           #the correct answer should print as i have specified not to remove it
            print (self.answerd['C'])
        if self.answerd['D'] is None:
            pass
        else:
            print (self.answerd['D'])
        if self.answerd['Correct'] is None:
            pass
        else:
            print (self.answerd['Correct'])
        

        


            
            

class Leaderboard():
    
    

    def __init__(self):
            self.data = []
            self.height = []
            self.leaderboard = {"Name":[], "Score":[], "Prize":[]}  #dictionary to make the leaderboard
            self.leaderboard2 = {"Name":[], "LifelinesUsed":[], "Score":[]}#ditionary for the lifeline leaderboard
        
        
    def leader(self):
        conn = sqlite3.connect("Real.db")
        cur = conn.cursor()
        cur.execute("SELECT Username, Score, MoneyWon FROM Leaderboard ORDER BY Score DESC;")
        tup = cur.fetchall()#SELECT statement used to get the data from the leaderboard field and order it
        if tup == None:
            print("There are no results yet, play the game and be the first on the leaderboard ")
        else:#if the user is the first person to play then they have to play the game first

            f = 0
            for i in tup:
                for k in i:
                    self.data.append(k)#data that is fetched from the database is broken up and put into the 
            f = 0
            t = 0
            while t < len(self.data):#iterates the length of the list
                                
                self.leaderboard["Name"].append(self.data[f])
                f = f + 1
                t = t + 1
                self.leaderboard["Score"].append(self.data[f])#increments the index of the list and goes through the length 1 by 1
                f = f + 1                                     #the data is added to the dictionary this way
                t = t + 1 
                self.leaderboard["Prize"].append(self.data[f])
                f = f + 1
                t = t + 1

                            
            #print(self.leaderboard)
            table = pd.DataFrame(self.leaderboard)    #pandas is used to create the leaderboard with the data                                                      
            print("\n")
            print(table)
            for p in self.leaderboard:
                self.leaderboard[p] = []    #this clears the dictionary and list of any previous data
            self.data.clear()               #this is done so previous values arent stacked 
            
            
    def lifes_used(self):
        conn = sqlite3.connect("Real.db")
        cur = conn.cursor()
        cur.execute("SELECT Username, LifelinesUsed, Score FROM Lifelines ORDER BY LifelinesUsed ASC;")
        tup = cur.fetchall()#same concept of getting the data from the database 
        if tup == None:
            print("There are no results yet, play the game and be the first on the leaderboard ")
        else:
            pass
        for i in tup:
            for u in i:
                self.data.append(u)#splits the data and appends it into the list

        f = 0
        t = 0
        while t < len(self.data):

            self.leaderboard2["Name"].append(self.data[f])
            f = f + 1
            t = t + 1
            self.leaderboard2["LifelinesUsed"].append(self.data[f])#same concept of incrementing the index and length of list
            f = f + 1                                              #data is added to the dictionary
            t = t + 1
            self.leaderboard2["Score"].append(self.data[f])
            f = f + 1
            t = t + 1

        #print(self.leaderboard2)
        table = pd.DataFrame(self.leaderboard2)#pandas used to format the leaderboard
        print("\n")
        print(table)
        
        for p in self.leaderboard2:
                self.leaderboard2[p] = []#clears the dictionary and list of previous data
        self.data.clear()
        
    #    print(self.data)
    

    def graph(self):
        
        left = [1,2]#graph dimensions
        height = []
        conn = sqlite3.connect("Real.db")
        cur = conn.cursor()
        cur.execute("SELECT avg(Score) FROM Leaderboard;")#the average of the score attribute is taken
        tup = cur.fetchone()
        #print(tup)
        for i in tup:
            height.append(i)#list is appended with the average value
        tee = input("Please enter your username to compare your score to the average ")
        conn = sqlite3.connect("Real.db")#user enters a username which is the score they want to compare to the average 
        cur = conn.cursor()
        hee = cur.execute("SELECT Score FROM Leaderboard WHERE Username = '" + tee + "';")
        ha = hee.fetchone()
        #print(ha)
        if ha == None:#validation check for the username 
            print("\nYour account was not found, please enter a valid username ")
        else:
            height.append(ha)#usernames score is appended to the list
        tick_label = ['Average Score', 'Your Score']

        plt.bar(left, height, tick_label = tick_label,
                width = 0.7, color = ['green', 'blue'])#the colour of the graph is chosen
                                                       #the dimensions in the list are added
        plt.xlabel('Score')#x axis labelled
        plt.ylabel('User')#y axis labelled
        plt.title('Graph to show the average vs the user')#title of the graph
        plt.show()#prints the graph
        plt.close()
            
        
            

           
                                             

            
class Menu():

    def __init__(self):
        self.game = Game()
        self.login = Login()
        self.leaderboard = Leaderboard()

    def menu(self):
        let = True
        while let:
            try:

                choice = int(input("\n1. Start Game\n2. Check Leaderboard\n3. Quit "))#user has 3 choices
                if choice == 1:#to start the game the user must login or create an account
                    f = input("Are you a new or existing user?")
                    if f == 'new':#new account
                     
                        print("\nWelcome, to continue onto the game please register an account or login to an exisiting one")
                        print("\nThis is done so your score can be tracked in a leaderboard")
                        run = True
                        while run:
                        
                            username = input("\nWhat would you like your usenrname to be? ")#username the user wants
                            password = input("What would you like your password to be? ")#password the user wants
                            show = input("\nWould you like to see your username and password? ")
                            if show == 'yes':
                                print("\nYour username is: " + username)#displays username
                                print("Your password is: " + password)#displays password
                                run = False
                                let = False#two loops are ended 
                            elif show == 'no':
                                run = False
                            else:
                                continue
                        self.login.new_user(username, password)#new_user function called from login class
                        self.game.start_game_new(username)#new game is started
                    

                    elif f == 'existing':#existing account
                        run = True
                        while run:
                            print("\nWelcome back! Please login to continue")
                            mu = input("\nPress m if you would like to return to the main menu, otherwise press any button ")
                            if mu == 'm':
                                Menu.menu(self)#press m if user wants to go back to the menu
                            else:
                                username = input("\nPlease enter your username ")#user to enter username
                                password = input("Please enter your password ")#user to enter password
                                self.login.existing_user(username, password)#esiting_user function called to check the login
                            self.game.start_game_new(username)#new game started
                            run = False

                elif choice == 2:
                    sel = int(input("\n1.Overall leaderboard\n2.Lifeline counter\n3.Average Score"))#menu asking if user wants leaderboard or graph
                    if sel == 1:
                        
                        self.leaderboard.leader()#general score leaderboard
                    elif sel == 2:
                        self.leaderboard.lifes_used()#lifeline leaderboard
                    elif sel == 3:
                        self.leaderboard.graph()#graph
                    else:
                        print("Please choose a valid option")#validation check
                
                elif choice == 3:#ends the program
                    quit()
                else:
                    print("Please choose a valid input")#validation check

            except:#validation
                print("Please choose a valid input")       


                         
             
             

class Questions():


    #start indexing at [5]

    def qs(self, q, r):
        return a[q][r]#q = 0 in the game loop and r is a random integer 0,9
                      #selects what question is asked
    global a
    a = [[0 for u in range(10)] for u in range(15)]#iterates through the questions which are labelled a, this creates a list with the question, answers and lifelines

    a[0][0] = ["In the UK, the abbreviation NHS stands for National what Service?","Humanity","Health","Honour","Household","Health", "I'm quite sure its health..."]
    a[0][1] = ["A spork is a utensil that typically combines a fork with which other item?", "Colander", "Whisk", "Spoon", "Corkscrew", "Spoon", "How did you not get that one, of course its a spoon"]
    a[0][2] = ["Obtaining the full details on something is said to be 'getting the' what?", "Lowdown", "Highdown", "Showdown", "Throwdown", "Lowdown", "It is 100% the lowdown, im surpirsed you didnt know that"]
    a[0][3] = ["According to legend, what was the name of the wizard who was adviser to King Arthur?", "Mervin", "Martin", "Marcus", "Merlin", "Merlin", "Dont ask how I know but it im pretty sure is Merlin"]
    a[0][4] = ["Which of these is most likely to be used as an archer?", "Bitterbow", "Crossbow", "Furiousbow", "Iratebow", "Crossbow", "Definantly a crossbow, what else?"]
    a[0][5] = ["On 24th March 2018, Clare Balding fronted live television coverage of which annual race?", "The Boat Race", "The Sack Race", "The Egg and Spoon Race", "The Three-Legged Race", "The Boat Race", "That's an easy one, its the boat race"]
    a[0][6] = ["Violing, violas and cellos all belong to what section of an orchestra?", "Yarn", "Twine", "String", "Rope", "String", "The answer is definantly string, I have no doubt"]
    a[0][7] = ["To apprehend someone in the act of committing a crime is to 'catch them...' what?", "Red-eyed", "Red-handed", "Red-headed", "Red-nosed", "Red-handed", "I've heard of this term before its 100% 'red-handed'"]
    a[0][8] = ["Which of these is the name of a traditional guessing game, often played on car journeys?", "I tinker", "I tailor", "I soldier", "I spy", "I spy", "You never played it before? Its 'I spy'"]
    a[0][9] = ["Which of these is a kind of porcelain?", "Marvellous mongolia", "Interesting india", "Priceless pakistan", "Fine china", "Fine china", "The answer is 100% Fine china im confident"]

    a[1][0] = ["Which Disney character famously leaves a glass slipper behind at a royal ball?","Pocahontas","Sleeping Beauty","Cinderella","Elsa","Cinderella", "Let me think, its Cinderella if I remember correctly"]
    a[1][1] = ["Someone expressing their anger is said to be 'venting their...' what?", "Spleen", "Liver", "Intestines", "Pancreas", "Spleen", "Someone said it at work today, its definantly A"]
    a[1][2] = ["A fascinator is usually worn on which part of the body?", "Head", "Shulders", "Knees", "Toes", "Head", "I saw them at Ascot when i went there, my final answer is head"]
    a[1][3] = ["What name is given to a dessert made with strawberries, meringue and whipped cream?", "Harrow muck", "Eton Mess", "Gordonstoun trifle", "Winchester shambles", "Eton Mess", "How ironic...I am having one right now, Eton Mess final answer"]
    a[1][4] = ["Who was appointed as the chief architect and supervisor of the rebuilding of St Paul's Cathedral after the Great Fire of London?", "Christpoher Robin", "Christopher Starling", "Christopher Wren", "Christopher Bullfinch", "Christopher Wren", "I know Chrisopher Wren is a famous architect so my final answer is C"]
    a[1][5] = ["Residents of cornwall and Devon traditionally disagree about the order in which cream and jam are placed on what food item?", "Scone", "Crumpet", "Pasty", "Kebab", "Scone", "Surprised you needed help with that...its definantly scone"]
    a[1][6] = ["Which of these is the name of the conspirator in the 1605 Gunpowder Plot?", "Guy Skewers", "Guy Nives", "Guy Fawkes", "Guy Spoones", "Guy Fawkes", "Do you know any history of bonfire night? Its Guy Fawkes"]
    a[1][7] = ["Whis of these animals is 'duck-billed'?", "Kangaroo", "Wallaby", "Platypus", "Koala", "Platypus", "Has to be a platypus since thats the one that lives in water"]
    a[1][8] = ["Which of these is the name of a sport included in the 2016 Summer Olympics programme?", "Integrated swimming", "Synchronised swimming", "Coordinated swimming", "Same-time swimming", "Synchronised swimming", "I watched it last time, its synchronised swimming"]
    a[1][9] = ["What was the first name of the character played by John Cleese in 'Fawlty Towers'?", "Chives", "Dill", "Mint", "Basil", "Basil", "You ever watched that series? Its Basil"]

    a[2][0] = ["What name is given to the revolving belt machinery in an airport that delivers checked luggage from the plane to baggage reclaim?", "Hangar", "Terminal", "Concourse", "Carousel", "Carousel", "Its definantly not hangar or termianl...I think its carousel i'm 70% sure"]
    a[2][1] = ["Which of this is a breed of spaniel?", "King James", "King John", "King Charles", "King George", "King Charles", "Good that you called me because I have one, King Charles final answer"]
    a[2][2] = ["Meghan Markle starred in which of these TV Series?", "Big Little Lies", "Suits", "The Crown", "Orange Is the New Black", "Suits", "I remember watching it and seeing her, the answer is definantly suits"]
    a[2][3] = ["Little, tawny and snowy are species of which bird", "Sparrow", "Cuckoo", "Owl", "Parrot", "Owl", "I am pretty sure its owl, final answer"]
    a[2][4] = ["According to Robert Burns, which food is the 'Great chieftain o' the pudding-race'?", "Teacake", "Haggis", "Bacon Roll", "Sticky toffee pudding", "Haggis", "Dont ask how I know this but it is Haggis, final answer"]
    a[2][5] = ["'Chippy' is a common slang term for which tradesperson?", "Electrician", "Gardener", "Carpenter", "Bricklayer", "Carpenter", "I'm pretty sure is carpenter, but im not certain"]
    a[2][6] = ["In the 1950 C.S. Lewis novel, Peter, Susan, Edmund and Lucy enter Narnia through which household item?", "Wardrobe", "Mirror", "Refrigerator", "Bath tub", "Wardrobe", "Mirror has thrown me off a bit but Im confident its wardrobe"]
    a[2][7] = ["Which of these is a horse race run annually at Epsom Downs?", "The Bolton", "The Loughborough", "The Sunderland", "The Derby", "The Derby", "I think its the derby, im pretty sure"]
    a[2][8] = ["Which of these countries did not host a Formula 1 Grand Prix race in 2003?","Monaco","France","Italy","Madagascar","Madagascar", "Don't remember Madagascar ever having a race so thats my answer"]
    a[2][9] = ["In 2012, the British athlete Greg Rutherford won an Olympic gold medal in which event?", "Long jump", "Pole vault", "Hammer throw", "Shot put", "Long jump", "I think i remember seeing him do long jump, thats my answer"]

    a[3][0] = ["Which of these brands was chiefly associated with the manufacture of household locks?", "Philips", "Flymo", "Chubb", "Ronseal", "Chubb", "I just know Phillips do screwdrivers so its definantly not them...my guess is Chubb"]
    a[3][1] = ["Which of these is the title of a famous artwork by Tracey Emin?", "Our Settee", "Your Bench", "Her Desk", "My Bed", "My Bed", "I think its My Bed but im not entierely sure"]
    a[3][2] = ["'Trebles for show, doubles for dough' is a phrase usually assosciated with which sport?", "Croquet", "Basketball", "Curling", "Darts", "Darts", "I am a big darts fan and I remember the phrase being said, darts final answer"]
    a[3][3] = ["The national flag of Sweden consists of which two colours?", "Blue and white", "White and Red", "Red and Yellow", "Yellow and Blue", "Yellow and Blue", "Well..IKEA is Blue and Yellow so I will say D, final answer"]
    a[3][4] = ["Something that gives away the plot or outcome of a TV show is called a... what?", "Fender", "Splitter", "Muffler", "Spoiler", "Spoiler", "It is obviously spoiler...I think you're nervous"]
    a[3][5] = ["What is the title of the 1965 Bond film starring Sean Connery?", "Thunderball", "Fireball", "Screwball", "Cannonball", "Thunderball", "This is a classic, of course its Thunderball"]
    a[3][6] = ["The famous landmark The Blackpool Tower is in which English county?", "Lancashire", "Hertfordshire", "Somerset", "Kent", "Lancashire", "Surprised you stumbled on this one, its Lancashire"]
    a[3][7] = ["Which of these is a unit of spped equivalent to nautical mile per hour?", "Ribbon", "Tie", "Knot", "Bow", "Knot", "Im sure its knot, never heard any of the other ones describe speed"]
    a[3][8] = ["In the 'Super Mario Bros' game franchise, what is the name of Mario's brother?", "Leonardo", "Lorenzo", "Luigi", "Larry", "Luigi", "Im surprised you needed help with this one but its Luigi"]
    a[3][9] = ["Which of these is a term for a group of actors or musicians who perform together?", "Ensuite", "Envogue", "Ensemble", "Engarde", "Ensemble", "I like to think its ensemble, but im not 100% confident"]

    a[4][0] = ["The hammer and sickle is one of the most recognisable symbols of which political ideology?", "Republicanism", "Communism", "Convervatism", "Liberalism", "Communism", "I did this in university its definantly communism"]
    a[4][1] = ["What is the name of the character played by Daisy Ridley in 'Star Wars: The Last Jedi'?", "Doh", "Rey", "Mee", "Farr", "Rey", "I have watched it and it is definantly Rey"]
    a[4][2] = ["Which of these is credited with inventing a type of compression-ignition engine?", "Franz Ethanol", "Dieter Propane", "Rudolf Diesel", "Hans Unleaded", "Rudolf Diesel", "Well all I know is that there is a diesel engine and all of these other names dont sound like engines, C final answer"]
    a[4][3] = ["Which of these is a term meaning 'collective intelligence'?", "Hutch mind", "Warren mind", "Sett mind", "Hive mind", "Hive mind", "Im pretty sure its Hive Mind if I remember correctly"]
    a[4][4] = ["LHR is the three-letter code for which UK airport?", "Liverpool", "Leicester", "Heathrow", "Humbershire", "Heathrow", "Dont you remember flying on holiday from there? Heathrow, final answer"]
    a[4][5] = ["In the folk tale 'Ali Baba and the Forty Thieves', what command does Ali Baba give to access a cave full of treasure?", "Abracadabra!", "Hocus, Pocus!", "Shazaam!", "Open, Sesame!", "Open, Sesame!", "If I remember correctly it is D, final answer"]
    a[4][6] = ["Which of these characters is voiced by James Corden in a 2018 film?", "Roger Rabbit", "Bugs Bunny", "Peter Rabbit", "Thumper", "Peter Rabbit", "I remember this movie coming out..I believe its Peter Rabbit, im not certain though"]
    a[4][7] = ["What is the name of the character played by Kit Harington in the TV drama 'Game of Thrones'?", "Edward Showers", "Jacob Sleet", "Jon Snow", "Barry Rain", "Jon Snow", "I've personally never watched it so I have no clue, possibly Barry Rain"]
    a[4][8] = ["Which of these is not one of the three body segments of an adult insect?", "Head", "Thorax", "Abdomen", "Appendix", "Appendix", "Im pretty sure its appendix, I am confident"]
    a[4][9] = ["Which of these might be sprinkled on a rice pudding?","Cinnabar","Cinnamon","Cincinnati","Cinerama","Cinnamon", "I had it this morning, its cinnamon"]

    a[5][0] = ["Which toys have been marketed with the phrase “robots in disguise”?", "Bratz Dolls", "Sylvanian Families", "Hatchminals", "Transformers", "Transformers", "The only one I know that aren't real people are Transformers, so go with that"]
    a[5][1] = ["Which county club play their home matches at the Oval?", "Middlesex", "Surrey", "Essex", "Hampshire", "Surrey", "I dont watch cricket but I know where the oval is...I think its Surrey"]
    a[5][2] = ["In the classic Hitchcock film 'Psycho', the famous shower scene takes place in which fictioal motel?", "Crane Motel", "Bates Motel", "Jefferies Motel", "Novak Motel", "Bates Motel", "The main character in the film was Bates so, Bates Motel final answer"]
    a[5][3] = ["In Greek mythology, who is the Goddess of Victory?", "Umbro", "Reebok", "Adidas", "Nike", "Nike", "None of these really sound like Greek words, I guess i'll go with Umbro"]
    a[5][4] = ["In the 'Transformers' film franchise, who is the leader of the Deceptions?", "Megaphone", "Megabyte", "Megatron", "Megabus", "Megatron", "You ever watched Transformers? Clearly not, Megatron final answer"]
    a[5][5] = ["In September 2017, the Bank of England issued a new £10 note featuring which author?", "Charlotte Bronte", "J.K Rowling", "Virginia Woolf", "Jane Austen", "Jane Austen", "Let me think...I think its Jane Austen if I remember correctly, im 70% sure"]
    a[5][6] = ["The hindu god Ganesh is traditioanally depicted as having the head of which animal?", "Elephant", "Tiger", "Rhino", "Cobra", "Elephant", "Its definantly elephant im very sure of it"]
    a[5][7] = ["Which meat is traditionally the main ingredient in the French dish 'coq au vin'?", "Chicken", "Beef", "Lamb", "Venison", "Chicken", "I think I had that when I went to France, I remember it having chicken"]
    a[5][8] = ["What is the title of the first chapter of the book 'Harry Potter and the Philosopher's Stone'?", "The Missing Mirror", "The Prince's Tale", "The Seven Potters", "The Boy Who Lived", "The Boy Who Lived", "I love Harry Potter, my answer is The boy who lived"]
    a[5][9] = ["Which of these is the main ingredient in a basic Indian 'dhal'?", "Lentils", "Potatoes", "Spinach", "Cauliflower", "Lentils", "Always one of my favourites, the answer is lentils"]

    a[6][0] = ["What does the word loquacious mean?", "Angry", "Chatty", "Beautiful", "Shy", "Chatty", "Sounds like something you would say about a sunset, so i'd say it means beautiful...not sure though never heard of the word"]
    a[6][1] = ["For what reason did Proffesor Robert Kelly gain internet fame in 2017?", "Mistaken identity on news", "Chasing after his dogs", "Kids gatecrashed interview", "Trying to catch a bat", "Kids gatecrashed interview", "I think I remember seeing this on the news so I think the answer is C"]
    a[6][2] = ["Vitamin B9 is also known by which of these names?", "Riboflavin", "Folic Acid", "Biotin", "Thiamin", "Folic Acid", "Its a complete guess but I think its Riboflavin, im honestly not sure"]
    a[6][3] = ["Which is not an electrical SI unit of measurement?","Volt","Ampere","Ohm","Gallon","Gallon"]
    a[6][4] = ["In 2000, which country joined rugby union's Five Nations Championship to make it the Six Nations?", "Romania", "Georgia", "Italy", "Spain", "Italy", "It is definanlty Italy, I still remember when they werent part of it"]
    a[6][5] = ["Wagyu is a Japanese breed of which animal?", "Cow", "Sheep", "Pig", "Chicken", "Cow", "You ever heard of a wagyu steak? It cow 100%"]
    a[6][6] = ["At the start of a game of chess, what is the total number of pawns on the board?", "Twelve", "Fourteen", "Sixteen", "Eighteen", "Sixteen", "I played chess the other day so im quite sure its sixteen"]
    a[6][7] = ["The historic location known as Checkpoint Charlie is a tourist attraction in which city?", "Warsaw", "Berlin", "Prague", "Vienna", "Berlin", "I remember learning about this in school, its Berlin"]
    a[6][8] = ["Who is the Roman Catholic patron saint of hopeless causes?", "St Jude", "St Julian", "St Jerome", "St Jeremy", "St Jude", "I have no clue at all, im going to guess St Jeremy"]
    a[6][9] = ["In March 2018, it was reported that Mount Etna is slowly sliding towards which neighbouring sea?", "Red", "Black", "Mediterranean", "Baltic", "Mediterranean", "Mount Etna is near sicily so that would be the mediterranean"]

    a[7][0] = ["Obstetrics is a branch of medicine particularly concerned with what?" , "Childbirth", "Broken Bones", "Heart Conditions", "Old Age", "Childbirth", "I've heard about this before, its Childbirth"]
    a[7][1] = ["Which of these words can be typed on a single row of a standard UK 'QWERTY' keyboard?", "Cheese", "Pork", "Salad", "Lager", "Salad", "I think its between pork and salad...I cant remember a keyboard fully"]
    a[7][2] = ["Which is a tough durable synthetic material?","PVC","PTO","POW","PBX","PVC", "I believe its PVC but im not entirely sure"]
    a[7][3] = ["Which is a breed of dog formerly used as coach dogs?","Croatian","Dalmatian","Montenegran","Bosnian","Dalmatian", "I honestly have no clue, I would just be guessing...croatian"]
    a[7][4] = ["What type of creature is a bunting?", "Bird", "Fish", "Frog", "Lizard", "Bird", "I know all about this, it is certainly bird final answer"]
    a[7][5] = ["What does the letter 'U' stand for in the name of the global children's agency UNICEF?", "United", "Uniform", "Unison", "Universal", "United", "Im honestly not sure, I think its united but I have doubts"]
    a[7][6] = ["In Scotland, what name designates any mountain peak 3,00 feet and over?", "Hamilton", "Munro", "Paisley", "Peebles", "Munro", "I am lost on this question, I think it may be Paisley"]
    a[7][7] = ["In 2012, Jean Dujardin won an Oscar for his role as a silent movie actor in which film?", "The Machinst", "The Postman", "The Artist", "The Pianist", "The Artist", "Its between the artist and the pianist, im just not sure which one its honestly 50/50, im going with the artist"]
    a[7][8] = ["What would you normally do with a Liebfraumilch?","Drink it","Play a tune on it","Drive it","Sit on it","Drink it", "Im sorry but I dont know, my guess is drink it"]
    a[7][9] = ["Which clothing item is named after a 19th century trapeze artist?", "Culottes", "Bikini", "Leotard", "Camisole", "Leotard", "I believe its leotard, but im just not 100% sure"]

    a[8][0] = ["In Doctor Who, what was the signature look of the fourth Doctor, as portrayed by Tom Baker?", "Bow-tie, braces and tweed jacket", "Wide-brimmed hat and extra long scarf", "Pinstripe suit and trainers", "Cape, velvet jacket and frilly shirt", "Wide-brimmed hat and extra long scarf", "Oh that was my favuorite Doctor Who...the answer is B"]
    a[8][1] = ["Which term means a dry wind blowing from North Africa, that picks up moisture crossing the Mediterrenan", "Mistral", "Sargasso", "Pampero", "Sirocco", "Sirocco", "I think its the Sargasso but honestly I do not know any of these, it is a complete guess"]
    a[8][2] = ["Which of these words is used to identify an Internet server?","Realm","Province","Kingdom","Domain","Domain"]
    a[8][3] = ["Which is an alternative name for a peanut?","Earthnut","Soilnut","Groundnut","Allnut","Groundnut"]
    a[8][4] = ["in Hokusai's print 'The Great Wave', which mountain is depcited in the background?", "Mount Emei", "Mount Kailash", "Mount Fuji", "Mount Sinai", "Mount Fuji", "The only Japanese mountain I know is Fuji, so I guess just go with that"]
    a[8][5] = ["'Cilantro' is the Spanish word for which herb?", "Basil", "Sage", "Coriander", "Rosemary", "Coriander", "Well the only other one that begins with c is coriander so im going with that, C final answer"]
    a[8][6] = ["Auguste Escoffier is most assosciated with which field?", "Painting", "Photography", "Cookery", "Music", "Cookery", "That is a tough one, I think its cookery but I wouldn't be surprised if it was painting"]
    a[8][7] = ["In Rene Magritte's portrait 'The Son of Man', the subject wears what type of hat?", "Bobble", "Beret", "Bowler", "Boater", "Bowler", "I have no clue about art to be honest, it sounds French so beret maybe"]
    a[8][8] = ["Originating in Italy, what type of food is mortadella?","Sausage","Pasta","Cheese","Pastry","Sausage"]
    a[8][9] = ["Which of these is the title of a 1985 dystopian novel by Margaret Atwood?", "The Butler's Story", "The Servant's Account", "The Handmaid's Tale", "The Nanny's Report", "The Handmaid's Tale", "I read the book and saw they made a tv show about it recently, the answer is C"]

    a[9][0] = ["Which of these religious observances lasts for the shortest period of time during the calendar year?", "Ramadan", "Diwali", "Lent", "Hanukkah", "Diwali", "I'm confident is is Diwali, go with B"]
    a[9][1] = ["What is the French word for England?","Angleterre","Etats-Unis","Inglaterra","Bretagne","Angleterre", "I've never heard of these words before, maybe its angleterrer"]
    a[9][2] = ["Which of these describes the rich and famous?","Glitterati","Hoi polloi","Establishment","Paparazzi","Glitterati", "The word glitterati sounds familiar, thats my answer"]
    a[9][3] = ["Which Italian term is used to describe painting on wet plaster?","Frappe","Fresco","Fredo","Frisson","Fresco"]
    a[9][4] = ["According to the Highway Code, what shape is the standard sign giving the order to 'Stop'?", "Pentagon", "Hexagon", "Heptagon", "Octagon", "Octagon", "It could be a hexagon or octagon, I honestly cant remember to be honest with you"]
    a[9][5] = ["The jazz musician Dave Brubeck was best known for playing which instrument?", "Piano", "Double Bass", "Trumpet", "Drums", "Piano", "I honestly have no clue, im going to say piano"]
    a[9][6] = ["'The Dead of Jericho' was the title of the first broadcast episode of which TV crime drama series?", "Midsomer Murders", "Inspector Morse", "Cracker", "A Touch of Frost", "Inspector Morse", "A complete guess as I dont watch these at all, I reckon Inspector Morse"]
    a[9][7] = ["What colour light indicates the port side of a ship?","Yellow","White","Blue","Red","Red", "I work with ships so I know its red"]
    a[9][8] = ["Which US city is the setting for the TV sitcom 'Taxi'?","Boston","Dallas","Los Angeles","New York","New York", "When I think tax I think New York so thats my answer"]
    a[9][9] = ["Which siogan featured on a 1943 poster of a woman in a red and white headscarf flexing her arm muscle?", "I Want You!", "Dig for Victory", "We Can Do It!", "Keep Calm and Carry On", "We Can Do It!", "They all sound like they can be right, I think im going to go with 'We Can Do It!'"]

    a[10][0] = ["At the closest point, which island group is only 50 miles south-east of the coast of Florida?", "Bahamas", "US Virgin Islands", "Turks and Caicos Islands", "Bermuda", "Bahamas", "I think its the Bahamas...I went on a trip there last year when I was in Florida"]
    a[10][1] = ["According to the Bible, which of these is not an archangel?","Michael","Raphael","Gabriel","Ishmael","Ishmael", "My bible knowledge is not the best but I dont remember there being an Ishamel"]
    a[10][2] = ["Which of these titles was bestowed upon Margaret Thatcher?","Marchioness","Duchess","Baroness","Countess","Baroness", "It definantly is Baroness, im quite sure"]
    a[10][3] = ["Which Jimmy, born in Jamaica in 1948, became a reggae star?","Edge","Mount","Cliff","Tor","Cliff", "I think it may be Cliff im not certain though"]
    a[10][4] = ["In the Bible, which land is said to be 'east of Eden'?", "Nineveh", "Nod", "Nazareth", "Nimrud", "Nod", "I have no clue sorry...Im going to say Nazareth"]
    a[10][5] = ["What did the legendary Trojan horse contain?","Horses","Gold","Wheat","Soldiers","Soldiers", "Im pretty sure it contained soldiers but im really not sure sorry"]
    a[10][6] = ["Margaret Thatcher's university tutor Dorothy Hodgkin won a Nobel Prize in which field?", "Physics", "Chemistry", "Economic Sciences", "Peace", "Chemistry", "I've never heard of Dorothy Hodgkin before..my guess is that its Economic sciences"]
    a[10][7] = ["Which present-day eastern European country was not part of the former USSR?","Hungary","Lithuania","Ukraine","Latvia","Ukraine", "I honestly have no clue about this one"]
    a[10][8] = ["The Mount of Olives is just east of which city?","Jerusalem","Moscow","Hong Kong","Paris","Jerusalem", "Im sure its A"]
    a[10][9] = ["In 2016, whom did Boris Johnson succeed as Foreign Secretary?", "Liam Fox", "Phillip Hammond", "Kenneth Clarke", "William Hague", "Phillip Hammond", "I honestly dont know, I think it may be Phillip Hammond but I honestly dont know"]

    a[11][0] = ["Construction of which of these famous landmarks was completed first?", "Empire State Building", "Royal Albert Hall", "Eiffel Tower", "Big Ben", "Big Ben", "I'm 50/50 on this one...it's either Big Ben or Royal Albert Hall, sorry"]
    a[11][1] = ["Which dinosaur could fly?","Allosaurus","Diplodocus","Stegosaurus","Pterodactyl","Pterodactyl", "If I remember correctly it is a Pterodactyl, I hope thats right"]
    a[11][2] = ["Which president was elected unopposed to a sixth term in March 2003?","George W Bush","Fidel Castro","Mary McAleese","Vladimir Putin","Fidel Castro", "Im rubbish with political history, but I will guess its George Bush"]
    a[11][3] = ["What, in August 2003, was 'Sobig.F'?","New airline","Computer virus","Archaeological dig","Meteorite","Computer virus", "I believe it was a computer virus but it could also be a meteorite"]
    a[11][4] = ["In October 2003, which became the third nation to put a man into space?","Japan","South Africa","Australia","China","China", "I think its China, they are the biggest power out of those 3"]
    a[11][5] = ["What would you normally do with a mai tai?","Eat it","Wear it","Drink it","Sing it","Drink it", "I believe you drink it but I may be wrong"]
    a[11][6] = ["What was the name of the two NASA missions sent to Mars in 1975?","Viking","Visigoth","Saxon","Hun","Viking", "I dont really know this one but Viking sounds like something the would call it"]
    a[11][7] = ["Which of these is an international motoring insurance?","Yellow card","Green card","Blue card","Red card","Green card", "Its green card, not sure how I know that but thats my final answer"]
    a[11][8] = ["What shape is an Australian Rules football pitch?","Rectangular","Circular","Diamond","Oval","Oval", "I remember watching it one time and found it a bit weird, its oval"]
    a[11][9] = ["Which is not one of golf's 'Majors'?","USPGA","US Masters","US Open","US Pro-Am","US Pro-Am", "I do watch golf and I dont remember seeing the US Pro-Am so thats my answer"]

    a[12][0] = ["Which of these cetaceans is classified as a “toothed whale”?", "Gray Whale", "Minke Whale", "Sperm Whale", "Humpback Whale", "Sperm Whale", "I'm not 100% sure but I believe its the Sperm Whale, that's my final answer"]
    a[12][1] = ["David Gates was the lead vocalist with which US band?","Yeast","Money","Dough","Bread","Bread", "My knowledge in this is terrible I honestly have no clue, who names a band bread anyways"]
    a[12][2] = ["Which of these is not a grain crop?","Wheat","Millet","Maize","Soya","Soya", "I know a bit about farming and im pretty sure the answer is soya"]
    a[12][3] = ["On a standard computer keyboard, what letter lies between 's' and 'f'?","c","d","e","r","d", "This is so easy I cant believe im struggling with this, I think its e"]
    a[12][4] = ["What type of fashion accessory is a 'pillbox'?","Scarf","Hat","Belt","Skirt","Hat", "This must be a ver old term because I've never heard of it..it might be hat"]
    a[12][5] = ["In which year was the last successful invasion of Britain?","55 BC","1066","1812","1914","1066", "I remember learning something about this in history when I was younger..I think its 1066"]
    a[12][6] = ["What name is given to the German air force?","Blitzkrieg","Luftwaffe","Panzer","Messerschmidt","Luftwaffe", "Im certain its the Luftwaffe, although Blitzkreig has crossed my mind"]
    a[12][7] = ["If you arrived at Split airport, which country would you be in?","Slovakia","Slovenia","Croatia","Hungary","Croatia", "I beleive when I travelled to Croatia I landed here so my answer is Croatia"]
    a[12][8] = ["Which of these oceans is the smallest?","Arctic","Pacific","Atlantic","Indian","Arctic", "Its either the Indian or Arctic, im not certain which one it is"]
    a[12][9] = ["The Dolomites are a range of mountains in the northeast of which country?","Poland","Turkey","Germany","Italy","Italy", "I know the alps are in Italy but im not sure if it has anything to do with it, im going with Italy"]

    a[13][0] = ["Who is the only British politician to have held all four 'Great Offices of State' at some point durin their career?", "David Lloyd George", "James Callaghan", "Harold Wilson", "John Major", "James Callaghan", "I'm rubbish at politics...I think its A but I honestly do not know"]
    a[13][1] = ["Which of these deserts is in the USA?","Atacama Desert","Gobi Desert","Sahara Desert","Mojave Desert","Mojave Desert", "I know for a fact its not the Sahara but thats all the help I can give really"]
    a[13][2] = ["In which US state is the city of Tucson?","Arizona","Kansas","Texas","Colorado","Arizona", "I went there on a trip once and I believe its Arizona"]
    a[13][3] = ["Approximately 61% of the world's population live on which continent?","Northh America","Europe","Asia","Africa","Asia", "Asia is the biggest out of all of them I think so Im saying Asia"]
    a[13][4] = ["What is the English title of the Brazilian film 'Cidade de Deus'?","Church","City of God","Angels","Eternal City","City of God", "I dont know the brazilian language at all but deus possibly means god, its a complete guess"]
    a[13][5] = ["What nationality is the tennis player Alex Corretja?","Peruvian","Chilean","Brazilian","Spanish","Spanish", "I dont know much about tennis, however this does sound like a Spanish name"]
    a[13][6] = ["Which sport is played by the Edmonton Oilers?","Basketball","Baseball","American football","Ice hockey","Ice hockey", "This is my favourite hockey team, the answer is hockey"]
    a[13][7] = ["Which sport uses the Christmas Tree starting system?","Formula 1","Motocross","Drag racing","Car rallying","Drag racing", "I dont really know what this means to be honest, I know its not F1 though"]
    a[13][8] = ["Which Formula 1 racing team has won the most Constructor's titles?","Williams","Ferrari","Lotus","McLaren","Ferrari", "It has to be Ferrari, I will be shocked if it anyone else"]
    a[13][9] = ["In which ocean are the Galapagos Islands?","Atlantic","Indian","Arctic","Pacific","Pacific", "They sound like warm islads so I reckon indian or pacific, however I could be completley wrong"]

    a[14][0] = [" In 1718, which pirate died in battle off the coast of what is now North Carolina?", "Calico Black", "Blackbeard", "Bartholomew Roberts", "Captain Kidd", "Blackbeard", "The only one I recognise is Blackbeard, so my final answer is B"]
    a[14][1] = ["Of which country is Phnom Penh the capital?","Vietnam","Thailand","Cambodia","Malaysia","Cambodia", "I know its not Malaysia or Thailand but I honestly dont know more than that"]
    a[14][2] = ["Vesper is an archaic term for which time of day?","Morning","Evening","Noon","Night","Evening", "I think it may be noon but honestly I do not know"]
    a[14][3] = ["Which of these chemical elements is named after a Norse god?","Uranium","Neptunium","Osmium","Thorium","Thorium", "Im not good with chemistry, possibly neptunism because it starts with n"]
    a[14][4] = ["What name was given to the amicable separation of Slovakia and the Czech Republic?","Satin Split","Velvet Divorce","Silk Separation","Damask Parting","Velvet Divorce", "My history with this is not good at all, but velvet divorce just sounds like the right answer"]
    a[14][5] = ["What is the UK equivalent of the CIA in the United States?","SAS","MI5","CND","MI6","MI6", "I know this is MI6, Im confident with my answer"]
    a[14][6] = ["What lies at the centre of a heliocentric model of the solar system?","Earth","Sun","Moon","North star","Sun", "I believe the answer is sun, however I wouldnt be surprised if it is North star"]
    a[14][7] = ["Who went on a 'Blonde Ambition' tour in 1990?","Blondie","Cher","Annie Lennox","Madonna","Madonna", "I went to one of these performances, its 100% Madonna"]
    a[14][8] = ["The Smurfs came from which country?","Sweden","Belgium","France","Denmark","Belgium", "I feel like its france but im not sure at all"]
    a[14][9] = ["The reputed last words of which famous composer were 'I shall hear in heaven'?","Wagner","Mozart","Albinoni","Beethoven","Beethoven", "I only know Mozart and Beethoven so surely one of them, which one though I have no clue"]


   
       
       
             
             
                       
   


m = Menu()
m.menu()
