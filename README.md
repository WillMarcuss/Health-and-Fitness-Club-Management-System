COMP 3005
Project V2
Group Members:

    William Marcus
    Joshua Saikali
    JC Sevigny


[Interface Diagram](https://miro.com/app/board/uXjVKXHDFIM=/?share_link_id=498777083993)

# SETUP INSTRUCTIONS

## Prerequisites
- Python 3.x
- PostgreSQL
- psycopg2 library

#### Installation
1. Ensure you have Python 3.x installed on your system. If not, download and install it from [Python's official website](https://www.python.org/downloads/).
2. Install PostgreSQL on your system if you haven't already. You can download it from [here](https://www.postgresql.org/download/).
3. Install the psycopg2 library by running the following command:
    ```
    pip install psycopg2
    ```
## Usage
1. Clone this repository to your local machine.
2. Open the directory where you cloned this repository.
3. Make sure the PostgreSQL server is running.
4. Modify the database connection details in the ```dbController.py``` file (dbname, user, password, host, port) according to your PostgreSQL setup.
5. Run the DDL.sql and the DML.sql files to create the tables and insert sample data.
6. Run the application using the following command:
    ```
    python ./main.py
    ```

## Video Demonstration
https://youtu.be/sXb_qM6-Mqk?si=eJhrS2W7_Y-XFT7S
