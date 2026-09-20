# -*- coding: utf-8 -*-
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from catalogue import CATALOGUE, PARAMETERS, PROGRAMS
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import Table, TableStyleInfo
from collections import Counter

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Cardlink_MY_Financial_Computations.xlsx')

FONT = 'Arial'
NAVY   = '1F3864'
HDRFIL = PatternFill('solid', fgColor=NAVY)
SUBFIL = PatternFill('solid', fgColor='D9E2F3')
NOTEFIL= PatternFill('solid', fgColor='FFF2CC')
THIN   = Side(style='thin', color='BFBFBF')
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
MONO   = 'Consolas'

wb = Workbook()

def style_header(ws, row, ncols):
    for c in range(1, ncols + 1):
        cell = ws.cell(row=row, column=c)
        cell.font = Font(name=FONT, bold=True, color='FFFFFF', size=10)
        cell.fill = HDRFIL
        cell.alignment = Alignment(vertical='center', horizontal='left', wrap_text=True)
        cell.border = BORDER
    ws.row_dimensions[row].height = 30

def body(ws, r0, r1, ncols, wrap_cols=(), mono_cols=()):
    for r in range(r0, r1 + 1):
        for c in range(1, ncols + 1):
            cell = ws.cell(row=r, column=c)
            cell.font = Font(name=MONO if c in mono_cols else FONT, size=9)
            cell.alignment = Alignment(vertical='top', wrap_text=(c in wrap_cols))
            cell.border = BORDER

def widths(ws, ws_widths):
    for i, w in enumerate(ws_widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w

# ---------------------------------------------------------------- 1. Read Me
ws = wb.active
ws.title = 'Read Me'
ws['A1'] = 'Cardlink MY — Financial Computations'
ws['A1'].font = Font(name=FONT, bold=True, size=18, color=NAVY)
ws['A2'] = 'Compiled and simplified from the Cardlink II Malaysia COBOL source'
ws['A2'].font = Font(name=FONT, size=11, italic=True, color='595959')

rows = [
 ('', ''),
 ('PURPOSE', ''),
 ('', 'A plain-English catalogue of every money calculation Cardlink MY performs — what each one computes, '
      'the rule in words, the COBOL exactly as written, and the program, paragraph and line it lives at. '
      'It is intended for impact analysis, UAT design, audit and onboarding.'),
 ('', ''),
 ('HOW TO USE THIS WORKBOOK', ''),
 ('Financial Formulas', 'The main deliverable — 98 computations, each with a plain-English rule and the source COBOL. Start here.'),
 ('Summary', 'Counts by domain, for both the simplified catalogue and the raw scan.'),
 ('Parameters & Rates', 'The table and master-file fields that drive the formulas. These are the levers: change a rate here, not in code.'),
 ('Programs', 'What each analysed program does.'),
 ('Arithmetic Detail', 'Every arithmetic statement extracted from the 19 analysed programs, with paragraph and line. Filterable evidence base.'),
 ('MY Scan Coverage', 'Repository-wide inventory: all 4,667 MY members that contain arithmetic, so the coverage of this study can be judged.'),
 ('', ''),
 ('SOURCE', ''),
 ('Repository', 'Cardlink-Source / Current / MY — snapshot "retrofit-mychg-20260919", read from Google Drive (folder: extracted_MY_members).'),
 ('Snapshot date', '19 September 2026'),
 ('Members in snapshot', '21,628 files; 11,650 canonical text members'),
 ('Members containing arithmetic', '4,667'),
 ('Arithmetic statements repository-wide', '86,996'),
 ('Statements with a monetary keyword', '29,239 across 1,359 members'),
 ('Programs read in full for this study', '19 (listed on the Programs tab) — 2,600,000+ lines of COBOL'),
 ('Statements extracted from those 19', '21,738, of which 11,964 carry a monetary keyword'),
 ('', ''),
 ('METHOD', ''),
 ('1. Locate', 'The repository-wide scan ranked members by the number of arithmetic statements carrying monetary keywords.'),
 ('2. Read', 'The top-ranked programs were downloaded and parsed in fixed COBOL format (columns 8-72; column-7 comment lines ignored; '
             'continuation lines joined up to 18 physical lines per statement).'),
 ('3. Classify', 'Each statement was assigned a domain from its target field, its enclosing paragraph name and its operands.'),
 ('4. Simplify', 'The distinct formulas in each domain were read in context — including the surrounding IF conditions that select between '
                 'them — and written up in plain English. Every entry was then re-verified against the source line it cites.'),
 ('', ''),
 ('SCOPE AND LIMITATIONS', ''),
 ('Read this before relying on the workbook', ''),
 ('Coverage', 'The 19 programs read in full hold roughly half of all monetary-keyword arithmetic in the MY repository. '
              'The remaining members are inventoried on the MY Scan Coverage tab but were not read line by line. '
              'Low-volume members may contain formulas not represented here.'),
 ('No COPY expansion', 'Copybooks were not expanded. Arithmetic inside a copybook is attributed to the copybook, not to every program that includes it.'),
 ('Static reading', 'Branches were read, not executed. Which formula actually fires for a given account depends on product configuration '
                    'and on runtime flags that only a live run or a UAT genbase will settle.'),
 ('Rates not included', 'Rate and limit values live in control tables and master records, not in code. The Parameters tab names the fields; '
                        'their current values must come from the production tables.'),
 ('Commented-out code', 'Lines commented out in the source were excluded. Several interest paragraphs carry commented history '
                        '(marked XXX or ***) showing superseded logic; the live path is what is documented.'),
 ('Verification', 'Every one of the 98 catalogue entries was checked back against the cited program, paragraph and line. '
                  'Line numbers are physical line numbers in the snapshot member, not COBOL sequence numbers.'),
 ('', ''),
 ('Prepared', 'Generated 20 September 2026'),
]
r = 4
for k, v in rows:
    ws.cell(row=r, column=1, value=k)
    ws.cell(row=r, column=2, value=v)
    a = ws.cell(row=r, column=1); b = ws.cell(row=r, column=2)
    if k and not v:
        a.font = Font(name=FONT, bold=True, size=11, color=NAVY)
        a.fill = SUBFIL; b.fill = SUBFIL
    else:
        a.font = Font(name=FONT, bold=True, size=9)
        b.font = Font(name=FONT, size=9)
    b.alignment = Alignment(wrap_text=True, vertical='top')
    a.alignment = Alignment(vertical='top', wrap_text=True)
    r += 1
widths(ws, [34, 108])
ws.sheet_view.showGridLines = False

# ------------------------------------------------- 2. Financial Formulas
ws = wb.create_sheet('Financial Formulas')
ws['A1'] = 'Cardlink MY — financial computations, simplified'
ws['A1'].font = Font(name=FONT, bold=True, size=14, color=NAVY)
ws['A2'] = ('One row per computation. "Rule in plain English" is the explanation; "COBOL as written" is the evidence. '
            'Line = physical line number in the snapshot member.')
ws['A2'].font = Font(name=FONT, size=9, italic=True, color='595959')
hdr = ['ID','Domain','What it computes','Rule in plain English','COBOL as written','Program','Paragraph','Line','Driver fields','Notes']
ws.append([]); ws.append(hdr)
HDR_ROW = 4
for row in CATALOGUE:
    ws.append(list(row))
last = ws.max_row
style_header(ws, HDR_ROW, len(hdr))
body(ws, HDR_ROW + 1, last, len(hdr), wrap_cols=(2,3,4,5,9,10), mono_cols=(5,))
for rr in range(HDR_ROW + 1, last + 1):
    ws.cell(row=rr, column=1).font = Font(name=FONT, size=9, bold=True, color=NAVY)
    ws.cell(row=rr, column=8).alignment = Alignment(horizontal='right', vertical='top')
    nlines = max(str(ws.cell(row=rr, column=5).value or '').count('\n') + 1,
                 len(str(ws.cell(row=rr, column=4).value or '')) // 58 + 1)
    ws.row_dimensions[rr].height = max(30, 12.5 * nlines)
widths(ws, [10, 26, 34, 56, 62, 11, 26, 8, 32, 44])
ws.auto_filter.ref = f'A{HDR_ROW}:J{last}'
ws.freeze_panes = 'D5'
ws.sheet_view.showGridLines = False

# ------------------------------------------------- 3. Summary
ws = wb.create_sheet('Summary')
ws['A1'] = 'Summary'
ws['A1'].font = Font(name=FONT, bold=True, size=14, color=NAVY)

ws['A3'] = 'Simplified catalogue — computations documented by domain'
ws['A3'].font = Font(name=FONT, bold=True, size=11, color=NAVY)
ws.append([]) ; ws['A4'] = 'Domain'; ws['B4'] = 'Computations'; ws['C4'] = 'Programs involved'
doms = sorted(Counter(r[1] for r in CATALOGUE).items(), key=lambda x: -x[1])
r = 5
for dom, n in doms:
    ws.cell(row=r, column=1, value=dom)
    ws.cell(row=r, column=2, value=f"=COUNTIF('Financial Formulas'!$B${HDR_ROW+1}:$B${HDR_ROW+len(CATALOGUE)},$A{r})")
    ws.cell(row=r, column=3, value=', '.join(sorted({x[5] for x in CATALOGUE if x[1] == dom})))
    r += 1
tot = r
ws.cell(row=tot, column=1, value='Total')
ws.cell(row=tot, column=2, value=f'=SUM(B5:B{tot-1})')
style_header(ws, 4, 3)
body(ws, 5, tot, 3, wrap_cols=(1,3))
for c in range(1, 4):
    cell = ws.cell(row=tot, column=c); cell.font = Font(name=FONT, bold=True, size=9); cell.fill = SUBFIL

ws.cell(row=tot+2, column=1, value='Raw scan — arithmetic statements extracted from the 19 programs read in full')
ws.cell(row=tot+2, column=1).font = Font(name=FONT, bold=True, size=11, color=NAVY)
ws.cell(row=tot+3, column=1, value='Classified domain'); ws.cell(row=tot+3, column=2, value='Statements')
ws.cell(row=tot+3, column=3, value='Of which COMPUTE / MULTIPLY / DIVIDE')
stmts = json.load(open(D + '/extracted_statements.json'))
fin = [s for s in stmts if s['financial']]
rawdoms = sorted(Counter(s['domain'] for s in fin).items(), key=lambda x: -x[1])
r = tot + 4
for dom, n in rawdoms:
    ws.cell(row=r, column=1, value=dom)
    ws.cell(row=r, column=2, value=n)
    ws.cell(row=r, column=3, value=sum(1 for s in fin if s['domain'] == dom and s['op'] in ('COMPUTE','MULTIPLY','DIVIDE')))
    r += 1
ws.cell(row=r, column=1, value='Total (monetary-keyword statements)')
ws.cell(row=r, column=2, value=f'=SUM(B{tot+4}:B{r-1})')
ws.cell(row=r, column=3, value=f'=SUM(C{tot+4}:C{r-1})')
style_header(ws, tot+3, 3)
body(ws, tot+4, r, 3, wrap_cols=(1,))
for c in range(1, 4):
    cell = ws.cell(row=r, column=c); cell.font = Font(name=FONT, bold=True, size=9); cell.fill = SUBFIL

n = r + 2
ws.cell(row=n, column=1, value='Note')
ws.cell(row=n, column=1).font = Font(name=FONT, bold=True, size=9)
ws.cell(row=n, column=2, value=('The two tables count different things. The upper table counts distinct business rules written up in this workbook. '
    'The lower table counts individual COBOL statements, most of which are accumulators repeating the same rule — which is why '
    'roughly 12,000 statements reduce to 98 rules. "Other / aggregation" is running totals, subtotals and averages carrying a '
    'monetary keyword but expressing no distinct pricing rule.'))
ws.cell(row=n, column=2).alignment = Alignment(wrap_text=True, vertical='top')
ws.cell(row=n, column=2).font = Font(name=FONT, size=9)
ws.cell(row=n, column=2).fill = NOTEFIL
ws.row_dimensions[n].height = 58
widths(ws, [42, 16, 74])
ws.sheet_view.showGridLines = False

# ------------------------------------------------- 4. Parameters & Rates
ws = wb.create_sheet('Parameters & Rates')
ws['A1'] = 'Parameters and rate drivers'
ws['A1'].font = Font(name=FONT, bold=True, size=14, color=NAVY)
ws['A2'] = ('These fields carry the rates, limits and flags the formulas use. They live in control tables and master records — '
            'changing a price is a data change here, not a code change.')
ws['A2'].font = Font(name=FONT, size=9, italic=True, color='595959')
ws.append([]); ws.append(['Field','Held in','What it controls','Unit','Used by','Program'])
PR = 4
for p in PARAMETERS:
    ws.append(list(p))
last = ws.max_row
style_header(ws, PR, 6)
body(ws, PR+1, last, 6, wrap_cols=(2,3,5), mono_cols=(1,))
widths(ws, [32, 30, 56, 24, 30, 12])
ws.auto_filter.ref = f'A{PR}:F{last}'
ws.freeze_panes = 'A5'
ws.sheet_view.showGridLines = False

# ------------------------------------------------- 5. Programs
ws = wb.create_sheet('Programs')
ws['A1'] = 'Programs read in full for this study'
ws['A1'].font = Font(name=FONT, bold=True, size=14, color=NAVY)
ws.append([]); ws.append([])
ws.append(['Program','Type','Role','Lines','Arithmetic statements','With monetary keyword','Computations documented'])
PG = 4
inv = {x['member']: x for x in json.load(open(D + '/arithmetic_inventory.json'))}
catcount = Counter(r[5] for r in CATALOGUE)
for name, typ, role in PROGRAMS:
    i = inv.get(name, {})
    ws.append([name, typ, role, i.get('lines'), i.get('arithmetic_count'), i.get('candidate_count'), catcount.get(name, 0)])
last = ws.max_row
style_header(ws, PG, 7)
body(ws, PG+1, last, 7, wrap_cols=(3,))
for rr in range(PG+1, last+1):
    ws.cell(row=rr, column=1).font = Font(name=MONO, size=9, bold=True)
    for c in (4,5,6,7):
        ws.cell(row=rr, column=c).number_format = '#,##0'
        ws.cell(row=rr, column=c).alignment = Alignment(horizontal='right', vertical='top')
    ws.row_dimensions[rr].height = 28
tr = last + 1
ws.cell(row=tr, column=1, value='Total')
for c in (4,5,6,7):
    ws.cell(row=tr, column=c, value=f'={get_column_letter(c)}{PG+1}:{get_column_letter(c)}{last}')
    ws.cell(row=tr, column=c).value = f'=SUM({get_column_letter(c)}{PG+1}:{get_column_letter(c)}{last})'
    ws.cell(row=tr, column=c).number_format = '#,##0'
for c in range(1, 8):
    cell = ws.cell(row=tr, column=c); cell.font = Font(name=FONT, bold=True, size=9); cell.fill = SUBFIL; cell.border = BORDER
widths(ws, [12, 10, 78, 10, 14, 14, 14])
ws.sheet_view.showGridLines = False

# ------------------------------------------------- 6. Arithmetic Detail
ws = wb.create_sheet('Arithmetic Detail')
ws['A1'] = 'Every arithmetic statement extracted from the 19 programs read in full'
ws['A1'].font = Font(name=FONT, bold=True, size=14, color=NAVY)
ws['A2'] = ('Evidence base. "Monetary" flags statements whose operands carry a money keyword. '
            'Filter on Domain or Program to trace a rule back to source.')
ws['A2'].font = Font(name=FONT, size=9, italic=True, color='595959')
ws.append([]); ws.append(['Program','Paragraph','Line from','Line to','Operation','Target field','Monetary','Domain','Statement'])
AD = 4
for s in sorted(stmts, key=lambda x: (x['member'], x['line_start'])):
    ws.append([s['member'], s['para'], s['line_start'], s['line_end'], s['op'], s['target'],
               'Yes' if s['financial'] else 'No', s['domain'] if s['financial'] else '', s['stmt']])
last = ws.max_row
style_header(ws, AD, 9)
for rr in range(AD+1, last+1):
    for c in range(1, 10):
        cell = ws.cell(row=rr, column=c)
        cell.font = Font(name=MONO if c in (6, 9) else FONT, size=8)
        cell.alignment = Alignment(vertical='top')
widths(ws, [11, 30, 10, 9, 11, 30, 10, 28, 120])
ws.auto_filter.ref = f'A{AD}:I{last}'
ws.freeze_panes = 'A5'
ws.sheet_view.showGridLines = False

# ------------------------------------------------- 7. MY Scan Coverage
ws = wb.create_sheet('MY Scan Coverage')
ws['A1'] = 'Repository-wide inventory — every MY member containing arithmetic'
ws['A1'].font = Font(name=FONT, bold=True, size=14, color=NAVY)
ws['A2'] = ('All 4,667 members in the 19-Sep-2026 MY snapshot that contain arithmetic. "Read in full" marks the 19 analysed here. '
            'Use this to judge coverage and to pick the next members to document.')
ws['A2'].font = Font(name=FONT, size=9, italic=True, color='595959')
ws.append([]); ws.append(['Member','Path','Lines','Arithmetic statements','With monetary keyword','COMPUTE','MULTIPLY','DIVIDE','ADD / SUBTRACT','Read in full'])
SC = 4
read_full = {p[0] for p in PROGRAMS}
for i in sorted(inv.values(), key=lambda x: (-x['candidate_count'], x['member'])):
    ws.append([i['member'], i['path'], i['lines'], i['arithmetic_count'], i['candidate_count'],
               i['compute'], i['multiply'], i['divide'], i['add_subtract'],
               'Yes' if i['member'] in read_full else ''])
last = ws.max_row
style_header(ws, SC, 10)
for rr in range(SC+1, last+1):
    for c in range(1, 11):
        cell = ws.cell(row=rr, column=c)
        cell.font = Font(name=MONO if c in (1, 2) else FONT, size=8)
        cell.alignment = Alignment(vertical='top', horizontal='right' if c in range(3, 10) else 'left')
        if c in range(3, 10):
            cell.number_format = '#,##0'
    if ws.cell(row=rr, column=10).value == 'Yes':
        for c in range(1, 11):
            ws.cell(row=rr, column=c).fill = SUBFIL
widths(ws, [13, 40, 10, 14, 14, 11, 11, 10, 14, 11])
ws.auto_filter.ref = f'A{SC}:J{last}'
ws.freeze_panes = 'A5'
ws.sheet_view.showGridLines = False

wb.save(OUT)
print('written:', OUT)
print('sheets:', wb.sheetnames)
