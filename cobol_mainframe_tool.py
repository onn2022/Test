"""
COBOL / z/OS Mainframe Excel Toolkit Generator
Creates a multi-sheet Excel workbook with tools useful for COBOL developers.
"""

import openpyxl
from openpyxl.styles import (
    Font, PatternFill, Alignment, Border, Side, GradientFill
)
from openpyxl.styles.numbers import FORMAT_NUMBER, FORMAT_TEXT
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.chart import BarChart, Reference
from openpyxl.formatting.rule import ColorScaleRule, CellIsRule, FormulaRule
from openpyxl.worksheet.table import Table, TableStyleInfo
import openpyxl.utils.cell as cell_utils

# ── Colour palette ────────────────────────────────────────────────────────────
C_GREEN_DARK  = "1F4E3D"   # header bg
C_GREEN_MID   = "2E7D52"   # sub-header bg
C_GREEN_LIGHT = "C8E6C9"   # alt row
C_AMBER       = "FF8F00"   # warning accent
C_BLUE        = "1565C0"   # info accent
C_YELLOW      = "FFF9C4"   # input cell bg
C_WHITE       = "FFFFFF"
C_GRAY        = "F5F5F5"
C_RED         = "C62828"

def hdr_font(size=11, bold=True, color=C_WHITE):
    return Font(name="Calibri", size=size, bold=bold, color=color)

def body_font(size=10, bold=False, color="000000"):
    return Font(name="Calibri", size=size, bold=bold, color=color)

def fill(hex_color):
    return PatternFill("solid", fgColor=hex_color)

def thin_border():
    s = Side(style="thin", color="BDBDBD")
    return Border(left=s, right=s, top=s, bottom=s)

def center():
    return Alignment(horizontal="center", vertical="center", wrap_text=True)

def left():
    return Alignment(horizontal="left", vertical="center", wrap_text=True)

def style_header_row(ws, row, cols, bg=C_GREEN_DARK, font_size=11):
    for col in range(1, cols + 1):
        c = ws.cell(row=row, column=col)
        c.fill = fill(bg)
        c.font = hdr_font(size=font_size)
        c.alignment = center()
        c.border = thin_border()

def style_data_row(ws, row, cols, alt=False):
    bg = C_GREEN_LIGHT if alt else C_WHITE
    for col in range(1, cols + 1):
        c = ws.cell(row=row, column=col)
        c.fill = fill(bg)
        c.font = body_font()
        c.alignment = left()
        c.border = thin_border()

def set_col_widths(ws, widths):
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w

def merge_title(ws, title, cell_range, bg=C_GREEN_DARK):
    ws.merge_cells(cell_range)
    c = ws[cell_range.split(":")[0]]
    c.value = title
    c.fill = fill(bg)
    c.font = hdr_font(size=14)
    c.alignment = center()

# ══════════════════════════════════════════════════════════════════════════════
# Sheet 1 – PIC Clause Calculator
# ══════════════════════════════════════════════════════════════════════════════
def sheet_pic_calculator(wb):
    ws = wb.create_sheet("PIC Calculator")
    ws.sheet_view.showGridLines = False
    ws.freeze_panes = "A4"

    merge_title(ws, "COBOL PIC Clause — Storage Calculator", "A1:G1")

    # Instructions
    ws.merge_cells("A2:G2")
    ws["A2"] = ("Enter a PIC clause in column A. Digits/decimal/sign info "
                "will auto-populate. Yellow cells are input.")
    ws["A2"].font = body_font(size=9, color="555555")
    ws["A2"].alignment = left()

    headers = ["PIC Clause", "Usage / COMP", "Digits (n)",
               "Decimal (d)", "Signed?", "Storage Bytes", "Notes"]
    for col, h in enumerate(headers, 1):
        ws.cell(row=3, column=col).value = h
    style_header_row(ws, 3, 7)

    # Reference data rows  (PIC, USAGE, digits, decimal, signed, bytes, notes)
    data = [
        ["PIC 9(4)",          "DISPLAY",  4, 0, "No",  4,  "Zoned decimal, 1 byte per digit"],
        ["PIC S9(4)",         "DISPLAY",  4, 0, "Yes", 5,  "Zoned decimal + sign nibble"],
        ["PIC 9(7)V99",       "DISPLAY",  9, 2, "No",  9,  "9 display bytes (V = implied decimal)"],
        ["PIC S9(5)V9(2)",    "DISPLAY",  7, 2, "Yes", 8,  "Signed zoned decimal"],
        ["PIC 9(4)",          "COMP",     4, 0, "No",  2,  "Binary: 1-4 digits → 2 bytes"],
        ["PIC 9(9)",          "COMP",     9, 0, "No",  4,  "Binary: 5-9 digits → 4 bytes"],
        ["PIC 9(18)",         "COMP",     18,0, "No",  8,  "Binary: 10-18 digits → 8 bytes"],
        ["PIC S9(4)",         "COMP",     4, 0, "Yes", 2,  "Signed binary 2 bytes"],
        ["PIC S9(9)",         "COMP",     9, 0, "Yes", 4,  "Signed binary 4 bytes"],
        ["PIC S9(18)",        "COMP",     18,0, "Yes", 8,  "Signed binary 8 bytes"],
        ["PIC S9(5)V9(2)",    "COMP-3",   7, 2, "Yes", 4,  "Packed: CEIL((7+1)/2)=4 bytes"],
        ["PIC S9(9)V9(2)",    "COMP-3",   11,2, "Yes", 6,  "Packed: CEIL((11+1)/2)=6 bytes"],
        ["PIC 9(4)",          "COMP-3",   4, 0, "No",  3,  "Packed: CEIL((4+1)/2)=3 bytes"],
        ["PIC 9(6)",          "COMP-3",   6, 0, "No",  4,  "Packed: CEIL((6+1)/2)=4 bytes"],
        ["PIC X(10)",         "DISPLAY",  "-","-","No",10, "Alphanumeric, 1 byte per char"],
        ["PIC X(256)",        "DISPLAY",  "-","-","No",256,"Alphanumeric 256 bytes"],
        ["PIC A(5)",          "DISPLAY",  "-","-","No", 5, "Alphabetic, 1 byte per char"],
        ["PIC 1",             "DISPLAY",  1, 0, "No",  1,  "Boolean / bit field"],
        ["PIC G(10)",         "DISPLAY",  "-","-","No",20, "DBCS graphic: 2 bytes per char"],
        ["PIC N(10)",         "NATIONAL", "-","-","No",20, "National (UTF-16): 2 bytes per char"],
        ["PIC S9(4)",         "COMP-1",   "-","-","Yes", 4, "Single-precision float (4 bytes)"],
        ["PIC S9(16)",        "COMP-2",   "-","-","Yes", 8, "Double-precision float (8 bytes)"],
        ["PIC S9(4)",         "COMP-4",   4, 0, "Yes", 2,  "Same as COMP (pure binary)"],
        ["PIC S9(4)",         "COMP-5",   4, 0, "Yes", 2,  "Native binary (no truncation)"],
    ]

    for r, row in enumerate(data, 4):
        alt = (r % 2 == 0)
        for c, val in enumerate(row, 1):
            cell = ws.cell(row=r, column=c, value=val)
            cell.font = body_font()
            cell.border = thin_border()
            cell.alignment = left()
            if alt:
                cell.fill = fill(C_GREEN_LIGHT)
            else:
                cell.fill = fill(C_WHITE)

    # Custom calculator section
    start = len(data) + 6
    ws.merge_cells(f"A{start}:G{start}")
    ws[f"A{start}"] = "Custom COMP-3 Storage Calculator"
    ws[f"A{start}"].fill = fill(C_GREEN_MID)
    ws[f"A{start}"].font = hdr_font(size=12)
    ws[f"A{start}"].alignment = center()

    labels = ["Total digits (n)", "Decimal digits (d)",
              "Signed (1=Yes 0=No)", "COMP-3 bytes = CEIL((n+1)/2)",
              "DISPLAY bytes = n+sign", "COMP bytes (approx)"]
    defaults = [7, 2, 1, None, None, None]

    for i, (lbl, dflt) in enumerate(zip(labels, defaults)):
        r = start + 1 + i
        ws.cell(row=r, column=1, value=lbl).font = body_font(bold=True)
        ws.cell(row=r, column=1).border = thin_border()
        ws.cell(row=r, column=1).fill = fill(C_GRAY)
        inp = ws.cell(row=r, column=2)
        inp.border = thin_border()
        if dflt is not None:
            inp.value = dflt
            inp.fill = fill(C_YELLOW)
        else:
            inp.fill = fill(C_GREEN_LIGHT)

    # Formulas (rows start+1..start+6, col B = column 2)
    n_cell  = f"B{start+1}"
    s_cell  = f"B{start+3}"
    ws[f"B{start+4}"] = f"=CEILING(({n_cell}+1)/2,1)"
    ws[f"B{start+4}"].font = body_font(bold=True, color=C_BLUE)
    ws[f"B{start+5}"] = f"={n_cell}+{s_cell}"
    ws[f"B{start+5}"].font = body_font(bold=True, color=C_BLUE)
    ws[f"B{start+6}"] = (f"=IF({n_cell}<=4,2,IF({n_cell}<=9,4,8))")
    ws[f"B{start+6}"].font = body_font(bold=True, color=C_BLUE)

    set_col_widths(ws, [22, 12, 10, 10, 10, 14, 48])
    ws.row_dimensions[1].height = 30
    ws.row_dimensions[3].height = 28

# ══════════════════════════════════════════════════════════════════════════════
# Sheet 2 – Record Layout Designer
# ══════════════════════════════════════════════════════════════════════════════
def sheet_record_layout(wb):
    ws = wb.create_sheet("Record Layout")
    ws.sheet_view.showGridLines = False
    ws.freeze_panes = "A5"

    merge_title(ws, "COBOL Copybook Record Layout Designer", "A1:K1")

    ws.merge_cells("A2:K2")
    ws["A2"] = ("Fill in field details. Start Position and End Position are "
                "auto-calculated. Total Record Length is shown at the bottom.")
    ws["A2"].font = body_font(size=9, color="555555")
    ws["A2"].alignment = left()
    ws["A2"].fill = fill(C_GRAY)

    # Legend row
    ws.merge_cells("A3:K3")
    ws["A3"] = ("  Usage codes: D=DISPLAY  C=COMP  C3=COMP-3  C1=COMP-1  "
                "C2=COMP-2  C4=COMP-4  C5=COMP-5  N=NATIONAL")
    ws["A3"].font = body_font(size=9, color=C_BLUE)
    ws["A3"].fill = fill("E3F2FD")
    ws["A3"].alignment = left()

    headers = ["#", "Field Name (COBOL)", "Level",
               "PIC Clause", "USAGE", "Digits (n)", "Dec (d)",
               "Signed", "Bytes", "Start Pos", "End Pos"]
    for col, h in enumerate(headers, 1):
        ws.cell(row=4, column=col).value = h
    style_header_row(ws, 4, 11)
    ws.row_dimensions[4].height = 28

    # Sample copybook record (EMPLOYEE-RECORD)
    sample = [
        [1,  "EMP-RECORD",       "01", "",         "",   "", "", "",  "",  "", ""],
        [2,  "EMP-ID",           "05", "9(6)",      "C",  6,  0, "N", 4,   "", ""],
        [3,  "EMP-NAME",         "05", "X(30)",     "D",  "", "", "N", 30,  "", ""],
        [4,  "EMP-DEPT",         "05", "X(10)",     "D",  "", "", "N", 10,  "", ""],
        [5,  "EMP-SALARY",       "05", "S9(7)V99",  "C3", 9,  2, "Y", 5,   "", ""],
        [6,  "EMP-DOB",          "05", "9(8)",      "D",  8,  0, "N", 8,   "", ""],
        [7,  "EMP-ACTIVE-FLAG",  "05", "X(1)",      "D",  "", "", "N", 1,   "", ""],
        [8,  "EMP-FILLER",       "05", "X(10)",     "D",  "", "", "N", 10,  "", ""],
    ]

    for r, row in enumerate(sample, 5):
        alt = (r % 2 == 0)
        for c, val in enumerate(row, 1):
            cell = ws.cell(row=r, column=c, value=val)
            cell.font = body_font()
            cell.border = thin_border()
            cell.alignment = left() if c > 1 else center()
            cell.fill = fill(C_GREEN_LIGHT if alt else C_WHITE)
            # Make editable fields yellow
            if c in (2, 3, 4, 5, 6, 7, 8, 9) and val != "":
                cell.fill = fill(C_YELLOW)

    # Auto-calculate Start/End using formulas
    for r in range(5, 5 + len(sample)):
        start_cell = ws.cell(row=r, column=10)
        end_cell   = ws.cell(row=r, column=11)
        bytes_col  = "I"
        if r == 5:
            start_cell.value = 1
        else:
            start_cell.value = f"=K{r-1}+1"
        end_cell.value = f"=J{r}+{bytes_col}{r}-1"
        for cell in (start_cell, end_cell):
            cell.font = body_font(bold=True, color=C_BLUE)
            cell.border = thin_border()
            cell.alignment = center()
            cell.fill = fill(C_GREEN_LIGHT if r % 2 == 0 else C_WHITE)

    # Total row
    total_row = 5 + len(sample) + 1
    ws.merge_cells(f"A{total_row}:H{total_row}")
    ws[f"A{total_row}"] = "TOTAL RECORD LENGTH (bytes)"
    ws[f"A{total_row}"].fill = fill(C_GREEN_DARK)
    ws[f"A{total_row}"].font = hdr_font()
    ws[f"A{total_row}"].alignment = center()

    total_bytes_cell = ws.cell(row=total_row, column=9)
    total_bytes_cell.value = f"=SUM(I5:I{total_row-2})"
    total_bytes_cell.font = hdr_font(size=12, color=C_AMBER)
    total_bytes_cell.fill = fill(C_GREEN_DARK)
    total_bytes_cell.border = thin_border()
    total_bytes_cell.alignment = center()

    # Merge end position to show max
    ws.merge_cells(f"J{total_row}:K{total_row}")
    ws[f"J{total_row}"] = f"=K{total_row-2}"
    ws[f"J{total_row}"].fill = fill(C_GREEN_DARK)
    ws[f"J{total_row}"].font = hdr_font(size=12, color=C_AMBER)
    ws[f"J{total_row}"].alignment = center()
    ws[f"J{total_row}"].border = thin_border()

    set_col_widths(ws, [4, 26, 6, 14, 8, 9, 8, 8, 8, 10, 10])

# ══════════════════════════════════════════════════════════════════════════════
# Sheet 3 – COMP-3 / Packed Decimal Tool
# ══════════════════════════════════════════════════════════════════════════════
def sheet_comp3(wb):
    ws = wb.create_sheet("COMP-3 Packed Decimal")
    ws.sheet_view.showGridLines = False

    merge_title(ws, "COMP-3 (Packed Decimal) Reference & Encoder", "A1:H1")

    # Theory section
    theory = [
        ("Rule", "Detail"),
        ("Storage formula", "CEIL( (total_digits + 1) / 2 )  bytes"),
        ("Sign nibble – positive", "0x0C  (hex C)"),
        ("Sign nibble – negative", "0x0D  (hex D)"),
        ("Sign nibble – unsigned", "0x0F  (hex F)"),
        ("Digit packing",          "Each decimal digit → 1 nibble (4 bits)"),
        ("Example: +1234",         "→  12 3C  (2 bytes)"),
        ("Example: -56789",        "→  05 67 8D  (3 bytes)"),
        ("Example:  0",            "→  0C  (1 byte)"),
        ("Max value S9(18)",       "→  999,999,999,999,999,999"),
    ]

    ws["A3"] = "Theory & Rules"
    ws["A3"].fill = fill(C_GREEN_MID)
    ws["A3"].font = hdr_font(size=12)
    ws.merge_cells("A3:H3")
    ws["A3"].alignment = center()

    for r, (label, detail) in enumerate(theory, 4):
        ws.cell(row=r, column=1, value=label).font  = body_font(bold=True)
        ws.cell(row=r, column=1).fill  = fill(C_GRAY if r % 2 else C_WHITE)
        ws.cell(row=r, column=1).border = thin_border()
        ws.merge_cells(f"B{r}:H{r}")
        ws.cell(row=r, column=2, value=detail).font = body_font(color=C_BLUE)
        ws.cell(row=r, column=2).fill  = fill(C_GRAY if r % 2 else C_WHITE)
        ws.cell(row=r, column=2).border = thin_border()

    # Reference table – digits → bytes
    ref_start = 4 + len(theory) + 2
    ws.merge_cells(f"A{ref_start}:H{ref_start}")
    ws[f"A{ref_start}"] = "COMP-3 Digits ↔ Bytes Quick Reference"
    ws[f"A{ref_start}"].fill = fill(C_GREEN_DARK)
    ws[f"A{ref_start}"].font = hdr_font(size=12)
    ws[f"A{ref_start}"].alignment = center()

    ref_headers = ["Digits (n)", "COMP-3 Bytes", "Max Value (unsigned)",
                   "DISPLAY Bytes", "COMP Bytes", "COMP-3 Hex Example",
                   "PIC Clause", "Notes"]
    for col, h in enumerate(ref_headers, 1):
        ws.cell(row=ref_start+1, column=col).value = h
    style_header_row(ws, ref_start+1, 8, bg=C_GREEN_MID, font_size=10)

    ref_data = [
        [1,  1, "9",                         1, 2, "9C",          "S9(1) COMP-3",    ""],
        [2,  2, "99",                        2, 2, "99C",         "S9(2) COMP-3",    ""],
        [3,  2, "999",                       3, 2, "09 9C",       "S9(3) COMP-3",    ""],
        [4,  3, "9,999",                     4, 2, "09 99C",      "S9(4) COMP-3",    ""],
        [5,  3, "99,999",                    5, 2, "99 99 9C",    "S9(5) COMP-3",    ""],
        [6,  4, "999,999",                   6, 2, "09 99 99C",   "S9(6) COMP-3",    ""],
        [7,  4, "9,999,999",                 7, 2, "09 99 99 9C", "S9(7) COMP-3",    "Common amount field"],
        [8,  5, "99,999,999",                8, 4, "...",         "S9(8) COMP-3",    ""],
        [9,  5, "999,999,999",               9, 4, "...",         "S9(9) COMP-3",    ""],
        [10, 6, "9,999,999,999",            10, 4, "...",         "S9(10) COMP-3",   ""],
        [11, 6, "99,999,999,999",           11, 4, "...",         "S9(11) COMP-3",   ""],
        [12, 7, "999,999,999,999",          12, 4, "...",         "S9(12) COMP-3",   ""],
        [15, 8, "999,999,999,999,999",      15, 8, "...",         "S9(15) COMP-3",   ""],
        [18, 10,"999,999,999,999,999,999",  18, 8, "...",         "S9(18) COMP-3",   "Max practical"],
    ]

    for r, row in enumerate(ref_data, ref_start+2):
        alt = (r % 2 == 0)
        for c, val in enumerate(row, 1):
            cell = ws.cell(row=r, column=c, value=val)
            cell.font = body_font()
            cell.border = thin_border()
            cell.alignment = center() if c <= 5 else left()
            cell.fill = fill(C_GREEN_LIGHT if alt else C_WHITE)

    # Interactive calculator
    calc_start = ref_start + len(ref_data) + 4
    ws.merge_cells(f"A{calc_start}:H{calc_start}")
    ws[f"A{calc_start}"] = "Interactive COMP-3 Calculator"
    ws[f"A{calc_start}"].fill = fill(C_GREEN_MID)
    ws[f"A{calc_start}"].font = hdr_font(size=12)
    ws[f"A{calc_start}"].alignment = center()

    calc_items = [
        ("Integer digits (n)",         5,  False),
        ("Decimal digits (d)",         2,  False),
        ("Signed? (1=Yes, 0=No)",      1,  False),
        ("Total digits (n+d)",         None, True),
        ("COMP-3 bytes",               None, True),
        ("DISPLAY bytes (n+d+sign)",   None, True),
        ("COMP binary bytes",          None, True),
        ("PIC clause generated",       None, True),
    ]

    n_r = calc_start + 1
    d_r = calc_start + 2
    s_r = calc_start + 3

    for i, (lbl, default, formula) in enumerate(calc_items):
        r = calc_start + 1 + i
        ws.cell(row=r, column=1, value=lbl).font  = body_font(bold=True)
        ws.cell(row=r, column=1).fill  = fill(C_GRAY)
        ws.cell(row=r, column=1).border = thin_border()
        ws.merge_cells(f"B{r}:H{r}")
        cell = ws.cell(row=r, column=2)
        cell.border = thin_border()
        if not formula:
            cell.value = default
            cell.fill = fill(C_YELLOW)
        else:
            cell.fill = fill(C_GREEN_LIGHT)
            cell.font = body_font(bold=True, color=C_BLUE)

    # Formulas
    ws[f"B{calc_start+4}"] = f"=B{n_r}+B{d_r}"
    ws[f"B{calc_start+5}"] = f"=CEILING((B{n_r}+B{d_r}+1)/2,1)"
    ws[f"B{calc_start+6}"] = f"=B{n_r}+B{d_r}+B{s_r}"
    ws[f"B{calc_start+7}"] = f'=IF(B{n_r}+B{d_r}<=4,2,IF(B{n_r}+B{d_r}<=9,4,8))'
    ws[f"B{calc_start+8}"] = (
        f'=IF(B{s_r}=1,"S","")&"9("&B{n_r}&")"&'
        f'IF(B{d_r}>0,"V9("&B{d_r}&")","")&" COMP-3"'
    )

    set_col_widths(ws, [26, 28, 22, 14, 12, 20, 18, 24])
    ws.row_dimensions[1].height = 30

# ══════════════════════════════════════════════════════════════════════════════
# Sheet 4 – EBCDIC ↔ ASCII Reference
# ══════════════════════════════════════════════════════════════════════════════
def sheet_ebcdic(wb):
    ws = wb.create_sheet("EBCDIC-ASCII Reference")
    ws.sheet_view.showGridLines = False
    ws.freeze_panes = "A4"

    merge_title(ws, "EBCDIC ↔ ASCII Character Reference (IBM Code Page 037)", "A1:F1")

    ws.merge_cells("A2:F2")
    ws["A2"] = ("Common printable characters.  "
                "Mainframe data arrives in EBCDIC; ASCII is used on PC/Linux.")
    ws["A2"].font = body_font(size=9, color="555555")
    ws["A2"].fill = fill(C_GRAY)
    ws["A2"].alignment = left()

    headers = ["Character", "EBCDIC (Dec)", "EBCDIC (Hex)",
               "ASCII (Dec)", "ASCII (Hex)", "Notes"]
    for col, h in enumerate(headers, 1):
        ws.cell(row=3, column=col).value = h
    style_header_row(ws, 3, 6)

    # EBCDIC CP037 printable mappings (char, ebcdic_dec, ebcdic_hex, ascii_dec, ascii_hex, note)
    ebcdic_data = [
        (" ", 64,  "40", 32,  "20", "Space"),
        (".", 75,  "4B", 46,  "2E", "Period"),
        ("<", 76,  "4C", 60,  "3C", "Less than"),
        ("(", 77,  "4D", 40,  "28", "Left paren"),
        ("+", 78,  "4E", 43,  "2B", "Plus"),
        ("|", 79,  "4F", 124, "7C", "Vertical bar"),
        ("&", 80,  "50", 38,  "26", "Ampersand"),
        ("!", 90,  "5A", 33,  "21", "Exclamation"),
        ("$", 91,  "5B", 36,  "24", "Dollar sign"),
        ("*", 92,  "5C", 42,  "2A", "Asterisk"),
        (")", 93,  "5D", 41,  "29", "Right paren"),
        (";", 94,  "5E", 59,  "3B", "Semicolon"),
        ("-", 96,  "60", 45,  "2D", "Hyphen/minus"),
        ("/", 97,  "61", 47,  "2F", "Slash"),
        (",", 107, "6B", 44,  "2C", "Comma"),
        ("%", 108, "6C", 37,  "25", "Percent"),
        ("_", 109, "6D", 95,  "5F", "Underscore"),
        (">", 110, "6E", 62,  "3E", "Greater than"),
        ("?", 111, "6F", 63,  "3F", "Question mark"),
        (":", 122, "7A", 58,  "3A", "Colon"),
        ("#", 123, "7B", 35,  "23", "Hash/pound"),
        ("@", 124, "7C", 64,  "40", "At sign"),
        ("'", 125, "7D", 39,  "27", "Apostrophe"),
        ("=", 126, "7E", 61,  "3D", "Equals"),
        ('"', 127, "7F", 34,  "22", "Double quote"),
        ("a", 129, "81", 97,  "61", ""),
        ("b", 130, "82", 98,  "62", ""),
        ("c", 131, "83", 99,  "63", ""),
        ("d", 132, "84", 100, "64", ""),
        ("e", 133, "85", 101, "65", ""),
        ("f", 134, "86", 102, "66", ""),
        ("g", 135, "87", 103, "67", ""),
        ("h", 136, "88", 104, "68", ""),
        ("i", 137, "89", 105, "69", ""),
        ("j", 145, "91", 106, "6A", ""),
        ("k", 146, "92", 107, "6B", ""),
        ("l", 147, "93", 108, "6C", ""),
        ("m", 148, "94", 109, "6D", ""),
        ("n", 149, "95", 110, "6E", ""),
        ("o", 150, "96", 111, "6F", ""),
        ("p", 151, "97", 112, "70", ""),
        ("q", 152, "98", 113, "71", ""),
        ("r", 153, "99", 114, "72", ""),
        ("s", 162, "A2", 115, "73", ""),
        ("t", 163, "A3", 116, "74", ""),
        ("u", 164, "A4", 117, "75", ""),
        ("v", 165, "A5", 118, "76", ""),
        ("w", 166, "A6", 119, "77", ""),
        ("x", 167, "A7", 120, "78", ""),
        ("y", 168, "A8", 121, "79", ""),
        ("z", 169, "A9", 122, "7A", ""),
        ("A", 193, "C1", 65,  "41", ""),
        ("B", 194, "C2", 66,  "42", ""),
        ("C", 195, "C3", 67,  "43", ""),
        ("D", 196, "C4", 68,  "44", ""),
        ("E", 197, "C5", 69,  "45", ""),
        ("F", 198, "C6", 70,  "46", ""),
        ("G", 199, "C7", 71,  "47", ""),
        ("H", 200, "C8", 72,  "48", ""),
        ("I", 201, "C9", 73,  "49", ""),
        ("J", 209, "D1", 74,  "4A", ""),
        ("K", 210, "D2", 75,  "4B", ""),
        ("L", 211, "D3", 76,  "4C", ""),
        ("M", 212, "D4", 77,  "4D", ""),
        ("N", 213, "D5", 78,  "4E", ""),
        ("O", 214, "D6", 79,  "4F", ""),
        ("P", 215, "D7", 80,  "50", ""),
        ("Q", 216, "D8", 81,  "51", ""),
        ("R", 217, "D9", 82,  "52", ""),
        ("S", 226, "E2", 83,  "53", ""),
        ("T", 227, "E3", 84,  "54", ""),
        ("U", 228, "E4", 85,  "55", ""),
        ("V", 229, "E5", 86,  "56", ""),
        ("W", 230, "E6", 87,  "57", ""),
        ("X", 231, "E7", 88,  "58", ""),
        ("Y", 232, "E8", 89,  "59", ""),
        ("Z", 233, "E9", 90,  "5A", ""),
        ("0", 240, "F0", 48,  "30", ""),
        ("1", 241, "F1", 49,  "31", ""),
        ("2", 242, "F2", 50,  "32", ""),
        ("3", 243, "F3", 51,  "33", ""),
        ("4", 244, "F4", 52,  "34", ""),
        ("5", 245, "F5", 53,  "35", ""),
        ("6", 246, "F6", 54,  "36", ""),
        ("7", 247, "F7", 55,  "37", ""),
        ("8", 248, "F8", 56,  "38", ""),
        ("9", 249, "F9", 57,  "39", ""),
    ]

    for r, row in enumerate(ebcdic_data, 4):
        alt = (r % 2 == 0)
        for c, val in enumerate(row, 1):
            cell = ws.cell(row=r, column=c, value=val)
            cell.font = body_font()
            cell.border = thin_border()
            cell.alignment = center()
            cell.fill = fill(C_GREEN_LIGHT if alt else C_WHITE)
            if c == 1:
                cell.font = Font(name="Courier New", size=12, bold=True)

    set_col_widths(ws, [12, 16, 16, 14, 14, 24])
    ws.row_dimensions[1].height = 30

# ══════════════════════════════════════════════════════════════════════════════
# Sheet 5 – ABEND Codes
# ══════════════════════════════════════════════════════════════════════════════
def sheet_abends(wb):
    ws = wb.create_sheet("ABEND Codes")
    ws.sheet_view.showGridLines = False
    ws.freeze_panes = "A4"

    merge_title(ws, "z/OS & COBOL ABEND Code Reference", "A1:F1")

    ws.merge_cells("A2:F2")
    ws["A2"] = "Common system (Sxxx) and user (Uxxx) abend codes with causes and fixes."
    ws["A2"].font = body_font(size=9, color="555555")
    ws["A2"].fill = fill(C_GRAY)
    ws["A2"].alignment = left()

    headers = ["ABEND Code", "Type", "Short Description",
               "Common Cause", "Likely Fix", "Severity"]
    for col, h in enumerate(headers, 1):
        ws.cell(row=3, column=col).value = h
    style_header_row(ws, 3, 6)

    abends = [
        ("S0C1", "System", "Invalid operation / bad branch",
         "Executing non-executable storage, wrong load module",
         "Check LOAD/CALL statements, verify linked modules", "Critical"),
        ("S0C4", "System", "Protection exception / invalid address",
         "Null pointer, uninitialised index, out-of-bounds subscript",
         "Add INITIALIZE, check subscript ranges, verify pointers", "Critical"),
        ("S0C7", "System", "Data exception – bad packed decimal",
         "Non-numeric data moved to COMP-3 field",
         "Validate input; add NUMERIC test before arithmetic", "Critical"),
        ("S0C9", "System", "Fixed-point divide exception",
         "Divide by zero",
         "Add IF DIVISOR = 0 guard before DIVIDE", "Critical"),
        ("S0CB", "System", "Decimal divide exception",
         "COMP-3 divide by zero",
         "Guard DIVIDE operation with ZERO check", "Critical"),
        ("S0F0", "System", "Decimal overflow",
         "Result exceeds PIC clause size",
         "Increase receiving field size or use ON SIZE ERROR", "High"),
        ("S013", "System", "DCB attributes mismatch",
         "LRECL/BLKSIZE mismatch between JCL and program",
         "Align DD statement LRECL with FD/SELECT clause", "High"),
        ("S022", "System", "Job cancelled by operator",
         "Manual cancel or time limit exceeded",
         "Optimise code or increase TIME= in JCL", "High"),
        ("S047", "System", "I/O error – VSAM",
         "Corrupt cluster or wrong VSAM open mode",
         "Check VSAM definition and open mode (I-O/INPUT/OUTPUT)", "High"),
        ("S0CB", "System", "VSAM logical error",
         "Duplicate key on WRITE or missing record on READ",
         "Check FILE STATUS field and add error handling", "High"),
        ("S222", "System", "Job cancelled – no dump",
         "Operator cancel or region size exceeded",
         "Check REGION= in JCL, add MEMLIMIT if needed", "Medium"),
        ("S322", "System", "CPU time limit exceeded",
         "Infinite loop or excessive processing",
         "Review loop logic, add EXIT conditions", "High"),
        ("S40F", "System", "Out of virtual storage",
         "GETMAIN/WORKING-STORAGE too large",
         "Reduce WORKING-STORAGE or increase REGION=", "High"),
        ("S80A", "System", "Insufficient virtual storage",
         "Program or data exceeds region",
         "Increase REGION= or reduce data sizes", "High"),
        ("S806", "System", "Module not found",
         "LOAD/CALL to non-existent or uncatalogued module",
         "Check STEPLIB/JOBLIB DD, verify module is linked", "Critical"),
        ("S837", "System", "DASD full – directory or extent",
         "Dataset ran out of space",
         "Increase SPACE= in JCL, archive old data", "High"),
        ("S878", "System", "Out of real storage",
         "Too many concurrent users or large datasets",
         "Reduce concurrent batch or increase real storage", "High"),
        ("SB37", "System", "Insufficient DASD space – primary",
         "Dataset exceeded primary allocation",
         "Increase SPACE primary or add secondary extents", "High"),
        ("SD37", "System", "Insufficient DASD space – secondary",
         "All secondary extents exhausted",
         "Increase secondary or use RLSE, clean up old data", "High"),
        ("SE37", "System", "All extents used",
         "Dataset at maximum 16 extents",
         "Reorganise dataset, use SMS or increase primary", "High"),
        ("U1000","User",   "File status error (non-zero)",
         "Unhandled VSAM/QSAM file status code",
         "Add FILE STATUS check and error handling paragraph", "High"),
        ("U1001","User",   "Invalid data in input record",
         "Data validation failure in program",
         "Add data validation logic and error logging", "Medium"),
        ("U4038","User",   "CICS ABEND – transaction",
         "CICS resource not available or invalid command",
         "Check CICS HANDLE ABEND and RESP codes", "High"),
        ("U0016","User",   "Custom ABEND – record not found",
         "Program called ABEND when record missing",
         "Check calling logic and add NOT FOUND handling", "Medium"),
    ]

    severity_colors = {
        "Critical": "FFCDD2",
        "High":     "FFE0B2",
        "Medium":   "FFF9C4",
        "Low":      "C8E6C9",
    }

    for r, row in enumerate(abends, 4):
        alt = (r % 2 == 0)
        for c, val in enumerate(row, 1):
            cell = ws.cell(row=r, column=c, value=val)
            cell.font = body_font()
            cell.border = thin_border()
            cell.alignment = left()
            if c == 6:  # Severity column
                cell.fill = fill(severity_colors.get(val, C_WHITE))
                cell.alignment = center()
                cell.font = body_font(bold=True)
            elif c == 1:
                cell.font = Font(name="Courier New", size=10, bold=True)
                cell.fill = fill(C_GREEN_LIGHT if alt else C_WHITE)
            else:
                cell.fill = fill(C_GREEN_LIGHT if alt else C_WHITE)

    set_col_widths(ws, [12, 10, 28, 38, 40, 12])
    ws.row_dimensions[1].height = 30

# ══════════════════════════════════════════════════════════════════════════════
# Sheet 6 – JCL Snippets Library
# ══════════════════════════════════════════════════════════════════════════════
def sheet_jcl(wb):
    ws = wb.create_sheet("JCL Snippets")
    ws.sheet_view.showGridLines = False
    ws.freeze_panes = "A4"

    merge_title(ws, "JCL Snippet Library — z/OS Job Control Language", "A1:D1")

    ws.merge_cells("A2:D2")
    ws["A2"] = "Common JCL patterns. Copy snippet from column C into your JCL editor."
    ws["A2"].font = body_font(size=9, color="555555")
    ws["A2"].fill = fill(C_GRAY)
    ws["A2"].alignment = left()

    headers = ["#", "Snippet Name", "JCL Code", "Description / Usage Notes"]
    for col, h in enumerate(headers, 1):
        ws.cell(row=3, column=col).value = h
    style_header_row(ws, 3, 4)

    jcl_snippets = [
        (1, "Job Card",
         "//JOBNAME  JOB (ACCT),'DESCRIPTION',\n//         CLASS=A,MSGCLASS=X,\n//         NOTIFY=&SYSUID",
         "Standard job card. Replace JOBNAME, ACCT, CLASS as per your installation."),
        (2, "EXEC COBOL Program",
         "//STEP01   EXEC PGM=MYPROG\n//STEPLIB  DD DSN=MY.LOADLIB,DISP=SHR\n//SYSOUT   DD SYSOUT=*",
         "Execute a compiled COBOL load module. STEPLIB points to your load library."),
        (3, "Sequential File Input",
         "//INFILE   DD DSN=MY.INPUT.FILE,\n//         DISP=SHR,\n//         LRECL=80,RECFM=FB",
         "Input sequential fixed-block file. Match LRECL to FD clause in COBOL."),
        (4, "Sequential File Output (new)",
         "//OUTFILE  DD DSN=MY.OUTPUT.FILE,\n//         DISP=(NEW,CATLG,DELETE),\n//         SPACE=(CYL,(10,5),RLSE),\n//         LRECL=132,RECFM=FB",
         "Create new output file. Space in cylinders; secondary=5; RLSE frees unused."),
        (5, "VSAM KSDS Open",
         "//VSAMFILE DD DSN=MY.KSDS.CLUSTER,\n//         DISP=SHR",
         "Open a VSAM KSDS for read. Use ACB/OPEN macros or COBOL SELECT/ASSIGN."),
        (6, "SORT Step (DFSORT)",
         "//SORT     EXEC PGM=SORT\n//SORTIN   DD DSN=MY.INPUT,DISP=SHR\n//SORTOUT  DD DSN=MY.SORTED,DISP=(NEW,CATLG)\n//SYSIN    DD *\n  SORT FIELDS=(1,10,CH,A,11,5,ZD,D)\n/*",
         "Sort on pos 1-10 alpha ascending, then pos 11-15 zoned-decimal descending."),
        (7, "IEFBR14 (Allocate/Delete)",
         "//ALLOC    EXEC PGM=IEFBR14\n//DD1      DD DSN=MY.FILE,\n//         DISP=(NEW,CATLG,DELETE),\n//         SPACE=(CYL,(5,1))",
         "Utility to allocate or delete datasets without running real code."),
        (8, "IDCAMS – Define KSDS",
         "//DEFVSAM  EXEC PGM=IDCAMS\n//SYSPRINT DD SYSOUT=*\n//SYSIN    DD *\n  DEFINE CLUSTER(NAME(MY.KSDS) -\n    INDEXED KEYS(10 0) -\n    RECORDSIZE(100 200) -\n    CYLINDERS(10 5) -\n    SHAREOPTIONS(2 3))\n/*",
         "Define a VSAM KSDS. Adjust KEY offset/length, RECORDSIZE, CYLINDERS."),
        (9, "IDCAMS – Repro (copy VSAM)",
         "//REPRO    EXEC PGM=IDCAMS\n//SYSPRINT DD SYSOUT=*\n//INFILE   DD DSN=MY.SOURCE.KSDS,DISP=SHR\n//OUTFILE  DD DSN=MY.TARGET.KSDS,DISP=SHR\n//SYSIN    DD *\n  REPRO INFILE(INFILE) OUTFILE(OUTFILE)\n/*",
         "Copy all records from one VSAM to another using IDCAMS REPRO."),
        (10,"IEBGENER (copy seq file)",
         "//COPY     EXEC PGM=IEBGENER\n//SYSPRINT DD SYSOUT=*\n//SYSIN    DD DUMMY\n//SYSUT1   DD DSN=MY.INPUT,DISP=SHR\n//SYSUT2   DD DSN=MY.OUTPUT,DISP=(NEW,CATLG),\n//         LRECL=80,RECFM=FB",
         "Copy a sequential file. SYSIN=DUMMY means no member selection."),
        (11,"DFSORT INCLUDE / OMIT",
         "//SYSIN    DD *\n  SORT FIELDS=COPY\n  INCLUDE COND=(10,2,CH,EQ,C'NY')\n/*",
         "Include only records where bytes 10-11 equal 'NY'. Use OMIT to exclude."),
        (12,"DFSORT SUM (dedup & sum)",
         "//SYSIN    DD *\n  SORT FIELDS=(1,9,ZD,A)\n  SUM FIELDS=(10,11,ZD)\n/*",
         "Sort on key and sum numeric field; eliminates duplicates on sort key."),
        (13,"COND Parameter",
         "//STEP02   EXEC PGM=MYPROG2,\n//         COND=(0,NE,STEP01)",
         "Run STEP02 only if STEP01 RC=0. COND=(rc,op,step) — skip if TRUE."),
        (14,"IF/THEN/ELSE (JCL 2.10+)",
         "//IF1      IF (STEP01.RC = 0) THEN\n//STEP02   EXEC PGM=GOODPATH\n//ELSE1    ELSE\n//STEP03   EXEC PGM=ERRPATH\n//ENDIF1   ENDIF",
         "Structured JCL conditional. Preferred over COND in modern z/OS."),
        (15,"SYSUDUMP / SYSABEND",
         "//SYSUDUMP DD SYSOUT=*",
         "Capture formatted dump on ABEND. Add to every EXEC step for diagnostics."),
        (16,"Instream SYSIN Data",
         "//STEP01   EXEC PGM=MYPROG\n//SYSIN    DD *\nINPUT DATA LINE 1\nINPUT DATA LINE 2\n/*",
         "Pass in-stream data to a program. /* ends the instream data."),
        (17,"DD DUMMY",
         "//DDNAME   DD DUMMY",
         "Simulate a file with no I/O. Useful for optional output files."),
        (18,"Symbolic Parameters",
         "//STEP01   EXEC PGM=&PROG,\n//         PARM='&ENV'",
         "Use symbolic parameters set in the JOB or PROC for portability."),
    ]

    for r, (num, name, code, desc) in enumerate(jcl_snippets, 4):
        alt = (r % 2 == 0)
        bg = C_GREEN_LIGHT if alt else C_WHITE

        ws.cell(row=r, column=1, value=num).fill = fill(bg)
        ws.cell(row=r, column=1).font = body_font(bold=True)
        ws.cell(row=r, column=1).border = thin_border()
        ws.cell(row=r, column=1).alignment = center()

        ws.cell(row=r, column=2, value=name).fill = fill(bg)
        ws.cell(row=r, column=2).font = body_font(bold=True, color=C_GREEN_MID)
        ws.cell(row=r, column=2).border = thin_border()
        ws.cell(row=r, column=2).alignment = left()

        code_cell = ws.cell(row=r, column=3, value=code)
        code_cell.fill = fill("F3E5F5")
        code_cell.font = Font(name="Courier New", size=9, color="4A148C")
        code_cell.border = thin_border()
        code_cell.alignment = Alignment(horizontal="left", vertical="top",
                                        wrap_text=True)

        ws.cell(row=r, column=4, value=desc).fill = fill(bg)
        ws.cell(row=r, column=4).font = body_font()
        ws.cell(row=r, column=4).border = thin_border()
        ws.cell(row=r, column=4).alignment = left()

        ws.row_dimensions[r].height = max(14 * code.count('\n') + 16, 32)

    set_col_widths(ws, [4, 26, 58, 50])
    ws.row_dimensions[1].height = 30

# ══════════════════════════════════════════════════════════════════════════════
# Sheet 7 – File Status Codes
# ══════════════════════════════════════════════════════════════════════════════
def sheet_file_status(wb):
    ws = wb.create_sheet("File Status Codes")
    ws.sheet_view.showGridLines = False
    ws.freeze_panes = "A4"

    merge_title(ws, "COBOL File Status Code Reference (QSAM & VSAM)", "A1:E1")
    ws.merge_cells("A2:E2")
    ws["A2"] = "Check FILE STATUS field after every READ/WRITE/REWRITE/DELETE/START."
    ws["A2"].font = body_font(size=9, color="555555")
    ws["A2"].fill = fill(C_GRAY)
    ws["A2"].alignment = left()

    headers = ["File Status", "VSAM / QSAM", "Meaning",
               "Common Cause", "Recommended Action"]
    for col, h in enumerate(headers, 1):
        ws.cell(row=3, column=col).value = h
    style_header_row(ws, 3, 5)

    codes = [
        ("00", "Both",  "Successful completion",            "Normal",                           "Continue processing"),
        ("02", "VSAM",  "Duplicate key (alternate index)",  "Alternate key not unique",         "If expected, continue; else log warning"),
        ("04", "QSAM",  "Record shorter than expected",     "LRECL mismatch",                   "Check FD RECORD CONTAINS vs dataset LRECL"),
        ("05", "Both",  "File not present (OPEN)",          "Dataset does not exist",           "Create file or change OPEN mode"),
        ("07", "QSAM",  "CLOSE attempted on non-open file", "Logic error",                      "Check OPEN/CLOSE pairing"),
        ("10", "Both",  "End of file (AT END)",             "Normal EOF on sequential READ",    "Expected; process in AT END clause"),
        ("14", "QSAM",  "Too many relative key values",     "Relative file boundary exceeded",  "Increase file size"),
        ("21", "Both",  "Key sequence error on WRITE",      "Records written out of sequence",  "Sort input before writing KSDS"),
        ("22", "VSAM",  "Duplicate primary key",            "WRITE with existing key",          "Add key uniqueness check before WRITE"),
        ("23", "Both",  "Record not found",                 "READ/DELETE on non-existent key",  "Add NOT FOUND handling; check key value"),
        ("24", "VSAM",  "Boundary violation (out of space)","VSAM cluster full",                "Reorganise/expand cluster"),
        ("30", "Both",  "Permanent I/O error",              "Hardware or disk error",           "Contact systems programmer; check SYSLOG"),
        ("34", "QSAM",  "Boundary violation",               "Write beyond end of fixed file",   "Check record count and file size"),
        ("35", "Both",  "File not found on OPEN INPUT",     "Dataset missing",                  "Verify DSN in JCL DD statement"),
        ("37", "QSAM",  "File already exists on OPEN OUT",  "Tried to create existing file",    "Use DISP=OLD or delete/uncatalog first"),
        ("38", "Both",  "File locked / already open",       "Another job holds exclusive lock", "Wait or coordinate job scheduling"),
        ("39", "Both",  "Attribute conflict on OPEN",       "FD attrs ≠ actual file attrs",    "Match LRECL/RECFM in FD and JCL"),
        ("41", "Both",  "OPEN already open",                "Duplicate OPEN statement",         "Check logic flow; add status check"),
        ("42", "Both",  "CLOSE not open",                   "CLOSE without prior OPEN",         "Check logic flow"),
        ("43", "VSAM",  "DELETE without prior READ",        "DELETE attempted without READ",    "Add READ before DELETE"),
        ("44", "Both",  "Record too large / too small",     "Record length mismatch",           "Align FD RECORD CONTAINS with actual size"),
        ("46", "Both",  "Sequential READ without OPEN",     "READ before OPEN",                 "Ensure OPEN precedes first READ"),
        ("47", "Both",  "READ on file not open INPUT",      "File opened OUTPUT or I-O",        "Change OPEN mode to INPUT or I-O"),
        ("48", "Both",  "WRITE on file not open OUTPUT",    "File opened INPUT",                "Change OPEN mode to OUTPUT or I-O"),
        ("49", "VSAM",  "REWRITE/DELETE not open I-O",      "File opened INPUT",                "Change OPEN mode to I-O"),
        ("90", "VSAM",  "VSAM logic error",                 "Internal VSAM error",              "Check IDCAMS LISTCAT; reorganise cluster"),
        ("91", "VSAM",  "VSAM password failure",            "Wrong or missing password",        "Check RACF/ACF2 permissions"),
        ("92", "VSAM",  "VSAM out of space",                "Cluster full",                     "Reorganise and increase CYLINDERS"),
        ("93", "VSAM",  "Resource not available",           "File exclusively held",            "Wait; check ENQ/DEQ contention"),
        ("94", "VSAM",  "Sequential record not found",      "Current record deleted externally","Retry or handle gracefully"),
        ("95", "VSAM",  "Invalid or incomplete file info",  "ACB/RPL error",                    "Check VSAM definition with LISTCAT"),
        ("96", "VSAM",  "No DD statement",                  "Missing JCL DD for dataset",       "Add DD statement to JCL"),
        ("97", "VSAM",  "OPEN successful after implicit close","Prior implicit close recovery", "Normal in some cases; log and continue"),
    ]

    sev_bg = {
        "00": "C8E6C9", "02": "FFF9C4", "04": "FFF9C4",
        "10": "C8E6C9",
    }

    for r, row in enumerate(codes, 4):
        alt = (r % 2 == 0)
        bg = C_GREEN_LIGHT if alt else C_WHITE
        code_val = row[0]
        row_bg = sev_bg.get(code_val, bg)

        for c, val in enumerate(row, 1):
            cell = ws.cell(row=r, column=c, value=val)
            cell.font = body_font()
            cell.border = thin_border()
            cell.fill = fill(row_bg)
            cell.alignment = center() if c <= 2 else left()
            if c == 1:
                cell.font = Font(name="Courier New", size=11, bold=True)
            if code_val not in ("00", "10") and c == 1:
                cell.font = Font(name="Courier New", size=11, bold=True,
                                 color=C_RED)

    set_col_widths(ws, [14, 12, 32, 38, 38])
    ws.row_dimensions[1].height = 30

# ══════════════════════════════════════════════════════════════════════════════
# Sheet 8 – Hex / Decimal / Binary Converter
# ══════════════════════════════════════════════════════════════════════════════
def sheet_hex_converter(wb):
    ws = wb.create_sheet("Hex-Dec Converter")
    ws.sheet_view.showGridLines = False

    merge_title(ws, "Hexadecimal ↔ Decimal ↔ Binary Converter", "A1:F1")

    ws.merge_cells("A2:F2")
    ws["A2"] = ("Enter a decimal value in B5 OR a hex value in B6.  "
                "Other conversions are calculated automatically.")
    ws["A2"].font = body_font(size=9, color="555555")
    ws["A2"].fill = fill(C_GRAY)
    ws["A2"].alignment = left()

    # Input section
    ws.merge_cells("A4:F4")
    ws["A4"] = "Interactive Converter  (yellow = input cells)"
    ws["A4"].fill = fill(C_GREEN_MID)
    ws["A4"].font = hdr_font(size=12)
    ws["A4"].alignment = center()

    items = [
        ("Decimal input",         5,  True,   256),
        ("Hex input (e.g. FF)",   6,  True,   "100"),
        ("Dec → Hex",             7,  False,  None),
        ("Dec → Binary",          8,  False,  None),
        ("Dec → Octal",           9,  False,  None),
        ("Hex input → Decimal",  10,  False,  None),
        ("Byte value (0-255)?",  11,  False,  None),
        ("Signed byte (-128..127)?",12,False, None),
    ]

    for lbl, row, is_input, default in items:
        ws.cell(row=row, column=1, value=lbl).font = body_font(bold=True)
        ws.cell(row=row, column=1).fill = fill(C_GRAY)
        ws.cell(row=row, column=1).border = thin_border()
        ws.merge_cells(f"B{row}:F{row}")
        cell = ws.cell(row=row, column=2)
        cell.border = thin_border()
        if is_input:
            cell.value = default
            cell.fill = fill(C_YELLOW)
            cell.font = Font(name="Courier New", size=12, bold=True)
        else:
            cell.fill = fill(C_GREEN_LIGHT)
            cell.font = Font(name="Courier New", size=12, bold=True,
                             color=C_BLUE)

    ws["B7"]  = '=DEC2HEX(B5)'
    ws["B8"]  = '=DEC2BIN(B5)'
    ws["B9"]  = '=DEC2OCT(B5)'
    ws["B10"] = '=HEX2DEC(B6)'
    ws["B11"] = '=IF(AND(B5>=0,B5<=255),"YES","NO")'
    ws["B12"] = '=IF(B5<128,B5,B5-256)'

    for r in range(5, 13):
        ws.cell(row=r, column=1).border = thin_border()

    # Quick reference table
    ws.merge_cells("A14:F14")
    ws["A14"] = "Quick Hex Reference Table (0–255)"
    ws["A14"].fill = fill(C_GREEN_DARK)
    ws["A14"].font = hdr_font(size=12)
    ws["A14"].alignment = center()

    cols = ["Decimal", "Hex", "Binary", "Octal", "ASCII", "EBCDIC note"]
    for c, h in enumerate(cols, 1):
        ws.cell(row=15, column=c, value=h)
    style_header_row(ws, 15, 6, bg=C_GREEN_MID)

    special = {
        0: "NUL", 7: "BEL", 8: "BS", 9: "TAB", 10: "LF",
        13: "CR", 27: "ESC", 32: "SPACE", 127: "DEL"
    }
    ebcdic_note = {
        64: "EBCDIC SPACE", 75: "EBCDIC .", 91: "EBCDIC $",
        92: "EBCDIC *", 96: "EBCDIC -", 97: "EBCDIC /",
        122: "EBCDIC :", 240: "EBCDIC 0", 241: "EBCDIC 1",
    }

    selected = list(range(0, 33)) + list(range(48, 58)) + \
               list(range(65, 91)) + list(range(97, 123)) + \
               [127, 240, 241, 242, 249]

    for r, dec in enumerate(selected, 16):
        alt = (r % 2 == 0)
        bg = C_GREEN_LIGHT if alt else C_WHITE
        try:
            ch = chr(dec)
            asc = special.get(dec, ch if 32 <= dec < 127 else f"\\x{dec:02X}")
        except Exception:
            asc = f"\\x{dec:02X}"

        row_data = [dec, f"{dec:02X}", f"{dec:08b}", f"{dec:03o}",
                    asc, ebcdic_note.get(dec, "")]
        for c, val in enumerate(row_data, 1):
            cell = ws.cell(row=r, column=c, value=val)
            cell.font = Font(name="Courier New", size=10)
            cell.border = thin_border()
            cell.fill = fill(bg)
            cell.alignment = center()

    set_col_widths(ws, [22, 16, 18, 12, 12, 22])
    ws.row_dimensions[1].height = 30

# ══════════════════════════════════════════════════════════════════════════════
# Sheet 9 – COBOL Date Formats
# ══════════════════════════════════════════════════════════════════════════════
def sheet_dates(wb):
    ws = wb.create_sheet("Date Formats")
    ws.sheet_view.showGridLines = False

    merge_title(ws, "COBOL / Mainframe Date Format Reference", "A1:G1")

    ws.merge_cells("A2:G2")
    ws["A2"] = ("Mainframe dates have no single standard — always document "
                "the format in your copybook! Yellow cells are editable inputs.")
    ws["A2"].font = body_font(size=9, color="555555")
    ws["A2"].fill = fill(C_GRAY)
    ws["A2"].alignment = left()

    # Format reference table
    ws.merge_cells("A3:G3")
    ws["A3"] = "Common Date Formats"
    ws["A3"].fill = fill(C_GREEN_MID)
    ws["A3"].font = hdr_font(size=12)
    ws["A3"].alignment = center()

    headers = ["Format Name", "PIC Clause", "Example Value",
               "Layout", "Notes", "COBOL FUNCTION", "Bytes"]
    for col, h in enumerate(headers, 1):
        ws.cell(row=4, column=col).value = h
    style_header_row(ws, 4, 7)

    date_formats = [
        ("YYYYMMDD (ISO)", "9(8)", "20260508", "YYYY MM DD",
         "Most common. Use FUNCTION INTEGER-OF-DATE to convert.",
         "FUNCTION INTEGER-OF-DATE", 8),
        ("YYMMDD", "9(6)", "260508", "YY MM DD",
         "2-digit year – Y2K risk! Windowing needed.",
         "None (manual windowing)", 6),
        ("DDMMYYYY (EU)", "9(8)", "08052026", "DD MM YYYY",
         "Common in European mainframe systems.",
         "None (reformat manually)", 8),
        ("MMDDYYYY (US)", "9(8)", "05082026", "MM DD YYYY",
         "US format – rare in COBOL batch.",
         "None (reformat manually)", 8),
        ("Julian YYYYDDD", "9(7)", "2026128", "YYYY DDD",
         "Day-of-year 001-366. Use FUNCTION DAY-OF-INTEGER.",
         "FUNCTION DAY-OF-INTEGER", 7),
        ("Julian YYDDD", "9(5)", "26128", "YY DDD",
         "2-digit Julian – Y2K risk.",
         "None (manual windowing)", 5),
        ("Packed YYYYMMDD", "S9(8) COMP-3", "20260508", "YYYY MM DD packed",
         "8 digits packed → 5 bytes. Common in DB2 tables.",
         "FUNCTION INTEGER-OF-DATE", 5),
        ("YYYY-MM-DD (SQL)", "X(10)", "2026-05-08", "YYYY-MM-DD",
         "With hyphens – used in DB2 DATE column display.",
         "N/A (string)", 10),
        ("Lilian Date",  "9(9)", "152519", "Integer days since 14-Oct-1582",
         "COBOL FUNCTION INTEGER-OF-DATE returns Lilian.",
         "FUNCTION INTEGER-OF-DATE", 9),
        ("COBOL CENTURY-DATE", "9(8)", "20260508", "YYYYMMDD via ACCEPT",
         "ACCEPT WS-DATE FROM DATE YYYYMMDD.",
         "ACCEPT … FROM DATE YYYYMMDD", 8),
        ("COBOL CENTURY-DAY",  "9(7)", "2026128", "YYYYDDD via ACCEPT",
         "ACCEPT WS-DAY FROM DAY YYYYDDD.",
         "ACCEPT … FROM DAY YYYYDDD", 7),
    ]

    for r, row in enumerate(date_formats, 5):
        alt = (r % 2 == 0)
        for c, val in enumerate(row, 1):
            cell = ws.cell(row=r, column=c, value=val)
            cell.font = body_font()
            cell.border = thin_border()
            cell.fill = fill(C_GREEN_LIGHT if alt else C_WHITE)
            cell.alignment = left() if c in (1, 4, 5, 6) else center()
            if c == 3:
                cell.font = Font(name="Courier New", size=10, bold=True)

    # Date calculator
    calc_start = 5 + len(date_formats) + 2
    ws.merge_cells(f"A{calc_start}:G{calc_start}")
    ws[f"A{calc_start}"] = "Date Calculator"
    ws[f"A{calc_start}"].fill = fill(C_GREEN_MID)
    ws[f"A{calc_start}"].font = hdr_font(size=12)
    ws[f"A{calc_start}"].alignment = center()

    calc_items = [
        ("Input date (YYYY-MM-DD)",  "2026-05-08", True),
        ("Days to add / subtract",   30,            True),
        ("Result date",              None,          False),
        ("Day of week (1=Mon)",      None,          False),
        ("Days between (A and B)",   None,          False),
        ("Input date B (YYYY-MM-DD)","2026-12-31",  True),
        ("Days A→B",                 None,          False),
    ]

    for i, (lbl, default, is_input) in enumerate(calc_items):
        r = calc_start + 1 + i
        ws.cell(row=r, column=1, value=lbl).font = body_font(bold=True)
        ws.cell(row=r, column=1).fill = fill(C_GRAY)
        ws.cell(row=r, column=1).border = thin_border()
        ws.merge_cells(f"B{r}:G{r}")
        cell = ws.cell(row=r, column=2)
        cell.border = thin_border()
        if is_input:
            cell.value = default
            cell.fill = fill(C_YELLOW)
            if isinstance(default, str):
                cell.number_format = FORMAT_TEXT
        else:
            cell.fill = fill(C_GREEN_LIGHT)
            cell.font = body_font(bold=True, color=C_BLUE)

    inp_r   = calc_start + 1
    days_r  = calc_start + 2
    res_r   = calc_start + 3
    dow_r   = calc_start + 4
    diff_r  = calc_start + 5
    inp2_r  = calc_start + 6
    diff2_r = calc_start + 7

    ws[f"B{res_r}"]  = f'=IFERROR(TEXT(DATEVALUE(B{inp_r})+B{days_r},"YYYY-MM-DD"),"Invalid date")'
    ws[f"B{dow_r}"]  = f'=IFERROR(TEXT(WEEKDAY(DATEVALUE(B{inp_r}),2),"0")&" ("&TEXT(DATEVALUE(B{inp_r}),"DDDD")&")","Err")'
    ws[f"B{diff2_r}"]= f'=IFERROR(DATEVALUE(B{inp2_r})-DATEVALUE(B{inp_r}),"Invalid dates")'

    set_col_widths(ws, [26, 16, 16, 14, 36, 30, 8])
    ws.row_dimensions[1].height = 30

# ══════════════════════════════════════════════════════════════════════════════
# Sheet 10 – COBOL Verb Quick Reference
# ══════════════════════════════════════════════════════════════════════════════
def sheet_verbs(wb):
    ws = wb.create_sheet("COBOL Verbs")
    ws.sheet_view.showGridLines = False
    ws.freeze_panes = "A4"

    merge_title(ws, "COBOL Verb Quick Reference (COBOL 85 / 2002 / 2014)", "A1:F1")

    headers = ["Verb", "Division / Section", "Syntax Skeleton",
               "Description", "Key Clauses", "Example"]
    for col, h in enumerate(headers, 1):
        ws.cell(row=3, column=col).value = h
    style_header_row(ws, 3, 6)

    verbs = [
        ("MOVE",       "PROCEDURE", "MOVE src TO dest",
         "Copy data between fields",
         "CORRESPONDING (MOVE CORR)",
         "MOVE WS-TOTAL TO RPT-TOTAL"),
        ("ADD",        "PROCEDURE", "ADD a b … TO dest [GIVING g]",
         "Add one or more values",
         "GIVING, ROUNDED, ON SIZE ERROR",
         "ADD WS-A WS-B TO WS-TOTAL GIVING WS-SUM"),
        ("SUBTRACT",   "PROCEDURE", "SUBTRACT a FROM dest [GIVING g]",
         "Subtract value from field",
         "GIVING, ROUNDED, ON SIZE ERROR",
         "SUBTRACT WS-TAX FROM WS-GROSS GIVING WS-NET"),
        ("MULTIPLY",   "PROCEDURE", "MULTIPLY a BY dest [GIVING g]",
         "Multiply two values",
         "GIVING, ROUNDED, ON SIZE ERROR",
         "MULTIPLY WS-QTY BY WS-PRICE GIVING WS-AMT"),
        ("DIVIDE",     "PROCEDURE", "DIVIDE a INTO dest [GIVING g] [REMAINDER r]",
         "Divide; optionally capture remainder",
         "GIVING, REMAINDER, ON SIZE ERROR",
         "DIVIDE WS-COUNT INTO WS-TOTAL GIVING WS-AVG"),
        ("COMPUTE",    "PROCEDURE", "COMPUTE dest [ROUNDED] = expr",
         "Evaluate arithmetic expression",
         "ROUNDED, ON SIZE ERROR",
         "COMPUTE WS-RESULT = (WS-A + WS-B) * 1.1"),
        ("IF",         "PROCEDURE", "IF cond [THEN] … [ELSE] … END-IF",
         "Conditional execution",
         "ELSE, END-IF, nested IF",
         "IF WS-STATUS = 'A' MOVE 'Active' TO OUT-STATUS END-IF"),
        ("EVALUATE",   "PROCEDURE", "EVALUATE var WHEN val … END-EVALUATE",
         "Multi-way branch (like switch/case)",
         "WHEN OTHER, ALSO, TRUE",
         "EVALUATE WS-CODE\n  WHEN 'A' PERFORM PROC-A\n  WHEN OTHER PERFORM PROC-ERR\nEND-EVALUATE"),
        ("PERFORM",    "PROCEDURE", "PERFORM para [UNTIL/TIMES/VARYING]",
         "Call paragraph or inline loop",
         "UNTIL, TIMES, VARYING, THRU, WITH TEST BEFORE/AFTER",
         "PERFORM PROC-READ UNTIL WS-EOF = 'Y'"),
        ("READ",       "PROCEDURE", "READ file-name [NEXT] [INTO ws-var]",
         "Read next record from file",
         "AT END, NOT AT END, INTO, KEY IS",
         "READ INFILE INTO WS-REC AT END MOVE 'Y' TO WS-EOF END-READ"),
        ("WRITE",      "PROCEDURE", "WRITE record-name [FROM ws-var]",
         "Write record to file",
         "FROM, BEFORE/AFTER ADVANCING, INVALID KEY",
         "WRITE OUT-REC FROM WS-DATA INVALID KEY PERFORM ERR-RTN END-WRITE"),
        ("REWRITE",    "PROCEDURE", "REWRITE record-name [FROM ws-var]",
         "Update current record (I-O files)",
         "FROM, INVALID KEY",
         "REWRITE EMP-REC FROM WS-EMP-DATA END-REWRITE"),
        ("DELETE",     "PROCEDURE", "DELETE file-name RECORD",
         "Delete current or keyed record",
         "INVALID KEY",
         "DELETE EMPFILE RECORD INVALID KEY PERFORM ERR-DEL END-DELETE"),
        ("START",      "PROCEDURE", "START file KEY IS [=/>/<] key-field",
         "Position cursor in indexed file",
         "KEY IS EQUAL / GREATER / NOT LESS",
         "START EMPFILE KEY >= EMP-ID INVALID KEY PERFORM ERR-START"),
        ("OPEN",       "PROCEDURE", "OPEN INPUT|OUTPUT|I-O|EXTEND file",
         "Open a file for processing",
         "INPUT, OUTPUT, I-O, EXTEND",
         "OPEN INPUT INFILE OUTPUT OUTFILE"),
        ("CLOSE",      "PROCEDURE", "CLOSE file [WITH LOCK]",
         "Close file and release resources",
         "WITH LOCK (prevents re-open)",
         "CLOSE INFILE OUTFILE"),
        ("STOP RUN",   "PROCEDURE", "STOP RUN",
         "Terminate program and return to OS",
         "—",
         "STOP RUN"),
        ("GOBACK",     "PROCEDURE", "GOBACK",
         "Return to caller (subprogram) or OS (main)",
         "—",
         "GOBACK"),
        ("CALL",       "PROCEDURE", "CALL 'pgmname' USING param …",
         "Call external subprogram or function",
         "USING, BY REFERENCE/VALUE/CONTENT, ON EXCEPTION",
         "CALL 'SUBRTN01' USING WS-INPUT WS-OUTPUT ON EXCEPTION PERFORM ERR-CALL"),
        ("STRING",     "PROCEDURE", "STRING src … DELIMITED BY … INTO dest",
         "Concatenate strings",
         "DELIMITED BY, WITH POINTER, ON OVERFLOW",
         "STRING WS-FIRST DELIMITED BY SPACE '-' DELIMITED BY SIZE INTO WS-FULL"),
        ("UNSTRING",   "PROCEDURE", "UNSTRING src DELIMITED BY delim INTO dest …",
         "Split string into sub-fields",
         "DELIMITED BY, INTO, TALLYING, ON OVERFLOW",
         "UNSTRING WS-CSV DELIMITED BY ',' INTO WS-F1 WS-F2 WS-F3"),
        ("INSPECT",    "PROCEDURE", "INSPECT src TALLYING|REPLACING …",
         "Count or replace characters in string",
         "TALLYING, REPLACING, CONVERTING",
         "INSPECT WS-DATA REPLACING ALL SPACES BY ZEROS"),
        ("INITIALIZE", "PROCEDURE", "INITIALIZE var …",
         "Set fields to type-appropriate defaults",
         "REPLACING, FILLER, VALUE",
         "INITIALIZE WS-WORK-AREA"),
        ("SORT",       "PROCEDURE", "SORT sort-file ON ASCENDING/DESCENDING KEY …",
         "Sort internal sort file",
         "ASCENDING/DESCENDING KEY, USING, GIVING, INPUT/OUTPUT PROCEDURE",
         "SORT SORTFILE ON ASCENDING KEY SR-KEY USING INFILE GIVING OUTFILE"),
        ("MERGE",      "PROCEDURE", "MERGE merge-file ON ASCENDING KEY … USING f1 f2",
         "Merge pre-sorted files",
         "ASCENDING/DESCENDING KEY, USING, GIVING",
         "MERGE MF ON ASCENDING KEY MK USING F1 F2 GIVING OUTF"),
        ("ACCEPT",     "PROCEDURE", "ACCEPT var [FROM DATE/DAY/TIME/…]",
         "Read from console or system source",
         "FROM DATE YYYYMMDD / DAY / TIME / ENVIRONMENT",
         "ACCEPT WS-DATE FROM DATE YYYYMMDD"),
        ("DISPLAY",    "PROCEDURE", "DISPLAY var …",
         "Write to console / SYSOUT",
         "WITH NO ADVANCING",
         "DISPLAY 'Error at: ' WS-KEY"),
        ("SET",        "PROCEDURE", "SET index/condition/ptr TO value",
         "Assign index, condition-name, or pointer",
         "TO TRUE, UP BY, DOWN BY",
         "SET IDX-EMP TO 1"),
        ("SEARCH",     "PROCEDURE", "SEARCH table-name WHEN cond … END-SEARCH",
         "Linear table search",
         "WHEN, AT END, VARYING",
         "SEARCH WS-TABLE AT END PERFORM NOT-FND WHEN WS-TBL-KEY(IDX)=WS-KEY CONTINUE"),
        ("SEARCH ALL", "PROCEDURE", "SEARCH ALL table WHEN cond …",
         "Binary search on sorted table",
         "WHEN (equality only), AT END",
         "SEARCH ALL WS-TABLE WHEN WS-T-ID(IDX)=WS-SEARCH-ID PERFORM FOUND-RTN"),
        ("CONTINUE",   "PROCEDURE", "CONTINUE",
         "No-operation placeholder",
         "—",
         "WHEN OTHER CONTINUE"),
        ("COPY",       "ANY",       "COPY copybook-name [REPLACING …]",
         "Include external copybook source",
         "REPLACING ==old== BY ==new==",
         "COPY EMPRECRD REPLACING ==EMPLOYEE== BY ==CONTRACT=="),
        ("WORKING-STORAGE SECTION", "DATA",
         "01 WS-var PIC ...",
         "Declare working variables",
         "REDEFINES, OCCURS, VALUE",
         "01 WS-COUNTER PIC 9(5) VALUE ZERO"),
        ("FILE SECTION / FD", "DATA",
         "FD file-name RECORDING MODE F",
         "File description in DATA DIVISION",
         "RECORDING MODE, BLOCK CONTAINS, LABEL RECORDS",
         "FD INFILE RECORDING MODE F."),
        ("REDEFINES",  "DATA",     "02 ws-a REDEFINES ws-b PIC …",
         "Overlay same memory with different layout",
         "Cannot have VALUE clause",
         "02 WS-DATE-ALPHA REDEFINES WS-DATE-NUM PIC X(8)"),
        ("OCCURS",     "DATA",     "n OCCURS n [TO m] TIMES [DEPENDING ON v]",
         "Declare table (array)",
         "INDEXED BY, DEPENDING ON (ODO), ASCENDING/DESCENDING KEY",
         "05 WS-TABLE PIC X(10) OCCURS 100 TIMES INDEXED BY IDX"),
    ]

    for r, row in enumerate(verbs, 4):
        alt = (r % 2 == 0)
        bg = C_GREEN_LIGHT if alt else C_WHITE
        for c, val in enumerate(row, 1):
            cell = ws.cell(row=r, column=c, value=val)
            cell.border = thin_border()
            cell.fill = fill(bg)
            if c in (1,):
                cell.font = Font(name="Courier New", size=10, bold=True,
                                 color=C_GREEN_MID)
                cell.alignment = left()
            elif c == 3:
                cell.font = Font(name="Courier New", size=9, color="4A148C")
                cell.alignment = Alignment(horizontal="left", vertical="top",
                                           wrap_text=True)
            elif c == 6:
                cell.font = Font(name="Courier New", size=9, color="1A237E")
                cell.alignment = Alignment(horizontal="left", vertical="top",
                                           wrap_text=True)
            else:
                cell.font = body_font()
                cell.alignment = left()
        ws.row_dimensions[r].height = 32

    set_col_widths(ws, [18, 14, 38, 32, 34, 44])
    ws.row_dimensions[1].height = 30
    ws.row_dimensions[2].height = 0  # hide empty row 2

# ══════════════════════════════════════════════════════════════════════════════
# Sheet 11 – DB2 / SQL Helper
# ══════════════════════════════════════════════════════════════════════════════
def sheet_db2(wb):
    ws = wb.create_sheet("DB2-SQL Helper")
    ws.sheet_view.showGridLines = False
    ws.freeze_panes = "A4"

    merge_title(ws, "DB2 for z/OS — COBOL Embedded SQL Reference", "A1:F1")

    ws.merge_cells("A2:F2")
    ws["A2"] = ("All SQL in COBOL must be embedded in EXEC SQL … END-EXEC. "
                "Host variables are prefixed with a colon (:var).")
    ws["A2"].font = body_font(size=9, color="555555")
    ws["A2"].fill = fill(C_GRAY)
    ws["A2"].alignment = left()

    headers = ["#", "Topic", "Code / Template", "Notes"]
    for col, h in enumerate(headers, 1):
        ws.cell(row=3, column=col).value = h
    style_header_row(ws, 3, 4)

    db2_items = [
        (1, "SQLCA Declaration",
         "EXEC SQL\n  INCLUDE SQLCA\nEND-EXEC.",
         "Required in WORKING-STORAGE. Gives SQLCODE, SQLSTATE, SQLERRM."),
        (2, "Host Variable Declaration",
         "EXEC SQL BEGIN DECLARE SECTION END-EXEC.\n01 WS-EMP-ID     PIC S9(6) COMP.\n01 WS-EMP-NAME   PIC X(30).\n01 WS-SALARY     PIC S9(7)V99 COMP-3.\nEXEC SQL END DECLARE SECTION END-EXEC.",
         "Host variables must be in the DECLARE SECTION. Match DB2 column types."),
        (3, "SELECT INTO (single row)",
         "EXEC SQL\n  SELECT EMP_NAME, SALARY\n  INTO :WS-EMP-NAME, :WS-SALARY\n  FROM EMPLOYEE\n  WHERE EMP_ID = :WS-EMP-ID\nEND-EXEC.\nIF SQLCODE = 0  CONTINUE\nELSE IF SQLCODE = +100  PERFORM NOT-FOUND-RTN\nELSE                    PERFORM SQL-ERROR-RTN\nEND-IF.",
         "Use for single-row retrieval. Always check SQLCODE after every SQL."),
        (4, "CURSOR Declaration",
         "EXEC SQL\n  DECLARE EMP-CSR CURSOR FOR\n    SELECT EMP_ID, EMP_NAME, SALARY\n    FROM EMPLOYEE\n    WHERE DEPT_ID = :WS-DEPT\n    ORDER BY EMP_ID\nEND-EXEC.",
         "Declare cursor in WORKING-STORAGE or PROCEDURE DIVISION header."),
        (5, "OPEN / FETCH / CLOSE Cursor",
         "EXEC SQL OPEN EMP-CSR END-EXEC.\nPERFORM UNTIL SQLCODE = +100\n  EXEC SQL\n    FETCH EMP-CSR\n    INTO :WS-EMP-ID, :WS-EMP-NAME, :WS-SALARY\n  END-EXEC\n  IF SQLCODE = 0\n    PERFORM PROCESS-ROW\n  END-IF\nEND-PERFORM.\nEXEC SQL CLOSE EMP-CSR END-EXEC.",
         "SQLCODE +100 = no more rows. Always CLOSE cursor when done."),
        (6, "INSERT",
         "EXEC SQL\n  INSERT INTO EMPLOYEE\n    (EMP_ID, EMP_NAME, SALARY, HIRE_DATE)\n  VALUES\n    (:WS-EMP-ID, :WS-EMP-NAME, :WS-SALARY,\n     CURRENT DATE)\nEND-EXEC.\nIF SQLCODE NOT = 0 PERFORM SQL-ERROR-RTN END-IF.",
         "Use CURRENT DATE / CURRENT TIMESTAMP for system timestamps."),
        (7, "UPDATE",
         "EXEC SQL\n  UPDATE EMPLOYEE\n  SET SALARY = :WS-SALARY,\n      LAST_UPD = CURRENT TIMESTAMP\n  WHERE EMP_ID = :WS-EMP-ID\nEND-EXEC.\nIF SQLCODE = +100 PERFORM NOT-FOUND-RTN END-IF.",
         "SQLCODE +100 means no rows matched WHERE clause."),
        (8, "DELETE",
         "EXEC SQL\n  DELETE FROM EMPLOYEE\n  WHERE EMP_ID = :WS-EMP-ID\nEND-EXEC.\nIF SQLCODE = +100 PERFORM NOT-FOUND-RTN END-IF.",
         "Check SQLERRD(3) for number of rows deleted."),
        (9, "SQLCODE Reference",
         "SQLCODE =  0   → Success\nSQLCODE = +100 → Row not found / EOF\nSQLCODE = -180 → Invalid date string\nSQLCODE = -302 → Host variable overflow\nSQLCODE = -304 → Value too large for column\nSQLCODE = -407 → NULL into NOT NULL column\nSQLCODE = -501 → Cursor not open\nSQLCODE = -803 → Duplicate key / UNIQUE violation\nSQLCODE = -904 → Resource unavailable\nSQLCODE = -911 → Deadlock / timeout (rolled back)\nSQLCODE = -922 → Auth failure\nSQLCODE = -30082→ Connection failed",
         "Always test SQLCODE. Negative = error, positive = warning, 0 = success."),
        (10,"COMMIT / ROLLBACK",
         "EXEC SQL COMMIT END-EXEC.\nEXEC SQL ROLLBACK END-EXEC.",
         "COMMIT every N records in batch. ROLLBACK on error. Coordinate with CICS UOW."),
        (11,"NULL indicator variable",
         "01 WS-NULL-IND  PIC S9(4) COMP.\n...\nEXEC SQL\n  SELECT BONUS INTO :WS-BONUS :WS-NULL-IND\n  FROM EMPLOYEE WHERE EMP_ID = :WS-EMP-ID\nEND-EXEC.\nIF WS-NULL-IND < 0 MOVE ZERO TO WS-BONUS END-IF.",
         "Indicator < 0 means NULL. Required for NULLABLE columns."),
        (12,"DB2 Type ↔ COBOL PIC",
         "CHAR(n)         → PIC X(n)\nVARCHAR(n)      → 01 g. 49 len PIC S9(4) COMP. 49 data PIC X(n).\nSMALLINT        → PIC S9(4) COMP\nINTEGER         → PIC S9(9) COMP\nBIGINT          → PIC S9(18) COMP\nDECIMAL(p,s)    → PIC S9(p-s)V9(s) COMP-3\nFLOAT           → COMP-1 or COMP-2\nDATE            → PIC X(10)  (YYYY-MM-DD)\nTIME            → PIC X(8)   (HH.MM.SS)\nTIMESTAMP       → PIC X(26)  (YYYY-MM-DD-HH.MM.SS.FFFFFF)",
         "Match COBOL host variable type exactly to avoid SQLCODE -302/-304."),
    ]

    for r, (num, topic, code, note) in enumerate(db2_items, 4):
        alt = (r % 2 == 0)
        bg = C_GREEN_LIGHT if alt else C_WHITE

        ws.cell(row=r, column=1, value=num).font = body_font(bold=True)
        ws.cell(row=r, column=1).fill = fill(bg)
        ws.cell(row=r, column=1).border = thin_border()
        ws.cell(row=r, column=1).alignment = center()

        ws.cell(row=r, column=2, value=topic).font = body_font(bold=True, color=C_GREEN_DARK)
        ws.cell(row=r, column=2).fill = fill(bg)
        ws.cell(row=r, column=2).border = thin_border()
        ws.cell(row=r, column=2).alignment = left()

        code_cell = ws.cell(row=r, column=3, value=code)
        code_cell.font = Font(name="Courier New", size=9, color="4A148C")
        code_cell.fill = fill("F3E5F5")
        code_cell.border = thin_border()
        code_cell.alignment = Alignment(horizontal="left", vertical="top",
                                        wrap_text=True)

        ws.cell(row=r, column=4, value=note).font = body_font()
        ws.cell(row=r, column=4).fill = fill(bg)
        ws.cell(row=r, column=4).border = thin_border()
        ws.cell(row=r, column=4).alignment = left()

        lines = code.count('\n') + 1
        ws.row_dimensions[r].height = max(lines * 14 + 8, 32)

    set_col_widths(ws, [4, 28, 60, 52])
    ws.row_dimensions[1].height = 30

# ══════════════════════════════════════════════════════════════════════════════
# Sheet 12 – Dashboard / Home
# ══════════════════════════════════════════════════════════════════════════════
def sheet_dashboard(wb):
    ws = wb.create_sheet("HOME", 0)
    ws.sheet_view.showGridLines = False
    ws.sheet_view.showRowColHeaders = False

    # Big title
    ws.merge_cells("B2:K2")
    ws["B2"] = "COBOL / z/OS Mainframe Developer Toolkit"
    ws["B2"].fill = fill(C_GREEN_DARK)
    ws["B2"].font = Font(name="Calibri", size=22, bold=True, color=C_WHITE)
    ws["B2"].alignment = center()
    ws.row_dimensions[2].height = 48

    ws.merge_cells("B3:K3")
    ws["B3"] = "Your all-in-one Excel reference — calculators, snippets, and lookup tables"
    ws["B3"].fill = fill(C_GREEN_MID)
    ws["B3"].font = Font(name="Calibri", size=12, italic=True, color=C_WHITE)
    ws["B3"].alignment = center()
    ws.row_dimensions[3].height = 24

    # Sheet index cards
    cards = [
        ("PIC Calculator",       "PIC Clause Calculator",
         "Calculate storage bytes for any PIC clause and USAGE combination. "
         "Includes interactive COMP-3 calculator."),
        ("Record Layout",        "Record Layout Designer",
         "Document your copybook fields with auto-calculated positions. "
         "Total record length computed automatically."),
        ("COMP-3 Packed Decimal","COMP-3 / Packed Decimal",
         "Packed decimal reference table, encoding rules, and an "
         "interactive digits→bytes calculator."),
        ("EBCDIC-ASCII Reference","EBCDIC ↔ ASCII",
         "CP037 character mapping for debugging EBCDIC data transferred "
         "from z/OS to distributed systems."),
        ("ABEND Codes",          "ABEND Code Reference",
         "Common S-codes and U-codes with causes and recommended fixes "
         "for fast problem determination."),
        ("JCL Snippets",         "JCL Snippet Library",
         "18 ready-to-use JCL patterns: job cards, SORT, IDCAMS, "
         "IEBGENER, conditional logic, and more."),
        ("File Status Codes",    "File Status Codes",
         "Complete QSAM & VSAM file status code reference with common "
         "causes and recommended COBOL actions."),
        ("Hex-Dec Converter",    "Hex / Dec / Binary Converter",
         "Interactive decimal ↔ hex ↔ binary ↔ octal converter plus "
         "a quick reference table for 0–255."),
        ("Date Formats",         "Date Format Reference",
         "11 mainframe date formats (YYYYMMDD, Julian, packed, SQL) "
         "with COBOL functions and date calculator."),
        ("COBOL Verbs",          "COBOL Verb Reference",
         "35+ COBOL verbs with syntax, description, key clauses, "
         "and copy-paste examples."),
        ("DB2-SQL Helper",       "DB2 / Embedded SQL",
         "12 essential DB2 COBOL patterns: SELECT, cursor, INSERT, "
         "UPDATE, DELETE, SQLCODE reference, type mapping."),
    ]

    bg_colors = [
        "1B5E20", "2E7D32", "388E3C", "43A047", "66BB6A",
        "1565C0", "1976D2", "1E88E5", "4CAF50", "8BC34A", "689F38"
    ]

    start_row = 5
    col_pairs = [(2, 6), (7, 11)]  # two columns of cards

    for i, (sheet_name, title, desc) in enumerate(cards):
        row = start_row + (i // 2) * 6
        col_start = col_pairs[i % 2][0]
        col_end   = col_pairs[i % 2][1]
        bg = bg_colors[i % len(bg_colors)]

        # Card header
        ws.merge_cells(f"{get_column_letter(col_start)}{row}:"
                       f"{get_column_letter(col_end)}{row}")
        hdr = ws.cell(row=row, column=col_start, value=title)
        hdr.fill = fill(bg)
        hdr.font = Font(name="Calibri", size=12, bold=True, color=C_WHITE)
        hdr.alignment = center()
        ws.row_dimensions[row].height = 22

        # Card body
        ws.merge_cells(f"{get_column_letter(col_start)}{row+1}:"
                       f"{get_column_letter(col_end)}{row+3}")
        body = ws.cell(row=row+1, column=col_start, value=desc)
        body.fill = fill("F9FBE7")
        body.font = Font(name="Calibri", size=10, color="33691E")
        body.alignment = Alignment(horizontal="left", vertical="top",
                                   wrap_text=True, indent=1)
        for r2 in range(row+1, row+4):
            ws.row_dimensions[r2].height = 16

        # Navigation note
        ws.merge_cells(f"{get_column_letter(col_start)}{row+4}:"
                       f"{get_column_letter(col_end)}{row+4}")
        nav = ws.cell(row=row+4, column=col_start,
                      value=f"→ Sheet: {sheet_name}")
        nav.fill = fill(bg)
        nav.font = Font(name="Calibri", size=9, italic=True, color="FFFFFF")
        nav.alignment = center()
        ws.row_dimensions[row+4].height = 14

        # Gap row
        ws.row_dimensions[row+5].height = 6

    # Footer
    footer_row = start_row + (len(cards) // 2 + 1) * 6 + 2
    ws.merge_cells(f"B{footer_row}:K{footer_row}")
    ws[f"B{footer_row}"] = (
        "Generated for COBOL / z/OS developers  |  "
        "Tip: Enable macros for extended functionality  |  "
        f"Sheet count: {len(cards) + 1}"
    )
    ws[f"B{footer_row}"].font = Font(name="Calibri", size=9,
                                     italic=True, color="757575")
    ws[f"B{footer_row}"].alignment = center()

    for col in range(1, 13):
        ws.column_dimensions[get_column_letter(col)].width = 12
    ws.column_dimensions["A"].width = 2
    ws.column_dimensions["L"].width = 2

# ══════════════════════════════════════════════════════════════════════════════
# Main builder
# ══════════════════════════════════════════════════════════════════════════════
def build_workbook(path="COBOL_Mainframe_Toolkit.xlsx"):
    wb = openpyxl.Workbook()
    # Remove default sheet
    wb.remove(wb.active)

    print("Building sheets…")
    sheet_dashboard(wb)
    print("  [1/11] HOME")
    sheet_pic_calculator(wb)
    print("  [2/11] PIC Calculator")
    sheet_record_layout(wb)
    print("  [3/11] Record Layout")
    sheet_comp3(wb)
    print("  [4/11] COMP-3 Packed Decimal")
    sheet_ebcdic(wb)
    print("  [5/11] EBCDIC-ASCII Reference")
    sheet_abends(wb)
    print("  [6/11] ABEND Codes")
    sheet_jcl(wb)
    print("  [7/11] JCL Snippets")
    sheet_file_status(wb)
    print("  [8/11] File Status Codes")
    sheet_hex_converter(wb)
    print("  [9/11] Hex-Dec Converter")
    sheet_dates(wb)
    print(" [10/11] Date Formats")
    sheet_verbs(wb)
    print(" [11/11] COBOL Verbs")
    sheet_db2(wb)
    print(" [12/12] DB2-SQL Helper")

    # Workbook-level properties
    wb.properties.title    = "COBOL / z/OS Mainframe Developer Toolkit"
    wb.properties.creator  = "Mainframe Toolkit Generator"
    wb.properties.subject  = "COBOL, z/OS, JCL, DB2, Mainframe"
    wb.properties.keywords = "COBOL COMP-3 EBCDIC JCL DB2 ABEND zOS mainframe"

    wb.save(path)
    print(f"\nSaved → {path}")
    return path

if __name__ == "__main__":
    build_workbook()
