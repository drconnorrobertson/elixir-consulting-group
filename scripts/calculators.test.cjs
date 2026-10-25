const test = require('node:test');
const assert = require('node:assert/strict');
const {calculate, format, resultCsv} = require('../operations-calculators.js');
const capacity = {people: 3, hours: 40, unavailable: 30, buffer: 10, demand: 95};
const margin = {revenue: 20000, laborHours: 180, laborRate: 50, external: 3000, other: 0};
const rework = {incidents: 8, hoursPer: 2, rate: 40, cashPer: 25, credits: 100};
const values = rows => rows.map(row => row[1]);
test('capacity reproduces the published example and exposes overload', () => {
  const rows = calculate('service-capacity-calculator', capacity);
  assert.deepEqual(values(rows).slice(0, 4), [120, 90, 81, -14]);
  assert.ok(Math.abs(rows[4][1] - 117.28395061728395) < 1e-10);
});
test('capacity rejects total unavailable time greater than scheduled time', () => {
  assert.throws(() => calculate('service-capacity-calculator', {...capacity, unavailable: 121}), /cannot exceed/);
});
test('zero capacity produces an explicit undefined ratio', () => {
  const rows = calculate('service-capacity-calculator', {...capacity, buffer: 100});
  assert.deepEqual(values(rows).slice(2), [0, -95, null]);
  assert.match(format(null, 'percent'), /zero denominator/);
});
test('zero scheduled time and zero demand remain finite', () => {
  assert.deepEqual(values(calculate('service-capacity-calculator', {people: 0, hours: 0, unavailable: 0, buffer: 0, demand: 0})), [0, 0, 0, 0, null]);
});
test('capacity distinguishes total unavailable hours from a per-person deduction', () => {
  const rows = calculate('service-capacity-calculator', {people: 2, hours: 30, unavailable: 10, buffer: 0, demand: 45});
  assert.deepEqual(values(rows).slice(0, 4), [60, 50, 50, 5]);
});
test('project margin matches the published direct-cost example', () => {
  assert.deepEqual(values(calculate('project-margin-calculator', margin)), [9000, 12000, 8000, 40]);
});
test('negative contribution is preserved', () => {
  assert.deepEqual(values(calculate('project-margin-calculator', {...margin, revenue: 10000})), [9000, 12000, -2000, -20]);
});
test('zero revenue does not claim a zero percent margin', () => {
  assert.deepEqual(values(calculate('project-margin-calculator', {...margin, revenue: 0})), [9000, 12000, -12000, null]);
});
test('rework matches the published period cost with no annualization', () => {
  assert.deepEqual(values(calculate('rework-cost-calculator', rework)), [16, 640, 200, 100, 940]);
});
test('zero incidents retain independently entered customer credits', () => {
  assert.deepEqual(values(calculate('rework-cost-calculator', {...rework, incidents: 0})), [0, 0, 0, 100, 100]);
});
test('invalid, empty, infinite, and negative values are rejected', () => {
  for (const revenue of ['', ' ', undefined, null, true, -1, 'NaN', Infinity, '1e100']) {
    assert.throws(() => calculate('project-margin-calculator', {...margin, revenue}));
  }
});
test('counts must be whole and buffers bounded', () => {
  assert.throws(() => calculate('service-capacity-calculator', {...capacity, people: 1.5}), /whole/);
  assert.throws(() => calculate('service-capacity-calculator', {...capacity, buffer: 101}), /100/);
  assert.throws(() => calculate('rework-cost-calculator', {...rework, incidents: 0.5}), /whole/);
});
test('unsafe magnitude is rejected before rendering or export', () => {
  assert.throws(() => calculate('project-margin-calculator', {...margin, laborHours: 1e12, laborRate: 1e12}), /range/);
});
test('string inputs from real HTML forms calculate correctly', () => {
  const input = Object.fromEntries(Object.entries(margin).map(([k, v]) => [k, String(v)]));
  assert.deepEqual(values(calculate('project-margin-calculator', input)), [9000, 12000, 8000, 40]);
});
test('CSV includes assumptions, exact outputs, units, and explicit undefined values', () => {
  const csv = resultCsv('project-margin-calculator', {...margin, revenue: 0}, calculate('project-margin-calculator', {...margin, revenue: 0}));
  assert.match(csv, /"revenue","0"/);
  assert.match(csv, /"Project contribution","-12000","money"/);
  assert.match(csv, /Not defined: zero denominator/);
  assert.doesNotMatch(csv, /NaN|Infinity|undefined/);
});
test('unknown calculators fail clearly', () => {
  assert.throws(() => calculate('unknown', {}), /Unknown/);
});
