
# BookSwap — Student Book Exchange

## Student Details
- Name: Mayur Chandrakiran Patil
- Roll Number: MCA-46
- Case Study: BookSwap

## Technology Stack
- Python
- Flask
- SQLite
- HTML, CSS, Bootstrap 5.3.3
- Jinja Templates

## Features
- Add book listings with server-side validation
- View books as responsive cards
- Search books by title or subject
- Filter by semester, condition, and status
- Mark available books as sold
- Dashboard for available books, sold books, and average selling price
- Automatic discount calculation
- SQLite database with sample records

## Setup Instructions
1. Install Python.
2. Clone or download this repository.
3. Create a virtual environment:
   `python -m venv venv`
4. Activate it in Windows PowerShell:
   `.\venv\Scripts\Activate.ps1`
5. Install dependencies:
   `pip install -r requirements.txt`
6. Initialize the database:
   `python database.py`
7. Run the application:
   `python app.py`
8. Open `http://127.0.0.1:5000` in your browser.

## Database
The `schema.sql` file contains the table creation statement and seed records.
