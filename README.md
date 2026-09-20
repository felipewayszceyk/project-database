# project-database
Felipe Wayszceyk – Assessment Module 4
Description: I’m using as base the website I built for module 2, Python. The website site it’s kind of a travel blog. My idea was incrementing pages as I could use to sell consultancy and services for people who are thinking to move to Ireland. Where the users can add, delete and edit and consulting clients.

Website : https://felipe-abroaddatabase.onrender.com
My repository : https://github.com/felipewayszceyk/project-database

Features
Register, list, edit and delete clients 						      
Register, list, edit and delete bookings (client + service + date)                                             
Each client is linked to a move type (Student, Work Visa, etc.)                                                
Data stored in a hosted PostgreSQL database

Tech Stack
Python, Flask, SQLAlchemy, PostgreSQL, HTML, CSS, Render

ERD
The database has five tables:
move_types : the routes to move to Ireland (Student, Work Visa, ...)
clients: people who hire the consultancy. Each client has one move type and service.
services: what the consultancy offers, with price and duration
bookings: a client booking a service at a date and time. A client can have many bookings as some consultancy are in more than one day
payments: payments for a booking or service(didn’t complete this part)

Relationships: One move_type has many clients, one client has many bookings, one service has many bookings, and one booking has many payments.

Run local
Clone the repository and create a virtual environment
pip install -r requirements.txt
Create a PostgreSQL database and run database/schema.sql
Create a .env file with DATABASE_URL=postgresql://USER:PASSWORD@localhost:5432/DATABASE_NAME
Terminal command: python app.py
Open on browser http://127.0.0.1:5000

Deployment no render
I created a database on Render and run database/schema.sql with pgAdmin.
Created a web service to connect with my Github repository.
Add the environment variable  database_URL with the internal database URL of the render database
Deployed it
So after each git push it redeploy automatically

Building
For build this website I used a lot of extras links the teacher showed us. It was very challenging work with database in this real website. I was making a lot of mistake like wrong typing, the spaces in the code. I avoid to use AI tools but few times they help me in this kind small stuffs that I couldn’t figure out. For example, the 4 and 8 spaces for starting some lines. I used a few youtube vídeos  that was very helpful mostly to make the routes and link with the form and html. But many codes were very similar but to easy the build wrong. 

Felipe Wayszceyk
