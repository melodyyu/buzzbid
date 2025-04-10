# Buzzbid
## Overview
This project took place during the Spring 2024 semester (January-April 2024), as the primary assignment for Georgia Tech's CS6400 Database System Concepts and Design course. As part of a team of five, I collaborated with my classmates to create a fully-featured relational database management system (DBMS) using PostgreSQL. The project specifications are detailed in Buzzbid.pdf. 

The following sections will discuss the deliverables required for each phase and the scores our team received. Phases 1 and 2 focused on database system design, while Phase 3 involved implementing a database and connecting it to our program with PostgreSQL. 

**Technologies and Libraries Used**: 
- Python 
- PostgreSQL
- DBeaver
- psycopg2 
- Customtkinter and Tkinter 
- Regex 

### Phase 1 
The crux of this phase focused on the Enhanced-Entity Relationship (EER) diagram and the project report. The deliverables for this phase were: 
- **Information Flow Diagram (IFD)** - A visual representation of how data moves between different components which in this case, represents the pages of the Buzzbid system. 
- **Enhanced Entity-Relation (EER) Diagram** - An extension of the traditional ER diagram, but includes more complex relationships and attributes (e.g, inheritance and constraints). This diagram demonstrates the entities (which later represent tables in our database) and the relations to their attributes (which will represent table columns). 
- **Project Report** 

The project report also contained the following information: data types for the database attributes, business logic constraints, task decompositions and abstract code (general psuedo-code, but also included input validation, error handling and navigation between tasks). Our team received 94.45/100.

### Phase 2 
The deliverables for this phase included:
- **EER Relational Mapping** - This converted the EER diagram from Phase 1 into a relational schema, by mapping the the relationships and constraints defined in the EER diagram to be represented in the relational database. 
- **SQL Create Table Statements** - These define the database schema and specify a table's columns, data types and constraints.
- **Abstract Code**

Phase 2 required us to make changes based on feedback received from Phase 1, which are documented in team050_p2_updatedEER.pdf.
This phase placed significant emphasis on updating the previous abstract code in our iniital report to include inline SQL queries. The requirement was to write a single query that output the complete data for the report whenever possible. The SQL_testing file was used to document the tests we ran to ensure that our SQL queries and create table statements were successful. We received 95.3/100.

### Phase 3 
Phase 3 was where we brought our database to life by coding the UI and implementing the database to create a fully functional product. Each team member was randomly assigned specific components to develop. For their assigned parts, they were responsible for writing the SQL queries, creating the GUI, and ensuring seamless integration with the existing pages and database. We presented our application through a live presentation and received 98.5/100. 

**I worked specifically on the Search window, the subsequent Search Results page, the Auction Results page and the summarized User Reports.** For the Search and Auction Results pages, I also implemented pagination to provide a cleaner look, with each page displaying only the top 20 results. Additionally, I overlaid a label on each result so that once clicked, the user was sent to the respective item page. 

## Setup: 
To run the program, refer to the instructions provided in the README in Phase 3 to set up the environment. Note: the .env file **must** be created in the phase3 team050 folder. 

The application requires first, that psycopg3 runs on your local machine. Run ```pip install psycopg2```

#### Setting up the server
Additionally, an existing PostgreSQL database must have already been created, though it can be populated with with the files in the Demo Data folder, and must run concurrently with the application. To create a PostgreSQL server, download from https://postgresapp.com/downloads.html. 

Create a server named 'buzzbid' (though the naming convention is irrelevant). Double click the postgres server, and then in the terminal run these two commands ```GRANT ALL PRIVILEGES ON DATABASE "postgres to admin;```
```GRANT and GRANT ALL ON SCHEMA public to admin;```
this command allows for the database public files to be accessed through SQL queries (alternative is that when writing a sequel query, you would have to include public.<table_name>). 


#### Setting up the database
Download DBeaver, an IDE for databases (https://dbeaver.io/download/). Right click the 'postgres' server and go to 'Edit Connections' and (1) change the database to 'postgres' or whatever your server where you ran the commands above is named. Then, change the username and password to the same credentials as are in the .env file. Test the connection to ensure it's owrking.

Only after this pre-work is done, can you then load the application. To do that, follow the instructions in the Phase 3 README. 

## Things I'd Change Retrospectively: 
My desired changes all have to do with how we implemented in Phase 3. Namely: 
- Rename the files to be more explanatory
- Split the login.py file so that it no longer contains the code for all the UI, but rather, one file for each function
- Update the UI for the parts I wasn't in charge of, to make the overall look more cohesive
- Refactor the code so that it's either more OOP and efficient
- Potentially scale the application so that multiple users could access the database at once (make it cloud-based perhaps)
- Add security measures 

## Reflections
I truly learned a lot from this project. I ended up getting a solid grasp on databases (as well as getting an A in the class), but to do so, I had to teach myself SQL and fight to make tkinter's UI look great. Thanks to that, I now have a solid grasp of both SQL and tkinter. I also used DBeaver for the first time, which was super helpful for visualizing databases (I had used PostgreSQL's main program to do so before, it was not pretty) and gained a better understanding of how Git commands, resolving merge conflicts and the branching system works (fun fact: I ended with over 25 test branches!). I spent a tiresome amount of time of debugging, but due to that I now know how to walk through python's checkpoint() and VSCode's built in debugger. 
