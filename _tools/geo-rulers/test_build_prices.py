#!/usr/bin/env python3
"""Checks of build_prices.py. Run: python3 tool/prices/test_build_prices.py

No network: the spreadsheets are made here, in memory.
"""

import io
import json
import os
import sys
import tempfile
import unittest
import zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_prices as bp  # noqa: E402


def col(n):
    s = ''
    n += 1
    while n:
        n, r = divmod(n - 1, 26)
        s = chr(65 + r) + s
    return s


def xlsx(months=30, first=(2024, 1), drop=None, bad=None, names=None,
         sheet='Monthly Prices', gap_at=None):
    """A small Pink Sheet look-alike. [drop]: a column name to leave out;
    [bad]: (column name, row number from 0, text)."""
    names = names or [c for _, c in bp.SERIES]
    header = ['', 'Crude oil, Brent'] + [
        n.title() + (' **' if i % 5 == 0 else '') for i, n in enumerate(names)
        if n != drop]
    units = ['', '($/bbl)'] + ['($/mt)' for n in names if n != drop]
    rows = [['World Bank Commodity Price Data (The Pink Sheet)'], [],
            ['Updated on November 03, 2026'], header, units]
    y, m = first
    for i in range(months):
        if gap_at == i:
            m += 1
        row = ['%04dM%02d' % (y, m), '80'] + [
            str(100 + i + j) for j, n in enumerate(names) if n != drop]
        if bad and bad[1] == i:
            row[header.index(next(h for h in header
                                  if bp._clean(h) == bad[0]))] = bad[2]
        rows.append(row)
        m += 1
        if m > 12:
            y, m = y + 1, 1
    out = ['<worksheet xmlns="%s"><sheetData>' % bp.M[1:-1]]
    for r, row in enumerate(rows):
        out.append('<row r="%d">' % (r + 1))
        for c, text in enumerate(row):
            if text == '':
                continue
            out.append('<c r="%s%d" t="inlineStr"><is><t>%s</t></is></c>'
                       % (col(c), r + 1, text))
        out.append('</row>')
    out.append('</sheetData></worksheet>')
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w') as z:
        z.writestr('xl/workbook.xml',
                   '<workbook xmlns="%s" xmlns:r="%s"><sheets>'
                   '<sheet name="%s" sheetId="1" r:id="rId1"/></sheets></workbook>'
                   % (bp.M[1:-1], bp.R[1:-1], sheet))
        z.writestr('xl/_rels/workbook.xml.rels',
                   '<Relationships xmlns="%s"><Relationship Id="rId1" '
                   'Target="worksheets/sheet1.xml"/></Relationships>' % bp.PR[1:-1])
        z.writestr('xl/worksheets/sheet1.xml', ''.join(out))
    return buf.getvalue()


def read(path):
    with open(path, encoding='utf-8') as f:
        return f.read()


class BuildTest(unittest.TestCase):
    def setUp(self):
        self._start = bp.START
        bp.START = (2024, 1)

    def tearDown(self):
        bp.START = self._start

    def test_builds_every_series(self):
        d = bp.build(xlsx())
        self.assertEqual(d['v'], 1)
        self.assertEqual(d['asOf'], '2026-06')
        self.assertEqual(list(d['series']), [s for s, _ in bp.SERIES])
        gold = d['series']['gold']
        self.assertEqual(gold['unit'], '$/mt')
        self.assertEqual(gold['start'], '2024-01')
        self.assertEqual(gold['values'][:2], [100, 101])
        self.assertEqual(len(gold['values']), 30)
        self.assertEqual(d['source']['released'], '2026-11-03')
        self.assertIn('CC BY 4.0', d['source']['licence'])
        self.assertNotIn('crude', json.dumps(d).lower())

    def test_missing_values_become_null_and_ends_are_trimmed(self):
        d = bp.build(xlsx(bad=('tin', 0, '…')))
        self.assertEqual(d['series']['tin']['start'], '2024-02')
        d = bp.build(xlsx(bad=('tin', 5, '...')))
        self.assertIsNone(d['series']['tin']['values'][5])

    def test_fails_loudly(self):
        cases = {
            'missing series': dict(drop='gold'),
            'zero price': dict(bad=('copper', 3, '0')),
            'negative price': dict(bad=('copper', 3, '-4')),
            'text for a price': dict(bad=('copper', 3, 'abc')),
            'wrong sheet': dict(sheet='Other'),
            'too short': dict(months=10),
            'month missing': dict(gap_at=7),
        }
        for name, kw in cases.items():
            with self.assertRaises(bp.BuildError, msg=name):
                bp.build(xlsx(**kw))
        with self.assertRaises(bp.BuildError):
            bp.build(b'<html>not a spreadsheet</html>')

    def test_never_a_step_back(self):
        old = bp.build(xlsx(months=30))
        bp.check_against(old, bp.build(xlsx(months=30)))
        bp.check_against(old, bp.build(xlsx(months=31)))
        with self.assertRaises(bp.BuildError):  # older newest month
            bp.check_against(old, bp.build(xlsx(months=29)))
        with self.assertRaises(bp.BuildError):  # a jump of years
            bp.check_against(old, bp.build(xlsx(months=45)))
        fewer = bp.build(xlsx(months=31))
        del fewer['series']['urea']
        with self.assertRaises(bp.BuildError):  # a series disappears
            bp.check_against(old, fewer)
        unit = bp.build(xlsx(months=31))
        unit['series']['gold']['unit'] = '$/kg'
        with self.assertRaises(bp.BuildError):
            bp.check_against(old, unit)
        jump = bp.build(xlsx(months=31))
        jump['series']['gold']['values'][-1] *= 9
        with self.assertRaises(bp.BuildError):
            bp.check_against(old, jump)
        with self.assertRaises(bp.BuildError):
            bp.check_against({'hello': 1}, old)

    def test_main_writes_only_good_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            src = os.path.join(tmp, 'in.xlsx')
            out = os.path.join(tmp, 'data', 'prices.json')
            with open(src, 'wb') as f:
                f.write(xlsx(months=30))
            self.assertEqual(bp.main(['--xlsx', src, '--out', out]), 0)
            first = read(out)
            self.assertEqual(json.loads(first)['asOf'], '2026-06')
            # The same data again: nothing changes.
            self.assertEqual(bp.main(['--xlsx', src, '--out', out]), 0)
            self.assertEqual(read(out), first)
            # An older or broken file: error, the good file stays.
            for bad in (xlsx(months=28), xlsx(drop='zinc'), b'junk'):
                with open(src, 'wb') as f:
                    f.write(bad)
                self.assertEqual(bp.main(['--xlsx', src, '--out', out]), 1)
                self.assertEqual(read(out), first)
            self.assertEqual(os.listdir(os.path.dirname(out)), ['prices.json'])

    def test_link_is_found_on_the_page(self):
        html = ('<a href="https:\\/\\/thedocs.worldbank.org\\/en\\/doc\\/abc-005'
                '\\/related\\/CMO-Historical-Data-Monthly.xlsx">Monthly</a>'
                '<a href="https://evil.example/CMO-Historical-Data-Monthly.xlsx">')
        links = bp.LINK_RE.findall(html.replace('\\/', '/'))
        self.assertEqual(links, ['https://thedocs.worldbank.org/en/doc/abc-005'
                                 '/related/CMO-Historical-Data-Monthly.xlsx'])
        self.assertTrue(bp.LINK_RE.fullmatch(bp.LAST_KNOWN_URL))

    def test_fetch_takes_the_link_from_the_page_or_the_last_known_one(self):
        real = bp._get
        asked = []
        book = xlsx()

        def page_ok(url, limit):
            asked.append(url)
            if url == bp.PAGE_URL:
                return (b'<a href="https://thedocs.worldbank.org/en/doc/new-2027'
                        b'/related/CMO-Historical-Data-Monthly.xlsx">x</a>')
            return book

        def page_down(url, limit):
            asked.append(url)
            if url == bp.PAGE_URL:
                raise OSError('page not reachable')
            return book

        def not_a_file(url, limit):
            return b'<html>Access denied</html>'

        try:
            bp._get = page_ok
            self.assertEqual(bp.build(bp.fetch())['asOf'], '2026-06')
            self.assertEqual(asked[-1], 'https://thedocs.worldbank.org/en/doc/'
                             'new-2027/related/CMO-Historical-Data-Monthly.xlsx')
            bp._get = page_down
            self.assertEqual(bp.build(bp.fetch())['asOf'], '2026-06')
            self.assertEqual(asked[-1], bp.LAST_KNOWN_URL)
            bp._get = not_a_file
            with self.assertRaises(bp.BuildError):
                bp.fetch()
            with tempfile.TemporaryDirectory() as tmp:
                out = os.path.join(tmp, 'prices.json')
                self.assertEqual(bp.main(['--fetch', '--out', out]), 1)
                self.assertFalse(os.path.exists(out))
        finally:
            bp._get = real
        with self.assertRaises(bp.BuildError):  # never plain http
            bp._get('http://example.org/x', 10)


if __name__ == '__main__':
    unittest.main()
