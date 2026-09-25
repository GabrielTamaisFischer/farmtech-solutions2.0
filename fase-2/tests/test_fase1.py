import contextlib
import csv
import importlib.util
import io
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('farmtech',ROOT/'farmtech.py')
farmtech=importlib.util.module_from_spec(spec); spec.loader.exec_module(farmtech)
class Fase1Tests(unittest.TestCase):
    def setUp(self):
        for name in ('nomes_cultura','areas_m2','areas_ha','qtd_ruas','comprimento_rua','produtos','metodos','dosagens_ml_m'): getattr(farmtech,name).clear()
    def call(self,fn,inputs):
        with patch('builtins.input',side_effect=inputs),contextlib.redirect_stdout(io.StringIO()): fn()
    def test_ciclo_crud_exportacao(self):
        self.call(farmtech.entrada_dados,['cafe','200','500','10','100','insumo','manual','5']); self.assertEqual(farmtech.areas_m2,[100000]); self.assertEqual(farmtech.areas_ha,[10])
        self.call(farmtech.atualizar_dados,['0','20','200','10'])
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'registros.csv'
            with contextlib.redirect_stdout(io.StringIO()): farmtech.exportar_csv(path)
            rows=list(csv.DictReader(path.open(encoding='utf-8'))); self.assertEqual(float(rows[0]['volume_total_L']),40)
        self.call(farmtech.deletar_dados,['0']); self.assertFalse(farmtech.nomes_cultura); self.assertFalse(farmtech.areas_ha)
    def test_rejeita_nao_finitos_e_negativos(self):
        with patch('builtins.input',side_effect=['nan','inf','-2','abc','0','2,5']),contextlib.redirect_stdout(io.StringIO()): self.assertEqual(farmtech.ler_numero('x'),2.5)
    def test_nome_vazio(self): self.call(farmtech.entrada_dados,['  ']); self.assertFalse(farmtech.nomes_cultura)
    def test_sair(self): self.call(farmtech.menu_principal,['6'])
if __name__=='__main__': unittest.main()
