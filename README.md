# TO-DO List
#### Video Demo: <URL https://youtu.be/NwBoFP5n8O8>
#### Description:
##### What my project is:
My final project is a TO-DO List which aims to improve users' procrastination due to short video addiction.
For users:
- Log in for logging in to their account, On this page, they are required to write the username and password.
- register for registering a new account, In this page, they are required to create a new username, password and confirmation of password
- append for appending the TO-DO List, I should decide the task name and its due date.
- change for changing the date of one of the tasks. On this page, users are required to write down the task they want to change its date and the new date.
- erase for erasing one of the tasks that had been appended to the TO-DO List
- destroy for destroying the entire TO-DO List, which is unable to be recovered.
The main page is for displaying users' TO-DO Lists with an indication of name, due date and remaining days. In addition, I have also displayed the number of tasks to remind users to better manage their time

##### What Each file is:
- app.py is a program connecting all programs(HTML Programs) using Flask. In this program, I have imported a variety of libraries to facilitate my total web application development process.

- helpers.py stores some of the Python functions(apology to remind users and login_required for login), which Python-based allows me to use the mastered language Python with good functions.
- static is for some documents such as photos(such as some gif ) to be stored in this folder for arrangement
- templates is for storing HTML templates ( I have built 9 templates for the program, four are different web section( append, change, erase, destroy) 1 is for the entire layout and 1 is for apology)

##### Design:
I have chosen a web design with simplicity
- white
- In append, beside task name and due to date, there isn't any other requirement for users to input
- 3 RGB colors which give users a comfortable User Interface
- Also, I haven't required the user to provide any additional information to make their mind complicated
Moreover, I decided to use Bootstrap for many UI designs to save time to optimise users' experience.

##### Improvement:
- Maybe change the colour of each page as they are now different and I would like to make a better colour combination.
- Connect to the real browser to truly share my TO-DO List with others who are interested in my explicit user-friendly TO-DO List.
- Adding more display instead of due to date and remaining days, perhaps adding the rate of necessity in there
- check for more information as in the world there are many dishonest programmers or hacker who may find a way to steal the data even though I have installed the lock
- Appending the column of the database table "lists"
- Using my recently learned machine learning to find some important information

