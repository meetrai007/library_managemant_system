import smtplib
import datetime
import json,logging
import pandas as pd
import re

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
today_date_formet=datetime.date.today()
time=str(datetime.date.today())

# a function to save now data to json file
def save_to_json(filename,data):
    with open (filename,"w") as file:
        json.dump(data,file)

# this function for send mail
def send_email(student_mail,name):
    sender_mail="deeprai22016@outlook.com"
    password="cfjbvbvwxpeazqwp"
    recever_mail=student_mail
    message ="""Subject: this mail from library!!

        """
    body = f'dear {name} you have more then 15 dayes to hold an book please return the book\n'
    message=message + body
    server=smtplib.SMTP("smtp-mail.outlook.com",587)
    server.starttls()
    server.login(sender_mail,password)
    server.sendmail(sender_mail,recever_mail,message)
    server.quit()



"""this is a class to mannage library inventory"""
class Library_inventry:
    def __init__(self,totalbooks,borrowbooks,avalable_inventry):
        self.totalbooks=totalbooks
        self.avalable_books=avalable_inventry
        self.borrow_books=borrowbooks

    def inventory_bookslist(self):
        for book,quantity in self.totalbooks:
            print(f"bookname:{book} ,quantity:{quantity}")

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

    def donatebook_by_student(self,bookname,qunantity):
        if bookname not in self.totalbooks:
            self.totalbooks[bookname]=qunantity
        else:
            self.totalbooks[bookname]=self.totalbooks[bookname]+qunantity
        save_to_json("library_inventry.json",self.totalbooks)


"""this class for save records of students like name,date,bookname """
class Library_record:
    def __init__(self,avalable_inventry,library_record):
        self.avalable_books = avalable_inventry
        self.library_record=library_record

    def borrowbook(self):
        student_name=input("enter student name: ")
        book_name=input("Enter book name: ")
        student_mail=input("enter your mail: ")
        date=time
        if self.avalable_books[book_name]>0:
            if (student_name in self.library_record):
                if len(self.library_record[student_name])<3:
                    self.library_record[student_name].append({"date":date,"bookname":book_name,"mail":student_mail})
                else:
                    print("student allrady borrow three books so no more bookes borrow possible")
            else:
                self.library_record[student_name]=[]
                self.library_record[student_name].append({"date":date,"bookname":book_name,"mail":student_mail})
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

    def send_alert(self):
        for student_name in self.library_record:
            for item in self.library_record[student_name]:
                converted_date_formet=datetime.datetime.strptime(item["date"], "%Y-%m-%d").date()
                if today_date_formet - converted_date_formet >= datetime.timedelta(days=15):
                    send_email(item["mail"],student_name)
                
        
            
library1=Library_inventry(totalbooks,borrowbooks,avalable_inventry)
library1_record=Library_record(avalable_inventry,library_record)

while True:
    print("########## Welcome to library management app ##########")
    print("""
                    Choose an option for any operation

                    1. Manage library inventory
                    2. Student record section
                    3. Exit app
          """)
    try:
        user_choice = int(input("Enter a number 1, 2, 3: "))
    except:
        print("envalid choice, please enter number only")
    if user_choice == 1:
        while True:
            print("########## Welcome to library inventory ##########")
            print("""
                            Choose an option for any operation

                            1. Check book status
                            2. Add books to inventory
                            3. Remove book from inventory
                            4. View inventory books list
                            5. Back to home manu
                """)
            try:
                choice = int(input("choose an operation: "))
            except:
                print("envalid choice, please enter number only")    
            if choice == 1:
                library1.check_book_status()
            elif choice == 2:
                library1.addbook_in_enventory()
            elif choice == 3:
                library1.bookremove_from_inventory()
            elif choice == 4:
                library1.inventory_bookslist()
            elif choice == 5:
                break
            else:
                print("Enter choice between 1-5, carefully")

    elif user_choice == 2:
        while True:
            print("########## Welcome to student record section ##########")
            print("""
                            Choose an option for any operation

                            1. View student record
                            2. Borrow book
                            3. View available books
                            4. Donate book
                            5. Return book
                            6. Send alert 
                            7. Back to home manu
            """)
            try:
                choice2 = int(input("choose an operation: "))
            except:
                print("envalid choice, please enter number only")
            if choice2 == 1:
                library1_record.viewrecord()
            elif choice2 == 2:
                library1_record.borrowbook()
            elif choice2 == 3:
                library1_record.bookslist()
            elif choice2 == 4:
                library1_record.donatebook()
            elif choice2 == 5:
                library1_record.returnbook()
            elif choice2 == 6:
                library1_record.send_alert()
            elif choice2 == 7:
                break
            else:
                print("Enter choice between 1-6,carefully")

    elif user_choice == 3:
        break
    else:
        print("enter a choice between 1-3")
