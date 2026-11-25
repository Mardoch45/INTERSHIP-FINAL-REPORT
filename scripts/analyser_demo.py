#!/usr/bin/env python3
"""Analyse de deux tables d'un export de démonstration, uniquement en local."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sqlite3
from decimal import Decimal
from pathlib import Path


def insert_statements(sql: str):
    """Trouve la fin des INSERT en tenant compte des chaînes SQL citées."""
    pattern = re.compile(r'INSERT\s+INTO\s+`?(staff|shareholders)`?\s*\(', re.I)
    for start in pattern.finditer(sql):
        for end in re.finditer(';', sql[start.start():]):
            candidate = sql[start.start():start.start()+end.end()]
            if sqlite3.complete_statement(candidate):
                yield candidate
                break
        else:
            raise ValueError('Instruction INSERT incomplète.')


def analyse(source: Path, output: Path) -> dict:
    initial = source.read_bytes()
    sql = initial.decode('utf-8')
    db = sqlite3.connect(':memory:')
    db.row_factory = sqlite3.Row
    db.execute('CREATE TABLE staff (id INTEGER PRIMARY KEY, full_name TEXT, job_title TEXT, department TEXT, monthly_salary_zar INTEGER)')
    db.execute('CREATE TABLE shareholders (id INTEGER PRIMARY KEY, shareholder_name TEXT, share_percent NUMERIC, shares_held INTEGER, share_class TEXT)')
    statements = list(insert_statements(sql))
    if not statements:
        raise ValueError('Aucun INSERT des tables de démonstration trouvé.')
    for statement in statements:
        # Les CREATE, DROP, LOCK, SET et commandes du serveur ne sont pas importés.
        # execute() ne permet pas d'enchaîner plusieurs instructions ici.
        db.execute(statement)
    staff = [dict(row) for row in db.execute('SELECT * FROM staff ORDER BY id')]
    holders = [dict(row) for row in db.execute('SELECT * FROM shareholders ORDER BY id')]
    if not staff or not holders:
        raise ValueError('Les deux tables doivent contenir des lignes.')
    if any(not isinstance(row['monthly_salary_zar'], int) or row['monthly_salary_zar'] < 0 for row in staff):
        raise ValueError('Salaires de démonstration invalides.')
    percent = sum(Decimal(str(row['share_percent'])) for row in holders)
    shares = sum(row['shares_held'] for row in holders)
    result = {
        'jeu': 'Données de démonstration ; vérifier la provenance avant interprétation',
        'employes': len(staff), 'actionnaires': len(holders),
        'total_mensuel_zar': sum(row['monthly_salary_zar'] for row in staff),
        'participation_totale_pct': str(percent), 'total_parts': shares,
        'participations_100_pct': percent == 100,
        'sha256_source': hashlib.sha256(initial).hexdigest(),
    }
    output.mkdir(parents=True, exist_ok=True)
    for name, rows in [('salaires_demo.csv', staff), ('actionnaires_demo.csv', holders)]:
        with (output/name).open('w', encoding='utf-8-sig', newline='') as stream:
            writer = csv.DictWriter(stream, fieldnames=list(rows[0]), delimiter=';')
            writer.writeheader(); writer.writerows(rows)
    (output/'synthese_demo.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    if source.read_bytes() != initial:
        raise RuntimeError('Le fichier source a changé durant l’analyse.')
    db.close()
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, default=Path('data/demo.sql'))
    parser.add_argument('--output', type=Path, default=Path('outputs'))
    args = parser.parse_args()
    print(json.dumps(analyse(args.source, args.output), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
