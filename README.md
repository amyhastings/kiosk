# kiosk

### Purpose of the website
This Kiosk web application comprises my project for Module 4: Databases of UCD's 24-03 Full-Stack Software Development Course. The objective of the project is as follows:

> Integrate PostgreSQL Database with Flask: To take your web development to the next level, you will integrate a PostgreSQL database with Flask. This integration will allow you to store and manage data related to your web application efficiently. You can utilize the database to store project information, user messages, contact details, or any other relevant data. You will also incorporate modern HTML, CSS, and JavaScript to create an engaging and visually appealing user experience. The web application can be tailored to your interests and needs, providing you the flexibility to showcase your projects, skills, or any other content you desire.

I chose to prepare a 'toy' magazine subscription website. The purpose of the project is to illustrate functionality between a web application and a database having regard to the following user stories:
- As a new visitor, I want to browse the catalogue of available magazines, so that I can see what interests me before committing to a subscription.
- As a user interested in multiple topics, I want to filter magazines by categories such as fashion & lifestyle, food & drink, and science & technology, so I can quickly find magazines I might like.
- As a returning user, I want to log into my account easily, so I can manage my personal details and my subscriptions.
- As a subscriber, I want to be able to update my delivery address, so my magazines are sent to the correct location if I move.
- As a potential customer, I want to see a clear and straightforward pricing structure, so I can make an informed decision about subscribing.
- As an Ops team member, I want to be able to easily add and edit magazine categories, to make it easy for customers to find magazines that they want.
- As an Ops team member, I want to be able to easily add new magazines, to improve the offer for customers.
- As an Ops team member, I want to easily view, edit and manage all active subscriptions, so I can keep track of current subscriber counts and status.

*Please note*, however, that, due to the limited scope of the project, the Kiosk web application is not representative of all features that would need to be included in a commercial magazine. For example, Kiosk does not include a checkout for taking payment methods. Moreover, following on from a class discussion about cybersecurity, we were instructed that it was outside the scope of this project to hash passwords in the database and that so doing in real world applications could result in serious issues. With that in mind, I opted not to hash the passwords in the database, which would, of course, be unacceptable for a real application.

### Required features of the website
The text below outlines the principal requirements of the project for the website and how each requirement was satisfied.

- *Set up the Flask Environment.* I installed Flask, created a new directory for my Flask project, and intialised and activated the virtual environment.
- *Create Flask Application Files.* I created a Python file named app.py, imported the necessary Flask modules and set up the Flask application object and defined routes for different sections of the website.
- *Create HTML Files.* The project file includes more than five HTML files. Each HTML file includes a basic structure, with the head and footer sections included in the base.html template.
- *Apply CSS Styling.* The CSS stylesheet, style.css, was included in the css subdirectory in the static directory of the project’s root directory. CSS styles were applied, as required to customize typography, colours, backgrounds, margins and padding. Responsiveness of this mobile-first website is addressed using CSS media queries.
- *Implement JavaScript Interactivity.* JavaScript files, script.js, magazine_cats.js and subscribe.js, were included in the js subdirectory in the static directory of the project’s root directory. JavaScript code was included in these files to add interactivity and dynamic behaviour to the website, including event listeners related to showing / hiding the navigation menu on smaller devices, for form validation and for providing dynamic pricing information.
- *Integrate HTML, CSS, and JavaScript with Flask.* CSS and JavaScript files were integrated into the HTML files using the appropriate tags.
- *Define Flask Routes and Render HTML Files.* The Kiosk web application includes the following elements: a. Routes were defined for each section of the website in the app.py file; b. The render_template function from Flask was used to render the respective HTML files for each route; c. SQLAlchemy model classes as well as any other custom classes and data structures appropriate to manage data within the application; d. GET and POST methods were used in implementing Flask routes; e. The Flask Login Manager Extension was used as part of the project.
- *Integrate PostgreSQL Database with Flask.* As part of this project, I used a PostgreSQL database, making use of SQLAlchemy python library, to store persistent data - this was integrated into the web application with Flask.
- *Test and Run the Flask Application.* The application was extensively tested on my local to ensure that all sections and pages were displayed and functioning correctly.
- *Hosting the Web App on Render.com.* The application was deployed to Render.com and the link is provided at the top of this document. Once deployed, it was extensively tested on several by multiple users simultaneously.

### Installation
A version of the website is deployed here: https://kiosk-fdv3.onrender.com. To view this website off-line and/or make changes:
- clone the gitHub repository at https://github.com/amyhastings/kiosk;
- pip install -r requirements.txt;
- run all of the code blocks in the init_data.ipynb file;
- in the terminal, launch the application python ./app.py.

### Licensing
This web application is the copyright of Amy Hastings. The photographs used to create the magazines were sourced from https://www.pexels.com and then altered to create mock-up covers. 