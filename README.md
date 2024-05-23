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
Phase 3 was where we brought our database to life by coding the UI and implementing the database to create a fully functional product. Each team member was randomly assigned speicfic components to develop. For their assigned parts, they were responsible for writing the SQL queries, creating the GUI, and ensuring seamless integration with the existing pages and database. We presented our application through a live presentation and received 98.5/100. 

**I worked specifically on the Search window, the subsequent Search Results page, the Auction Results page and the summarized User Reports.** For the Search and Auction Results pages, I also implemented pagination to provide a cleaner look, with each page displaying only the top 20 results. Additionally, I overlaid a label on each result so that once clicked, the user was sent to the respective item page. 

## Setup: 
To run the program, refer to the instructions provided in the README in Phase 3. The application requires first, that psycopg3 runs on your local machine. Additionally, an existing PostgreSQL database must have already been created, though it can be populated with with the files in the Demo Data folder. 
