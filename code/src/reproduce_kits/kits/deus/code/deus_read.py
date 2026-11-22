#!/usr/bin/env python3
"""deus_read.py: DEUS reader, PLAN.md (sealed, indahl-ai/calibrations lane-research 8527300) applied as written.
Inputs (all saved first by fetch_reruns.py, fetch_stated.py, tables.py; untrusted, read as text only, nothing executed):
  raw/epoch/<date>/csv/*.csv                  Epoch AI Benchmarking Hub snapshot (read_reruns.py)
  raw/stated/<host>/<page>.{text,tables}.txt  the labs' own pages
  claims_text.json, claims_image.json         where each printed score sits on its page (no value is typed for text pages)
  stated_sources.json, raw/stated/fetch_log.jsonl
Outputs: data/deus.json (every claim, every pairing), summary_deus.json, data/deus_live.json, data/deus_history.jsonl.
--selftest: rule checks only. No network."""
import sys as _cfsys, os as _cfos
try:   # 22 Nov 2026: one shared Cloudflare part (lib/cf.py: kv token, rings on failure)
    _cfsys.path.insert(0, _cfos.path.expanduser('~/forge/lib')); from cf import run_put as _cf_run
except Exception:
    import subprocess as _cfsp; _cf_run = _cfsp.run
import os, sys, re, json, time, math, random, hashlib, collections as C
H = os.path.dirname(os.path.abspath(__file__)); os.chdir(H); sys.path.insert(0, H)
import heuremen_kit as K, read_reruns as RR
SEED = 20261122; NBOOT = 2000
FRAME_START, FRAME_END = '2026-01-01', '2026-10-31'
LABS = ['OpenAI', 'Anthropic', 'Google DeepMind', 'Meta', 'xAI', 'DeepSeek', 'Alibaba (Qwen)']
BENCH = ['GPQA Diamond', 'SWE-bench Verified', 'FrontierMath', "Humanity's Last Exam", 'AIME 2025']
COI = ('The readers and builders of this desk are Claude models, made by Anthropic, one of the labs measured. Anthropic rows get the same rules and '
       'outcomes as every other lab, with no rule written for one lab alone.')
PRELIM = 'PRELIMINARY: first run, not refereed'
FIELDS = RR.SETUP_FIELDS

# ---------------- models ----------------
# In-frame models: the lab's own page that introduces the model is dated 2026-01-01 to 2026-10-31 (page dates in PAGES below).
# key -> (lab, Epoch model_group or None, introducing page id)
MODELS = {
 'opus 4.6': ('Anthropic', 'Claude Opus 4.6', 'anthropic-claude-opus-4-6'), 'sonnet 4.6': ('Anthropic', 'Claude Sonnet 4.6', 'anthropic-claude-sonnet-4-6'),
 'mythos preview': ('Anthropic', 'Claude Mythos Preview', 'anthropic-claude-mythos-preview'), 'opus 4.7': ('Anthropic', 'Claude Opus 4.7', 'anthropic-claude-opus-4-7'),
 'opus 4.8': ('Anthropic', 'Claude Opus 4.8', 'anthropic-claude-opus-4-8'), 'fable 5': ('Anthropic', 'Claude Fable 5', 'anthropic-claude-fable-5'),
 'mythos 5': ('Anthropic', None, 'anthropic-claude-fable-5'), 'mythos 5 / fable 5': ('Anthropic', None, 'anthropic-claude-fable-5'),
 'sonnet 5': ('Anthropic', 'Claude Sonnet 5', 'anthropic-claude-sonnet-5'), 'opus 5': ('Anthropic', 'Claude Opus 5', 'anthropic-claude-opus-5'),
 'fable 5.1': ('Anthropic', 'Claude Fable 5.1', 'anthropic-claude-fable-5-1'), 'opus 5.5': ('Anthropic', 'Claude Opus 5.5', 'anthropic-claude-opus-5-5'),
 'sonnet 5.5': ('Anthropic', 'Claude Sonnet 5.5', 'anthropic-claude-sonnet-5-5'), 'haiku 5.5': ('Anthropic', 'Claude Haiku 5.5', 'anthropic-claude-haiku-5-5'),
 'gpt-5.3-codex': ('OpenAI', 'GPT-5.3 Codex', 'openai-gpt-5-3-codex'), 'gpt-5.4': ('OpenAI', 'GPT-5.4', 'openai-gpt-5-4'), 'gpt-5.4 pro': ('OpenAI', 'GPT-5.4 Pro', 'openai-gpt-5-4'),
 'gpt-5.4 mini': ('OpenAI', 'GPT-5.4 Mini', 'openai-gpt-5-4-mini-and-nano'), 'gpt-5.4 nano': ('OpenAI', 'GPT-5.4 Nano', 'openai-gpt-5-4-mini-and-nano'),
 'gpt-5.5': ('OpenAI', 'GPT-5.5', 'openai-gpt-5-5'), 'gpt-5.5 pro': ('OpenAI', 'GPT-5.5 Pro', 'openai-gpt-5-5'), 'gpt-5.5 instant': ('OpenAI', 'GPT-5.5 Instant', 'openai-gpt-5-5-instant'),
 'gpt-5.6 sol': ('OpenAI', 'GPT-5.6 Sol', 'openai-gpt-5-6'), 'gpt-5.6 terra': ('OpenAI', 'GPT-5.6 Terra', 'openai-gpt-5-6'), 'gpt-5.6 luna': ('OpenAI', 'GPT-5.6 Luna', 'openai-gpt-5-6'),
 'gpt-6 astra': ('OpenAI', 'GPT-6 Astra', 'openai-gpt-6-astra'), 'gpt-6 sol': ('OpenAI', 'GPT-6 Sol', 'openai-gpt-6-sol-and-luna'), 'gpt-6 luna': ('OpenAI', 'GPT-6 Luna', 'openai-gpt-6-sol-and-luna'),
 'gpt-6.1 sol': ('OpenAI', 'GPT-6.1 Sol', 'openai-gpt-6-1-sol'), 'gpt-6.1 terra': ('OpenAI', 'GPT-6.1 Terra', 'openai-gpt-6-1-terra'),
 'gemini 3.1 pro': ('Google DeepMind', 'Gemini 3.1 Pro', 'google-gemini-3-1-pro'), 'gemini 3.1 flash-lite': ('Google DeepMind', 'Gemini 3.1 Flash-Lite', 'google-gemini-3-1-flash-lite'),
 'gemini 3.5 flash': ('Google DeepMind', 'Gemini 3.5 Flash', 'google-gemini-3-5-flash'), 'gemini 3.5 flash-lite': ('Google DeepMind', 'Gemini 3.5 Flash-Lite', 'google-gemini-3-5-flash-lite'),
 'gemini 3.6 flash': ('Google DeepMind', 'Gemini 3.6 Flash', 'google-gemini-3-6-flash'), 'gemini 3.7 flash': ('Google DeepMind', 'Gemini 3.7 Flash', 'google-gemini-3-7-flash'),
 'gemini 3.8 flash': ('Google DeepMind', 'Gemini 3.8 Flash', 'google-gemini-3-8-flash'), 'gemini 4 argon': ('Google DeepMind', 'Gemini 4 Argon', 'google-gemini-4-argon'),
 'gemini 3 deep think': ('Google DeepMind', 'Gemini 3 Deep Think', 'google-gemini-3-deep-think'),
 'gemma 4 31b it': ('Google DeepMind', 'Gemma 4 31B IT', 'google-gemma-4'), 'gemma 4 26b a4b it': ('Google DeepMind', 'Gemma 4 26B A4B', 'google-gemma-4'),
 'gemma 4 e4b it': ('Google DeepMind', None, 'google-gemma-4'), 'gemma 4 e2b it': ('Google DeepMind', None, 'google-gemma-4'),
 'muse spark': ('Meta', 'Muse Spark', 'meta-muse-spark'), 'muse spark 1.1': ('Meta', 'Muse Spark 1.1', 'meta-muse-spark-1-1'), 'muse spark 1.2': ('Meta', 'Muse Spark 1.2', 'meta-muse-spark-1-2'),
 'muse spark 1.3': ('Meta', 'Muse Spark 1.3', 'meta-muse-spark-1-3'), 'muse glimmer-30b': ('Meta', 'Muse Glimmer', 'meta-muse-glimmer'), 'muse glimmer': ('Meta', 'Muse Glimmer', 'meta-muse-glimmer'),
 'muse wonder': ('Meta', 'Muse Wonder', 'meta-muse-wonder'), 'muse spark open': ('Meta', 'Muse Spark Open', 'meta-muse-spark-open'),
 'qwen3.5-397b-a17b': ('Alibaba (Qwen)', 'Qwen3.5 397B-A17B', 'alibaba-qwen3-5'), 'qwen3.6-plus': ('Alibaba (Qwen)', 'Qwen 3.6 Plus', 'alibaba-qwen3-6-plus'),
 'qwen3.6-max-preview': ('Alibaba (Qwen)', 'Qwen 3.6 Max (Preview)', 'alibaba-qwen3-6-max-preview'), 'qwen3.7-max': ('Alibaba (Qwen)', 'Qwen3.7-Max', 'alibaba-qwen3-7-max'),
 'qwen3.7-plus': ('Alibaba (Qwen)', 'Qwen3.7-Plus', 'alibaba-qwen3-7-plus'), 'qwen3.8-max': ('Alibaba (Qwen)', 'Qwen 3.8 Max', 'alibaba-qwen3-8-max'),
 'qwen3.8-27b': ('Alibaba (Qwen)', 'Qwen 3.8 27B', 'alibaba-qwen3-8-flash'), 'qwen3.8-flash-next': ('Alibaba (Qwen)', None, 'alibaba-qwen3-8-flash'),
 'qwen3.6-27b': ('Alibaba (Qwen)', 'Qwen3.6 27B', 'alibaba-qwen3-6-27b-card'), 'qwen3.6-35b-a3b': ('Alibaba (Qwen)', 'Qwen 3.6 35B-A3B', 'alibaba-qwen3-6-35b-a3b-card'),
 'deepseek-v4-pro': ('DeepSeek', 'DeepSeek-V4-Pro', 'deepseek-deepseek-v4'), 'ds-v4-pro': ('DeepSeek', 'DeepSeek-V4-Pro', 'deepseek-deepseek-v4'),
 'deepseek-v4-flash': ('DeepSeek', 'DeepSeek-V4-Flash', 'deepseek-deepseek-v4'), 'deepseek-v4-flash-0731': ('DeepSeek', 'DeepSeek V4 Flash 0731', 'deepseek-deepseek-v4-flash-0731-card'),
 'deepseek-v4-pro-0813': ('DeepSeek', 'DeepSeek V4 Pro 0813', 'deepseek-deepseek-v4-pro-0813-card'), 'deepseek-v4.1-flash': ('DeepSeek', 'DeepSeek V4.1 Flash', 'deepseek-deepseek-v4-1-flash'),
 'deepseek-v4.1-flash-1017': ('DeepSeek', 'DeepSeek V4.1 Flash 1017', 'deepseek-deepseek-v4-1-flash-1017'),
 'grok 4.5': ('xAI', 'Grok 4.5', 'xai-grok-4-5'), 'grok 4.6': ('xAI', 'Grok 4.6', 'xai-grok-4-6'), 'grok 4.7': ('xAI', 'Grok 4.7', 'xai-grok-4-7'), 'grok build 0.1': ('xAI', 'Grok Build 0.1', 'xai-grok-build-0-1'),
}
# Models printed only as comparisons (introduced before the window or by a page outside the frame): used for order claims (type 2) only.
OTHERS = {'opus 4.5': 'Claude Opus 4.5', 'sonnet 4.5': 'Claude Sonnet 4.5', 'haiku 4.5': 'Claude Haiku 4.5', '4.5 haiku': 'Claude Haiku 4.5', 'gemini 3 pro': 'Gemini 3 Pro',
          'gemini 3 flash': 'Gemini 3 Flash', 'gpt-5.2': 'GPT-5.2', 'gpt-5.2 pro': 'GPT-5.2 Pro', 'gpt-5 mini': 'GPT-5 mini', 'gemini 2.5 flash': None, 'gemini 2.5 flash-lite': None,
          'grok 4.1 fast': None, 'gemma 3 27b it': 'Gemma 3 27B', 'gpt-5.2-codex': None, 'gemini 3.1-pro': 'Gemini 3.1 Pro', 'gemma4-31b': 'Gemma 4 31B IT',
          'k2.6': None, 'glm-5.1': None, 'k2.5-1t-a32b': None, 'qwen3-max': None, 'gpt5.2': 'GPT-5.2', 'gemini-3 pro': 'Gemini 3 Pro', 'gemini3.1-pro': 'Gemini 3.1 Pro', 'gemini-3.1-pro': 'Gemini 3.1 Pro', 'k3': None, 'kimi k3': None, 'glm 5.3': None, 'glm-5.3': None, 'gpt-5.6-sol': 'GPT-5.6 Sol', 'opus 5.0': 'Claude Opus 5', 'k2.6': None}
EFFORTS = ['max', 'xhigh', 'high', 'medium', 'low', 'none', 'minimal']

def norm_label(label):
    """column label as printed -> (model key, effort or None, the label). Effort words are read only from the label itself."""
    s = label.replace('‑', '-').replace('‐', '-').replace('¹', '').replace('¹', '')
    s = re.sub(r'(?i)\(?for reference\)?|\(all models\)', '', s).strip()
    s = re.sub(r'(?i)^claude\s+', '', s).strip()
    s = re.sub(r'(?i)^claude-', '', s).strip()
    eff = None; word = None
    for _ in range(3):
        m = re.search(r'(?i)\bthinking\s*\((max|xhigh|high|medium|low)\)|\((max|xhigh|high|medium|low|none|minimal)\)|\s(high|low|medium|xhigh|max)$', s)
        if m: eff = eff or (m.group(1) or m.group(2) or m.group(3)).lower(); s = (s[:m.start()] + s[m.end():]).strip()
        for w in ('Extended Thinking', 'Thinking Mode', 'Dynamic', 'Reasoning', 'Thinking'):
            if s.lower().endswith(' ' + w.lower()): word = word or w.lower(); s = s[:-len(w)].strip()
    eff = eff or word
    s = re.sub(r'(?i)^(opus|sonnet|haiku|fable|mythos)[-\s]?(\d)', lambda m: m.group(1) + ' ' + m.group(2), s)
    s = re.sub(r'(?i)^gpt[-\s]?(\d)', r'GPT-\1', s)
    s = re.sub(r'(?i)\s+non-think$', ' (none)', s)
    m2 = re.search(r'\((none)\)$', s)
    if m2: eff = eff or 'none'; s = s[:m2.start()].strip()
    s = re.sub(r'(?i)^(?:deepseek[-\s]|ds-)?(v4(?:\.1)?)', lambda m: 'deepseek-' + m.group(1).lower(), s) if re.match(r'(?i)^(deepseek[-\s]v4|ds-v4|v4)', s) else s
    s = re.sub(r'(?i)^(deepseek-v4(?:\.1)?)[-\s]+(pro|flash)[-\s]*(\d{4})?$', lambda m: m.group(1) + '-' + m.group(2).lower() + ('-' + m.group(3) if m.group(3) else ''), s)
    s = re.sub(r'\s+preview$', '', s, flags=re.I) if not s.lower().startswith('mythos') else s
    k = re.sub(r'\s+', ' ', s.lower()).replace('gpt 5', 'gpt-5').replace('gpt 6', 'gpt-6')
    if k == '4.5 haiku': k = 'haiku 4.5'
    return k, eff, label

def epoch_effort(name, version):
    m = re.search(r'\(([^)]*)\)\s*$', name or '')
    t = (m.group(1) if m else '').lower()
    if not t:
        v = (version or '').lower()
        m2 = re.search(r'[_-](max|xhigh|high|medium|low|none)$', v) or re.search(r'thinking-(max)', v)
        if m2: return m2.group(1), None
        if 'non-thinking' in (name or '').lower(): return 'none', None
        return None, None
    variant = 'with fallback' if 'fallback' in t else None
    t = t.replace('with fallback,', '').strip()
    if t in ('no thinking', 'non-thinking', 'none'): return 'none', variant
    if re.fullmatch(r'\d+k thinking', t): return t + ' budget', variant
    if t in EFFORTS: return t, variant
    if re.fullmatch(r'\d{4}-\d{2}-\d{2}', t) or t in ('preview', 'unknown thinking'): return None, variant
    return t, variant

# ---------------- pages ----------------
MONTHS = {m: i + 1 for i, m in enumerate(['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'])}
MON3 = {k[:3]: v for k, v in MONTHS.items()}
def page_date(text):
    """the page's own date as printed: 'Published <date>' first, else the first full date in the page head. Returns (iso or None, quote)."""
    for pat in (r'Published:?\s+(\d{1,2}) ([A-Z][a-z]+) (20\d\d)', r'Published:?\s+([A-Z][a-z]{2})[a-z]* (\d{1,2}), (20\d\d)'):
        m = re.search(pat, text)
        if m:
            g = m.groups()
            if g[0].isdigit(): d, mo, y = int(g[0]), MONTHS.get(g[1]), int(g[2])
            else: mo, d, y = MON3.get(g[0]), int(g[1]), int(g[2])
            if mo: return '%04d-%02d-%02d' % (y, mo, d), m.group(0)
    m = re.search(r'^(.+) (20\d\d)/(\d\d)/(\d\d)\nOn this page', text, re.M)   # DeepSeek news pages: the entry for the page itself, just above its body
    if m: return '%s-%s-%s' % (m.group(2), m.group(3), m.group(4)), m.group(0).split('\n')[0]
    head = '\n'.join(text.split('\n')[:30])
    m = re.search(r'(?<!Update on )\b(' + '|'.join(MONTHS) + r') (\d{1,2}), (20\d\d)', head)
    if m and not re.search(r'Update on\s*$', head[:m.start()]):
        return '%04d-%02d-%02d' % (int(m.group(3)), MONTHS[m.group(1)], int(m.group(2))), m.group(0)
    m = re.search(r'(?:Back to news|News|Research)\s+(' + '|'.join(MON3) + r') (\d{1,2}), (20\d\d)', head)
    if m: return '%04d-%02d-%02d' % (int(m.group(3)), MON3[m.group(1)], int(m.group(2))), m.group(0)
    m = re.search(r'^(' + '|'.join(MONTHS) + r') (20\d\d)$', head, re.M)
    if m: return '%04d-%02d' % (int(m.group(2)), MONTHS[m.group(1)]), m.group(0) + ' (month only)'
    return None, None

def load_pages():
    src = {s['id']: s for s in json.load(open('stated_sources.json'))}
    log = {}
    for l in open('raw/stated/fetch_log.jsonl'):
        r = json.loads(l); log[r['id']] = r   # the last fetch of each page
    P = {}
    for pid, s in src.items():
        r = log.get(pid, {}); tp = os.path.join(H, r['text']) if r.get('text') else None
        text = open(tp, encoding='utf-8').read() if tp and os.path.exists(tp) else ''
        d, q = page_date(text) if text else (None, None)
        if 'huggingface.co/' in s['url']: d, q = None, 'a model card on Hugging Face prints no page date (the date found in the page chrome is not the card\'s)'
        P[pid] = dict(id=pid, lab=s['lab'], model=s['model'], url=s['url'], kind=s['kind'], status=r.get('status', 'NOT_FETCHED'), read_utc=r.get('fetched_utc'),
                      date=d, date_quote=q, text_path=r.get('text'), sha256=r.get('sha256'), images=r.get('images') or [])
    # pages whose own launch date is not printed in the page head (checked by reading): the date is inferred and labelled as such
    for pid, d, why in (('openai-gpt-6-astra', '2026-09-22', 'not printed; the earliest update line on the page reads "Update on September 22, 2026", so the page is from that day or before'),):
        if pid in P and (P[pid]['date'] is None or P[pid]['date'] > d): P[pid].update(date=d, date_quote=why, date_inferred=True)
    return P

def in_window(d): return d is not None and FRAME_START[:len(d)] <= d <= FRAME_END[:len(d)]

# ---------------- stated claims ----------------
PCT = re.compile(r'^\s*(\d+(?:\.\d+)?)\s*%')
def parse_cell(c):
    """'60.9%no tools' -> ('60.9%', 0.609, 'no tools'); '—' or '-' -> None"""
    c = (c or '').strip()
    m = PCT.match(c)
    if not m:
        # a bare number in a score table whose cells carry no percent sign (Qwen and DeepSeek cards print accuracy as 0 to 100 with no sign)
        b = re.match(r'^\s*(\d{1,2}(?:\.\d+)?|100(?:\.0+)?)\s*$', c)
        if not b: return None
        return (b.group(1), float(b.group(1)) / 100, None)
    return (m.group(1) + '%', float(m.group(1)) / 100, c[m.end():].strip() or None)

def table_row(page, line):
    import glob as _g
    fs = _g.glob(os.path.join('raw', 'stated', '*', page + '.tables.txt'))
    if len(fs) != 1: raise SystemExit('tables file for %s: %r' % (page, fs))
    host = fs[0].split(os.sep)[-2]
    L = open(fs[0], encoding='utf-8').read().split('\n')
    row = L[line - 1]; i = line - 1
    while i > 0 and not L[i].startswith('=== table'): i -= 1
    header = L[i + 1]
    return header, row, os.path.join('raw', 'stated', host, page + '.tables.txt')

def page_effort(page, lab):
    """an effort the page states for all of its own evaluations (quoted from the saved page text)"""
    Q = {'openai-gpt-5-4': ('xhigh', 'Evals were run with reasoning effort set to xhigh, except where specified otherwise.'),
         'openai-gpt-5-5': ('xhigh', 'Evals of GPT were run with reasoning effort set to xhigh'),
         'openai-gpt-5-3-codex': ('xhigh', 'All evaluations in the blog were run on GPT-5.3-Codex with xhigh reasoning effort.')}
    return Q.get(page, (None, None))

def build_claims(P):
    T = json.load(open('claims_text.json')); I = json.load(open('claims_image.json'))
    rows = []   # one per printed cell: (page, benchmark, column label, printed, value, variant, quote, source)
    problems = []
    for r in T['table_rows']:
        header, row, f = table_row(r['page'], r['line'])
        hc = header.split(' | '); rc = row.split(' | ')
        nv = len([x for x in hc]) ; hv = hc[-len(rc):] if len(rc) <= len(hc) else None
        # value columns align from the right: a continuation row lacks the leading label cell(s)
        cols = hc[1:] if hc and hc[0].strip() in ('', 'Benchmark', 'Eval', 'Academic', 'Category') else hc
        while cols and cols[0].strip() in ('', 'Benchmark', 'Notes'): cols = cols[1:]
        vals = rc[-len(cols):]
        lead = rc[:-len(cols)]
        note_variant = lead[-1].strip() if len(lead) >= 1 and not re.search(r'(?i)gpqa|swe-bench|frontiermath|humanity|aime|reasoning', lead[-1]) else None
        bench_label = ' '.join(lead).strip()
        paren = re.search(r'\(([^)]*)\)\s*$', bench_label)
        for col, v in zip(cols, vals):
            if not col.strip(): continue
            p = parse_cell(v)
            variant = (p[2] if p else None) or note_variant or (paren.group(1) if paren else None)
            rows.append(dict(page=r['page'], benchmark=r['benchmark'], label=col.strip(), cell=v.strip(), printed=p[0] if p else None, value=p[1] if p else None,
                             variant=variant, row_label=bench_label, source='text table', quote=row, header=header, where='%s line %d' % (f, r['line'])))
    for r in I['rows']:
        meta = next((im for im in P[r['page']]['images'] if (im.get('saved') or '').split('.')[-2] == r['image']), {})
        for col, pr, nt in zip(r['columns'], r['printed'], r['note']):
            p = parse_cell(pr) if pr else None
            rows.append(dict(page=r['page'], benchmark=r['benchmark'], label=col, cell=pr or '—', printed=p[0] if p else None, value=p[1] if p else None,
                             variant=r['variant'], cell_note=nt, row_label=r['benchmark'], source='image table', quote='%s: %s' % (col, pr or '—'),
                             header=' | '.join(r['columns']), where='%s (sha256 %s)' % (meta.get('saved'), (meta.get('sha256') or '')[:16])))
    for r in T['text_claims']:
        tp = P[r['page']]['text_path']; line = open(tp, encoding='utf-8').read().split('\n')[r['line'] - 1]
        if r['printed'] not in line: problems.append('text claim %s line %d: %s not on the line' % (r['page'], r['line'], r['printed'])); continue
        p = parse_cell(r['printed'])
        rows.append(dict(page=r['page'], benchmark=r['benchmark'], label=r['model'], cell=r['printed'], printed=p[0], value=p[1], variant=r['variant'], row_label=r['benchmark'],
                         source='running text', quote=line.strip(), header=None, where='%s line %d' % (tp, r['line'])))
    return rows, problems

# ---------------- reading rules ----------------
def stated_range(printed):
    """printed rounding: '88.2%' -> (0.8815, 0.8825); '92%' -> (0.915, 0.925)"""
    s = printed.rstrip('%'); dec = len(s.split('.')[1]) if '.' in s else 0; h = 0.5 * 10 ** (-dec) / 100; v = float(s) / 100
    return v - h, v + h

def position(srange, lo, hi):
    """where the stated value sits against one rerun interval: 'inside', 'above', 'below' or None (no interval)"""
    if lo is None or hi is None: return None
    a, b = srange
    if a > hi: return 'above'
    if b < lo: return 'below'
    return 'inside'

def setup_unmatched(stated, rerun):
    """fields not named on both sides or named differently (PACK L carriers). stated, rerun: dicts field -> text or None"""
    out = []
    for f in FIELDS:
        a, b = stated.get(f), rerun.get(f)
        if a is None or b is None: out.append('%s unnamed (%s)' % (f, 'both sides' if a is None and b is None else ('stated side' if a is None else 'rerun side')))
        elif f == 'reasoning effort' and str(a).lower() != str(b).lower(): out.append('reasoning effort differs (%s against %s)' % (a, b))
    return out

def read_claim(c, reruns):
    """PLAN.md sections 4 and 5 for one claim. reruns: the independent rerun rows of this pairing."""
    sr = stated_range(c['printed'])
    pos = [(r, position(sr, r['lo'], r['hi'])) for r in reruns]
    withint = [(r, p) for r, p in pos if p is not None]
    if not withint: return dict(outcome=K.CANNOT_TELL, reason=K.NO_INTERVAL_FORMABLE, direction=None, carriers=[])
    sides = {p for _, p in withint}
    if 'above' in sides and 'below' in sides: return dict(outcome=K.CANNOT_TELL, reason='RERUNS_DISAGREE', direction=None, carriers=[])
    carriers = sorted({u for r, _ in withint for u in setup_unmatched(c['setup'], r['setup'])})
    if sides == {'inside'}: return dict(outcome=K.CONSISTENT, reason=None, direction=None, carriers=carriers)
    d = 'above' if 'above' in sides else 'below'
    if carriers or 'inside' in sides:
        return dict(outcome=K.CANNOT_TELL, reason='SETUP_UNMATCHED' if carriers else 'RERUNS_DISAGREE', direction=d, carriers=carriers)
    return dict(outcome=K.ABOVE if d == 'above' else K.BELOW, reason=None, direction=d, carriers=[])

def selftest():
    full = {f: 'x' for f in FIELDS}
    c = dict(printed='88.2%', setup=dict(full))
    R = lambda lo, hi, s=None: dict(lo=lo, hi=hi, setup=s or dict(full))
    assert stated_range('88.2%') == (0.8815000000000001, 0.8825) or abs(stated_range('88.2%')[0] - 0.8815) < 1e-12
    assert read_claim(c, [R(0.80, 0.85)])['outcome'] == K.ABOVE
    assert read_claim(c, [R(0.90, 0.95)])['outcome'] == K.BELOW
    assert read_claim(c, [R(0.88, 0.89)])['outcome'] == K.CONSISTENT
    assert read_claim(c, [R(0.8825, 0.89)])['outcome'] == K.CONSISTENT   # touches the rounding edge
    part = dict(full); part['temperature'] = None
    x = read_claim(c, [R(0.80, 0.85, part)]); assert x['outcome'] == K.CANNOT_TELL and x['direction'] == 'above' and x['reason'] == 'SETUP_UNMATCHED'
    assert read_claim(c, [R(0.80, 0.85), R(0.90, 0.95)])['reason'] == 'RERUNS_DISAGREE'
    assert read_claim(c, [R(None, None)])['reason'] == K.NO_INTERVAL_FORMABLE
    assert read_claim(c, [R(0.88, 0.89, part)])['outcome'] == K.CONSISTENT and read_claim(c, [R(0.88, 0.89, part)])['carriers']
    e = dict(full); e['reasoning effort'] = 'max'; f = dict(full); f['reasoning effort'] = 'xhigh'
    assert read_claim(dict(printed='88.2%', setup=e), [R(0.80, 0.85, f)])['outcome'] == K.CANNOT_TELL
    assert norm_label('Gemini 3.1 Pro Thinking (High)')[:2] == ('gemini 3.1 pro', 'high')
    assert norm_label('GPT‑5.4 Pro')[:2] == ('gpt-5.4 pro', None)
    assert norm_label('GPT-5.4 mini (xhigh)')[:2] == ('gpt-5.4 mini', 'xhigh')
    assert norm_label('Sonnet 5.5For reference')[0] == 'sonnet 5.5'
    assert norm_label('Claude Mythos Preview')[0] == 'mythos preview'
    assert norm_label('Gemini 3.1 Flash-Lite High')[:2] == ('gemini 3.1 flash-lite', 'high')
    assert norm_label('Claude 4.5 Haiku Extended Thinking')[0] == 'haiku 4.5'
    assert epoch_effort('Claude Opus 4.6 (32k thinking)', '') == ('32k thinking budget', None)
    assert epoch_effort('Claude Opus 5.5 (with fallback, max)', '') == ('max', 'with fallback')
    assert epoch_effort('claude-opus-4-6-thinking-max', 'claude-opus-4-6-thinking-max') == ('max', None)
    assert parse_cell('60.9%no tools') == ('60.9%', 0.609, 'no tools') and parse_cell('—') is None
    print('deus selftest: ok')


# ---------------- the run ----------------
# Setup words printed beside a score in a footnote of the same page (quoted from the saved page text by the reader).
FOOT = {('anthropic-claude-opus-4-6', 'SWE-bench Verified'): {'trials averaged': '25 ("Our score was averaged over 25 trials")'},
        ('anthropic-claude-sonnet-4-6', 'SWE-bench Verified'): {'trials averaged': '10 ("Our score was averaged over 10 trials")'}}
FM_V2_DATE = '2026-06-12'   # Epoch: "On 2026-06-12, we released a major update" (raw/epoch/pages/benchmarks_frontiermath.text.txt)

def stated_setup(row, eff, page, bench):
    st = {f: None for f in FIELDS}
    if eff: st['reasoning effort'] = eff
    v = (row.get('variant') or '')
    if re.search(r'(?i)no tools|without tools', v): st['tools and scaffold'] = 'no tools'
    elif re.search(r'(?i)with tools|search|code|w/ tools', v): st['tools and scaffold'] = v
    if re.search(r'(?i)single attempt', v): st['attempts'] = 'single attempt'
    if re.search(r'(?i)prompt modification', v): st['prompt format'] = 'a prompt modification (not printed)'
    st['dataset version'] = row.get('row_label') or bench
    st.update(FOOT.get((page, bench), {}))
    return st

def fm_file(row, pdate):
    lab = row.get('row_label') or ''
    if 'v2' in lab: return 'frontiermath_tiers_1_3_v2.csv'
    if pdate and pdate < FM_V2_DATE: return 'frontiermath.csv'
    return 'frontiermath_tiers_1_3_v2.csv'

def candidates(group, bench, eff, reruns, row, pdate):
    """the independent rerun rows of one pairing, and why there are none"""
    if group is None: return [], 'no rerun source names this model'
    rs = [r for r in reruns.get(bench, []) if r['group'] == group]
    if bench == 'FrontierMath':
        f = fm_file(row, pdate); rs = [r for r in rs if r['file'] == f]
    if not rs: return [], 'no independent rerun of this model on this benchmark'
    out = []
    for r in rs:
        e, var = epoch_effort(r['name'], r['model_version'])
        st = dict(r['setup']); st['reasoning effort'] = e
        if var: st['tools and scaffold'] = (st.get('tools and scaffold') or '') + ' (' + var + ')'
        out.append(dict(r, setup=st, effort=e, variant=var))
    if eff:
        same = [r for r in out if r['effort'] is None or r['effort'] == eff]
        if not same: return [], 'reruns exist only at another reasoning effort (%s), a different pairing' % ', '.join(sorted({str(r['effort']) for r in out}))
        out = same
    return out, None

def block_boot(groups, nboot=NBOOT, seed=SEED):
    """share ABOVE with a 95%% percentile interval from a bootstrap that draws whole models (claims of one model stay together)"""
    keys = sorted(groups); rnd = random.Random(seed)
    if not keys: return None, None, None
    tot = sum(len(groups[k]) for k in keys); ab = sum(sum(1 for o in groups[k] if o == K.ABOVE) for k in keys)
    draws = []
    for _ in range(nboot):
        pick = [keys[rnd.randrange(len(keys))] for _ in keys]
        n = sum(len(groups[k]) for k in pick); a = sum(sum(1 for o in groups[k] if o == K.ABOVE) for k in pick)
        draws.append(a / n if n else 0.0)
    draws.sort()
    return ab / tot, draws[int(0.025 * nboot)], draws[int(0.975 * nboot) - 1]

def scan_other_types(P):
    """types 3 to 5: every line of the in-frame pages that states a context window, a knowledge cutoff, a price or a speed (candidate claims, counted)"""
    pats = {'context': re.compile(r'(?i)(\d[\d,.]*\s*(?:[KkMm]|million|thousand)?[- ]token context|context window of [^.]{0,40}\d|\d[\d,.]*\s*(?:[KkMm]|million)\s+(?:token\s+)?context window)'),
            'cutoff': re.compile(r'(?i)(knowledge|training[- ]data|data) cut-?off'),
            'speed_price': re.compile(r'(?i)(\$\s?\d+(?:\.\d+)?\s*(?:per|/)\s*(?:1M|million|M)\b|price \$/1M|tokens per second|tokens/s(?:ec)?\b|output tokens per second)')}
    out = {k: [] for k in pats}
    for pid, pg in P.items():
        if not pg.get('text_path') or not in_window(pg.get('date')): continue
        for i, line in enumerate(open(pg['text_path'], encoding='utf-8').read().split('\n')):
            for k, rx in pats.items():
                if rx.search(line): out[k].append(dict(page=pid, lab=pg['lab'], line_no=i + 1, line=line.strip()[:300], url=pg['url']))
    return out

def held_pages_of(P):
    # PLAN.md section 5: a page read only in part is held, listed by URL, and left out of the headline. A page counts as read in part when its fetch failed
    # or when an image on it that may hold a table (empty alt, or alt naming a table, benchmark, chart or evaluation) was refused by robots.txt or did not return.
    held_pages = []
    for pid, pg in P.items():
        if pg['status'] != 200: held_pages.append(dict(id=pid, lab=pg['lab'], url=pg['url'], why='the page did not return (%s)' % pg['status'])); continue
        miss = [im for im in pg['images'] if im.get('status') in ('ROBOTS_DISALLOWED', 'NOTHING_RETURNED')]
        if miss: held_pages.append(dict(id=pid, lab=pg['lab'], url=pg['url'], why='%d table or chart images not read (%s)' % (len(miss), ', '.join(sorted({im['status'] for im in miss})))))
    for pid, why in MANUAL_HELD.items():
        if pid in P and pid not in {h['id'] for h in held_pages}: held_pages.append(dict(id=pid, lab=P[pid]['lab'], url=P[pid]['url'], why=why))
    return held_pages

# pages read by the reader and found to be read only in part in a way the image check above cannot see
MANUAL_HELD = {
    'meta-muse-wonder': 'the page says it "achieves state-of-the-art results across key benchmarks" but serves no table or chart in its HTML. Its media sit on lookaside.fbsbx.com, which robots.txt refuses to this reader',
    'alibaba-qwen3-6-plus': 'the page presents its evaluations but serves no table or table image in its HTML (read 22 Nov 2026), so the scores were not read',
    'alibaba-qwen3-6-max-preview': 'the page says "Below we present evaluations" but serves no table or table image in its HTML, so the scores were not read',
    'meta-muse-spark-open': 'the page has a "Key Benchmarks" section with no table or chart in its HTML as served. Its media sit on lookaside.fbsbx.com, which robots.txt refuses to this reader',
}

def main():
    P = load_pages(); rows, problems = build_claims(P); reruns = RR.all_rows(); held_pages = held_pages_of(P); held_ids = {h['id'] for h in held_pages}
    # benchmarks in the frame: kept only if the zip holds at least one independent run (PLAN.md section 4). Read from the file list and its columns, never a score.
    bstat = {}
    for b in BENCH:
        rs = reruns.get(b, [])
        indep = [r for r in rs if r['kind'] == 'Epoch internal' or (r['source'] and r['setup'].get('harness'))]
        if indep: bstat[b] = dict(status='in frame', independent_rows=len(indep), why='Epoch AI internal runs (%s)' % ', '.join(sorted({r['file'] for r in indep})))
        elif rs: bstat[b] = dict(status='dropped', independent_rows=0, why='The zip holds %d rows (%s) from "official leaderboards or primary sources", with no source column and no setup named on any row, so none can be shown to be a third-party run with a stated setup (PLAN.md section 4). Dropped, nothing replaces it.' % (len(rs), rs[0]['file']))
        else: bstat[b] = dict(status='dropped', independent_rows=0, why=RR.DROPPED.get(b, 'no rows in the zip'))
    # own claims: a column whose model is one of the page lab's in-frame models
    claims = {}; order_rows = []; out_of_frame = []; held = []
    labmap = {'Google DeepMind': 'Google DeepMind', 'Meta': 'Meta', 'Alibaba (Qwen)': 'Alibaba (Qwen)'}
    for r in rows:
        pg = P[r['page']]; k, eff, _ = norm_label(r['label'])
        own = k in MODELS and MODELS[k][0] == pg['lab']
        if not own: continue
        if r['printed'] is None: continue
        intro = P.get(MODELS[k][2], {}); idate = intro.get('date')
        pe, pq = page_effort(r['page'], pg['lab'])
        eff2 = eff or pe
        # one claim per model, benchmark, variant and printed figure: the same figure printed on several pages of the lab is one claim with every page
        # listed. An effort named on one page fills in a page that names none; two pages naming different efforts stay two claims.
        key = (k, r['benchmark'], (r.get('variant') or '').lower().strip(), r['printed'], '')
        c = claims.get(key)
        if c is not None and eff2 and c['effort'] and c['effort'] != eff2:
            key = key[:4] + (eff2,); c = claims.get(key)
        if c is not None and eff2 and not c['effort']:
            c['effort'] = eff2; c['setup']['reasoning effort'] = eff2; c['effort_source'] = ('column label' if eff else 'page: "%s"' % pq) + ' (%s)' % r['page']
        if c is None:
            c = claims[key] = dict(lab=pg['lab'], model=k, model_label=r['label'], epoch_group=MODELS[k][1], benchmark=r['benchmark'], variant=r.get('variant'), printed=r['printed'],
                                   value=r['value'], effort=eff2, effort_source=('column label' if eff else ('page: "%s"' % pq if pe else None)), intro_page=MODELS[k][2], intro_date=idate,
                                   pages=[], setup=stated_setup(r, eff2, r['page'], r['benchmark']), page_date=pg['date'], coi=(COI if pg['lab'] == 'Anthropic' else None))
        c['pages'].append(dict(page=r['page'], url=pg['url'], page_date=pg['date'], read_utc=pg['read_utc'], source=r['source'], where=r['where'], quote=r['quote'], header=r.get('header')))
        if r['benchmark'] in bstat and bstat[r['benchmark']]['status'] == 'in frame': order_rows.append((r, k, eff2))
    # frame membership and readings
    out = []
    for key, c in claims.items():
        if all(pp['page'] in held_ids for pp in c['pages']): c.update(outcome='HELD', reason='every page printing it was read only in part')
        elif not c['intro_date']: c.update(outcome='HELD', reason='the page that introduces the model prints no date, so frame membership cannot be read')
        elif not in_window(c['intro_date']): c.update(outcome='OUT_OF_FRAME', reason='introduced %s' % c['intro_date'])
        elif bstat[c['benchmark']]['status'] != 'in frame': c.update(outcome='BENCHMARK_DROPPED', reason=bstat[c['benchmark']]['why'])
        else:
            first = c['pages'][0]; rr = dict(row_label=next((rw['row_label'] for rw in rows if rw['page'] == first['page'] and rw['quote'] == first['quote']), c['benchmark']))
            cand, why = candidates(c['epoch_group'], c['benchmark'], c['effort'], reruns, rr, c['page_date'])
            c['reruns'] = [dict(file=x['file'], model_version=x['model_version'], name=x['name'], effort=x['effort'], value=x['value'], lo=x['lo'], hi=x['hi'], interval=x['interval_what'], row_id=x['row_id']) for x in cand]
            if not cand: c.update(outcome=K.NOTHING_RETURNED, reason='no independent rerun: ' + why)
            else: c.update(read_claim(c, cand))
        out.append(c)
    # headline (type 1)
    read = [c for c in out if c['outcome'] in K.OUTCOMES]
    groups = C.defaultdict(list)
    for c in read: groups[c['model']].append(c['outcome'])
    share, lo, hi = block_boot(groups)
    four = {o: sum(1 for c in read if c['outcome'] == o) for o in K.OUTCOMES}
    ct_reasons = C.Counter(c['reason'] for c in read if c['outcome'] == K.CANNOT_TELL)
    ct_dir = C.Counter(c.get('direction') for c in read if c['outcome'] == K.CANNOT_TELL)
    frame = [c for c in out if c['outcome'] in K.OUTCOMES or c['outcome'] == K.NOTHING_RETURNED]
    norerun = [c for c in out if c['outcome'] == K.NOTHING_RETURNED]
    nr_by = C.Counter((c['lab'], c['benchmark']) for c in norerun)
    # type 2: order claims
    ords = {}
    for r, k, eff in order_rows:
        pg = P[r['page']]
        if not in_window(P.get(MODELS[k][2], {}).get('date')): continue
        for r2 in rows:
            if r2['page'] != r['page'] or r2['quote'] != r['quote'] or r2 is r or r2['printed'] is None: continue
            if r['source'] == 'image table' and (r2['header'] != r['header'] or r2.get('variant') != r.get('variant')): continue
            k2, e2, _ = norm_label(r2['label'])
            if k2 == k: continue
            g2 = MODELS[k2][1] if k2 in MODELS else OTHERS.get(k2)
            if k2 in MODELS and MODELS[k2][0] == pg['lab'] and not e2: e2 = page_effort(r['page'], pg['lab'])[0]
            if r['value'] == r2['value']: continue
            hiR, loR = ((r, k, eff, MODELS[k][1]), (r2, k2, e2, g2)) if r['value'] > r2['value'] else ((r2, k2, e2, g2), (r, k, eff, MODELS[k][1]))
            okey = (hiR[1], hiR[2] or '', loR[1], loR[2] or '', r['benchmark'], hiR[0]['printed'], loR[0]['printed'])
            if okey in ords: ords[okey]['pages'].append(r['page']); continue
            o = dict(lab=pg['lab'], benchmark=r['benchmark'], higher=hiR[1], higher_printed=hiR[0]['printed'], higher_effort=hiR[2], lower=loR[1], lower_printed=loR[0]['printed'], lower_effort=loR[2],
                     pages=[r['page']], coi=(COI if pg['lab'] == 'Anthropic' else None))
            rr = dict(row_label=r.get('row_label'))
            A, wa = candidates(hiR[3], r['benchmark'], hiR[2], reruns, rr, pg['date']); Bc, wb = candidates(loR[3], r['benchmark'], loR[2], reruns, rr, pg['date'])
            if not A or not Bc: o.update(outcome=K.NOTHING_RETURNED, reason='no independent rerun of both models under one source: ' + (wa or wb))
            else:
                apart_up = all(a['lo'] is not None and b['hi'] is not None and a['lo'] > b['hi'] for a in A for b in Bc)
                apart_dn = all(a['hi'] is not None and b['lo'] is not None and a['hi'] < b['lo'] for a in A for b in Bc)
                same = all(a['file'] == b['file'] and a['effort'] is not None and a['effort'] == b['effort'] and not a['variant'] and not b['variant'] for a in A for b in Bc)
                if apart_up and same: o.update(outcome=K.CONSISTENT, reason=None)
                elif apart_dn and same: o.update(outcome=K.ABOVE, reason=None)
                else: o.update(outcome=K.CANNOT_TELL, reason='SETUP_UNMATCHED' if not same else 'INTERVALS_OVERLAP',
                               direction=('rerun order agrees' if apart_up else ('rerun order reversed' if apart_dn else None)))
                o['reruns'] = dict(higher=[(a['name'], a['value'], a['lo'], a['hi']) for a in A], lower=[(b['name'], b['value'], b['lo'], b['hi']) for b in Bc])
            ords[okey] = o
    ordl = list(ords.values())
    oth = scan_other_types(P)
    labs_cov = sorted({pg['lab'] for pg in P.values() if pg.get('text_path')})
    pages_read = [dict(id=pid, lab=pg['lab'], url=pg['url'], kind=pg['kind'], page_date=pg['date'], date_quote=pg['date_quote'], read_utc=pg['read_utc'], status=pg['status']) for pid, pg in P.items()]
    pages_failed = [x for x in pages_read if x['status'] != 200]
    now = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    S = dict(desk='DEUS', generated=now, updated=now, label=[PRELIM, 'PRELIMINARY: partial frame'], plan=json.load(open('data/plan_seal.json')), coi=COI,
             frame=dict(labs=LABS, window=[FRAME_START, FRAME_END], benchmarks=bstat, labs_with_pages_read=labs_cov),
             headline=dict(field='deus.stated_above_share', share=share, lo=lo, hi=hi, n=four[K.ABOVE], of=len(read), models=len(groups), four=four,
                           cannot_tell_reasons=dict(ct_reasons), cannot_tell_direction={str(k): v for k, v in ct_dir.items()},
                           interval='95%% percentile interval, bootstrap of whole models, %d draws, seed %d' % (NBOOT, SEED), size_that_matters=None),
             no_rerun=dict(field='deus.no_rerun_count', count=len(norerun), by_lab_benchmark={'%s | %s' % k: v for k, v in sorted(nr_by.items())},
                           reasons=dict(C.Counter(c['reason'].split(': ', 1)[1].split(' (')[0] for c in norerun)), rerun_is_the_claim=0,
                           rerun_is_the_claim_note='No Epoch internal row is a developer\'s own figure, and the external benchmark (HLE) was dropped, so no row was set aside as the claim repeated.'),
             counts=dict(printed_cells=len(rows), own_claims=len(out), in_frame=len(frame), read=len(read), no_rerun=len(norerun),
                         held=sum(1 for c in out if c['outcome'] == 'HELD'), out_of_frame=sum(1 for c in out if c['outcome'] == 'OUT_OF_FRAME'),
                         benchmark_dropped=sum(1 for c in out if c['outcome'] == 'BENCHMARK_DROPPED')),
             order=dict(field='deus.order_outcomes', count=len(ordl), four={o: sum(1 for x in ordl if x['outcome'] == o) for o in K.OUTCOMES}, nothing_returned=sum(1 for x in ordl if x['outcome'] == K.NOTHING_RETURNED),
                        reasons=dict(C.Counter(x.get('reason') for x in ordl if x['outcome'] == K.CANNOT_TELL))),
             context=dict(field='deus.context_outcomes', candidates=len(oth['context']), no_rerun=len(oth['context']), source=None, note='No public long-context rerun with released data and a stated threshold was named and quoted before this read (PLAN.md section 4a), so every candidate counts as no rerun.'),
             cutoff=dict(field='deus.cutoff_outcomes', candidates=len(oth['cutoff']), no_rerun=len(oth['cutoff']), source=None, note='No independent cutoff probe with published method and data was named and quoted before this read, so every candidate counts as no rerun.'),
             speed_price=dict(field='deus.speed_price_outcomes', candidates=len(oth['speed_price']), no_rerun=len(oth['speed_price']), source=None, note='No keyless independent speed or price data with a stated method was named and quoted before this read, so every candidate counts as no rerun.'),
             pages=dict(read=len(pages_read) - len(pages_failed), failed=pages_failed, held=held_pages, list=pages_read),
             problems=problems,
             sources=dict(epoch=json.load(open(sorted(__import__('glob').glob('raw/epoch/2*/manifest.json'))[-1])), epoch_licence='CC BY 4.0, Epoch AI, Capabilities & benchmarking, https://epoch.ai/benchmarks/use-this-data'))
    S['plan']['first_comparison'] = S['plan'].get('first_comparison') or now
    full = dict(S, claims=out, orders=ordl, other_types=oth)
    json.dump(full, open('data/deus.json', 'w'), indent=1, ensure_ascii=False, default=str)
    json.dump(S, open('summary_deus.json', 'w'), indent=1, ensure_ascii=False, default=str)
    live = dict(S); live.pop('pages', None); live['claims'] = [{k: c.get(k) for k in ('lab', 'model', 'benchmark', 'variant', 'printed', 'effort', 'outcome', 'reason', 'direction', 'coi')} for c in out if c['outcome'] in K.OUTCOMES or c['outcome'] == K.NOTHING_RETURNED]
    json.dump(live, open('data/deus_live.json', 'w'), indent=1, ensure_ascii=False, default=str)
    with open('data/deus_history.jsonl', 'a') as f: f.write(json.dumps(dict(t=now, headline=S['headline'], no_rerun=len(norerun), order=S['order']['four']), default=str) + '\n')
    seal = json.load(open('data/plan_seal.json'))
    if not seal.get('first_comparison'): seal['first_comparison'] = now; json.dump(seal, open('data/plan_seal.json', 'w'), indent=1)
    print(json.dumps(dict(headline=S['headline'], no_rerun=S['no_rerun']['count'], counts=S['counts'], order=S['order'], problems=problems), indent=1, default=str))
    if '--publish' in sys.argv or os.environ.get('HEUREMEN_PUBLISH') == '1':   # the site KV is written only by a run given --publish (house publish guard)
        import subprocess
        p = _cf_run(['/opt/homebrew/bin/npx', 'wrangler', 'kv', 'key', 'put', 'deus_live', '--path', os.path.join(H, 'data', 'deus_live.json'), '--namespace-id', '<kv-namespace-id>', '--remote'],
                           cwd=os.path.expanduser('~/forge/cloudflare-workers/heuremen-door'), capture_output=True, text=True, env=dict(os.environ, PATH='/opt/homebrew/bin:/usr/bin:/bin'))
        print('deus_live', 'published' if p.returncode == 0 else 'publish FAILED ' + (p.stderr or '')[-300:], file=sys.stderr)

if __name__ == '__main__':
    if '--selftest' in sys.argv: selftest(); sys.exit(0)
    main()
