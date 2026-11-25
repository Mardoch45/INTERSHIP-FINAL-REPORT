import csv
import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('analyser_demo', ROOT/'scripts/analyser_demo.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class AnalyseExportTests(unittest.TestCase):
    def test_demo_complete_et_source_preservee(self):
        source = ROOT/'data/demo.sql'
        original = source.read_bytes()
        with tempfile.TemporaryDirectory() as folder:
            result = module.analyse(source, Path(folder))
            self.assertEqual(result['employes'], 30)
            self.assertEqual(result['actionnaires'], 10)
            self.assertEqual(result['total_mensuel_zar'], 1215000)
            self.assertEqual(result['participation_totale_pct'], '100')
            self.assertEqual(result['total_parts'], 10000)
            with (Path(folder)/'salaires_demo.csv').open(encoding='utf-8-sig', newline='') as f:
                rows = list(csv.DictReader(f, delimiter=';'))
            self.assertEqual(rows[25]['full_name'], "Employé d'exemple 026")
        self.assertEqual(source.read_bytes(), original)

    def test_apostrophes_et_point_virgule_dans_une_chaine(self):
        sql = """INSERT INTO staff (id,full_name,job_title,department,monthly_salary_zar)
        VALUES (1,'Employé d''exemple ; test','Démo','IT',100);
        INSERT INTO shareholders (id,shareholder_name,share_percent,shares_held,share_class)
        VALUES (1,'Organisation fictive',100,10,'Démo');"""
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder)/'demo.sql'; source.write_text(sql, encoding='utf-8')
            output = Path(folder)/'outputs'
            result = module.analyse(source, output)
            self.assertEqual(result['employes'], 1)
            with (output/'salaires_demo.csv').open(encoding='utf-8-sig', newline='') as f:
                row = next(csv.DictReader(f, delimiter=';'))
            self.assertEqual(row['full_name'], "Employé d'exemple ; test")


if __name__ == '__main__':
    unittest.main()
