/*
 * Version minima: ESP32-WROOM-32 + BME280 + DS3231.
 * SDA=21, SCL=22; modulos a 3.3 V. Serial: 115200.
 * Dos acciones HTTP: ajustar RTC y registrar/mostrar una muestra.
 * Sin LittleFS, CSV, contexto, muestreo periodico ni conexion cloud.
 * Solo conserva la ultima muestra en RAM; transcribir al dashboard.
 */
#include <Arduino.h>
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>
#include <RTClib.h>
#include <WiFi.h>
#include <WebServer.h>
#include <esp_system.h>
#include <math.h>

const char *AP_SSID = "TESIS-NODO-01";
const char *AP_PASSWORD = "TesisCampo2026"; // Personalizar; minimo ocho caracteres.
const char *FIRMWARE_VERSION = "2.0.0-minimal";
constexpr uint32_t EPOCH_MIN = 1704067200UL; // 2024-01-01 UTC.
constexpr uint32_t EPOCH_MAX = 4102444799UL; // 2099-12-31 UTC.

Adafruit_BME280 bme;
RTC_DS3231 rtc;
WebServer server(80);
bool sensorReady = false, rtcReady = false, clockVerified = false;
String bootId, latestJson = "null", serialBuffer;
uint32_t sequence = 0, lastEpoch = 0, lastEpochMs = 0;

String jsonQuote(const String &input) {
  String output = "\"";
  for (size_t i = 0; i < input.length(); ++i) {
    char c = input[i];
    if (c == '"' || c == '\\') { output += '\\'; output += c; }
    else if (c == '\n') output += "\\n";
    else if (c == '\r') output += "\\r";
    else if (static_cast<uint8_t>(c) >= 32) output += c;
  }
  return output + "\"";
}

String isoUtc(const DateTime &date) {
  char buffer[25];
  snprintf(buffer, sizeof(buffer), "%04u-%02u-%02uT%02u:%02u:%02uZ",
           date.year(), date.month(), date.day(), date.hour(), date.minute(), date.second());
  return String(buffer);
}

String checkedUtc() {
  if (!rtcReady || !clockVerified) return "";
  if (rtc.lostPower()) { clockVerified = false; return ""; }
  DateTime date = rtc.now();
  uint32_t epoch = date.unixtime(), nowMs = millis();
  if (epoch < EPOCH_MIN || epoch > EPOCH_MAX) { clockVerified = false; return ""; }
  if (lastEpoch != 0) {
    int64_t delta = static_cast<int64_t>(epoch) - lastEpoch;
    int64_t expected = static_cast<uint32_t>(nowMs - lastEpochMs) / 1000;
    if (delta - expected < -5 || delta - expected > 5) { clockVerified = false; return ""; }
  }
  if (lastEpoch == 0 || static_cast<uint32_t>(nowMs - lastEpochMs) >= 10000) {
    lastEpoch = epoch; lastEpochMs = nowMs;
  }
  return isoUtc(date);
}

bool initializeSensor() {
  if (!bme.begin(0x76, &Wire) && !bme.begin(0x77, &Wire)) return false;
  bme.setSampling(Adafruit_BME280::MODE_FORCED,
    Adafruit_BME280::SAMPLING_X1, Adafruit_BME280::SAMPLING_X1,
    Adafruit_BME280::SAMPLING_X1, Adafruit_BME280::FILTER_OFF);
  return true;
}

bool setClock(const String &input) {
  if (!rtcReady) rtcReady = rtc.begin(&Wire);
  if (!rtcReady || input.length() != 10) return false;
  for (size_t i = 0; i < input.length(); ++i) if (input[i] < '0' || input[i] > '9') return false;
  uint64_t epoch = strtoull(input.c_str(), nullptr, 10);
  if (epoch < EPOCH_MIN || epoch > EPOCH_MAX) return false;
  rtc.adjust(DateTime(static_cast<uint32_t>(epoch)));
  clockVerified = !rtc.lostPower(); lastEpoch = 0;
  String actual = checkedUtc();
  Serial.println("RTC UTC: " + (actual.length() ? actual : String("NO VERIFICADO")));
  return actual.length() > 0;
}

String numberJson(float value) {
  return isfinite(value) ? String(value, 3) : "null";
}

String acquire(const String &utc) {
  // Solo se llama al pulsar Registrar muestra o enviar CAPTURE por serial.
  float temperature = NAN, humidity = NAN, pressure = NAN;
  String sensorStatus;
  if (!sensorReady) sensorReady = initializeSensor();
  if (!sensorReady) sensorStatus = "sensor_not_found";
  else if (!bme.takeForcedMeasurement()) { sensorStatus = "conversion_failed"; sensorReady = false; }
  else {
    temperature = bme.readTemperature();
    humidity = bme.readHumidity();
    pressure = bme.readPressure(); // Pa, no presion al nivel del mar.
    if (!isfinite(temperature) || !isfinite(humidity) || !isfinite(pressure)) {
      sensorStatus = "invalid_value"; sensorReady = false;
    } else if (temperature < -40 || temperature > 85 || humidity < 0 || humidity > 100 ||
               pressure < 30000 || pressure > 110000) sensorStatus = "outside_spec_range";
    else sensorStatus = "ok";
  }
  String id = bootId + "/" + String(++sequence);
  latestJson = "{\"sample_id\":" + jsonQuote(id) + ",\"timestamp_utc\":" + jsonQuote(utc) +
    ",\"temperature_c\":" + numberJson(temperature) +
    ",\"relative_humidity_pct\":" + numberJson(humidity) +
    ",\"pressure_pa\":" + numberJson(pressure) +
    ",\"sensor_status\":" + jsonQuote(sensorStatus) + "}";
  Serial.println("MUESTRA " + latestJson);
  return latestJson;
}

String statusJson() {
  String utc = checkedUtc();
  return "{\"firmware_version\":" + jsonQuote(FIRMWARE_VERSION) +
    ",\"now_utc\":" + jsonQuote(utc) + ",\"rtc_ready\":" + (rtcReady ? "true" : "false") +
    ",\"time_verified\":" + (utc.length() ? "true" : "false") +
    ",\"sensor_ready\":" + (sensorReady ? "true" : "false") +
    ",\"latest\":" + latestJson + "}";
}

const char PAGE[] PROGMEM = R"HTML(
<!doctype html><html lang="es"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Temperatura y humedad</title><style>
body{font:17px system-ui;max-width:620px;margin:auto;padding:20px;background:#eef3f0;color:#172a22}
section{background:white;padding:20px;margin:16px 0;border-radius:12px}
button{font:inherit;display:block;width:100%;padding:16px;border:0;border-radius:8px;background:#174d3a;color:white;cursor:pointer}
button:disabled{opacity:.5;cursor:wait}#values{font-size:29px;font-weight:bold;margin:18px 0}
pre{font:inherit;white-space:pre-wrap;overflow-wrap:anywhere}.bad{color:#a21929}.good{color:#175939}
</style><h1>Medición ambiental</h1>
<section><button id="clock" onclick="syncTime()">Verificar / ajustar RTC con el teléfono</button><p id="status">Consultando reloj y sensor…</p></section>
<section><button id="capture" onclick="capture()">Registrar muestra</button><div id="values">Sin muestra</div><pre id="sample"></pre></section>
<p>Lectura fija para transcribir al dashboard. Sin archivos ni guardado permanente; anota antes de registrar otra muestra.</p><p id="message" role="status"></p>
<script>
const $=id=>document.getElementById(id);let busy=false;
function message(text,bad=false){$('message').textContent=text;$('message').className=bad?'bad':'good';}
function lock(value){busy=value;$('clock').disabled=value;$('capture').disabled=value;}
async function api(path,data){const options=data===undefined?{}:{method:'POST',headers:{'Content-Type':'application/x-www-form-urlencoded'},body:new URLSearchParams(data)};
 const response=await fetch(path,{...options,cache:'no-store'});const result=await response.json();if(!response.ok)throw Error(result.error||'Error '+response.status);return result;}
async function refresh(initial=false){try{const s=await api('/status');$('status').textContent=`RTC: ${s.rtc_ready?'detectado':'no detectado'} · Hora: ${s.time_verified?'verificada':'ajustar antes de medir'} · BME280: ${s.sensor_ready?'detectado':'revisar conexión'}`;
 $('status').className=s.time_verified&&s.sensor_ready?'good':'bad';if(initial&&s.latest)renderSample(s.latest);
 }catch(e){message('No se pudo consultar el ESP32: '+e.message,true);}}
async function syncTime(){if(busy)return;if(!confirm('¿Es correcta la fecha y hora de este teléfono? '+new Date().toLocaleString()))return;lock(true);
 try{await api('/clock',{epoch:Math.floor(Date.now()/1000)});message('RTC ajustado. Ya puedes registrar una muestra.');await refresh();}catch(e){message(e.message,true);}finally{lock(false);}}
function renderSample(s){const t=Number.isFinite(s.temperature_c)?s.temperature_c.toFixed(2):'—';const h=Number.isFinite(s.relative_humidity_pct)?s.relative_humidity_pct.toFixed(2):'—';
 $('values').textContent=`T: ${t} °C · HR: ${h} %`;
 $('sample').textContent=`Muestra: ${s.sample_id}\nColombia: ${s.timestamp_utc?new Date(s.timestamp_utc).toLocaleString('es-CO',{timeZone:'America/Bogota'}):'hora inválida'}\nUTC: ${s.timestamp_utc||'no disponible'}\nPresión: ${Number.isFinite(s.pressure_pa)?(s.pressure_pa/100).toFixed(2)+' hPa':'—'}\nSensor: ${s.sensor_status==='ok'?'OK':s.sensor_status}`;
 $('sample').className=s.sensor_status==='ok'?'good':'bad';$('values').className=$('sample').className;}
async function capture(){if(busy)return;lock(true);$('values').textContent='Midiendo…';$('values').className='';$('sample').textContent='';
 try{const s=await api('/samples',{});renderSample(s);message(s.sensor_status==='ok'?'Muestra obtenida. Anota los valores y toma la foto.':'Lectura con error; no utilizar como medición válida.',s.sensor_status!=='ok');await refresh();}
 catch(e){$('values').textContent='No se obtuvo una muestra';message(e.message+'. La siguiente pulsación solicita una lectura nueva.',true);}finally{lock(false);}}
refresh(true);
</script></html>
)HTML";

void sendJson(int code, const String &body) {
  server.sendHeader("Cache-Control", "no-store");
  server.send(code, "application/json", body);
}

void captureOrReport() {
  String utc = checkedUtc();
  if (!utc.length()) { Serial.println("Ajustar/verificar RTC antes de medir."); return; }
  acquire(utc);
}

void serialCommand(String command) {
  command.trim();
  if (command == "CAPTURE") captureOrReport();
  else if (command == "STATUS") Serial.println(statusJson());
  else if (command.startsWith("TIME ")) {
    Serial.println(setClock(command.substring(5)) ? "Hora verificada." : "Error de RTC o epoch UTC invalido.");
  } else Serial.println("Comandos: CAPTURE | STATUS | TIME <epoch UTC>");
}

void setup() {
  Serial.begin(115200); delay(300);
  Wire.begin(21, 22); Wire.setClock(100000); Wire.setTimeOut(100);
  char boot[20];
  snprintf(boot, sizeof(boot), "B%08lX%08lX", (unsigned long)esp_random(), (unsigned long)esp_random());
  bootId = boot;
  sensorReady = initializeSensor(); rtcReady = rtc.begin(&Wire);
  // Verificacion explicita por arranque: no ajustar nunca a la hora de compilacion.
  WiFi.mode(WIFI_AP);
  bool apReady = WiFi.softAP(AP_SSID, AP_PASSWORD, 1, false, 2);
  server.on("/", HTTP_GET, [](){
    server.sendHeader("Cache-Control", "no-store");
    server.send_P(200, "text/html; charset=utf-8", PAGE);
  });
  server.on("/status", HTTP_GET, [](){ sendJson(200, statusJson()); });
  server.on("/clock", HTTP_POST, [](){
    if (!setClock(server.arg("epoch"))) { sendJson(400, "{\"error\":\"RTC no disponible o fecha invalida\"}"); return; }
    sendJson(200, "{\"ok\":true}");
  });
  server.on("/samples", HTTP_POST, [](){
    String utc = checkedUtc();
    if (!utc.length()) { sendJson(409, "{\"error\":\"Verifica o ajusta el RTC con el telefono antes de medir\"}"); return; }
    sendJson(200, acquire(utc));
  });
  server.onNotFound([](){ sendJson(404, "{\"error\":\"Ruta no disponible en version minima\"}"); });
  server.begin();
  Serial.printf("Firmware %s; BME=%s; RTC=%s\n", FIRMWARE_VERSION, sensorReady ? "ok" : "error", rtcReady ? "ok" : "error");
  Serial.println("Wi-Fi: " + String(AP_SSID) + "; http://" + WiFi.softAPIP().toString());
  if (!apReady) Serial.println("Error al iniciar AP; revisar configuracion.");
  Serial.println("Sin almacenamiento. Ajustar RTC y solicitar muestras; anotar en dashboard.");
}

void loop() {
  server.handleClient();
  while (Serial.available()) {
    char c = static_cast<char>(Serial.read());
    if (c == '\n') { serialCommand(serialBuffer); serialBuffer = ""; }
    else if (c != '\r') {
      if (serialBuffer.length() < 80) serialBuffer += c;
      else serialBuffer = "";
    }
  }
  delay(2);
}
