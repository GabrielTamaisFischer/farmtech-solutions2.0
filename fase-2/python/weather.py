"""Open-Meteo -> comando serial manual. Python 3.10+, biblioteca padrao."""
import argparse
import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import urlopen

def analisar(payload):
    """Proximas 6 horas; acumulado >=1 mm OU probabilidade maxima >=60%."""
    if not isinstance(payload, dict): raise ValueError("Resposta JSON nao e um objeto")
    hourly = payload.get("hourly", {})
    if not isinstance(hourly, dict): raise ValueError("Resposta sem bloco hourly valido")
    chuva = hourly.get("precipitation"); prob = hourly.get("precipitation_probability"); horas = hourly.get("time")
    if not all(isinstance(x, list) and len(x) == 6 for x in (chuva, prob, horas)): raise ValueError("A API deve retornar exatamente seis horas completas")
    for values, upper in ((chuva, float("inf")), (prob, 100)):
        if any(isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v) or not 0 <= v <= upper for v in values):
            raise ValueError("Previsao contem valores ausentes ou invalidos")
    if any(not isinstance(t, str) for t in horas): raise ValueError("Previsao contem horario invalido")
    try: parsed = [datetime.fromisoformat(t) for t in horas]
    except ValueError as error: raise ValueError("Previsao contem horario invalido") from error
    if any((b-a).total_seconds() != 3600 for a,b in zip(parsed,parsed[1:])): raise ValueError("Horas fora de ordem ou nao consecutivas")
    total = sum(chuva); maxima = max(prob)
    return {"inicio": horas[0], "fim": horas[-1], "precipitacao_mm": total, "probabilidade_maxima_pct": maxima, "comando": f"RAIN={int(total >= 1 or maxima >= 60)}"}

def consultar(latitude=-23.71694444, longitude=-46.84916667):
    if not math.isfinite(latitude) or not -90 <= latitude <= 90: raise ValueError("Latitude invalida")
    if not math.isfinite(longitude) or not -180 <= longitude <= 180: raise ValueError("Longitude invalida")
    params = {"latitude": latitude, "longitude": longitude, "hourly": "precipitation,precipitation_probability", "forecast_hours": 6, "timezone": "America/Sao_Paulo"}
    url = "https://api.open-meteo.com/v1/forecast?" + urlencode(params)
    with urlopen(url, timeout=20) as response: payload = json.load(response)
    if not isinstance(payload, dict): raise ValueError("Resposta JSON nao e um objeto")
    result = analisar(payload)
    result.update({"fonte": url, "consultado_em_utc": datetime.now(timezone.utc).isoformat(), "timezone": payload.get("timezone"), "latitude": latitude, "longitude": longitude})
    return result, payload

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--latitude", type=float, default=-23.71694444); parser.add_argument("--longitude", type=float, default=-46.84916667)
    parser.add_argument("--save", type=Path, help="Salvar evidencias reais da consulta em JSON"); args = parser.parse_args()
    try:
        result, payload = consultar(args.latitude,args.longitude)
        if args.save:
            args.save.parent.mkdir(parents=True,exist_ok=True); args.save.write_text(json.dumps({"resultado":result,"api":payload},indent=2),encoding="utf-8")
        print(json.dumps(result,ensure_ascii=False,indent=2)); print("Copie para o Serial Monitor (115200 baud), pressione Enter:"); print(result["comando"]); return 0
    except (HTTPError, URLError, TimeoutError, OSError, ValueError, TypeError) as error:
        print(f"Previsao indisponivel: {error}",file=sys.stderr); print("RAIN=UNKNOWN"); return 1

if __name__ == "__main__": raise SystemExit(main())
