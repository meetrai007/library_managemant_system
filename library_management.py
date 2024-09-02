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

# for store all library books issues record from json file to library_record variable
try:
    with open ("library_record.json","r") as file:
        library_record=json.load(file)
except:
    library_record={}

#for check avlable books in library
avalable_inventry=totalbooks.copy()
for bookname_kays in borrowbooks.keys():
    avalable_inventry[bookname_kays]=totalbooks[bookname_kays]-borrowbooks[bookname_kays]
    
# for auto select current date
time = str(datetime.datetime.now().strftime("%x"))

# a function to save now data to json file
def save_to_json(filename,data):
    with open (filename,"w") as file:
        json.dump(data,file)



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
        if bookname not in self.totalbooks:
            self.totalbooks[bookname]=book_quantity
        else:
            self.totalbooks[bookname]=self.totalbooks[bookname]+book_quantity
        save_to_json("library_inventry.json",self.totalbooks)
    
    def donatebook_by_student(self,bookname,qunantity):
        if bookname not in self.totalbooks:
            self.totalbooks[bookname]=qunantity
        else:
            self.totalbooks[bookname]=self.totalbooks[bookname]+qunantity
        save_to_json("library_inventry.json",self.totalbooks)

        
    def bookremove_from_inventory(self):
        bookname=input("enter book name to add in inventry: ")
        if bookname in self.totalbooks:
            del self.totalbooks[bookname]
        else:
            print("book not found in inventory")
        save_to_json("library_inventry.json",self.totalbooks)

    def borrow_a_book(self,bookname):
        if self.avalable_books[bookname]>0:
            if bookname in self.borrow_books:
                self.borrow_books[bookname]=self.borrow_books[bookname]+1
            else:
                self.borrow_books[bookname]=1
        else:
            print("book not avalable for borrow")
        save_to_json("borrow_books.json",self.borrow_books)

    def return_a_book(self,bookname):
        if bookname in self.borrow_books:
            if self.borrow_books[bookname]!=0:
                self.borrow_books[bookname]=self.borrow_books[bookname]-1
        else:
            print("book record not found in borroe book record")
        save_to_json("borrow_books.json",self.borrow_books)



"""this class for save records of students like name,date,bookname """
class Library_record:
    def __init__(self,avalable_inventry,library_record):
        self.avalable_books = avalable_inventry
        self.library_record=library_record

    def borrowbook(self):
        student_name=input("enter student name: ")
        book_name=input("Enter book name: ")
        date=time
        if self.avalable_books[book_name]>0:
            if (student_name in self.library_record):
                if len(self.library_record[student_name])<3:
                    self.library_record[student_name].append({"date":date,"bookname":book_name})
                else:
                    print("student allrady borrow three books so no more bookes borrow possible")
            else:
                self.library_record[student_name]=[]
                self.library_record[student_name].append({"date":date,"bookname":book_name})
            save_to_json("library_record.json",self.library_record)
            library1.borrow_a_book(book_name)
        else:
            print("book not avlable")


    def donatebook(self):
        bookname=input("Enter book name to donate: ")
        qunantity=int(input("Enter book qunanty: "))
        library1.donatebook_by_student(bookname,qunantity)
        

    def bookslist(self):
        for books in self.avalable_books.keys():
            print(books)

    def returnbook(self):
        student_name=input("Enter your name: ")
        book_name=input("Enter book name to return: ")
        if student_name in self.library_record:
            for items in self.library_record[student_name]:
                if items["bookname"]==book_name:
                    self.library_record[student_name].remove(items)
                    library1.return_a_book(book_name)
                    save_to_json("library_record.json",self.library_record)
                    print("book returend")
                    break
        else:
            print("student name not found in record")
    
    def viewrecord(self):
        print("""
            1.view all student record
            2.serch a student record
              """)
        userchoice=int(input("Enter your choice: "))
        if userchoice==1:
            for students_name in self.library_record:
                print(students_name)
                for items in self.library_record[students_name]:
                    print(f"date:{items["date"]} book name:{items["bookname"]}")
        if userchoice==2:
            studentname=input("Enter student name: ")
            print(studentname)
            try:
                for items in self.library_record[studentname]:
                    print(f"date:{items["date"]} book name:{items["bookname"]}")
            except:
                print("name not found ")


        
            
library1=Library_inventry(totalbooks,borrowbooks,avalable_inventry)
library1_record=Library_record(avalable_inventry,library_record)

# print(library1.avalable_books)
# library1.bookremove_from_inventory()
# library1.addbook_in_enventory()
# library1_record.bookslist()
# print(avalable_inventry)
# library1_record.returnbook()
# library1_record.borrowbook()
# library1_record.viewrecord()