import smtplib
import datetime
import json

try:
    with open("library_record.json", "r") as file:
        library_recoard = json.load(file)
        books = library_recoard["books"]
        issue_record = library_recoard["issue_record"]
except:
    library_recoard = {}
    books = []
    issue_record = []

time = datetime.datetime.now().strftime("%x")


class Library:
    def __init__(self):
        self.nbooks=0
        self.books = ["To Kill a Mockingbird","1984","The Great Gatsby","The Catcher in the Rye","The Lord of the Rings","Pride and Prejudice",
    "The Chronicles of Narnia","Animal Farm","Moby-Dick","War and Peace","Crime and Punishment","The Odyssey","Jane Eyre","Brave New World",
    "Wuthering Heights","The Scarlet Letter","Great Expectations","The Hobbit","Fahrenheit 451","The Adventures of Huckleberry Finn","Les Misérables",
    "Dracula","Frankenstein","The Picture of Dorian Gray","The Count of Monte Cristo","The Brothers Karamazov","Sense and Sensibility","Emma",
    "Persuasion","David Copperfield","Madame Bovary","Anna Karenina","The Divine Comedy","Don Quixote","The Iliad","Heart of Darkness",
    "The Grapes of Wrath","The Old Man and the Sea","The Sound and the Fury","The Call of the Wild","The Alchemist","Catch-22","One Hundred Years of Solitude",
    "Beloved","Slaughterhouse-Five","Lolita","Gone with the Wind","The Sun Also Rises","Ulysses","The Metamorphosis",]
        self.issue_record={}

    def borrowbook(self, book, name):
        if book in self.books:
            if name not in self.issue_record:
                self.issue_record[name]=[{"date": time, "book": book}]
                self.books.remove(book)
                print("book issued successfully")
            else:
                self.issue_record[name].append({"date": time, "book": book})
                self.books.remove(book)
                print("new book issued succesfully")

        else:
            print("book not avalible in library")

    def donatebook(self, book):
        if book not in books:
            self.books.append(book)
        else:
            print("book alrady exists in library")

    def bookslist(self):
        print(f"the total books is {len(self.books)}")
        for i in self.books:
            print(i)

    def returnbook(self,name):
        self.issue_record.pop([name])
        print(self.issue_record)

library1=Library()
library1.borrowbook("1984","meet")
library1.borrowbook("Ulysses","meet")
print(library1.issue_record)
# library1.returnbook("meet")
