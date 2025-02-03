"""
Defines EDAPDF class.
"""
from tempfile import NamedTemporaryFile

from fpdf import FPDF, Align
from matplotlib.figure import Figure
from matplotlib.pyplot import savefig
import pandas as pd
import polars as pl
from great_tables import GT

class EDAPDF(FPDF):
    """
    PDF class that inherits from FPDF and automatically
    sets certain options.
    """

    _title: str

    def __init__(self, title: str = ""):
        self._title = title  # Initialize _title properly
        super().__init__(orientation="portrait", unit="mm", format="A4")

    def header(self):
        # Setting font: helvetica bold 15
        self.set_font("helvetica", style="B", size=20)
        # Printing title:
        self.cell(w=None, h=None, text=self._title)
        # Performing a line break:
        self.ln(20)
        self.set_font("helvetica", size=12)

    def footer(self):
        # Position cursor at 1.5 cm from bottom:
        self.set_y(-15)
        # Setting font: helvetica italic 8
        self.set_font("helvetica", size=8)
        # Printing page number:
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")

    def add_figure(self, figure: Figure, title: str="Figure"):
        self.add_page()
        self.set_font("helvetica", size=12, style="B")
        self.cell(w=0, h=None, text=title, align="C")
        self.ln(5)
        with NamedTemporaryFile(suffix=".png") as tempfile:
            figure.savefig(tempfile)
            self.image(tempfile.name, x=Align.C, w=self.epw, keep_aspect_ratio=True)
        self.set_font("helvetica", size=12)
    
    def add_table(self, table: pd.DataFrame | pl.DataFrame, title: str="Table"):
        self.add_page()
        self.set_font("helvetica", size=12, style="B")
        self.cell(w=0, h=None, text=title, align="C")
        self.ln(5)
        with NamedTemporaryFile(suffix=".png") as tempfile:
            gt = GT(table)
            gt.save(tempfile.name, scale=2)
            self.image(tempfile.name, x=Align.C, w=self.epw, keep_aspect_ratio=True)
        self.set_font("helvetica", size=12)
    



