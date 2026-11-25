import csv
import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('analyze_demo', ROOT/'scripts/analyze_demo.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class SQLAnalysisTests(unittest.TestCase):
    def test_complete_demo_and_source_preservation(self):
        source = ROOT/'data/demo.sql'
        original = source.read_bytes()
        with tempfile.TemporaryDirectory() as folder:
            result = module.analyze(source, Path(folder))
            self.assertEqual(result['employee_count'], 30)
            self.assertEqual(result['shareholder_count'], 10)
            self.assertEqual(result['total_monthly_payroll_zar'], 1215000)
            self.assertEqual(result['total_shareholding_percent'], '100')
            self.assertEqual(result['total_shares'], 10000)
            with (Path(folder)/'employee_salaries_demo.csv').open(encoding='utf-8-sig', newline='') as f:
                rows = list(csv.DictReader(f, delimiter=';'))
            self.assertEqual(rows[25]['full_name'], "Example Employee's Record 026")
        self.assertEqual(source.read_bytes(), original)

    def test_escaped_apostrophe_and_quoted_semicolon(self):
        sql = """INSERT INTO staff (id,full_name,job_title,department,monthly_salary_zar)
        VALUES (1,'Employee''s example ; test','Demo','IT',100);
        INSERT INTO shareholders (id,shareholder_name,share_percent,shares_held,share_class)
        VALUES (1,'Synthetic Organization',100,10,'Demo');"""
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder)/'demo.sql'; source.write_text(sql)
            output = Path(folder)/'outputs'
            result = module.analyze(source, output)
            self.assertEqual(result['employee_count'], 1)
            with (output/'employee_salaries_demo.csv').open(encoding='utf-8-sig', newline='') as f:
                row = next(csv.DictReader(f, delimiter=';'))
            self.assertEqual(row['full_name'], "Employee's example ; test")


if __name__ == '__main__':
    unittest.main()
