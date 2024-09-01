import smtplib
import datetime
import json,logging
import pandas as pd

# for store all books data from json file to totalbooks variable
try:
    with open ("lIbrary_inventry.json","r") as file:
        totalbooks=json.load(file)
except:
    totalbooks={}

# for store all borrow books data from json file to borrowbooks variable
try:
    with open ("borrow_books.json","r") as file:
        borrowbooks=json.load(file)
except:
    borrowbooks={}

#for check avlable books in library
avalable_inventry=totalbooks.copy()
for bookname_kays in borrowbooks.keys():
    avalable_inventry[bookname_kays]=totalbooks[bookname_kays]-borrowbooks[bookname_kays]
    
# for auto select current date
time = datetime.datetime.now().strftime("%x")

"""this is a class to mannage library inventory"""
class Library_inventry:
    def __init__(self,totalbooks,borrowbooks,avalable_inventry):
        self.totalbooks=totalbooks
        self.avalable_books=avalable_inventry
        self.borrow_books=borrowbooks

    def check_book_status(self):
        bookname=input("enter book name: ")
        if (bookname in self.totalbooks) and (self.totalbooks[bookname]>0):
            print("book avlable to borrow")
        else:
            print("book not avlable")
    
    def addbook_in_enventory(self):
        bookname=input("enter book name to add in inventry: ")
        book_quantity=int(input("enter quantity of book: "))
        self.totalbooks[bookname]=book_quantity

     
library1=Library_inventry(totalbooks,borrowbooks,avalable_inventry)

class Library_record:
    def __init__(self,books):
        self.nbooks=0
        self.books = books
        self.issue_record={}

    def borrowbook(self):
        pass

    def donatebook(self):
        pass

    def bookslist(self):
        pass

    def returnbook(self):
        pass
    
    def viewrecord(self):
        pass
            

# print(library1.avalable_books)