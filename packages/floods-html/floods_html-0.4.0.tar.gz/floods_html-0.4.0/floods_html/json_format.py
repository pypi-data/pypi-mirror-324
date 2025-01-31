from pydantic import BaseModel, model_validator
from pydantic_core import SchemaValidator

from typing import List, Literal, Union, Optional, Dict


def check_schema(model: BaseModel) -> None:
    schema_validator = SchemaValidator(schema=model.__pydantic_core_schema__)
    schema_validator.validate_python(model.__dict__)


class FHTableEntry(BaseModel):
    value: Union[str, int, float, None]
    html_options: Dict[str, Union[Dict[str, str], str]] = {}


class FHTableRow(BaseModel):
    data: List[FHTableEntry]
    html_options: Dict[str, Union[Dict[str, str], str]] = {}


class FHTableHeader(BaseModel):
    data: List[FHTableRow] = []
    html_options: Dict[str, Union[Dict[str, str], str]] = {}


class FHTableBody(BaseModel):
    data: List[FHTableRow] = []
    html_options: Dict[str, Union[Dict[str, str], str]] = {}


class FHTable(BaseModel):
    title: str
    headers: FHTableHeader = FHTableHeader()
    rows: FHTableBody = FHTableBody()
    html_options: Dict[str, Union[Dict[str, str], str]] = {}

    @model_validator(mode="after")
    def rows_wrong_size(self):
        header_lens = self.header_len()
        row_lens = self.rows_len()
        if len(header_lens) != 0 and len(row_lens) != 0:
            for row_len in row_lens:
                for header_len in header_lens:
                    if row_len != header_len:
                        raise ValueError("Not all row lengths match header lengths.")
        return self

    def header_len(self):
        lengths = []
        for header in self.headers.data:
            length = 0
            for entry in header.data:
                col_span = 1 if entry.html_options is None else int(entry.html_options.get("colspan", 1))
                length += col_span
            lengths.append(length)
        return lengths

    def rows_len(self):
        lengths = []
        for row in self.rows.data:
            length = 0
            for entry in row.data:
                col_span = 1 if entry.html_options is None else int(entry.html_options.get("colspan", 1))
                length += col_span
            lengths.append(length)
        return lengths

    def add_row(self, row: List[FHTableEntry], html_options: Optional[Dict[str, Union[Dict[str, str], str]]] = {}):
        self.rows.data.append(FHTableRow(data=row, html_options=html_options))
        check_schema(self)

    def add_header(
        self, header: List[FHTableEntry], html_options: Optional[Dict[str, Union[Dict[str, str], str]]] = {}
    ):
        self.headers.data.append(FHTableRow(data=header, html_options=html_options))
        check_schema(self)


class FHFigure(BaseModel):
    title: str
    filename: str


class FHObject(BaseModel):
    type: Literal["table", "svg_figure"]
    data: Union[FHTable, FHFigure]


class FHJSON(BaseModel):
    data: List[FHObject] = []

    def add_table(self, table):
        self.data.append(FHObject(type="table", data=table))
        check_schema(self)

    def add_svg_figure(self, figure):
        self.data.append(FHObject(type="svg_figure", data=figure))
        check_schema(self)
