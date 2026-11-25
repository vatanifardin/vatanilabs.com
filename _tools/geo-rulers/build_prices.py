#!/usr/bin/env python3
"""Builds prices.json for the Geo-Rulers Market page.

Reads the World Bank "Pink Sheet" monthly file
(CMO-Historical-Data-Monthly.xlsx, CC BY 4.0) and writes the monthly
average prices of the metals and minerals the app shows, as one small
JSON file.

  python3 -I tool/prices/build_prices.py --xlsx data_src/worldbank/CMO-Historical-Data-Monthly.xlsx --out assets/market/prices.json
  python3 -I build_prices.py --fetch --out geo-rulers/data/prices.json

--fetch finds the address of the current file on the World Bank page
(it changes about once a year), downloads it and builds from it.
--print-url only prints the address that --fetch would use.

Python 3 standard library only. The spreadsheet is treated as untrusted
data: it is read as a zip of XML files, nothing in it is run.

The script fails loudly (exit code 1, nothing written) when the result
looks wrong: a series is missing, a value is not positive, the newest
month is older than in the file already there, or the file shrank.
"""

import argparse
import datetime
import io
import json
import os
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
import zipfile

FORMAT_VERSION = 1
SHEET_NAME = 'Monthly Prices'
PAGE_URL = 'https://www.worldbank.org/en/research/commodity-markets'
FILE_NAME = 'CMO-Historical-Data-Monthly.xlsx'
# The address on 25 November 2026; used when the page cannot be read.
LAST_KNOWN_URL = ('https://thedocs.worldbank.org/en/doc/'
                  '74e8be41ceb20fa0da750cda2f6b9e4e-0050012026/related/'
                  + FILE_NAME)
USER_AGENT = 'geo-rulers-prices/1 (monthly data build)'
MAX_DOWNLOAD = 8 * 1024 * 1024  # the file is about 0.6 MB
MAX_XML = 64 * 1024 * 1024  # largest unpacked part we are willing to read

# The first month kept in the output.
START = (1960, 1)

# Our id -> the column name in the spreadsheet (compared in lower case,
# without the "*" marks and extra spaces). Every one must be found.
SERIES = [
    ('gold', 'gold'),
    ('silver', 'silver'),
    ('platinum', 'platinum'),
    ('copper', 'copper'),
    ('aluminium', 'aluminum'),
    ('nickel', 'nickel'),
    ('zinc', 'zinc'),
    ('lead', 'lead'),
    ('tin', 'tin'),
    ('iron_ore', 'iron ore, cfr spot'),
    ('coal_au', 'coal, australian'),
    ('coal_za', 'coal, south african'),
    ('potash', 'potassium chloride'),
    ('phosphate_rock', 'phosphate rock'),
    ('dap', 'dap'),
    ('tsp', 'tsp'),
    ('urea', 'urea'),
]

M = '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}'
R = '{http://schemas.openxmlformats.org/officeDocument/2006/relationships}'
PR = '{http://schemas.openxmlformats.org/package/2006/relationships}'


class BuildError(Exception):
    pass


# ---------- reading the spreadsheet ----------

def _read_part(z, name):
    try:
        info = z.getinfo(name)
    except KeyError:
        raise BuildError('the spreadsheet has no part "%s"' % name)
    if info.file_size > MAX_XML:
        raise BuildError('part "%s" is too large (%d bytes)' % (name, info.file_size))
    data = z.read(name)
    # No DTDs or entities: a spreadsheet never needs them.
    if b'<!DOCTYPE' in data or b'<!ENTITY' in data:
        raise BuildError('part "%s" has a DTD; refusing to read it' % name)
    return ET.fromstring(data)


def _col_index(ref):
    """'BR7' -> 69 (A = 0)."""
    n = 0
    for ch in ref:
        if 'A' <= ch <= 'Z':
            n = n * 26 + (ord(ch) - 64)
        else:
            break
    return n - 1


def read_sheet(xlsx_bytes, sheet_name=SHEET_NAME):
    """Returns the rows of the sheet: a list of {column index: text}."""
    try:
        z = zipfile.ZipFile(io.BytesIO(xlsx_bytes))
    except zipfile.BadZipFile:
        raise BuildError('the file is not an xlsx (zip) file')
    with z:
        wb = _read_part(z, 'xl/workbook.xml')
        rid = None
        for s in wb.iter(M + 'sheet'):
            if (s.get('name') or '').strip().lower() == sheet_name.lower():
                rid = s.get(R + 'id')
        if rid is None:
            raise BuildError('sheet "%s" not found' % sheet_name)
        rels = _read_part(z, 'xl/_rels/workbook.xml.rels')
        target = None
        for rel in rels.iter(PR + 'Relationship'):
            if rel.get('Id') == rid:
                target = rel.get('Target')
        if not target or '..' in target:
            raise BuildError('sheet "%s" has no file' % sheet_name)
        part = target.lstrip('/')
        if not part.startswith('xl/'):
            part = 'xl/' + part
        shared = []
        if 'xl/sharedStrings.xml' in z.namelist():
            for si in _read_part(z, 'xl/sharedStrings.xml').findall(M + 'si'):
                shared.append(''.join(t.text or '' for t in si.iter(M + 't')))
        rows = []
        for row in _read_part(z, part).iter(M + 'row'):
            cells = {}
            for c in row.findall(M + 'c'):
                ref = c.get('r')
                if not ref:
                    continue
                kind = c.get('t')
                if kind == 'inlineStr':
                    text = ''.join(t.text or '' for t in c.iter(M + 't'))
                else:
                    v = c.find(M + 'v')
                    if v is None or v.text is None:
                        continue
                    text = v.text
                    if kind == 's':
                        try:
                            text = shared[int(text)]
                        except (ValueError, IndexError):
                            continue
                cells[_col_index(ref)] = text
            rows.append(cells)
        return rows


def _clean(name):
    return re.sub(r'\s+', ' ', name.replace('*', '')).strip().lower()


MONTH_RE = re.compile(r'^(\d{4})M(\d{2})$')
RELEASE_RE = re.compile(r'Updated on (\w+) (\d{1,2}), (\d{4})')
MONTH_NAMES = ['january', 'february', 'march', 'april', 'may', 'june', 'july',
               'august', 'september', 'october', 'november', 'december']


def month_index(year, month):
    return year * 12 + (month - 1)


def month_text(index):
    return '%04d-%02d' % (index // 12, index % 12 + 1)


def parse_month(text):
    m = re.match(r'^(\d{4})-(\d{2})$', text or '')
    if not m or not 1 <= int(m.group(2)) <= 12:
        raise BuildError('bad month "%s"' % text)
    return month_index(int(m.group(1)), int(m.group(2)))


def build(xlsx_bytes):
    """The prices.json content (a dict) from the bytes of the xlsx file."""
    rows = read_sheet(xlsx_bytes)
    wanted = {col: sid for sid, col in SERIES}

    # The header row is the one that names our columns; units are below it.
    header_at = None
    for i, cells in enumerate(rows[:40]):
        names = {_clean(v) for v in cells.values()}
        if sum(1 for n in wanted if n in names) >= len(wanted) // 2:
            header_at = i
            break
    if header_at is None or header_at + 1 >= len(rows):
        raise BuildError('the header row with the commodity names was not found')
    columns = {}  # series id -> column index
    for col, text in rows[header_at].items():
        sid = wanted.get(_clean(text))
        if sid is not None:
            if sid in columns:
                raise BuildError('column "%s" appears twice' % text)
            columns[sid] = col
    missing = [sid for sid, _ in SERIES if sid not in columns]
    if missing:
        raise BuildError('series not found in the file: ' + ', '.join(missing))
    units = {}
    for sid, col in columns.items():
        unit = (rows[header_at + 1].get(col) or '').strip()
        m = re.match(r'^\((.+)\)$', unit)
        if not m:
            raise BuildError('no unit for "%s" (found "%s")' % (sid, unit))
        units[sid] = re.sub(r'\s+', ' ', m.group(1)).strip()

    released = None
    for cells in rows[:header_at]:
        m = RELEASE_RE.search(cells.get(0) or '')
        if m and m.group(1).lower() in MONTH_NAMES:
            released = '%04d-%02d-%02d' % (
                int(m.group(3)), MONTH_NAMES.index(m.group(1).lower()) + 1,
                int(m.group(2)))

    # Data rows: "1960M01" in the first column, one row per month, in order.
    start = month_index(*START)
    values = {sid: [] for sid in columns}
    expected = None
    for cells in rows[header_at + 2:]:
        m = MONTH_RE.match((cells.get(0) or '').strip())
        if not m:
            continue
        idx = month_index(int(m.group(1)), int(m.group(2)))
        if not 1 <= int(m.group(2)) <= 12:
            raise BuildError('bad month "%s"' % cells.get(0))
        if expected is not None and idx != expected:
            raise BuildError('months are not in order at "%s"' % cells.get(0))
        expected = idx + 1
        if idx < start:
            continue
        if not values[SERIES[0][0]] and idx != start:
            raise BuildError('the file starts after %s' % month_text(start))
        for sid, col in columns.items():
            text = (cells.get(col) or '').strip()
            if text in ('', '…', '...', '..', 'n.a.', 'NA'):
                values[sid].append(None)
                continue
            try:
                v = float(text)
            except ValueError:
                raise BuildError('"%s" is not a number (%s, %s)'
                                 % (text, sid, cells.get(0)))
            if not (v > 0) or v != v or v in (float('inf'),):
                raise BuildError('price not positive: %s (%s, %s)'
                                 % (text, sid, cells.get(0)))
            v = round(v, 2)
            values[sid].append(int(v) if v == int(v) else v)
    months = len(values[SERIES[0][0]])
    if months < 24:
        raise BuildError('only %d months of data' % months)

    # Months at the end that no series has a price for are not data.
    while months and all(values[s][months - 1] is None for s in values):
        months -= 1
    as_of = start + months - 1

    series = {}
    for sid, _ in SERIES:
        v = values[sid][:months]
        first = next((i for i, x in enumerate(v) if x is not None), None)
        if first is None:
            raise BuildError('series "%s" has no prices' % sid)
        last = max(i for i, x in enumerate(v) if x is not None)
        # A series may run a little behind the others, never far behind.
        if months - 1 - last > 3:
            raise BuildError('series "%s" ends in %s, long before %s'
                             % (sid, month_text(start + last), month_text(as_of)))
        if sum(1 for x in v[-24:] if x is not None) < 12:
            raise BuildError('series "%s" has too many gaps in the last two years' % sid)
        series[sid] = {
            'unit': units[sid],
            'start': month_text(start + first),
            'values': v[first:last + 1],
        }
    with_newest = sum(1 for s in series.values()
                      if parse_month(s['start']) + len(s['values']) - 1 == as_of)
    if with_newest < len(series) * 2 // 3:
        raise BuildError('only %d of %d series have a price for %s'
                         % (with_newest, len(series), month_text(as_of)))
    out = {
        'v': FORMAT_VERSION,
        'asOf': month_text(as_of),
        'frequency': 'monthly average',
        'source': {
            'name': 'World Bank Commodity Price Data (The Pink Sheet)',
            'licence': 'CC BY 4.0',
            'url': PAGE_URL,
            'changes': 'adapted: selected series, values rounded to 2 decimals',
        },
        'series': series,
    }
    if released:
        out['source']['released'] = released
    return out


# ---------- checks against the file already there ----------

def check_against(old, new):
    """Raises BuildError when [new] would be a step back from [old]."""
    try:
        old_as_of = parse_month(old['asOf'])
        old_series = old['series']
    except (KeyError, TypeError):
        raise BuildError('the existing output file is not a prices file; '
                         'delete it by hand if it should be replaced')
    new_as_of = parse_month(new['asOf'])
    if new_as_of < old_as_of:
        raise BuildError('newest month %s is older than the %s already there'
                         % (new['asOf'], old['asOf']))
    if new_as_of > old_as_of + 6:
        raise BuildError('newest month jumps from %s to %s; check by hand'
                         % (old['asOf'], new['asOf']))
    for sid, o in old_series.items():
        n = new['series'].get(sid)
        if n is None:
            raise BuildError('series "%s" would disappear' % sid)
        if n['unit'] != o['unit']:
            raise BuildError('unit of "%s" changed from %s to %s'
                             % (sid, o['unit'], n['unit']))
        if parse_month(n['start']) > parse_month(o['start']):
            raise BuildError('series "%s" would start later' % sid)
        if (parse_month(n['start']) + len(n['values'])
                < parse_month(o['start']) + len(o['values'])):
            raise BuildError('series "%s" would end earlier' % sid)
    # A price that moves more than five-fold in a month is a broken file.
    for sid, n in new['series'].items():
        v = [x for x in n['values'][-3:] if x is not None]
        for a, b in zip(v, v[1:]):
            if b > a * 5 or b < a / 5:
                raise BuildError('price of "%s" jumps from %s to %s' % (sid, a, b))


def encode(data):
    """Compact, stable text: the same data always gives the same bytes."""
    return json.dumps(data, ensure_ascii=False, separators=(',', ':'),
                      sort_keys=False) + '\n'


# ---------- finding and downloading the current file ----------

def _get(url, limit):
    if not url.lower().startswith('https://'):
        raise BuildError('refusing a non-https address: ' + url)
    req = urllib.request.Request(url, headers={
        'User-Agent': USER_AGENT,
        'Accept': '*/*',
    })
    with urllib.request.urlopen(req, timeout=60) as resp:
        if resp.status != 200:
            raise BuildError('HTTP %s from %s' % (resp.status, url))
        data = resp.read(limit + 1)
    if len(data) > limit:
        raise BuildError('answer from %s is larger than %d bytes' % (url, limit))
    return data


LINK_RE = re.compile(
    r'https://[A-Za-z0-9./_-]*worldbank\.org/[A-Za-z0-9./_%-]*'
    + re.escape(FILE_NAME))


def find_url():
    """The address of the current monthly file, and where it came from."""
    try:
        html = _get(PAGE_URL, 4 * 1024 * 1024).decode('utf-8', 'replace')
        links = LINK_RE.findall(html.replace('\\/', '/'))
        if links:
            return links[0], 'World Bank page'
        print('warning: no link to %s on %s' % (FILE_NAME, PAGE_URL),
              file=sys.stderr)
    except Exception as e:  # network errors: use the last known address
        print('warning: could not read %s (%s)' % (PAGE_URL, e), file=sys.stderr)
    return LAST_KNOWN_URL, 'last known address'


def fetch():
    url, origin = find_url()
    print('downloading %s (%s)' % (url, origin))
    try:
        data = _get(url, MAX_DOWNLOAD)
    except BuildError:
        raise
    except Exception as e:
        raise BuildError('download failed: %s' % e)
    if data[:2] != b'PK':
        raise BuildError('the download is not an xlsx file (it starts with %r)'
                         % data[:20])
    return data


# ---------- main ----------

def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    src = p.add_mutually_exclusive_group(required=True)
    src.add_argument('--xlsx', help='path of CMO-Historical-Data-Monthly.xlsx')
    src.add_argument('--fetch', action='store_true',
                     help='find and download the current file')
    src.add_argument('--print-url', action='store_true',
                     help='print the address --fetch would download, and stop')
    p.add_argument('--out', help='path of prices.json to write')
    args = p.parse_args(argv)

    try:
        if args.print_url:
            url, origin = find_url()
            print('%s (%s)' % (url, origin))
            return 0
        if not args.out:
            raise BuildError('--out is needed')
        if args.fetch:
            raw = fetch()
        else:
            with open(args.xlsx, 'rb') as f:
                raw = f.read()
        new = build(raw)
        text = encode(new)
        old_text = None
        if os.path.exists(args.out):
            with open(args.out, 'r', encoding='utf-8') as f:
                old_text = f.read()
            try:
                old = json.loads(old_text)
            except ValueError:
                raise BuildError('the existing %s is not JSON; delete it by '
                                 'hand if it should be replaced' % args.out)
            check_against(old, new)
        n = len(new['series'])
        if old_text == text:
            print('no change: %s is already up to date (%d series, to %s)'
                  % (args.out, n, new['asOf']))
            return 0
        os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
        tmp = args.out + '.tmp'
        with open(tmp, 'w', encoding='utf-8', newline='\n') as f:
            f.write(text)
        os.replace(tmp, args.out)
        print('wrote %s: %d series, to %s, %d bytes (built %s)'
              % (args.out, n, new['asOf'], len(text.encode('utf-8')),
                 datetime.date.today().isoformat()))
        return 0
    except BuildError as e:
        print('ERROR: %s' % e, file=sys.stderr)
        print('Nothing was written.', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
