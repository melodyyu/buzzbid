# BuzzBid Application

## Overview

This repository contains the source code for the BuzzBid application, which is developed for Phase 3 of our project. The application includes features such as user login, main menu navigation, and user registration. 

## Package Structure

- **app.py**: This file serves as the main entry point for launching the server. You can start the application by running `python3 app.py` in the terminal.

- **Database/**: This directory contains database connection and query execution functions. These functions are responsible for interacting with the database to perform CRUD (Create, Read, Update, Delete) operations.

- **GUI/**: The GUI directory holds the primary functional components of the application. It currently includes `login_window.py`, which implements the login functionality. Additional files such as `report.py` and `item.py` may be added in the future to extend the application's features.

- **Services/**: This directory contains a collection of authentication service functions. These functions handle user authentication, registration, and other related tasks.

- **media/**: This directory stores images or icons used in the application's user interface.


## Setting up Database Credentials

To securely store your database credentials and avoid hardcoding them into the code, we utilize environment variables. Follow these steps to set up your own `.env` file:

1. Create a new file named `.env` in the root directory of the project if it doesn't already exist.

2. Add the following lines to your `.env` file, replacing the placeholder values with your actual database credentials:

    ```plaintext
    DB_NAME=your_database_name
    DB_USER=your_database_user
    DB_PASSWORD=your_database_password
    DB_HOST=your_database_host
    ```

3. Save the `.env` file.

Once you've set up your `.env` file with your database credentials, you can load them into your code using the `python-dotenv` library. Ensure you have the library installed by running:


## Getting Started

To run the BuzzBid application locally, follow these steps:

1. Clone this repository to your local machine.
2. Navigate to the project directory.
4. Create a virtual environment by running:
    ```bash
    python3 -m venv venv
    ```
4. Activate the virtual environment:
    - On macOS/Linux:
        ```bash
        source venv/bin/activate
        ```
    - On Windows:
        ```bash
        .\venv\Scripts\activate
        ```
5. Install the required dependencies by running:
    ```bash
    pip install -r requirements.txt
    ```
6. Run the application:
    ```bash
    python3 app.py
    ```

