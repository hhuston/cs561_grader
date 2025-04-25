from decimal import Decimal
import re
import os
from dotenv import dotenv_values
from postgre import pg, Table
from canvasapi import Canvas
import config


# Connect to PostgreSQL
print("Connecting to PostgreAdmin...")
pg = pg(dotenv_values(".env"))

# Connect to Canvas
print("Connecting to Canvas...")
canvas = Canvas(config.API_URL, config.API_TOKEN)
course = canvas.get_course(config.COURSE_ID)
assignment = course.get_assignment(config.ASSIGNMENT_ID)

TEST_STUDENT_ID = 86095

# Get the answer key
print("Running answer key queries...")
key : dict[Table] = {}
with open("key.txt", "r") as f:
    lines = f.readlines()
lines = " ".join(list(map(lambda x: x.strip(), lines)))
queries = re.split("\s*#+QUERY[1-5]#+\s+", lines)[1:]

print("Writing answer key in ANSWER_KEY.txt...")
with open("ANSWER_KEY.txt", "w") as f:
    for count in range(len(queries)):
        key[f"Query_{count + 1}"] =  pg.runQuery(queries[count])
        f.write(f"#####Query {count + 1}#####\n")
        f.write(pg.formatTable(key[f"Query_{count + 1}"]) + "\n")

# Check Student Answers
print("Checking Student Submissions...")
submissions = assignment.get_submissions()
for submission in submissions:
    file = submission.attachments[0]
    lines = file.get_contents()
    queries = re.split("\s*#+QUERY[1-5]#+\s+", lines)
    header, queries = queries[0], queries[1:]
    header = [line.strip() for line in header.split("\n")]
    name = header[0]

    f = open("autograder_generated_comments.txt", "w", encoding="utf-8")
    f.writelines(header + ["\n"])

    # Run the student queries
    for count in range(len(queries)):
        printTables = False
        f.write(f"#####Query {count + 1}#####\n")

        banned_keyword_found = False
        for keyword in config.BANNED_SQL_KEYWORDS:
            if keyword.lower() in queries[count].lower():
                f.write(f"X: Banned keyword found - {keyword}\n")
                banned_keyword_found = True
        if banned_keyword_found:
            f.write("\n")
            continue
        
        expected : Table = key[f"Query_{count + 1}"]
        try:
            result : Table = pg.runQuery(queries[count])
        except Exception as e:
            f.write(f"X: SQL Error - {str(e).strip()}\n")
            pg.rollback()
            continue

        # Checking column headers
        colStr = ""
        colDiff = len(result["columns"]) - len(expected["columns"])
        if colDiff < 0:
            colStr += f"X: Missing {abs(colDiff)} column{'s' if abs(colDiff) > 1 else ''}\n"
            printTables = True
        elif colDiff > 0:
            colStr += f"X: {colDiff} extra column{'s' if colDiff > 1 else ''}\n"
            printTables = True
        else:
            colStr += f"{chr(10003)}: Correct number of columns\n"
            temp = f"{chr(10003)}: Correct column headers\n"
            for col in result["columns"]:
                # Gives leeway so that if extra headers were included
                # it will not be counted as an incorrect header
                if col not in expected["columns"] and colDiff < 1:
                    temp = "X: Incorrect column header(s)\n"
                    printTables = True
                    break
                elif col not in expected["columns"]:
                    colDiff -= 1
            colStr += temp
        f.write(f"Columns:\n{colStr}\n")
        
        # Checking rows
        rRows = result["rows"]
        eRows = expected["rows"]
        rowStr = ""

        rowDiff = len(rRows) - len(eRows)
        if rowDiff < 0:
            rowStr += f"X: Missing {abs(rowDiff)} row{'s' if abs(rowDiff) > 1 else ''}\n"
            errorLevel = 2
            printTables = True
        elif rowDiff > 0:
            rowStr += f"X: {rowDiff} extra row{'s' if rowDiff > 1 else ''}\n"
            errorLevel = 2
            printTables = True
        else:
            rowStr += f"{chr(10003)}: Correct number of rows\n"
            for index, eRow in enumerate(eRows):
                for col in expected["columns"]:
                    if eRow[col] != rRows[index][col]:
                        rowStr += "X: Incorrect values\n"
                        printTables = True
                        break
                    # if rRows[i] in eRows[i]:
                    #     rowStr += "X: Incorrect order\n" if "X: Incorrect order\n" not in rowStr else ""
                    #     errorLevel = 2
                    #     printTables = True
                    # else:
                    rowStr += "X: Incorrect values\n"
                    errorLevel = 2
                    printTables = True
                    break
        rowStr += f"{chr(10003)}: All rows correct" + "\n" if rowStr == "" else ""
        f.write(f"Rows:\n{rowStr}\n")
        if printTables:
            f.write("Result\n" + pg.formatTable(result) + "\n")

    f.close()
    
pg.disconnect()
os.remove("autograder_generated_comments.txt")


# test_student_submission.upload_comment(file="./api_test_comment")
# test_student_submission.edit(submission={"posted_grade": 100})