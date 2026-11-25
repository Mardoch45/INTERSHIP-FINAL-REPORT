#!/usr/bin/env python3
"""Analyze the two demonstration SQL tables locally without a server connection."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sqlite3
from decimal import Decimal
from pathlib import Path


def insert_statements(sql):
    """Find statement endings without splitting quoted SQL string values."""
    pattern = re.compile(r'INSERT\s+INTO\s+`?(staff|shareholders)`?\s*\(', re.I)
    for start in pattern.finditer(sql):
        for end in re.finditer(';', sql[start.start():]):
            statement = sql[start.start():start.start()+end.end()]
            if sqlite3.complete_statement(statement):
                yield statement
                break
        else:
            raise ValueError('Incomplete INSERT statement.')


def analyze(source, output):
    original = source.read_bytes()
    sql = original.decode('utf-8')
    db = sqlite3.connect(':memory:')
    db.row_factory = sqlite3.Row
    db.execute('CREATE TABLE staff (id INTEGER PRIMARY KEY, full_name TEXT, job_title TEXT, department TEXT, monthly_salary_zar INTEGER)')
    db.execute('CREATE TABLE shareholders (id INTEGER PRIMARY KEY, shareholder_name TEXT, share_percent NUMERIC, shares_held INTEGER, share_class TEXT)')
    statements = list(insert_statements(sql))
    if not statements:
        raise ValueError('No INSERT statements for the demonstration tables were found.')
    for statement in statements:
        # Ignore the dump's CREATE, DROP, LOCK and SET statements.
        # execute() accepts only one statement at a time.
        db.execute(statement)
    employees = [dict(r) for r in db.execute('SELECT * FROM staff ORDER BY id')]
    shareholders = [dict(r) for r in db.execute('SELECT * FROM shareholders ORDER BY id')]
    if not employees or not shareholders:
        raise ValueError('Both demonstration tables must contain records.')
    if any(not isinstance(r['monthly_salary_zar'], int) or r['monthly_salary_zar'] < 0 for r in employees):
        raise ValueError('Invalid demonstration salary value.')
    percent = sum(Decimal(str(r['share_percent'])) for r in shareholders)
    result = {
        'dataset':'Synthetic demonstration data; verify provenance before interpretation',
        'employee_count':len(employees), 'shareholder_count':len(shareholders),
        'total_monthly_payroll_zar':sum(r['monthly_salary_zar'] for r in employees),
        'total_shareholding_percent':str(percent), 'total_shares':sum(r['shares_held'] for r in shareholders),
        'shareholding_equals_100_percent':percent == 100,
        'source_sha256':hashlib.sha256(original).hexdigest(),
    }
    output.mkdir(parents=True, exist_ok=True)
    for name, rows in [('employee_salaries_demo.csv', employees), ('shareholders_demo.csv', shareholders)]:
        with (output/name).open('w', encoding='utf-8-sig', newline='') as stream:
            writer = csv.DictWriter(stream, fieldnames=list(rows[0]), delimiter=';')
            writer.writeheader(); writer.writerows(rows)
    (output/'demo_summary.json').write_text(json.dumps(result, indent=2)+'\n')
    if source.read_bytes() != original:
        raise RuntimeError('The source changed during analysis.')
    db.close()
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, default=Path('data/demo.sql'))
    parser.add_argument('--output', type=Path, default=Path('outputs'))
    args = parser.parse_args()
    print(json.dumps(analyze(args.source, args.output), indent=2))


if __name__ == '__main__':
    main()
