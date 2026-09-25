# Roteiro de vídeo — até 5 minutos

**0:00–0:25 — Apresentação.** Mostre o nome do grupo e diga: “Este é o sistema didático de irrigação de alface da FarmTech Solutions. O ESP32 combina NPK, pH simulado, umidade simulada e previsão de chuva para comandar uma bomba.”

**0:25–0:55 — Arquivos.** Abra `fase-2/README.md`, `esp32/sketch.ino` e `python/weather.py`. Mostre rapidamente a função de decisão e os comandos `RAIN=0`, `RAIN=1` e `RAIN=UNKNOWN`.

**0:55–1:30 — Circuito.** No Wokwi, mostre ESP32, três botões verdes N/P/K, LDR, DHT22 e relé. Explique que GPIO25/26/27 são N/P/K, GPIO34 é LDR, GPIO15 é DHT22 e GPIO4 é o relé.

**1:30–2:20 — Sensores.** Pressione os três botões. Ajuste o LDR até o Serial mostrar pH entre 6,0 e 6,5. No DHT22 coloque 40%. Explique que LDR e DHT22 são substituições didáticas e que os botões representam presença adequada de nutrientes.

**2:20–3:10 — Bomba.** Com NPK adequado, pH 6,35, DHT em 40% e `RAIN=0`, mostre `Bomba LIGADA`. Depois coloque 70% ou envie `RAIN=1` e mostre `Bomba DESLIGADA`.

**3:10–4:00 — Python.** Execute `python fase-2/python/weather.py`. Mostre a consulta real ao Open-Meteo e o comando impresso. Explique que a API pública não exige chave.

**4:00–4:35 — Serial.** Copie `RAIN=1` para o Serial Monitor e pressione Enter. Mostre a suspensão da irrigação. Em seguida, se quiser mostrar a recuperação, envie `RAIN=0` com o DHT em 40%.

**4:35–5:00 — Conclusão.** Mostre o README, a captura do circuito e o resultado dos testes. Diga que a lógica é didática, que não há dosador de fertilizante e que a sincronização final do Wokwi, GitHub e vídeo depende da conta do grupo.
