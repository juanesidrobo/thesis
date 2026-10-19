// Verifica el flujo manual y sus fallos; no simula el hardware.
// node scripts/registrador_invernadero/tests/pagina_local.test.cjs
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const assert = require('node:assert/strict');

const source = fs.readFileSync(path.join(__dirname, '..', 'registrador_invernadero.ino'), 'utf8');
const html = source.match(/R"HTML\(([\s\S]*?)\)HTML"/)[1];
const javascript = html.match(/<script>([\s\S]*?)<\/script>/)[1];
assert.equal((html.match(/<button\b/g) || []).length, 2, 'La interfaz solo tiene dos acciones');
const elements = new Map();
const element = id => {
  if (!elements.has(id)) elements.set(id, { textContent: '', className: '', disabled: false });
  return elements.get(id);
};
const sample = {
  sample_id: 'BTEST/1', timestamp_utc: '2026-10-20T14:00:00Z',
  temperature_c: 27.43, relative_humidity_pct: 61.2, pressure_pa: 83540, sensor_status: 'ok',
};
let mode = 'success';
const requests = [];
const context = vm.createContext({
  document: { getElementById: element }, URLSearchParams, confirm: () => true,
  fetch: async (url, options = {}) => {
    requests.push({ url, options });
    if (url === '/samples' && mode === 'network') throw new Error('Conexión interrumpida');
    if (url === '/samples' && mode === 'clock') {
      return { ok: false, status: 409, json: async () => ({ error: 'Ajustar RTC' }) };
    }
    return { ok: true, status: 200, json: async () => {
      if (url === '/samples') return sample;
      if (url === '/status') return { rtc_ready: true, time_verified: true, sensor_ready: true, latest: sample };
      return { ok: true };
    } };
  },
});

async function main() {
  new vm.Script(javascript).runInContext(context);
  await vm.runInContext('refresh()', context);
  await vm.runInContext('syncTime()', context);
  const clock = requests.find(r => r.url === '/clock');
  assert.equal(clock.options.method, 'POST');
  assert.ok(Number(clock.options.body.get('epoch')) > 1704067200);

  await vm.runInContext('capture()', context);
  assert.match(element('values').textContent, /27\.43/);
  assert.match(element('sample').textContent, /BTEST\/1/);
  assert.match(element('sample').textContent, /835\.40 hPa/);
  const fixed = element('sample').textContent;
  sample.temperature_c = 30;
  await vm.runInContext('refresh()', context);
  assert.equal(element('sample').textContent, fixed, 'Consultar estado no cambia la lectura transcrita');

  mode = 'network';
  await vm.runInContext('capture()', context);
  assert.equal(element('sample').textContent, '', 'No mostrar muestra anterior como adquisición nueva');
  assert.equal(element('message').className, 'bad');
  assert.equal(element('capture').disabled, false, 'Permitir otra medición tras fallo');
  assert.equal(element('clock').disabled, false);

  mode = 'clock';
  await vm.runInContext('capture()', context);
  assert.match(element('message').textContent, /Ajustar RTC/);

  await vm.runInContext(`renderSample({sample_id:'error',timestamp_utc:'',temperature_c:null,
    relative_humidity_pct:null,pressure_pa:null,sensor_status:'sensor_not_found'})`, context);
  assert.match(element('values').textContent, /—/);
  assert.equal(element('sample').className, 'bad');
  console.log('OK: dos acciones, ajuste UTC, captura fija, red/reloj fallidos y valores ausentes.');
}
main().catch(error => { console.error(error); process.exitCode = 1; });
