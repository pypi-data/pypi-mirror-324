from collections.abc import Sequence
from typing import Union
from rich.table import Column, Table
from rich.text import Text
from rich.console import Console
from json import dumps

def _plain(text: Union[Text, str]) -> str:
    return text.plain if isinstance(text, Text) else text

def display_table(
    columns: Sequence[Union[Column, str]],
    rows: Sequence[Sequence[Union[Text, str]]],
    json: bool = False,
    title: str = "",
):
    def col_to_str(col: Union[Column, str]) -> str:
        return str(col.header) if isinstance(col, Column) else col

    console = Console()
    if json:
        json_data = [{col_to_str(col): _plain(row[i]) for i, col in enumerate(columns)} for row in rows]
        console.print_json(dumps(json_data))
    else:
        table = Table(*columns, title=title)
        for row in rows:
            table.add_row(*row)
        console.print(table)