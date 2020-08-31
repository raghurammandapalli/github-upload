Dependencies:
1. You need to install Python 3 and MySQL.


2. The tkinter, pymysql, numpy and pandas libraries of python needs to be installed. This can be done by running following commands from command line:


pip install tkinter (or) pip3 install tkinter
pip install pymysql (or) pip3 install pymysql  
pip install numpy (or) pip3 install numpy
pip install pandas (or) pip3 install pandas


Set-up:
1. Then you should run pre_processing.py file to process the CSV files and make them suitable to be mapped to tables.
Make sure that before running this, you change the file paths at lines 11,31,37,42


2. Then run the Library-database-MySQL.sql file from mysql prompt using the “source” command:   source Library-database-MySQL.sql
Make sure before running this file that for last 4 queries you replace the given file path with your own correct file path.


3. After successfully completing the above steps, change the parameters “host”, “user” , “password” of the pymysql.connect() method to your values in each .py file except pre_processing.py file.


4. Now your application is ready to launch, just run the main.py file from the terminal.