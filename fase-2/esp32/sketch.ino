#include <DHTesp.h>
#include <math.h>

// Substituicoes didaticas FIAP: botoes=NPK, LDR=pH, DHT22=solo.
const int BTN_N = 25, BTN_P = 26, BTN_K = 27;
const int DHT_PIN = 15, LDR_PIN = 34, RELE_PIN = 4;
const int RELE_LIGADO = LOW, RELE_DESLIGADO = HIGH;
const float PH_MIN = 6.0f, PH_MAX = 6.5f;
const float UMIDADE_LIGA = 60.0f, UMIDADE_DESLIGA = 70.0f;
const unsigned long INTERVALO_SENSOR = 2000;
const unsigned long VALIDADE_CHUVA = 6UL * 60UL * 60UL * 1000UL;
DHTesp dhtSensor;
bool bombaLigada = false, chuva = false, climaRecebido = false;
unsigned long ultimaChuva = 0, ultimaLeitura = 0, ultimoRelatorio = 0;
float umidade = NAN;
char comando[48];
size_t tamanhoComando = 0;
bool comandoLongo = false;

struct Decisao { bool ligar; const char *motivo; };

Decisao decidir(bool n, bool p, bool k, float ph, float u, bool chove, bool anterior) {
  if (!isfinite(u) || u < 0 || u > 100) return {false, "Falha na leitura de umidade"};
  if (!isfinite(ph) || ph < 0 || ph > 14) return {false, "Falha na leitura de pH simulado"};
  if (chove) return {false, "Chuva prevista: irrigacao suspensa"};
  if (!n || !p || !k) return {false, "NPK inadequado: verificar manejo"};
  if (ph < PH_MIN || ph > PH_MAX) return {false, "pH fora da faixa operacional"};
  if (u < UMIDADE_LIGA) return {true, "Umidade abaixo de 60%"};
  if (u >= UMIDADE_DESLIGA) return {false, "Umidade atingiu 70%"};
  return {anterior, "Histerese 60-70%: manter estado anterior"};
}

void autoteste() {
  int passou = 0, total = 0;
  auto testar = [&](const char *nome, bool esperado, bool n, bool p, bool k, float ph, float u, bool chove, bool anterior) {
    bool ok = decidir(n,p,k,ph,u,chove,anterior).ligar == esperado;
    total++; if (ok) passou++;
    Serial.printf("TEST %s: %s\n", nome, ok ? "PASS" : "FAIL");
  };
  testar("seco",true,1,1,1,6.25,40,0,0); testar("molhado",false,1,1,1,6.25,80,0,1);
  testar("chuva",false,1,1,1,6.25,40,1,1); testar("N",false,0,1,1,6.25,40,0,1);
  testar("P",false,1,0,1,6.25,40,0,1); testar("K",false,1,1,0,6.25,40,0,1);
  testar("pH_baixo",false,1,1,1,5.9,40,0,1); testar("pH_alto",false,1,1,1,6.6,40,0,1);
  testar("pH_min",true,1,1,1,6.0,40,0,0); testar("pH_max",true,1,1,1,6.5,40,0,0);
  testar("60_desligada",false,1,1,1,6.25,60,0,0); testar("60_ligada",true,1,1,1,6.25,60,0,1);
  testar("65_desligada",false,1,1,1,6.25,65,0,0); testar("65_ligada",true,1,1,1,6.25,65,0,1);
  testar("70",false,1,1,1,6.25,70,0,1); testar("NaN_umidade",false,1,1,1,6.25,NAN,0,1);
  testar("umidade_negativa",false,1,1,1,6.25,-1,0,1); testar("umidade_101",false,1,1,1,6.25,101,0,1);
  testar("NaN_ph",false,1,1,1,NAN,40,0,1);
  Serial.printf("SELFTEST %d/%d PASS (logica; nao testa fiacao)\n", passou,total);
}

void executarComando() {
  comando[tamanhoComando] = '\0';
  if (!strcmp(comando,"RAIN=0") || !strcmp(comando,"RAIN=1")) {
    chuva = comando[5] == '1'; climaRecebido = true; ultimaChuva = millis();
    Serial.printf("OK RAIN=%d (validade: 6 horas de simulacao)\n", chuva);
  } else if (!strcmp(comando,"RAIN=UNKNOWN")) { climaRecebido = false; Serial.println("OK previsao indisponivel: bomba bloqueada");
  } else if (!strcmp(comando,"SELFTEST")) { autoteste();
  } else if (tamanhoComando) Serial.println("ERRO: use RAIN=0, RAIN=1, RAIN=UNKNOWN ou SELFTEST");
}
void lerSerial() {
  while (Serial.available()) {
    char c = Serial.read(); if (c == '\r') continue;
    if (c == '\n') {
      if (comandoLongo) Serial.println("ERRO: comando muito longo, descartado"); else executarComando();
      tamanhoComando = 0; comandoLongo = false;
    } else if (!comandoLongo) {
      if (tamanhoComando < sizeof(comando)-1) comando[tamanhoComando++] = c; else comandoLongo = true;
    }
  }
}
void setup() {
  Serial.begin(115200); digitalWrite(RELE_PIN, RELE_DESLIGADO); pinMode(RELE_PIN, OUTPUT);
  pinMode(BTN_N, INPUT_PULLUP); pinMode(BTN_P, INPUT_PULLUP); pinMode(BTN_K, INPUT_PULLUP);
  analogReadResolution(12); dhtSensor.setup(DHT_PIN, DHTesp::DHT22);
  Serial.println("FARMTECH FASE 2 | ALFACE | SIMULACAO DIDATICA");
  Serial.println("Envie RAIN=0 ou RAIN=1 + Enter. Sem previsao, bomba bloqueada.");
  Serial.println("Ctrl+clique trava botoes. Ao mudar NPK, ajuste manualmente LDR.");
  Serial.println("SELFTEST executa testes da logica sem acionar o rele.");
}
void loop() {
  lerSerial(); unsigned long agora = millis();
  if (agora - ultimaLeitura >= INTERVALO_SENSOR) { ultimaLeitura = agora; umidade = dhtSensor.getTempAndHumidity().humidity; }
  bool n = digitalRead(BTN_N) == LOW, p = digitalRead(BTN_P) == LOW, k = digitalRead(BTN_K) == LOW;
  int adc = analogRead(LDR_PIN); float ph = adc * 14.0f / 4095.0f;
  bool climaValido = climaRecebido && agora - ultimaChuva < VALIDADE_CHUVA;
  Decisao d = decidir(n,p,k,ph,umidade,chuva,bombaLigada);
  if (!climaValido) d = {false,"Previsao ausente/expirada: envie RAIN=0 ou RAIN=1"};
  bombaLigada = d.ligar; digitalWrite(RELE_PIN,bombaLigada ? RELE_LIGADO : RELE_DESLIGADO);
  if (agora - ultimoRelatorio >= INTERVALO_SENSOR) {
    ultimoRelatorio = agora; Serial.println("========== FARMTECH | ALFACE ==========");
    Serial.printf("N: %s | P: %s | K: %s\n",n?"OK":"BAIXO",p?"OK":"BAIXO",k?"OK":"BAIXO");
    Serial.printf("ADC: %d | pH simulado: %.2f | Umidade solo (simulada): %.1f %%\n",adc,ph,umidade);
    Serial.printf("Chuva: %s | Bomba: %s | GPIO4: %s\n",!climaValido?"DESCONHECIDA":chuva?"SIM":"NAO",bombaLigada?"LIGADA":"DESLIGADA",bombaLigada?"LOW":"HIGH");
    Serial.printf("Motivo: %s\n",d.motivo);
  }
  delay(20);
}
