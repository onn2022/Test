import re, json, os, glob
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

OP   = re.compile(r'^\s*(COMPUTE|MULTIPLY|DIVIDE|SUBTRACT|ADD)\s+(.+)', re.I)
STOP = re.compile(r'^\s*(?:IF|ELSE|END-|MOVE|PERFORM|GO\s|GOBACK|CALL|EXEC|DISPLAY|READ|WRITE|REWRITE|DELETE|OPEN|CLOSE|SET|EVALUATE|WHEN|CONTINUE|EXIT|INITIALIZE|ACCEPT|STRING|UNSTRING|INSPECT|SEARCH|STOP|COMPUTE|MULTIPLY|DIVIDE|SUBTRACT|ADD)\b', re.I)
PARA = re.compile(r'^\s{0,4}([A-Z0-9][A-Z0-9-]{2,30})\s*(SECTION)?\s*\.\s*$')

def load(path):
    """Return list of (lineno, code, is_comment, comment_text)."""
    out = []
    for n, line in enumerate(open(path, encoding='utf-8', errors='replace').read().splitlines(), 1):
        ind = line[6] if len(line) > 6 else ' '
        body = line[7:72] if len(line) > 7 else ''
        if ind in '*/':
            out.append((n, '', True, body.rstrip()))
        else:
            out.append((n, body.rstrip(), False, ''))
    return out

def statements(rows):
    """Yield dicts for each arithmetic statement, with paragraph + preceding comments."""
    para = ''
    recent = []          # rolling window of recent comment lines
    for i, (ln, code, iscmt, cmt) in enumerate(rows):
        if iscmt:
            t = cmt.strip().strip('*').strip()
            if t and not re.fullmatch(r'[-=*+_ ]+', t):
                recent.append(t)
                recent[:] = recent[-6:]
            continue
        if not code.strip():
            continue
        p = PARA.match(code)
        if p:
            para = p.group(1)
            recent.clear()
            continue
        m = OP.match(code)
        if not m:
            continue
        parts = [code.strip()]
        end = ln
        if not re.search(r'\.(?:\s|$)', code):
            for ln2, code2, iscmt2, _ in rows[i+1:i+19]:
                if iscmt2 or not code2.strip():
                    continue
                if STOP.match(code2) or PARA.match(code2):
                    break
                parts.append(code2.strip())
                end = ln2
                if re.search(r'\.(?:\s|$)', code2):
                    break
        yield {
            'op': m.group(1).upper(),
            'para': para,
            'line_start': ln,
            'line_end': end,
            'stmt': re.sub(r'\s+', ' ', ' '.join(parts)).strip(),
            'comments': ' / '.join(recent[-3:]),
        }

# ---- domain classification -------------------------------------------------
DOMAINS = [
    ('Interest / finance charge', r'\b(FIN[A-Z]*-?CHG|FINCHG|FIN-CHARGE|INT-RATE|INTEREST|INTRST|APR|DAILY-RATE|PER-DIEM|ADB|AVG-DAILY|AVERAGE-DAILY|CYCLE-INT|RETAIL-INT|CASH-INT|ACCRU)\w*'),
    ('Cash advance',             r'\b(CASH-ADV|CSH-ADV|CASHADV|ADVANCE)\w*'),
    ('Late / penalty charge',    r'\b(LATE|PENALT|OVERLIMIT|OVER-LIMIT|OVRLMT|DELINQ|DLQ)\w*'),
    ('Tax (GST/SST/service tax)',r'\b(GST|SST|TAX|SVC-TAX|SERVICE-TAX)\w*'),
    ('Rewards / points / rebate',r'\b(POINT|BONUS|REWARD|REBATE|REDEEM|REDMP|CASHBACK|CASH-BACK)\w*'),
    ('Instalment / EPP',         r'\b(INSTAL|INSTL|EPP|IPP|TENURE|MTHLY-PRIN|PRINCIPAL)\w*'),
    ('Minimum payment / due',    r'\b(MIN-PAY|MINPAY|MIN-PYMT|MIN-DUE|MINIMUM|AMT-DUE|AMOUNT-DUE|PAY-DUE)\w*'),
    ('Currency conversion / FX', r'\b(CONV|EXCH|FOREX|FX-|RATE-TBL|CURR-RATE|CNV-RATE|USD|DEST-AMT|SETL-AMT|SETTLE)\w*'),
    ('Interchange / MDR / fees', r'\b(INTCHG|INTERCHANGE|MDR|DISCOUNT|DISC-RATE|COMM|MERCH-FEE|MSF)\w*'),
    ('Fees (annual/service/misc)',r'\b(FEE|ANNUAL|SVC-CHG|SERVICE-CHG|CHARGE)\w*'),
    ('Balances / ageing / cycle', r'\b(BAL|BALANCE|AGE|AGEING|AGING|BUCKET|CYCLE-TO-DATE|CTD|YTD|MTD|OUTSTAND)\w*'),
    ('Credit limit / exposure',  r'\b(LIMIT|LMT|EXPOSURE|AVAIL|OPEN-TO-BUY|OTB)\w*'),
    ('GL / provision / accounting', r'\b(GL-|GENERAL-LEDGER|PROVISION|PROVSN|WRITE-OFF|WRTOFF|CHARGE-OFF|RECOVER)\w*'),
    ('Merchant volume / settlement', r'\b(MERCH|VOLUME|VOL-|SUBMIT|DEPOSIT|SETLMT|NET-DEP)\w*'),
    ('Payment / credit posting', r'\b(PAYMENT|PYMT|PMT|CREDIT|REFUND|REVERSAL|ADJUST|ADJ-)\w*'),
]
MONEY = re.compile(r'AMT|AMOUNT|BAL(?:ANCE)?|INTEREST|INT-|FEE|CHARGE|CASH|PAY(?:M|MENT)|PMT|PRINCIPAL|PRINC|REBATE|REB-|REWARD|BONUS|POINT|COMM(?:ISSION)?|DISCOUNT|DISC-|TAX|GST|SST|PROFIT|CREDIT|LIMIT|LMT|SETTLE|REFUND|EXCHANGE|RATE|REVENUE|COST|PROVISION|INCOME|ACCRU|GROSS|NETT', re.I)

def classify(s):
    hits = [name for name, pat in DOMAINS if re.search(pat, s, re.I)]
    return hits[0] if hits else 'Other / aggregation'

def target(stmt, op):
    if op == 'COMPUTE':
        m = re.match(r'COMPUTE\s+([A-Z0-9][\w-]*(?:\s*\([^)]*\))?)', stmt, re.I)
        return m.group(1) if m else ''
    m = re.search(r'\b(?:GIVING|TO|FROM|BY)\s+([A-Z0-9][\w-]*)', stmt, re.I)
    return m.group(1) if m else ''

rows_out = []
for path in sorted(glob.glob(D + '/*.txt')):
    member = os.path.basename(path)[:-4]
    rows = load(path)
    for st in statements(rows):
        fin = bool(MONEY.search(st['stmt']))
        st.update(member=member, financial=fin,
                  domain=classify(st['stmt'] + ' ' + st['para']) if fin else 'Other / aggregation',
                  target=target(st['stmt'], st['op']))
        rows_out.append(st)

json.dump(rows_out, open(D + '/extracted_statements.json', 'w'), indent=1)
from collections import Counter
print('total arithmetic statements:', len(rows_out))
print('financial (monetary keyword):', sum(r['financial'] for r in rows_out))
print()
c = Counter(r['domain'] for r in rows_out if r['financial'])
for k, v in c.most_common():
    print(f'{v:6d}  {k}')
