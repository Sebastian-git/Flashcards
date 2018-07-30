""" Flash card program """

import os
import random
from tkinter import *
from tkinter import messagebox

# Window functions

def find(name, array):
    if len(array) <= 0:
        return -1
    found = False
    lowIndex = 0
    upIndex = len(array)
    index = int(upIndex/2)
    while not found:
        if array[index].lower() == name.lower():
            found = True
            break
        else:
            if name < array[index]:
                upIndex = index
            elif name > array[index]:
                lowIndex = index
            if lowIndex == index:
                break
            index = int(lowIndex+(upIndex-lowIndex)/2)
    if found:
        return index
    else:
        return -1

def clear():
    category.delete(0,"end")
    name.delete(0,"end")
    description.delete(0,"end")

def flashcard_window(root2, width, height):
    x = root.winfo_x()+root.winfo_width()/2-width/2
    y = root.winfo_y()+root.winfo_height()/2-height/2
    root2.geometry('%dx%d+%d+%d' % (width, height, x, y))

def help_window(root3, width, height):
    x = (root.winfo_x()+root.winfo_width()/2-width/2)-400
    y = (root.winfo_y()+root.winfo_height()/2-height/2)-50
    root3.geometry('%dx%d+%d+%d' % (width-200, height, x, y))

def main_window(width, height):
    x = root.winfo_screenwidth()/2-width/2
    y = root.winfo_screenheight()/2-height/2
    root.geometry('%dx%d+%d+%d' % (width, height, x, y))

def submit():
    categoryData = category.get()
    nameData = name.get().strip(" ")
    descriptionData = "::"+description.get()
    try:
        contents = open("database/"+categoryData.lower()+".txt","r")
    except:
        contents = open("database/"+categoryData.lower()+".txt","w")
        contents.close()
        contents = open("database/"+categoryData.lower()+".txt","r")
    contents.seek(0)
    lines = sorted(contents.readlines())
    contents.close()
    arr = list(x.split("::")[0] for x in lines)
    if find(nameData, arr) == -1:
        data = open("database/"+categoryData.lower()+'.txt', 'a')
        data.write(nameData+descriptionData+"\n")
        data.close()
        messagebox.showinfo("Successful", "Flashcard added")
    else:
        messagebox.showerror("Unsuccessful", "Flashcard already exists")
    clear()

def cards():
    root2.deiconify()
    flashcard_window(root2, 600, 400)
    catData = category.get()
    nameData = name.get()
    descData = description.get()
    try:
        workspace = open("database/"+catData+".txt","r")
    except:
        root2.withdraw()
        clear()
        messagebox.showerror("Error", "Flashcard not found")
        return
    lines = workspace.readlines()
    cards = []
    element = ""
    for i in lines:
        cards.append(i.strip("\n"))
    for i in range(len(cards)):
        element = cards[i]
        rIndex = random.randint(0,len(cards)-1)
        cards[i] = cards[rIndex]
        cards[rIndex] = element
    names = (list(i.split("::")[0] for i in cards))
    desc = (list(i.split("::")[1] for i in cards))
    name2.config(text=("\n\n\n"+names[randNum]), font=("Times New Roman", 25))
    side.config(text="Front")
    side.pack()
    name2.pack()
    global cardMode
    cardMode = True

# When desc > 49 \n

    def key(event):
        global cardMode
        global randNum
        if event.char == " ":
            if cardMode == True:
                side.config(text="Back")
                name2.config(text=("\n\n\n"+desc[randNum]))
                cardMode = False
            else:
                side.config(text="Front")
                name2.config(text="\n\n\n"+(names[randNum]))
                cardMode = True
        elif event.char == "\r":
            randNum += 1
            randNum %= len(cards)
            side.config(text="Front")
            name2.config(text=("\n\n\n"+names[randNum]))

    root2.bind("<Key>", key)
    name2.pack()
    side.pack()
    clear()
    root2.mainloop()

def helpb():
    root3 = Tk()
    root3.configure(background="gray")
    root3.title("Flashcards")
    root3.minsize(width=470, height=500)
    help_window(root3, 500, 400)
    Label(root3, text="Help Menu\n", bg="gray").pack()
    binformation = 'Buttons:\nSubmit - Submit button adds any entry to the database.\n Cards - Cards button shows flash cards for a category.\n Remove - Remove button deletes entries based off name. \nHelp - Help buttom explains the functions of the program. \nExit - Exit button closes out of the program.\n'
    Label(root3, text=binformation, bg="gray").pack()
    einformation = 'Entries:\nCategory - Category entry refers to what category the flash card set will be about.\nName - Name entry refers to what the "front side" of the flash card will be. \nDescription - Description entry refers to what the "back side" of the flash card will be.\n'
    Label(root3, text=einformation, bg="gray").pack()
    cinformation = 'Flash Cards:\n In the flash card window, there are several different cards which may be flipped\n up or down. Which set of flash cards will depend on what is typed into the\n category entry. When referencing cards, front is the name, and back is the description.\n'
    Label(root3, text=cinformation, bg="gray").pack()
    ccinformation = 'Flash Card Controls:\n Space - Flip card upside down.\n Enter - Change card being viewed.\n'
    Label(root3, text=ccinformation, bg="gray").pack()
    exit3 = Button(root3, text="EXIT", bg="red", fg="white", command=root3.destroy).pack(padx=20, pady=30, anchor=CENTER, side=BOTTOM, fill=BOTH)
    root3.mainloop()

def remove():
    categoryData = category.get()
    nameData = name.get().strip(" ")
    try:
        contents = open("database/"+categoryData.lower()+".txt","r")
    except:
        messagebox.showerror("Error", "Flashcard not found")
        return
    contents.seek(0)
    lines = sorted(contents.readlines())
    arr = list(x.split("::")[0] for x in lines)
    index = find(nameData, arr)
    if index == -1:
        messagebox.showerror("Unsuccessful", "Flashcard not found")
    else:
        del lines[index]
        contents.close()
        contents = open("database/"+categoryData.lower()+".txt","w")
        for line in lines:
            contents.write(line)
        contents.close()
        messagebox.showinfo("Successful", "Flashcard removed")
    clear()

# Database

try:
    os.mkdir("database")
    readme = open("database/readme.txt","w")
    readme.write('The database folder will hold all of the card decks, or "category" text files. If deleted, all data will be lost')
    readme.close()
except:
    pass


# Global variables

cardMode = True
randNum = 0

# Window configuration

root = Tk()
root.configure(background="gray")
root.title("Flashcards")
root.minsize(width=700, height=500)
main_window(700,500)
root2 = Tk()
root2.configure(background="gray")
root2.title("Flashcards")
root2.minsize(width=600, height=400)
name2 = Label(root2, text="", bg="gray", fg="black")
side = Label(root2, text="Front", bg="gray")
exit2 = Button(root2, text="EXIT", bg="red", fg="white", command=root2.withdraw).pack(padx=20, pady=30, anchor=CENTER, side=BOTTOM, fill=BOTH)
root2.withdraw()

# Window options

name = Label(root, text="Main Menu", bg="gray", fg="black")
name.config(font=("Times New Roman", 25))
name.pack()
barrier = Label(root, text=(""), bg="gray", fg="black").pack()
exit = Button(root, text="EXIT", bg="red", fg="white", command=exit).pack(padx=20, pady=30, anchor=CENTER, side=BOTTOM, fill=BOTH)
helpb = Button(root, text="Help", command=helpb).pack(padx=10, pady=10, side=BOTTOM, anchor=CENTER)
Label(root, bg="gray").pack()
categoryLabel = Label(root, text="Category of Flashcards", bg="gray")
categoryLabel.config(font=("Times New Roman", 15))
categoryLabel.pack()
category = Entry(root, width=30)
category.pack()
Label(root, bg="gray").pack()
nameLabel = Label(root, text="Name of Flashcard", bg="gray")
nameLabel.config(font=("Times New Roman", 15))
nameLabel.pack()
name = Entry(root, width=30)
name.pack()
Label(root, bg="gray").pack()
descriptionLabel = Label(root, text="Description of Flashcard", bg="gray")
descriptionLabel.config(font=("Times New Roman", 15))
descriptionLabel.pack()
description = Entry(root, width=50)
description.pack(ipady=15)
Label(root, text="                                        ", bg="gray").pack(side=LEFT)
Label(root, text="                                        ", bg="gray").pack(side=LEFT)
submit = Button(root, text="Submit", command=submit).pack(padx=10, pady=10, side=LEFT, anchor=N)
cards = Button(root, text="Cards", command=cards).pack(padx=10, pady=10, side=LEFT, anchor=N)
remove = Button(root, text="Remove", command=remove).pack(padx=10, pady=10, side=LEFT, anchor=N)

# Calling functions

root.mainloop()
