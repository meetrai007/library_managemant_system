import smtplib
from email.message import EmailMessage
import datetime
import json

try:
    with open("library_record.json","r") as file:
        library_recoard=json.load(file)
        books=library_recoard["books"]
        issue_record=library_recoard["issue_record"]
except:
        library_recoard={}
        books=[]
        issue_record=[]

time=datetime.datetime.now().strftime("%x")

class Library():
    def __init__(self,books):
        self.books=books
        library_recoard["books"]=books
        with open("library_record.json","w") as file:
            json.dump(library_recoard,file)

    def borrowbook(self,book,name,date):
        if book in books:
            issue_record.append({date:{"name":name,"book":book}})
            self.books.remove(book)
        else:
             print("book not avalible in library")
                
    def donatebook(self,book):
        if book not in books:
            self.books.append(book)
        else:
             print("book not avalible in library")
         
Library.donatebook("meet",)