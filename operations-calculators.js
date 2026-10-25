(function (root) {
  'use strict';
  const MAX_INPUT = 1e12;
  function value(input, key, options = {}) {
    const raw = input[key];
    if (raw === '' || (typeof raw === 'string' && raw.trim() === '') || raw === null || raw === undefined || typeof raw === 'boolean') throw new Error('Complete every field with a non-negative number.');
    const n = Number(raw);
    if (!Number.isFinite(n) || n < 0 || n > MAX_INPUT) throw new Error('Use finite numbers between 0 and 1 trillion.');
    if (options.whole && !Number.isInteger(n)) throw new Error('People and incident counts must be whole numbers.');
    if (options.percent && n > 100) throw new Error('The buffer must be between 0% and 100%.');
    return n;
  }
  function calculate(kind, input) {
    let rows;
    if (kind === 'service-capacity-calculator') {
      const people = value(input, 'people', {whole: true});
      const hours = value(input, 'hours');
      const unavailable = value(input, 'unavailable');
      const buffer = value(input, 'buffer', {percent: true});
      const demand = value(input, 'demand');
      const scheduled = people * hours;
      if (unavailable > scheduled) throw new Error('Unavailable team hours cannot exceed total scheduled team hours.');
      const available = scheduled - unavailable;
      const planned = available * (1 - buffer / 100);
      rows = [
        ['Scheduled team hours', scheduled, 'hours'],
        ['Delivery hours before buffer', available, 'hours'],
        ['Planned delivery capacity', planned, 'hours'],
        ['Capacity gap (capacity minus demand)', planned - demand, 'hours'],
        ['Demand / planned capacity', planned > 0 ? demand / planned * 100 : null, 'percent'],
      ];
    } else if (kind === 'project-margin-calculator') {
      const revenue = value(input, 'revenue');
      const labor = value(input, 'laborHours') * value(input, 'laborRate');
      const direct = labor + value(input, 'external') + value(input, 'other');
      const contribution = revenue - direct;
      rows = [
        ['Delivery labor cost', labor, 'money'],
        ['Total direct costs entered', direct, 'money'],
        ['Project contribution', contribution, 'money'],
        ['Contribution margin', revenue > 0 ? contribution / revenue * 100 : null, 'percent'],
      ];
    } else if (kind === 'rework-cost-calculator') {
      const incidents = value(input, 'incidents', {whole: true});
      const hours = incidents * value(input, 'hoursPer');
      const labor = hours * value(input, 'rate');
      const cash = incidents * value(input, 'cashPer');
      const credits = value(input, 'credits');
      rows = [
        ['Correction labor hours', hours, 'hours'],
        ['Modeled labor cost', labor, 'money'],
        ['Additional cash expenses', cash, 'money'],
        ['Customer credits', credits, 'money'],
        ['Modeled cost for chosen period', labor + cash + credits, 'money'],
      ];
    } else {
      throw new Error('Unknown calculator.');
    }
    if (rows.some(row => row[1] !== null && (!Number.isFinite(row[1]) || Math.abs(row[1]) > Number.MAX_SAFE_INTEGER))) {
      throw new Error('These inputs exceed the supported calculation range. Use a smaller planning period or scale.');
    }
    return rows;
  }
  function format(n, unit) {
    if (n === null) return 'Not defined (zero denominator)';
    if (unit === 'money') return new Intl.NumberFormat('en-US', {style: 'currency', currency: 'USD'}).format(n);
    return new Intl.NumberFormat('en-US', {maximumFractionDigits: 2}).format(n) + (unit === 'percent' ? '%' : ' hours');
  }
  function csvCell(v) { return '"' + String(v).replace(/"/g, '""') + '"'; }
  function resultCsv(kind, fields, rows) {
    return [
      ['Calculator', kind], ['Planning model — not guaranteed savings or company net profit'],
      ['Inputs'], ...Object.entries(fields), ['Outputs', 'Value', 'Unit'],
      ...rows.map(([label, n, unit]) => [label, n === null ? 'Not defined: zero denominator' : n, unit]),
    ].map(row => row.map(csvCell).join(',')).join('\r\n') + '\r\n';
  }
  const api = {calculate, format, resultCsv};
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  if (!root.document) return;
  root.document.querySelectorAll('[data-calculator]').forEach(form => {
    const kind = form.dataset.calculator;
    const output = form.querySelector('.calc-output');
    const exportButton = form.querySelector('[data-export]');
    form.querySelector('[data-calculate]').disabled = false;
    let latest = null;
    function invalidate() {
      latest = null;
      exportButton.disabled = true;
      output.textContent = 'Inputs changed. Choose Calculate to update the result.';
    }
    form.addEventListener('input', invalidate);
    form.addEventListener('reset', () => {
      latest = null;
      exportButton.disabled = true;
      output.textContent = 'Example restored. Choose Calculate to calculate the example.';
    });
    form.addEventListener('submit', event => {
      event.preventDefault();
      latest = null;
      exportButton.disabled = true;
      output.replaceChildren();
      try {
        const fields = Object.fromEntries(new FormData(form).entries());
        const rows = calculate(kind, fields);
        const dl = root.document.createElement('dl');
        for (const [label, n, unit] of rows) {
          const dt = root.document.createElement('dt');
          const dd = root.document.createElement('dd');
          dt.textContent = label;
          dd.textContent = format(n, unit);
          dl.append(dt, dd);
        }
        const note = root.document.createElement('p');
        note.textContent = 'Planning estimate from your inputs. Review the formula, assumptions, and limits below before making a decision.';
        output.append(dl, note);
        latest = {fields, rows};
        exportButton.disabled = false;
      } catch (error) {
        const message = root.document.createElement('p');
        message.className = 'calc-error';
        message.textContent = error.message;
        output.append(message);
      }
    });
    exportButton.addEventListener('click', () => {
      if (!latest) return;
      const blob = new Blob([resultCsv(kind, latest.fields, latest.rows)], {type: 'text/csv;charset=utf-8'});
      const url = URL.createObjectURL(blob);
      const link = root.document.createElement('a');
      link.href = url;
      link.download = kind + '-result.csv';
      root.document.body.append(link);
      link.click();
      link.remove();
      setTimeout(() => URL.revokeObjectURL(url), 1000);
    });
  });
})(typeof globalThis !== 'undefined' ? globalThis : this);
