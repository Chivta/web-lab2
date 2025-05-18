# Library Management Web Application

This project is a web application built with Flask (Python) for managing library resources. It allows users to browse books, add new books, edit and delete existing ones, and manage user subscriptions to books.

## Key Features

  * **Book Management:**
      * View a list of all books.
      * View detailed information for each book.
      * Add new books with title, author, publication year, and description.
      * Edit information for existing books.
      * Delete books.
      * Prevention of creating books with the same title and author.
  * **User Management:**
      * View a list of all users.
      * Add new users with username and email.
      * Edit information for existing users.
      * Delete users.
      * Prevention of creating users with the same username or email.
  * **Subscription Management:**
      * View a list of all user subscriptions to books with the date added.
      * Create new subscriptions by selecting a user and a book.
      * Prevention of creating duplicate subscriptions for the same user and book.
      * Delete subscriptions.
  * **User Interface:**
      * Intuitive web interface built using HTML and Jinja2 for data rendering.
      * Styling with CSS for improved visual appearance.
      * Confirmation of deletion actions via JavaScript alert.
      * Display of success and error messages using Flask flash messages.
      * Server-side validation of input data to ensure data integrity.

## Technologies

  * **Python:** The primary programming language.
  * **Flask:** A microframework for web development in Python.
  * **SQLAlchemy:** An ORM (Object-Relational Mapper) for database interaction.
  * **Jinja2:** A template engine for generating HTML.
  * **HTML:** Markup language for creating the structure of web pages.
  * **CSS:** Stylesheet language for designing web pages.
  * **JavaScript:** A scripting language for adding client-side interactivity (e.g., delete confirmation).

## Installation and Setup

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/Chivta/web-lab2.git
    cd web-lab2
    ```

2.  **Create a virtual environment (recommended):**

    ```bash
    python -m venv venv
    source venv/bin/activate  # For Linux/macOS
    venv\Scripts\activate  # For Windows
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure the database:**

      * Set up the database connection in your application's configuration file (e.g., `config.py` or directly in the code).
      * Create tables manually by running models (`models.py`).

5.  **Run the application:**

    ```bash
    flask --app server run --debug
    ```

6.  **Open your web browser and navigate to `http://127.0.0.1:5000/` (or the address specified by Flask).**

## Project Structure

````

web-lab2/
│
├── server/         \# Flask backend code
│   ├── **init**.py
│   ├── controllers/  \# Flask route handlers
│   │   ├── book\_controller.py
│   │   ├── user\_controller.py
│   │   └── subscription\_controller.py
│   └── models.py     \# SQLAlchemy database model definitions
│
├── client/         \# Frontend files
│   └── templates/  \# Jinja2 templates (HTML)
│       ├── base.html
│       ├── books/
│       │   ├── list.html
│       │   ├── view.html
│       │   └── form.html
│       ├── users/
│       │   ├── list.html
│       │   └── form.html
│       └── subscription/
│           ├── list.html
│           └── form.html
│
├── static/         \# Static files (CSS, JavaScript, images)
│   └── styles.css
│
├── requirements.txt  \# Python dependency list
└── README.md         \# This file
