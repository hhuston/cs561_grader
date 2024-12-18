import psycopg2
from typing import TypedDict
from decimal import Decimal

class Table(TypedDict):
    """Typed Dictionary with attributes 'columns' -> list[str] and rows -> list[tuple]"""
    columns: list[str]
    rows: list[tuple]

class pg():
    global conn
    global curr

    def __init__(self, config) -> None:
        self.conn = psycopg2.connect(database=config['DBNAME'], user=config['USER'], password=config['PASSWORD'], host=config["HOST"])
        self.curr = self.conn.cursor()

    def disconnect(self) -> None:
        self.conn.close()
        self.curr.close()

    def runQuery(self, sql: str) -> Table:
        self.curr.execute(sql)
        rows = self.curr.fetchall()
        rows = [[index + 1] + list(rows[index]) for index in range(len(rows))]
        return {
            "columns": [''] + [column.name.upper() for column in self.curr.description],
            "rows": rows,
        }
    
    def rollback(self) -> None:
        self.curr.execute("ROLLBACK")
        self.conn.commit()

    def formatTable(self, table: Table) -> str:
        PADDING = 2

        numCols = len(table["columns"])
        numRows = len(table["rows"])

        max_widths = [0 for i in range(numCols)]
        max_widths[0] = len(str(numRows))

        for col in range(1, numCols):
            max_widths[col] = max(max_widths[col], len(table["columns"][col]) + PADDING)

        for row in table["rows"]:
            for col in range(1, numCols):
                val = row[col]
                if isinstance(val, Decimal):
                    val = round(val, 2)
                max_widths[col] = max(max_widths[col], len(str(val)) + PADDING)

        tableStr = ""
        for col in range(numCols):
            tableStr += f"|{table['columns'][col]:>{max_widths[col]}}"
        tableStr += f"|\n{'=' * (sum(max_widths) + numCols + 1)}\n"

        for row in table["rows"]:
            for col in range(numCols):
                val = row[col]
                if isinstance(val, Decimal):
                    val = round(val, 2)
                tableStr += f"|{str(val):>{max_widths[col]}}"
            # Swap the commented tableStr if you want lines separating each row in the output
            # tableStr += f"|\n-{'-' * ((sum(max_widths) + 1) * numCols)}\n"
            tableStr += f"|\n"

        return tableStr    