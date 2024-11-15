from decimal import Decimal
import re
import os
import psycopg2
from dotenv import dotenv_values

PRINT_WIDTH = 12

# Connect to PostgreSQL
config = dotenv_values(".env")
conn = psycopg2.connect(database=config['DBNAME'], user=config['USER'], password=config['PASSWORD'], host=config["HOST"])
cur = conn.cursor()

# Get the answer key
key = {}
with open("key.txt", "r") as f:
    lines = f.readlines()
lines = " ".join(list(map(lambda x: x.strip(), lines)))
queries = re.split("\s*#+QUERY[1-5]#+\s+", lines)[1:]

count = 1
for q in queries:
    cur.execute(q)
    columns = ["Correct?"] + [column.name for column in cur.description]
    key[f"Query_{count}"] =  {
        "columns": columns,
        "rows": [record for record in cur],
    }
    count += 1

os.makedirs("results")

# Check Student Answers
for submission in os.scandir("submissions"):
    print(submission.path)
    with open(submission.path, "r") as f:
        lines = f.readlines()
        
    lines = " ".join(list(map(lambda x: x.strip(), lines)))
    queries = re.split("\s*#+QUERY[1-5]#+\s+", lines)
    name, queries = queries[0], queries[1:]

    with open(submission.path.replace("submissions", "results"), "w") as f:
            f.write(name)

    count = 1
    for q in queries:
        expected = key[f"Query_{count}"]
        
        cur.execute(q)

        header = ""
        for col in expected["columns"]:   
            header += f"|{col:>{PRINT_WIDTH}}"
        header += "\n"

        i = 0
        rows = []
        for record in cur:
            correct = f"|{chr(10003):>{PRINT_WIDTH}}"
            row = f"|{1:>{PRINT_WIDTH}}"
            if len(record) != len(expected["rows"][i]):
                header = ["Incorrect number of columns in output\n"]
                break
            for j in range(len(expected["rows"][i])):
                if record[j] != expected["rows"][i][j]:
                    correct = f"|{'X':>{PRINT_WIDTH}}"
                val = record[j]
                if isinstance(record[j], Decimal):
                    val = round(record[j], 2)
                row += f"|{str(val):>{PRINT_WIDTH}}"
            i += 1
            rows += [correct + row + "\n"]

        with open(submission.path.replace("submissions", "results"), "a") as f:
            f.write(f"Query_{count}\n")
            f.writelines(header)
            f.writelines(rows)
        count += 1
    

cur.close()
conn.close()   