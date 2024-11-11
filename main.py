import re
import os
import psycopg2
import tabulate
from dotenv import dotenv_values

RED   = "\033[1;31m"  
BLUE  = "\033[1;34m"
CYAN  = "\033[1;36m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"
BOLD    = "\033[;1m"
REVERSE = "\033[;7m"

# Connect to PostgreSQL
config = dotenv_values(".env")
conn = psycopg2.connect(f"dbname={config['DBNAME']} user={config['USER']} password={config['PASSWORD']}"
)
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
        key[f"Query_{count}"] =  {
            "columns": [column.name for column in cur.description],
            "result": [record for record in cur],
            "print_width": len(max([column.name for column in cur.description], key=lambda col: len(col) + 3))
        }
        print( key[f"Query_{count}"]["print_width"])

        for col in key[f"Query_{count}"]["columns"]:
            print("\t", col, end="\t| ")
        print()

        count += 1

exit()

# Check Student Answers
for submission in os.scandir("submissions"):
    print(submission.path)
    with open(submission.path, "r") as f:
        lines = f.readlines()
        lines = " ".join(list(map(lambda x: x.strip(), lines)))
        queries = re.split("\s*#+QUERY[1-5]#+\s+", lines)[1:]

        count = 1
        for q in queries:
            expected = key[f"Query_{count}"]
            cur.execute(q)

            i = 0
            for record in cur:
                if record != expected[i]:
                    print(f"Failed Query {count}")
                    break
                i += 1
            
            count += 1

cur.close()
conn.close()   