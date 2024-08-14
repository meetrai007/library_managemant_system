import smtplib
from email.message import EmailMessage
import datetime
import json

with open("library_record.json","r") as file:
    try:
        library_data=json.load(file)
    except:
        library_data={}

time=datetime.datetime.now().strftime("%x")

def issue_book():
    name=str(input("enter your nasme:"))
    book=str(input("enter book nasme:"))
    email=str(input("enter your gmail:"))
    library_data[name]={"time":time,"issued_books":book,"email":email}


def add_recoard(name,time,book,email):
    library_data[name]={"time":time,"issued_books":book,"email":email}

class Library_recoard():
    def __init__(self,name,book,email):
        self.name=name
        self.book=book
        self.email=email
        self.time=time
        add_recoard(self.name,self.time,self.book,self.email)

s1=Library_recoard("meet","the secret","meetrai101@gmail.com")
s2=Library_recoard("deep","the secret 2","harmeetsingh77216@gmail.com")
print(library_data)
