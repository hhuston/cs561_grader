from decimal import Decimal
import re
import os
from dotenv import dotenv_values
from postgre import pg, Table

RED    = "\033[31m"  
YELLOW = "\033[33m"
GREEN  = "\033[32m"
RESET  = "\033[0m"

# Connect to PostgreSQL
print("Connecting to PostgreAdmin...")
pg = pg(dotenv_values(".env"))

# Get the answer key
print("Running answer key queries...")
key : dict[Table] = {}
with open("key.txt", "r") as f:
    lines = f.readlines()
lines = " ".join(list(map(lambda x: x.strip(), lines)))
queries = re.split("\s*#+QUERY[1-5]#+\s+", lines)[1:]

for count in range(len(queries)):
    key[f"Query_{count + 1}"] =  pg.runQuery(queries[count])

# Create / Clear results dir
print("Preparing results directory...")
try:
    os.mkdir("results")
except FileExistsError:
    for file in os.scandir("results"):
        os.remove(file.path)

errorTracker = [0, 0, 0]
# Check Student Answers
print("Checking Student Submissions...")
submissions = os.scandir("submissions")
for submission in submissions:
    with open(submission.path, "r") as f:
        lines = f.readlines()
    lines = "\n".join(list(map(lambda x: x.strip(), lines)))
    queries = re.split("\s*#+QUERY[1-5]#+\s+", lines)
    name, queries = queries[0], queries[1:]

    f = open(submission.path.replace("submissions", "results"), "w", encoding="utf-8")
    f.write(name + "\n")

        
    # Integer to represent the level of mistakes in the query
    # 0 -> No errors
    # 1 -> Potential issues, but could be full credit (i.e. incorrect column names)
    # 2 -> Indisbutible mistakes in the query output
    errorLevel = 0

    # Run the student queries
    for count in range(len(queries)):
        printTables = False
        f.write(f"#####Query {count + 1}#####\n")
        
        expected : Table = key[f"Query_{count + 1}"]
        try:
            result : Table = pg.runQuery(queries[count])
        except Exception as e:
            f.write(f"SQL Error: {str(e).strip()}\n")
            errorLevel = 2
            pg.rollback()
            continue

        # Checking column headers
        colStr = ""
        if len(result["columns"]) < len(expected["columns"]):
            colStr += "X: Missing columns\n"
            errorLevel = 2
            printTables = True
        if len(result["columns"]) > len(expected["columns"]):
            colStr += "X: Extra columns\n"
            errorLevel = 2
            printTables = True
        else:
            for col in result["columns"]:
                if col not in expected["columns"]:
                    colStr += "X: Incorrect column header(s) - Manual Checking Required\n"
                    errorLevel = 1 if errorLevel <= 1 else errorLevel
                    printTables = True
                    break
        colStr += f"{chr(10003)}: Correct column headers" + "\n" if colStr == "" else ""
        f.write(f"Columns:\n{colStr}\n")
        
        # Checking rows
        rRows = result["rows"]
        eRows = expected["rows"]

        rowStr = ""
        if len(rRows) < len(eRows):
            rowStr += "X: Missing rows\n"
            errorLevel = 2
        if len(rRows) > len(eRows):
            rowStr += "X: Extra rows\n"
            errorLevel = 2
        else:
            for i in range(len(rRows)):
                if rRows[i] != eRows[i]:
                    if rRows[i] in eRows[i]:
                        rowStr += "X: Incorrect order\n" if "X: Incorrect order\n" not in rowStr else ""
                        errorLevel = 2
                        printTables = True
                    else:
                        rowStr += "X: Incorrect values\n"
                        errorLevel = 2
                        printTables = True
                        break
        rowStr += f"{chr(10003)}: Correct rows" + "\n" if rowStr == "" else ""
        f.write(f"Rows:\n{rowStr}\n")
        if printTables:
            f.write("Expected\n" + pg.formatTable(expected) + "\n")
            f.write("Result\n" + pg.formatTable(result) + "\n")
    
    colors = [GREEN, YELLOW, RED]
    print(f"{colors[errorLevel]}{name}{RESET}")
    errorTracker[errorLevel] += 1

    f.close()
    
print("\nSummary:")
print(f"{GREEN}{errorTracker[0]} students have correct queries{RESET}")
print(f"{YELLOW}{errorTracker[1]} students need further review{RESET}")
print(f"{RED}{errorTracker[2]} students have incorrect queries{RESET}")
submissions.close()
pg.disconnect()