# Guia de teste — FarmTech Fase 2

## Preparação

1. Abra o [projeto Wokwi](https://wokwi.com/projects/476105970700739585).
2. Se o projeto online ainda estiver com a versão antiga, substitua `sketch.ino`, `diagram.json` e `libraries.txt` pelos arquivos da pasta `fase-2/esp32/` e salve com uma conta que tenha acesso. As alterações locais já estão prontas; o login e o salvamento online dependem do grupo.
3. Inicie a simulação e abra o Serial Monitor em 115200 baud.

## Testes do circuito

Em cada caso, faça a ação, aguarde a próxima linha de relatório e compare com o resultado esperado.

| Teste | O que fazer / valor | Deve aparecer | Relé |
|---|---|---|---|
| N | Ctrl+clique no botão verde N (GPIO25) | `N=OK` | permanece conforme os demais sinais |
| P | Ctrl+clique no botão verde P (GPIO26) | `P=OK` | permanece conforme os demais sinais |
| K | Ctrl+clique no botão verde K (GPIO27) | `K=OK` | permanece conforme os demais sinais |
| Nutriente ausente | Solte um dos três botões | `N=BAIXO`, `P=BAIXO` ou `K=BAIXO` | desligado |
| pH | Ajuste o LDR; confirme o valor `pH=` | pH calculado entre 0 e 14; a faixa didática é 6,0–6,5 | fora da faixa: desligado |
| Umidade seca | No DHT22, coloque 40% | `umidade=40.0%` e motivo de umidade baixa | ligado, se NPK/pH estiverem adequados e não houver chuva |
| Umidade limite | Coloque 60% | a histerese mantém o estado anterior | não use este ponto isolado para concluir |
| Umidade molhada | Coloque 70% | motivo de umidade suficiente | desligado |
| Chuva | Digite `RAIN=1` e Enter | `chuva prevista` | desligado |
| Sem chuva | Digite `RAIN=0` e Enter | `sem chuva prevista` | decide por umidade/NPK/pH |
| Previsão ausente | Digite `RAIN=UNKNOWN` e Enter | `previsão indisponível` | desligado por segurança |

Para demonstrar a bomba ligada, deixe os três botões pressionados, ajuste o LDR até a leitura mostrar pH dentro de 6,0–6,5, coloque o DHT em 40% e envie `RAIN=0`.

## Python e Open-Meteo

Na raiz execute `python fase-2/python/weather.py --save fase-2/docs/weather-live.json`. Copie para o Serial Monitor somente o comando impresso.

## Autotestes locais

Na raiz, execute `python -m unittest discover -s fase-2/tests -p "test_*.py"`. No Wokwi, digite `SELFTEST`.
