import smtplib
import datetime
import json
import re
import logging

# Regular expressions for input validation
name_pattern = r"^[a-z 0-9 ]+$"
bookname_pattern = r"^[A-Za-z0-9\s]+$"
email_pattern = r"\b[a-z][A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"

# Load books data from JSON files
try:
    with open("library_inventory.json", "r") as file:
        total_books = json.load(file)
except FileNotFoundError:
    total_books = {}

try:
    with open("borrow_books.json", "r") as file:
        borrowed_books = json.load(file)
except FileNotFoundError:
    borrowed_books = {}

try:
    with open("library_record.json", "r") as file:
        library_record = json.load(file)
except FileNotFoundError:
    library_record = {}

# Calculate available inventory
available_inventory = total_books.copy()
for book_name in borrowed_books.keys():
    available_inventory[book_name] = total_books[book_name] - borrowed_books[book_name]

today_date = datetime.date.today()

# Function to save data to JSON file
def save_to_json(filename, data):
    """Saves data to a JSON file."""
    with open(filename, "w") as file:
        json.dump(data, file)

# Function to send email alert
def send_email(student_email, name):
    """Sends an email alert to the student."""
    try:
        sender_email = "deeprai22016@outlook.com"
        password = "cfjbvbvwxpeazqwp"
        receiver_email = student_email
        subject = "Subject: Library Alert\n"
        body = f"Dear {name},\n\nYou have held a book for more than 15 days. Please return it.\n"
        message = subject + body

        server = smtplib.SMTP("smtp-mail.outlook.com", 587)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
        server.quit()
        print("Email sent successfully.")
    except Exception as e:
        logging.error("Failed to send email", exc_info=True)

class LibraryInventory:
    """Manages library inventory."""
    def __init__(self, total_books, borrowed_books, available_inventory):
        self.total_books = total_books
        self.borrowed_books = borrowed_books
        self.available_books = available_inventory

    def list_inventory(self):
        """Lists all books in the inventory."""
        for book, quantity in self.total_books.items():
            print(f"Book: {book}, Quantity: {quantity}")

    def check_book_status(self):
        """Checks if a book is available in the inventory."""
        book_name = input("Enter book name to check: ")
        if re.match(bookname_pattern, book_name):
            if book_name in self.total_books and self.total_books[book_name] > 0:
                print("Book is available to borrow.")
            else:
                print("Book is not available.")
        else:
            print("Invalid book name format.")

    def add_book(self):
        """Adds a new book to the inventory."""
        book_name = input("Enter book name to add: ")
        if re.match(bookname_pattern, book_name):
            try:
                quantity = int(input("Enter quantity: "))
                self.total_books[book_name] = self.total_books.get(book_name, 0) + quantity
                save_to_json("library_inventory.json", self.total_books)
                print("Book added successfully.")
            except ValueError:
                print("Quantity must be a number.")
        else:
            print("Invalid book name format.")

    def remove_book(self):
        """Removes a book from the inventory."""
        book_name = input("Enter book name to remove: ")
        if re.match(bookname_pattern, book_name):
            if book_name in self.total_books:
                del self.total_books[book_name]
                save_to_json("library_inventory.json", self.total_books)
                print("Book removed successfully.")
            else:
                print("Book not found in inventory.")
        else:
            print("Invalid book name format.")

    def borrow_book(self, book_name):
        """Borrows a book from the inventory."""
        if self.available_books.get(book_name, 0) > 0:
            self.borrowed_books[book_name] = self.borrowed_books.get(book_name, 0) + 1
            save_to_json("borrow_books.json", self.borrowed_books)
            print("Book borrowed successfully.")
        else:
            print("Book not available for borrowing.")

    def return_book(self, book_name):
        """Returns a book to the inventory."""
        if self.borrowed_books.get(book_name, 0) > 0:
            self.borrowed_books[book_name] -= 1
            save_to_json("borrow_books.json", self.borrowed_books)
            print("Book returned successfully.")
        else:
            print("No record of borrowed book found.")

    def donate_book(self, book_name, quantity):
        """Allows students to donate books."""
        self.total_books[book_name] = self.total_books.get(book_name, 0) + quantity
        save_to_json("library_inventory.json", self.total_books)
        print("Thank you for your donation!")

class LibraryRecord:
    """Manages student records."""
    def __init__(self, available_books, library_record):
        self.available_books = available_books
        self.library_record = library_record

    def borrow_book(self):
        """Records a book borrowing event."""
        student_name = input("Enter student name: ")
        if re.match(name_pattern, student_name):
            book_name = input("Enter book name: ")
            if re.match(bookname_pattern, book_name):
                student_email = input("Enter email: ")
                if re.match(email_pattern, student_email):
                    if book_name in self.available_books and self.available_books[book_name] > 0:
                        self.library_record.setdefault(student_name, []).append(
                            {"date": str(today_date), "book_name": book_name, "email": student_email}
                        )
                        save_to_json("library_record.json", self.library_record)
                        library_inventory.borrow_book(book_name)
                    else:
                        print("Book not available.")
                else:
                    print("Invalid email format.")
            else:
                print("Invalid book name format.")
        else:
            print("Invalid student name format.")

    def return_book(self):
        """Records a book return event."""
        student_name = input("Enter student name: ")
        if re.match(name_pattern, student_name):
            book_name = input("Enter book name: ")
            if re.match(bookname_pattern, book_name):
                if student_name in self.library_record:
                    for record in self.library_record[student_name]:
                        if record["book_name"] == book_name:
                            self.library_record[student_name].remove(record)
                            library_inventory.return_book(book_name)
                            save_to_json("library_record.json", self.library_record)
                            print("Book returned successfully.")
                            break
                    else:
                        print("Record not found.")
                else:
                    print("Student not found in records.")
            else:
                print("Invalid book name format.")
        else:
            print("Invalid student name format.")

    def view_records(self):
        """Displays student borrowing records."""
        for student, records in self.library_record.items():
            print(f"Student: {student}")
            for record in records:
                print(f"Date: {record['date']}, Book: {record['book_name']}")

    def send_alerts(self):
        """Sends email alerts for overdue books."""
        for student_name, records in self.library_record.items():
            for record in records:
                borrowed_date = datetime.datetime.strptime(record['date'], "%Y-%m-%d").date()
                if today_date - borrowed_date > datetime.timedelta(days=15):
                    send_email(record['email'], student_name)

# Create instances of the classes
library_inventory = LibraryInventory(total_books, borrowed_books, available_inventory)
library_record_manager = LibraryRecord(available_inventory, library_record)

# Main application loop
while True:
    print("\nWelcome to Library Management System")
    print("1. Manage Library Inventory")
    print("2. Manage Student Records")
    print("3. Exit")
    choice = input("Enter your choice: ")
    
    if choice == "1":
        while True:
            print("\nLibrary Inventory Management")
            print("1. List Inventory")
            print("2. Check Book Status")
            print("3. Add Book")
            print("4. Remove Book")
            print("5. Back to Main Menu")
            sub_choice = input("Enter your choice: ")
            
            if sub_choice == "1":
                library_inventory.list_inventory()
            elif sub_choice == "2":
                library_inventory.check_book_status()
            elif sub_choice == "3":
                library_inventory.add_book()
            elif sub_choice == "4":
                library_inventory.remove_book()
            elif sub_choice == "5":
                break
            else:
                print("Invalid choice. Please try again.")

    elif choice == "2":
        while True:
            print("\nStudent Records Management")
            print("1. Borrow Book")
            print("2. Return Book")
            print("3. View Records")
            print("4. Send Alerts")
            print("5. Back to Main Menu")
            sub_choice = input("Enter your choice: ")
            
            if sub_choice == "1":
                library_record_manager.borrow_book()
            elif sub_choice == "2":
                library_record_manager.return_book()
            elif sub_choice == "3":
                library_record_manager.view_records()
            elif sub_choice == "4":
                library_record_manager.send_alerts()
            elif sub_choice == "5":
                break
            else:
                print("Invalid choice. Please try again.")

    elif choice == "3":
        print("Exiting the system. Goodbye!")
        break
    else:
        print("Invalid choice. Please try again.")
