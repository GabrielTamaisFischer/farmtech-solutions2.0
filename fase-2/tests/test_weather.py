import sys
import unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"python"))
import weather
class WeatherTests(unittest.TestCase):
    def payload(self,mm=0,prob=0):
        return {"hourly":{"time":[f"2026-09-25T{h:02d}:00" for h in range(6)],"precipitation":[mm]*6,"precipitation_probability":[prob]*6}}
    def test_sem_chuva(self): self.assertEqual(weather.analisar(self.payload())["comando"],"RAIN=0")
    def test_volume(self): self.assertEqual(weather.analisar(self.payload(.2))["comando"],"RAIN=1")
    def test_probabilidade_limite(self): self.assertEqual(weather.analisar(self.payload(0,60))["comando"],"RAIN=1")
    def test_respostas_invalidas(self):
        for bad in (None,-1,float('nan'),True,101):
            p=self.payload(); p['hourly']['precipitation_probability'][0]=bad
            with self.subTest(bad=bad), self.assertRaises(ValueError): weather.analisar(p)
    def test_horas_incompletas(self):
        p=self.payload(); p['hourly']['time'].pop()
        with self.assertRaises(ValueError): weather.analisar(p)
    def test_horas_desordenadas(self):
        p=self.payload(); p['hourly']['time'].reverse()
        with self.assertRaises(ValueError): weather.analisar(p)
    def test_timeout(self):
        with patch('weather.urlopen',side_effect=TimeoutError),self.assertRaises(TimeoutError): weather.consultar()
    def test_coordenadas(self):
        for lat in (91,float('nan')):
            with self.assertRaises(ValueError): weather.consultar(latitude=lat)
if __name__ == '__main__': unittest.main()
