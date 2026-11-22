// STANYO training, live (12 Nov 2026). Reads /iris/lab/stan.json, which stan/scripts/live_status.py writes (numbers and fixed words only).
// Refreshes every 60 s.
(function () {
  var box = document.getElementById('stan-live'); if (!box) return;
  var STAGES = ['teachers', 'crosstalk', 'silver', 'training', 'paired test'];
  var STAGE_TEXT = {
    'teachers': 'Three teacher models are labelling claims, each on its own.',
    'crosstalk': 'The teachers are labelling again after seeing each other’s labels.',
    'silver': 'Agreements between the teachers are being turned into training examples.',
    'training': 'STANYO is training.',
    'paired test': 'STANYO is trained and is being tested on the answer key.',
    'kept': 'The paired test is read. STANYO was kept.',
    'not kept': 'The paired test is read. STANYO was not kept.'
  };
  var NAMES = { base: 'Untrained base (Qwen3-1.7B)', llama: 'Llama 3.1 8B', mistral: 'Mistral 7B', gemma: 'Gemma 3 4B' };
  function h(tag, txt, cls) { var e = document.createElement(tag); if (cls) e.className = cls; if (txt != null) e.textContent = txt; return e; }
  function pct(x) { return x == null ? '-' : Math.round(x * 100) + '%'; }
  function p3(x) { return x == null ? '-' : x.toFixed(3); }
  function iv(w) { return w && w.length === 2 ? '[' + p3(w[0]) + ', ' + p3(w[1]) + ']' : '-'; }
  function nm(k) { return NAMES[k] || k; }
  function utc(iso) { return iso ? iso.replace('T', ' ').replace(/:\d\dZ$/, ' UTC') : '-'; }
  function ago(iso) {
    if (!iso) return ''; var m = Math.max(0, Math.round((Date.now() - Date.parse(iso)) / 60000));
    if (m < 1) return 'just now'; if (m < 60) return m + ' min ago'; var hh = Math.floor(m / 60); return hh + ' h ' + (m % 60) + ' min ago';
  }
  function table(head, rows) {
    var t = h('table', null, 'hl-tab'), th = h('thead'), tr = h('tr'); head.forEach(function (c) { tr.appendChild(h('th', c)); }); th.appendChild(tr); t.appendChild(th);
    var tb = h('tbody'); rows.forEach(function (r) { var x = h('tr'); r.forEach(function (c) { x.appendChild(h('td', c)); }); tb.appendChild(x); }); t.appendChild(tb);
    var w = h('div', null, 'tablewrap'); w.appendChild(t); return w;
  }
  var DESK = { sagar: 'SAGAR, gravitational-wave papers', brands: 'BRANDS, papers by authors at named companies', quant: 'Quant desk' };
  var MACH = { arm: 'GPU host', mac: 'Mac seat' };
  function drawLive(d, old) {   // 15 Nov 2026 (the owner): STAN-E and the pipelines stay open; the LoRA ladder and the closed STAN A lane sit in one collapsed block
    var E = d.stan_e;
    if (E) {
      box.appendChild(h('h3', 'STAN-E, errata drafted by local models'));
      box.appendChild(h('p', 'Each model is graded against findings that a first reader marked and a second reader, shown the same passages, confirmed. Confirmed papers so far: ' + E.verified_positive_papers + '. A hit is a confirmed finding the model also drafted.', 'meta'));
      if (E.runs && E.runs.length) box.appendChild(table(['Run', 'Papers seen', 'Papers flagged', 'Confirmed papers seen', 'Hits', 'Recall, 95% interval', 'Unreadable replies'],
        E.runs.map(function (r) { return [r.model, r.papers_seen, r.papers_flagged, r.verified_positive_papers_seen, r.hits, iv(r.recall_wilson95), r.parse_fail]; })));
      if (E.running_now && E.running_now.length) box.appendChild(h('p', 'Running now: ' + E.running_now.map(function (j) { return j.model + ' on the ' + MACH[j.machine]; }).join(', ') + '.'));
    }
    var L = d.ladder;
    if (L && L.rows && L.rows.length) {
      old.appendChild(h('h3', 'STAN-E training ladder'));
      old.appendChild(h('p', 'LoRA adapters on Qwen2.5-7B-Instruct (4-bit, MLX), each tested on two held-out sets of paper excerpts: one marked by our readers and one from the desk pipelines. Caught: excerpts with a confirmed finding that the model flagged. False flags: excerpts with no finding that it flagged. No adapter is kept yet.', 'meta'));
      var SN = { test_hand: 'hand-marked', test_pipeline: 'pipeline' };
      function cell(x) { return x ? x.pos_flag + ' of ' + x.pos + ' caught, ' + x.neg_flag + ' of ' + x.neg + ' false flags' + (x.parse_fail ? ', ' + x.parse_fail + ' unreadable' : '') : '-'; }
      old.appendChild(table(['Model', 'Hand-marked set', 'Pipeline set'], L.rows.map(function (r) { return [r.model, cell(r.test_hand), cell(r.test_pipeline)]; })));
      if (L.clustered && L.clustered.length) {
        old.appendChild(h('p', 'Against the untouched model on the same excerpts, with the paper as the unit (several excerpts come from one paper, so intervals are drawn by resampling papers). Flips count excerpts that changed each way. A difference reads cannot tell when its interval reaches both zero and 0.10, a size defined after the data.', 'meta'));
        old.appendChild(table(['Model', 'Set', 'Papers', 'Caught, change', 'Flips', 'Outcome', 'False flags, change', 'Flips', 'Outcome'],
          L.clustered.map(function (c) { return [c.model, SN[c.set] || c.set, c.papers, p3(c.recall_diff) + ' ' + iv(c.recall_diff_ci95), '+' + c.recall_flips_up + ' / -' + c.recall_flips_down, c.recall_outcome.replace('_', ' ').toLowerCase(),
            p3(c.false_flag_diff) + ' ' + iv(c.false_flag_diff_ci95), '+' + c.false_flag_flips_up + ' / -' + c.false_flag_flips_down, c.false_flag_outcome.replace('_', ' ').toLowerCase()]; })));
      }
    }
    var P2 = d.pipelines;
    if (P2) {
      box.appendChild(h('h3', 'Where the confirmed findings come from'));
      Object.keys(P2).forEach(function (k) { var x = P2[k]; box.appendChild(h('p', (DESK[k] || k) + ': ' + x.findings_confirmed + ' findings confirmed, ' + x.batches_merged + ' batches merged, ' + x.queue_left + ' papers still queued.')); });
    }
    box.appendChild(h('p', 'Feed written ' + utc(d.updated) + ' (' + ago(d.updated) + '). Updated again every minute.', 'meta'));
  }
  function draw(d) {
    box.textContent = '';
    if (!d || !d.stage) { box.appendChild(h('p', 'The live feed has not been written yet.')); return; }
    var old = h('details', null, 'stan-earlier'); old.appendChild(h('summary', 'Earlier STANYO runs: the STAN-E LoRA ladder and the closed STAN A lane (teachers, training examples, baseline, paired test, plan)'));
    drawLive(d, old);
    old.appendChild(h('h3', 'The closed abstract lane'));
    old.appendChild(h('p', 'The record of the first STANYO run, on titles and abstracts, stays below. Its last stage was: ' + d.stage + '.', 'meta'));
    var si = STAGES.indexOf(d.stage); if (si < 0) si = STAGES.length;
    old.appendChild(h('h3', 'Where the run is'));
    old.appendChild(h('p', STAGE_TEXT[d.stage] || ''));
    old.appendChild(table(['Stage', 'State'], STAGES.map(function (s, i) { return [s, i < si ? 'done' : (i === si ? 'now' : 'not yet')]; })));
    var T = d.teachers || {};
    if (T.names && T.names.length) {
      old.appendChild(h('h3', 'Teachers'));
      old.appendChild(table(['Teacher', 'First round, claims labelled', 'Second round, claims labelled'],
        T.names.map(function (n) { var l = (T.labelled || {})[n] || {}; return [nm(n), (l.round1 || {}).labelled, (l.round2 || {}).labelled]; })));
      if (T.slices && T.slices.length) {
        old.appendChild(h('p', 'By slice of the claim pool, first round then second round, for each teacher.', 'meta'));
        old.appendChild(table(['Slice', 'Claims'].concat(T.names.map(nm)),
          T.slices.map(function (s) { return [s.slice, s.items].concat(T.names.map(function (n) { return (s.labelled_round1 || {})[n] + ' / ' + (s.labelled_round2 || {})[n]; })); })));
      }
    }
    var S = d.silver || {};
    if (S.silver_pairs != null) {
      old.appendChild(h('h3', 'Training examples from agreement'));
      old.appendChild(table(['Reading', 'Value'], [
        ['Claim and code pairs where all three teachers agreed with a quote', S.silver_pairs],
        ['Training rows built so far', S.train_rows], ['Validation rows', S.valid_rows],
        ['Pairs where two of three agreed, held for review', S.review_queue_two_of_three],
        ['Claims not yet labelled by all three', S.items_not_yet_labelled_by_all_three]]));
    }
    var B = d.baseline_gold_dev;
    if (B) {
      old.appendChild(h('h3', 'Baseline on the development half of the answer key'));
      old.appendChild(h('p', 'Agreement counts a cannot tell answer as agreeing with every recount that did not flag the code, so it mostly measures how often a model abstains, not skill. Our referee caught this on 12 November. Read it beside the share of calls each model commits to, in the headline above.'));
      var order = ['base', 'llama', 'mistral', 'gemma'].filter(function (k) { return B[k]; }).concat(Object.keys(B).filter(function (k) { return ['base', 'llama', 'mistral', 'gemma'].indexOf(k) < 0; }));
      old.appendChild(table(['Model', 'Agree', 'Of', 'Agreement', '95% interval', 'Always guess the most common answer'],
        order.map(function (k) { var q = (B[k] || {}).pooled || {}; return [nm(k), q.agree, q.n, p3(q.rate), iv(q.wilson95), p3(B[k].majority_class_rate)]; })));
    }
    var C = d.bench_gold_dev;
    if (C && Object.keys(C).length) {
      old.appendChild(h('h3', 'Scoreboard: other small models on the same claims'));
      old.appendChild(table(['Model', 'Claims labelled', 'Agreement', '95% interval'],
        Object.keys(C).map(function (k) { var q = C[k].pooled || {}; return [k, C[k].labelled + ' of ' + C[k].n_items, p3(q.rate), iv(q.wilson95)]; })));
    }
    var R = d.training;
    if (R) {
      old.appendChild(h('h3', 'Training'));
      old.appendChild(table(['Reading', 'Value'], [['Base model', R.base + ' (' + R.license + ')'], ['Training rows', R.train_rows], ['Steps', R.iters], ['Seconds', R.seconds], ['LoRA rank', R.rank]]));
    }
    var P = d.paired_test;
    if (P) {
      var pp = (P.paired_stan_minus_base || {}).pooled || {};
      old.appendChild(h('h3', 'Paired test'));
      old.appendChild(table(['Reading', 'Value'], [
        ['Claims in the test half', P.n_items], ['Base agreement', p3(((P.base || {}).pooled || {}).rate)], ['STANYO agreement', p3(((P.stan || {}).pooled || {}).rate)],
        ['STANYO minus base, mean over seven codes', p3(pp.mean)], ['95% paired bootstrap interval', pp.ci95 ? '[' + p3(pp.ci95[0]) + ', ' + p3(pp.ci95[1]) + ']' : '-'],
        ["Band reading", P.band_reading], ['Kept', P.kept ? 'yes' : 'no']].concat(P.base_conversion && P.base_conversion.base ? [['Base answers turned into CANNOT_TELL by the quote rule (no word-for-word quote)', P.base_conversion.base.ct_by_quote_rule + ' of ' + P.base_conversion.base.calls], ['STANYO answers that chose CANNOT_TELL itself', P.base_conversion.stan.ct_chosen_by_model + ' of ' + P.base_conversion.stan.calls]] : [])));
      if (P.base_conversion) old.appendChild(h('p', 'The base model never chose CANNOT_TELL. Our quote rule made most of its answers CANNOT_TELL. STANYO chose it every time, so the two columns do not measure the same act.'));
    }
    var L = d.plan;
    if (L) {
      old.appendChild(h('h3', 'The plan, written first'));
      old.appendChild(table(['File', 'sha256', 'OpenTimestamps'], [['PLAN.md', L.sha256, L.stamp], ['PLAN_ADDENDUM_1.md', L.addendum_1_sha256, L.addendum_1_stamp]]));
    }
    box.appendChild(old);
  }
  function load() {
    fetch('/iris/lab/stan.json', { cache: 'no-store' }).then(function (r) { return r.json(); }).then(draw).catch(function () { box.textContent = 'The live feed is not reachable right now.'; });
  }
  load(); setInterval(load, 60000);
})();
