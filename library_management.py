import smtplib
import datetime
import json, logging
import pandas as pd
import re

name_pattren = r"^[a-z 0-9 ]+$"
bookname_pattren = r"^[A-Za-z0-9\s]+$"
email_pattren = r"\b[a-z][A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"

# for store all books data from json file to totalbooks variable
try:
    with open("lIbrary_inventry.json", "r") as file:
        totalbooks = json.load(file)
except:
    totalbooks = {}

# for store all borrow books data from json file to borrowbooks variable
try:
    with open("borrow_books.json", "r") as file:
        borrowbooks = json.load(file)
except:
    borrowbooks = {}

# for store all library books issues record from json file to library_record variable
try:
    with open("library_record.json", "r") as file:
        library_record = json.load(file)
except:
    library_record = {}

# for check avlable books in library
avalable_inventry = totalbooks.copy()
for bookname_kays in borrowbooks.keys():
    avalable_inventry[bookname_kays] = (
        totalbooks[bookname_kays] - borrowbooks[bookname_kays]
    )

# for auto select current date
today_date_formet = datetime.date.today()
time = str(datetime.date.today())


# a function to save now data to json file
def save_to_json(filename, data):
    with open(filename, "w") as file:
        json.dump(data, file)


# this function for send mail
def send_email(student_mail, name):
    try:
        sender_mail = "deeprai22016@outlook.com"
        password = "cfjbvbvwxpeazqwp"
        recever_mail = student_mail
        message = """Subject: this mail from library!!

            """
        body = f"dear {name} you have more then 15 dayes to hold an book please return the book\n"
        message = message + body
        server = smtplib.SMTP("smtp-mail.outlook.com", 587)
        server.starttls()
        server.login(sender_mail, password)
        server.sendmail(sender_mail, recever_mail, message)
        server.quit()
    except Exception as e:
        print("email not send due to this error", e)


"""this is a class to mannage library inventory"""


class Library_inventry:
    def __init__(self, totalbooks, borrowbooks, avalable_inventry):
        self.totalbooks = totalbooks
        self.avalable_books = avalable_inventry
        self.borrow_books = borrowbooks

    def inventory_bookslist(self):
        try:
            for book, quantity in self.totalbooks.items():
                print(f"bookname:{book} ,quantity:{quantity}")
        except Exception as e:
            print("error oucer", e)

    def check_book_status(self):
        while True:
            bookname = input("enter book name to check in inventry: ")
            if re.match(bookname_pattren, bookname):
                break
            else:
                print("enter bookname carefully and in wright format")
        if (bookname in self.totalbooks) and (self.totalbooks[bookname] > 0):
            print("book avlable to borrow")
        else:
            print("book not avlable")

    def addbook_in_enventory(self):
        while True:
            bookname = input("enter book name to add in inventry: ")
            if re.match(bookname_pattren, bookname):
                break
            else:
                print("enter bookname carefully and in wright format")
        while True:
            try:
                book_quantity = int(input("enter quantity of book: "))
                break
            except Exception as e:
                print("enter book quantity in numbers")
        try:
            if bookname not in self.totalbooks:
                self.totalbooks[bookname] = book_quantity
            else:
                self.totalbooks[bookname] = self.totalbooks[bookname] + book_quantity
            save_to_json("library_inventry.json", self.totalbooks)
        except Exception as e:
            print("an error oucur", e)

    def bookremove_from_inventory(self):
        while True:
            bookname = input("enter book name to remove from inventry: ")
            if re.match(bookname_pattren, bookname):
                break
            else:
                print("enter bookname carefully and in wright format")

        if bookname in self.totalbooks:
            del self.totalbooks[bookname]
        else:
            print("book not found in inventory")
        save_to_json("library_inventry.json", self.totalbooks)

    def borrow_a_book(self, bookname):
        try:
            if self.avalable_books[bookname] > 0:
                if bookname in self.borrow_books:
                    self.borrow_books[bookname] = self.borrow_books[bookname] + 1
                else:
                    self.borrow_books[bookname] = 1
            else:
                print("book not avalable for borrow")
            save_to_json("borrow_books.json", self.borrow_books)
        except Exception as e:
            print("an error oucur", e)

    def return_a_book(self, bookname):
        try:
            if bookname in self.borrow_books:
                if self.borrow_books[bookname] != 0:
                    self.borrow_books[bookname] = self.borrow_books[bookname] - 1
            else:
                print("book record not found in borroe book record")
            save_to_json("borrow_books.json", self.borrow_books)
        except Exception as e:
            print("an error oucur", e)

    def donatebook_by_student(self, bookname, qunantity):
        try:
            if bookname not in self.totalbooks:
                self.totalbooks[bookname] = qunantity
            else:
                self.totalbooks[bookname] = self.totalbooks[bookname] + qunantity
            save_to_json("library_inventry.json", self.totalbooks)
        except Exception as e:
            print("an error oucur", e)


"""this class for save records of students like name,date,bookname """


class Library_record:
    def __init__(self, avalable_inventry, library_record):
        self.avalable_books = avalable_inventry
        self.library_record = library_record

    def borrowbook(self):
        while True:
            student_name = input("enter student name: ")
            if re.match(name_pattren, student_name):
                break
            else:
                print("enter name again carefully and in wright format")
        while True:
            book_name = input("Enter book name: ")
            if re.match(bookname_pattren, book_name):
                break
            else:
                print("enter bookname again carefully and in wright format")
        while True:
            student_mail = input("enter your mail: ")
            if re.match(email_pattren, student_mail):
                break
            else:
                print("enter email again carefully and in wright format")

        try:
            date = time
            if book_name in self.avalable_books:
                if self.avalable_books[book_name] > 0:
                    if student_name in self.library_record:
                        if len(self.library_record[student_name]) < 3:
                            self.library_record[student_name].append(
                                {
                                    "date": date,
                                    "bookname": book_name,
                                    "mail": student_mail,
                                }
                            )
                        else:
                            print(
                                "student allrady borrow three books so no more bookes borrow possible"
                            )
                    else:
                        self.library_record[student_name] = []
                        self.library_record[student_name].append(
                            {"date": date, "bookname": book_name, "mail": student_mail}
                        )
                    save_to_json("library_record.json", self.library_record)
                    library1.borrow_a_book(book_name)
                else:
                    print("book not avlable")
            else:
                print("sorry,book not avlable")
        except Exception as e:
            print("an error oucur", e)

    def donatebook(self):
        while True:
            bookname = input("Enter book name to donate: ")
            if re.match(bookname_pattren, bookname):
                break
            else:
                print("enter book name again carefully and in wright format")
        while True:
            try:
                qunantity = int(input("Enter book qunanty: "))
                break
            except:
                print("enter book quantity in numbers")

        library1.donatebook_by_student(bookname, qunantity)

    def bookslist(self):
        try:
            for books in self.avalable_books.keys():
                print(books)
        except Exception as e:
            print("error found", e)

    def returnbook(self):
        while True:
            student_name = input("Enter your name: ")
            if re.match(name_pattren, student_name):
                break
            else:
                print("enter name again in wright formet")
        while True:
            book_name = input("Enter book name to return: ")
            if re.match(bookname_pattren, book_name):
                break
            else:
                print("enter bookname again in wright formet")

        if student_name in self.library_record:
            for items in self.library_record[student_name]:
                if items["bookname"] == book_name:
                    self.library_record[student_name].remove(items)
                    library1.return_a_book(book_name)
                    save_to_json("library_record.json", self.library_record)
                    print("book returend")
                    break
        else:
            print("student name not found in record")

    def viewrecord(self):
        print(
            """
            1.view all student record
            2.serch a student record
              """
        )
        while True:
            try:
                userchoice = int(input("Enter your choice: "))
                break
            except:
                print("enter choice aganin in numbers only")

        if userchoice == 1:
            for students_name in self.library_record:
                print(students_name)
                for items in self.library_record[students_name]:
                    print(f"date:{items["date"]} book name:{items["bookname"]}")
        elif userchoice == 2:
            while True:
                studentname = input("Enter student name: ")
                if re.match(name_pattren, studentname):
                    break
                else:
                    print("enter name again in wright formet")
            print(studentname)
            try:
                for items in self.library_record[studentname]:
                    print(f"date:{items["date"]} book name:{items["bookname"]}")
            except:
                print("name not found ")
        else:
            print("choice not match enter again 1 or 2 only")

    def send_alert(self):
        try:
            for student_name in self.library_record:
                for item in self.library_record[student_name]:
                    converted_date_formet = datetime.datetime.strptime(
                        item["date"], "%Y-%m-%d"
                    ).date()
                    if today_date_formet - converted_date_formet >= datetime.timedelta(
                        days=15
                    ):
                        send_email(item["mail"], student_name)
        except Exception as e:
            print("error oucur", e)


library1 = Library_inventry(totalbooks, borrowbooks, avalable_inventry)
library1_record = Library_record(avalable_inventry, library_record)

while True:
    print("########## Welcome to library management app ##########")
    print(
        """
                    Choose an option for any operation

                    1. Manage library inventory
                    2. Student record section
                    3. Exit app
          """
    )
    while True:
        try:
            user_choice = int(input("Enter a number 1, 2, 3: "))
            break
        except:
            print("envalid choice, please enter number only")
    if user_choice == 1:
        while True:
            print("########## Welcome to library inventory ##########")
            print(
                """
                            Choose an option for any operation

                            1. Check book status
                            2. Add books to inventory
                            3. Remove book from inventory
                            4. View inventory books list
                            5. Back to home manu
                """
            )
            while True:
                try:
                    choice = int(input("choose an operation: "))
                    break
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
            print(
                """
                            Choose an option for any operation

                            1. View student record
                            2. Borrow book
                            3. View available books
                            4. Donate book
                            5. Return book
                            6. Send alert 
                            7. Back to home manu
            """
            )
            while True:
                try:
                    choice2 = int(input("choose an operation: "))
                    break
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
