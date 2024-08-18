import smtplib
import datetime
import json
import pandas as pd

df=pd.read_csv("example.csv")

time = datetime.datetime.now().strftime("%x")
books=["To Kill a Mockingbird","1984","The Great Gatsby","The Catcher in the Rye","The Lord of the Rings","Pride and Prejudice",
    "The Chronicles of Narnia","Animal Farm","Moby-Dick","War and Peace","Crime and Punishment","The Odyssey","Jane Eyre","Brave New World",
    "Wuthering Heights","The Scarlet Letter","Great Expectations","The Hobbit","Fahrenheit 451","The Adventures of Huckleberry Finn","Les Misérables",
    "Dracula","Frankenstein","The Picture of Dorian Gray","The Count of Monte Cristo","The Brothers Karamazov","Sense and Sensibility","Emma",
    "Persuasion","David Copperfield","Madame Bovary","Anna Karenina","The Divine Comedy","Don Quixote","The Iliad","Heart of Darkness",
    "The Grapes of Wrath","The Old Man and the Sea","The Sound and the Fury","The Call of the Wild","The Alchemist","Catch-22","One Hundred Years of Solitude",
    "Beloved","Slaughterhouse-Five","Lolita","Gone with the Wind","The Sun Also Rises","Ulysses","The Metamorphosis",]
     
class Record:
    def __init__(self,date,name,book):
        self.date=date
        self.name=name
        self.book=book

class Library:
    def __init__(self,books):
        self.nbooks=0
        self.books = books
        self.issue_record=[]

    def borrowbook(self):
        name=input("enter your name:")
        date=time
        book=input("enter book name:")
        if book in self.books:
            new_record=Record(date,name,book)
            self.issue_record.append(new_record)
            a=f"\n{name},{date},{book}"
            with open("example.csv","a") as file:
                file.write(a)
        else:
            print("book not avalible in library")

    def donatebook(self):
        book=input("enter book name:")
        if book not in self.books:
            self.books.append(book)
        else:
            print("book alrady exists in library")

    def bookslist(self):
        print(f"the total books is {len(self.books)}")
        for indx,bookname in enumerate(self.books,start=1):
            print(f"{indx}. {bookname}")

    def returnbook(self):
        name=input("enter your name:")
        # book=input("enter book name:")
        for objects in self.issue_record:
            if objects.name==name:
                self.issue_record.remove(objects)
                self.books.append(objects.book)
                print(f"{objects.name}={objects.book} are removed")
            else:
                print(f"no record found of {name}")
        print (self.issue_record)
    
    def viewrecord(self):
        for objects in self.issue_record:
            print(f"\nstudent_name-{objects.name}\ndate-{objects.date}\nbookname-{objects.book}")
            

library1=Library(books)
# library1.borrowbook()
library1.borrowbook()
# library1.borrowbook()
# library1.viewrecord()
