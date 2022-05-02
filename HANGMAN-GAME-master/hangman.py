#my project is a fun twist on the old game of hangman. In my game, instead of building the acual hang "man" you are building a tesla car.
#Now heres the catch. When you select a wrong awnser, python selects a random date in Febuary 2021. If Tesla stock went up during that day, you get saved from the hangman.
#But if Tesla stock went down, one more piece of the hangman is added
import random #essential for choosing a random day
from tkinter import *
from tkinter import messagebox
import datetime as dt #essential for distinguishing between dates
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web
import random

def teslaUp202102(day): #code for the stock save mechanism
    print (day)
    start = dt.datetime(2022, 2, day) #start of stock day
    end = dt.datetime(2022, 2, day) #end of stock day
    try:
        df = web.DataReader("TSLA", 'yahoo', start, end)#how we get stock info
    except:
        print("Exception")
        return True
    df.reset_index(inplace=True)
    df.set_index("Date", inplace=True) #these lines indicate if the statement is true or false and what to do with that info
    open = df.iloc[0]['Open']
    close = df.iloc[0]['Close']
    print(open)
    print(close)
    print(day)
    print ((close-open>0))
    if (close-open) > 0:#this is how we determine if stocks went up
        messagebox.showinfo("Free Save",#message box stating the save
        "Because Tesla stock increased on 2021-02-"+ str(day)+" from "+str(open)+ " to " + str(close)+
        " We have decided to not count your mistake.")
    return (open-close)>0

def FailedSave():#if the random day selected is not a stock day (saturday,sunday, or holiday) marks another point on the hangman
    randomDay = random.randrange(1,28,1)
    isUp=teslaUp202102(randomDay)
    return isUp

score = 0
run = True

# main loop
while run:
    root = Tk() #next few lines are the GUI
    root.geometry('905x700')
    root.title('HANG TESLA')
    root.config(bg = 'white')
    count = 0
    win_count = 0




    # choosing word
    index = random.randint(0,853)#this is where random words are selected for the hangman game
    file = open('words.txt','r')
    l = file.readlines()
    selected_word = l[index].strip('\n')
    
    # creation of word dashes variables
    x = 250
    for i in range(0,len(selected_word)):#where the words are randomly selected and below is how they are displayed
        x += 60
        exec('d{}=Label(root,text="_",bg="white",font=("arial",40))'.format(i))
        exec('d{}.place(x={},y={})'.format(i,x,450))
        
    #letters icon. #Below is a png of each of the letter buttons. Instead of a normal python button. These have an image so they look a little nicer
    al = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    for let in al:
        exec('{}=PhotoImage(file="{}.png")'.format(let,let))
        
    # hangman images
    h123 = ['h1','h2','h3','h4','h5','h6','h7']#each image is destroyed and then replaced each time a wrong awnser is chosen
    for hangman in h123:
        exec('{}=PhotoImage(file="{}.png")'.format(hangman,hangman))
        
    #letters placement
    button = [['b1','a',0,595],['b2','b',70,595],['b3','c',140,595],['b4','d',210,595],['b5','e',280,595],['b6','f',350,595],['b7','g',420,595],['b8','h',490,595],['b9','i',560,595],['b10','j',630,595],['b11','k',700,595],['b12','l',770,595],['b13','m',840,595],['b14','n',0,645],['b15','o',70,645],['b16','p',140,645],['b17','q',210,645],['b18','r',280,645],['b19','s',350,645],['b20','t',420,645],['b21','u',490,645],['b22','v',560,645],['b23','w',630,645],['b24','x',700,645],['b25','y',770,645],['b26','z',840,645]]

    for q1 in button:#
        exec('{}=Button(root,bd=0,command=lambda:check("{}","{}"),bg="white",activebackground="#E7FFFF",font=10,image={})'.format(q1[0],q1[1],q1[0],q1[1]))
        exec('{}.place(x={},y={})'.format(q1[0],q1[2],q1[3]))
        
    #hangman placement
    han = [['c1','h1'],['c2','h2'],['c3','h3'],['c4','h4'],['c5','h5'],['c6','h6'],['c7','h7']]
    for p1 in han:
        exec('{}=Label(root,bg="white",image={})'.format(p1[0],p1[1]))

    # placement of first hangman image
    c1.place(x = 300,y =- 50)#this determines where all the rest of the images will be placed
    
    # exit buton
    def close():
        global run
        answer = messagebox.askyesno('ALERT','YOU WANT TO EXIT THE GAME?')
        if answer == True:
            run = False
            root.destroy()
            
    e1 = PhotoImage(file = 'exit.png') #specs of the close button (color, font, where its placed)
    ex = Button(root,bd = 0,command = close,bg="white",activebackground = "#E7FFFF",font = 10,image = e1)
    ex.place(x=770,y=10)
    s2 = 'SCORE:'+str(score)
    s1 = Label(root,text = s2,bg = "#E7FFFF",font = ("arial",25))
    s1.place(x = 10,y = 10)

    # button press check function
    def check(letter,button):
        global count,win_count,run,score
        exec('{}.destroy()'.format(button)) #once pressed, the button is destroy in order to make it disapear
        if letter in selected_word:
            for i in range(0,len(selected_word)):
                if selected_word[i] == letter:
                    win_count += 1
                    exec('d{}.config(text="{}")'.format(i,letter.upper()))
            if win_count == len(selected_word):
                score += 1 #this is how python knows to add another hangman part
                answer = messagebox.askyesno('GAME OVER','YOU WON!\nWANT TO PLAY AGAIN?')
                if answer == True:
                    run = True
                    root.destroy()#destroys the game either way, the only difference is one restarts the game
                else:
                    run = False
                    root.destroy()
        else:
            if count == 0:#how the count is counted
                count += 1
            else:
                failedSave = FailedSave()
                if failedSave:
                  count += 1
            exec('c{}.destroy()'.format(count))
            exec('c{}.place(x={},y={})'.format(count+1,300,-50))
            if count == 6:#the maximum number of tries before you lose the game
                answer = messagebox.askyesno('GAME OVER','YOU LOST!\nWANT TO PLAY AGAIN?')
                if answer == True:
                    run = True
                    score = 0
                    root.destroy()
                else:
                    run = False
                    root.destroy()         
    root.mainloop()

