# CS 561 SQL Homework Auto-grader

## Setup

### PostgreAdmin

Ensure that PostgreAdmin is installed on your device and can be accessed through an account.

### Pip

You will need to install two modules, psycopg2 and dotenv, to use this auto-grader. A [requirements.txt](/requirements.txt) file has been included to allow for easy installation using pip.

In the terminal, on your system default or in a virutal environment, execute `pip install -r requirements.txt` to install the needed modules.

### .env

This auto-grader uses the dotenv module to load data from a .env file. This file must contain login information for PostgreAdmin. 4 variables need to be included: USER, PASSWORD, DBNAME, and HOST. An example is shown below.

```
    USER=postgres
    PASSWORD=pgadmin
    DBNAME=CS561
    HOST=localhost
```

### Submissions

Gather the student submissions from canvas by going onto the assignment page and clicking the "Download Submissions" button. This will save a zip file to your computer. Extract the files into a folder named "submissions" and place that folder in the directory with [main.py](/main.py).

Each submission must be in the format shown in [SUBMISSION_TEMPLATE.txt](/SUBMISSION_TEMPLATE.txt) in order for the regex to read each query.

## Usage

### Execution

Run the script in [main.py](/main.py) through the command line or through any other means.

### Output

#### Terminal

Multiple status updates will be printed to the terminal indicating the progress made by the auto-grader. When a student submission is graded, the name from their submission will be printed to the screen in one of three colors, indicating their results.

Green -> The student's queries match exactly to the key

Yellow -> The student's queries have mistakes that may or may not result in a deduction of points

Red -> The student's queries have mistakes that should result in a deduction of points

#### /results

Each submission will have a result file created for it. The file will have the same name as the submission, and will be found inside the results folder that is created during the auto-grader's execution.

Each result file will include the student's name at the top, and a section for each query. Each query will have a "Columns" and "Rows" section, where messages about their results will be printed. If an expected query is not exactly the result query, then both will be printed in a table format to allow for easy grading.

The intention of the results folder is to provide automatic commenting of student assignments so that they can be attached to their submissions when grades are posted.