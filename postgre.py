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
        rows = [record for record in self.curr]
        return {
            "columns": [column.name.upper() for column in self.curr.description],
            "rows": rows,
        }
    
    def rollback(self) -> None:
        self.curr.execute("ROLLBACK")
        self.conn.commit()

    def formatTable(self, table: Table) -> str:
        max_width = 0
        for col in table["columns"]:
            max_width = max(max_width, len(col))

        for row in table["rows"]:
            for val in row:
                if isinstance(val, Decimal):
                    val = round(val, 2)
                max_width = max(max_width, len(str(val)) + 1)

        PRINT_WIDTH = max_width

        tableLength = len(table["columns"])
        tableStr = ""
        for col in table["columns"]:
            tableStr += f"|{col:>{PRINT_WIDTH}}"
        tableStr += f"|\n{'=' * ((PRINT_WIDTH + 1) * tableLength)}\n"

        for row in table["rows"]:
            for val in row:
                if isinstance(val, Decimal):
                    val = round(val, 2)
                tableStr += f"|{str(val):>{PRINT_WIDTH}}"
            tableStr += f"|\n-{'-' * ((PRINT_WIDTH + 1) * tableLength)}\n"

        return tableStr    