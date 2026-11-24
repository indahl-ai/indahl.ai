#!/usr/bin/env python
"""FINANCE DEMO v2: ONE layout (the client's record pick), three fits on the SAME shots.
 N = no fade (client)   S = fade at the vendor's STATED CZ error (generic fix)   O = fade at OUR measured CZ error (today).
Job P: RB-style gate-error measurement on the ladder's own CZ pairs. Main job: 4 interleaved copies of the 4-rung ladder.
Modes: --test --dry --fire --fetch --analyze --reanalyze-v1.  Never prints keys/CRNs."""
import os, sys, json, math, time, argparse, random
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import random_clifford
import demo as D
from demo import OPT, price_of, KMAX, mlae, n2q, tgt_tables, candidates, rung, fake_backend, counts_of, get_service, usage_remaining, wait

HERE = D.HERE
# state per chip: kingston keeps state_v2.json; other chips get state_v2_<backend>.json
STATE2 = os.path.join(HERE, "state_v2.json" if D.BACKEND == "ibm_kingston" else f"state_v2_{D.BACKEND}.json")
COPIES, SHOTS = 32, 4000
D.MAX_SECONDS = 400   # Finance only, 19 Nov: shot noise dominates the copy floor (bootstrap of v2 hits), so power needs more copies, not fewer shots; the aim is a result a skeptical reader can rerun
RB_LENGTHS, RB_SEQ, RB_SHOTS = [1, 4, 8, 16], 3, 300
def tq(n):
    """Student t, 99% two-sided, n-1 dof (5.841 at 4 copies)."""
    from scipy import stats
    return float(stats.t.ppf(0.995, n - 1))
EQUIV = 0.04  # CONSISTENT margin on price-error difference (price units)

def head():
    print(f"backend={D.BACKEND} exact a={OPT['a']:.6f} exact price={OPT['price']:.5f}")

def ladder(be, cand):
    q, nb = cand
    return [transpile(rung(k), backend=be, initial_layout=D.layout_for(q, nb), optimization_level=3, seed_transpiler=7) for k in range(KMAX + 1)]

def edges_of(tcs):
    es = set()
    for tc in tcs:
        for i in tc.data:
            if i.operation.name in ("cz", "ecr", "cx"):
                a, b = (tc.find_bit(x).index for x in i.qubits); es.add(tuple(sorted((a, b))))
    return sorted(es)

# ---------- Job P: RB-style on the ladder's own CZ pairs ----------
def rb_circuits(be, edges, seed=11):
    rng = random.Random(seed); circs = []; meta = []
    for e in edges:
        for m in RB_LENGTHS:
            for s in range(RB_SEQ):
                cl = random_clifford(2, seed=rng.randrange(10**9)); qc = QuantumCircuit(2)
                comp = None
                from qiskit.quantum_info import Clifford
                comp = Clifford(np.eye(4, dtype=bool)[:, :] if False else QuantumCircuit(2))
                for _ in range(m):
                    c = random_clifford(2, seed=rng.randrange(10**9)); qc.compose(c.to_circuit(), inplace=True); comp = comp.compose(c)
                qc.compose(comp.adjoint().to_circuit(), inplace=True)
                qc.measure_all()
                tc = transpile(qc, backend=be, initial_layout=list(e), optimization_level=1, seed_transpiler=5)
                circs.append(tc); meta.append((e, m, n2q(tc)))
    return circs, meta

def rb_fit(counts_list, meta):
    """per edge: fit P00 = 0.25 + A r^ncz (A absorbs readout/prep) over transpiled CZ count; error per CZ = 0.75 (1-r)."""
    out = {}
    for e in sorted(set(x[0] for x in meta)):
        xs, ys = [], []
        for c, (ee, m, nz) in zip(counts_list, meta):
            if ee != e: continue
            tot = sum(c.values()); xs.append(nz); ys.append(c.get("00", 0) / tot)
        xs, ys = np.array(xs, float), np.array(ys)
        best = None
        for A in np.linspace(0.60, 0.75, 31):
          for r in np.linspace(0.90, 1.0, 1001):
            sse = ((0.25 + A * r ** xs - ys) ** 2).sum()
            if best is None or sse < best[0]: best = (sse, r)
        out[e] = 0.75 * (1 - best[1])
    return out

def edge_err(d, a, b): return d.get((a, b), d.get((b, a)))

def retention(tcs, errs, fallback):
    vis = []
    for tc in tcs:
        v = 1.0
        for i in tc.data:
            if i.operation.name in ("cz", "ecr", "cx"):
                a, b = (tc.find_bit(x).index for x in i.qubits); e = edge_err(errs, a, b)
                e = fallback if e is None else e; v *= 1 - 4 * e / 3
        vis.append(v)
    return vis

def three_fits(hits, tcs, stated, measured):
    """hits: [copy][rung]. returns per-copy & pooled estimates for N,S,O."""
    fb_s = float(np.mean(list(stated.values()))); fb_o = float(np.mean(list(measured.values())))
    vis = {"N": [1.0] * (KMAX + 1), "S": retention(tcs, stated, fb_s), "O": retention(tcs, measured, fb_o)}
    pooled = [sum(h[k] for h in hits) for k in range(KMAX + 1)]
    res = {"vis": vis, "pooled_hits": pooled}
    for f in "NSO":
        res[f] = {"copies": [mlae(h, SHOTS, vis[f]) for h in hits], "pooled": mlae(pooled, SHOTS * len(hits), vis[f])}
    return res

def summarize(res, label=""):
    L = []; ex = OPT["price"]; n = len(res["N"]["copies"])
    L.append(f"{label}exact price {ex:.4f}")
    errs = {}
    for f, nm in (("N", "no fade (client)"), ("S", "fade at stated CZ error"), ("O", "fade at our measured CZ error")):
        pr = np.array([price_of(a) for a in res[f]["copies"]]); pe = np.abs(pr - ex); errs[f] = pe
        t = tq(n)
        half = t * pr.std(ddof=1) / math.sqrt(n) if n > 1 else float("nan")
        pooled = price_of(res[f]["pooled"])
        L.append(f"  {f} {nm}: price {pr.mean():.4f} (99% interval {pr.mean()-half:.4f} to {pr.mean()+half:.4f}), mean abs error {pe.mean():.4f}; pooled-shots price {pooled:.4f} error {abs(pooled-ex):.4f}")
    d = errs["O"] - errs["S"]
    if len(d) > 1:
        half = tq(n) * d.std(ddof=1) / math.sqrt(len(d)); lo, hi = d.mean() - half, d.mean() + half
        word = "ABOVE" if lo > 0 else "BELOW" if hi < 0 else "CONSISTENT" if (-EQUIV < lo and hi < EQUIV) else "CANNOT_TELL"
        L.append(f"  OUTCOME ours minus S (error difference, 99% interval {lo:+.4f} to {hi:+.4f}; ABOVE = ours worse, BELOW = ours better, CONSISTENT = inside +-{EQUIV}): {word}")
    else:
        L.append("  OUTCOME ours minus S: CANNOT_TELL (one copy, no interval)")
    dn = errs["O"] - errs["N"]
    if len(dn) > 1:
        hn = tq(n) * dn.std(ddof=1) / math.sqrt(len(dn)); lo2, hi2 = dn.mean() - hn, dn.mean() + hn
        w2 = "ABOVE" if lo2 > 0 else "BELOW" if hi2 < 0 else "CONSISTENT" if (-EQUIV < lo2 and hi2 < EQUIV) else "CANNOT_TELL"
        L.append(f"  OUTCOME ours minus CLIENT N (headline; error difference, 99% interval {lo2:+.4f} to {hi2:+.4f}; BELOW = ours better): {w2}")
    ep, eN = errs["S"].mean(), errs["N"].mean()
    L.append(f"  HEADLINE vs S: ours error {errs['O'].mean():.4f} vs S {ep:.4f}  (N beside it: {eN:.4f})")
    return "\n".join(L)

def residuals(res, shots_total, label=""):
    L = [f"{label}per-rung residuals (observed P(1) minus model at that fit's pooled theta):"]
    ph = [h / shots_total for h in res["pooled_hits"]]
    th_ideal = math.asin(math.sqrt(OPT["a"]))
    for k in range(KMAX + 1):
        ideal = math.sin((2 * k + 1) * th_ideal) ** 2; se = math.sqrt(max(ph[k] * (1 - ph[k]), 1e-9) / shots_total)
        row = f"  k={k}: observed {ph[k]:.4f} ideal {ideal:.4f}"
        for f in "NSO":
            th = math.asin(math.sqrt(res[f]["pooled"])); p = 0.5 + (math.sin((2 * k + 1) * th) ** 2 - 0.5) * res["vis"][f][k]
            row += f" | {f} resid {ph[k]-p:+.4f}"
        flag = abs(ph[k] - 0.5) > abs(ideal - 0.5) + 3 * se
        row += "  <-- MOVES AWAY FROM 1/2 beyond what fade can do (layout/readout fault)" if flag else ""
        L.append(row)
    return "\n".join(L)

# ---------- modes ----------
def aer_nm(be, tables, true_ratio, flip):
    from qiskit_aer.noise import NoiseModel, depolarizing_error, ReadoutError
    ro, adj, cz = tables; nm = NoiseModel(basis_gates=["cz", "sx", "rz", "x", "id"])
    for (a, b), e in cz.items(): nm.add_quantum_error(depolarizing_error(min(4 * e * true_ratio / 3, 1.0), 2), ["cz"], [a, b])
    for q in ro:
        nm.add_quantum_error(depolarizing_error(3.3e-4, 1), ["sx", "x"], [q])
        nm.add_readout_error(ReadoutError([[1 - flip, flip], [flip, 1 - flip]]), [q])
    return nm

def stated_for(tables, edges):
    cz = tables[2]; return {e: cz[e] for e in edges}

def run_all_sim(seed_base, true_ratio, label):
    from qiskit_aer import AerSimulator
    be = fake_backend(); tables = tgt_tables(be); cand = candidates(*tables)[0]
    tcs = ladder(be, cand); edges = edges_of(tcs); stated = stated_for(tables, edges)
    nm = aer_nm(be, tables, true_ratio, 0.003); sim = AerSimulator()
    rbc, meta = rb_circuits(be, edges)
    cl = [sim.run(c, shots=RB_SHOTS, noise_model=nm, seed_simulator=seed_base + i).result().get_counts() for i, c in enumerate(rbc)]
    meas = rb_fit(cl, meta)
    hits = []
    for c in range(COPIES):
        hits.append([sim.run(tc, shots=SHOTS, noise_model=nm, seed_simulator=seed_base * 7 + c * 10 + k).result().get_counts().get("1", 0) for k, tc in enumerate(tcs)])
    return tcs, edges, stated, meas, hits

def mode_test():
    head(); be = fake_backend(); print(f"[SIMULATION] fake {D.BACKEND}; true CZ error = 1.30 x stated (hidden from fit S, found by RB for fit O); one layout (client's)")
    tcs, edges, stated, meas, hits = run_all_sim(3, 1.30, "")
    print("ladder CZ pairs:", edges)
    print("stated vs RB-measured CZ error:", [(e, round(stated[e], 5), round(meas[e], 5), round(meas[e] / stated[e], 2)) for e in edges])
    print("2q per rung:", [n2q(t) for t in tcs], "depth:", [t.depth() for t in tcs])
    res = three_fits(hits, tcs, stated, meas)
    print(summarize(res, "[SIMULATION] ")); print(residuals(res, SHOTS * COPIES))

def mode_dry():
    head()
    try:
        svc = get_service(); be = svc.backend(D.BACKEND); print("live backend ok; usage_remaining_seconds =", usage_remaining(svc))
    except SystemExit: raise
    except Exception as e: print("live unavailable:", type(e).__name__, "-> fake tables"); be = fake_backend()
    tables = tgt_tables(be); cand = candidates(*tables)[0]; tcs = ladder(be, cand); edges = edges_of(tcs)
    print(f"ONE layout: client's record pick q{cand[0]} neighbours {cand[1]}; CZ pairs {edges}")
    for k, t in enumerate(tcs): print(f"rung k={k}: depth={t.depth()} 2q={n2q(t)}")
    rbc, meta = rb_circuits(be, edges); est_p = 3.0 + sum(RB_SHOTS * (0.0006 + 1e-6 * c.depth()) for c in rbc)
    est_m = 3.0 + COPIES * sum(SHOTS * (0.0006 + 1e-6 * t.depth()) for t in tcs)
    print(f"job P: {len(rbc)} RB circuits x {RB_SHOTS} shots, est {est_p:.1f} s;  main job: {COPIES} copies x {KMAX+1} rungs x {SHOTS} shots, est {est_m:.1f} s")
    print(f"TOTAL estimate {est_p+est_m:.1f} s (limit {D.MAX_SECONDS})")
    return est_p + est_m

def s2(d=None):
    s = json.load(open(STATE2)) if os.path.exists(STATE2) else {}
    if d: s.update(d); json.dump(s, open(STATE2, "w"), indent=1)
    return s

def mode_fire():
    from qiskit_ibm_runtime import SamplerV2
    head(); svc = get_service(); be = svc.backend(D.BACKEND); tables = tgt_tables(be); cand = candidates(*tables)[0]
    tcs = ladder(be, cand); edges = edges_of(tcs); rbc, meta = rb_circuits(be, edges)
    est = 6.0 + sum(RB_SHOTS * (0.0006 + 1e-6 * c.depth()) for c in rbc) + COPIES * sum(SHOTS * (0.0006 + 1e-6 * t.depth()) for t in tcs)
    rem = usage_remaining(svc); print(f"estimate {est:.1f} s, remaining {rem:.0f} s")
    if est > D.MAX_SECONDS or est > rem: sys.exit("REFUSED: estimate exceeds 300 s or remaining usage")
    s2(dict(cand=[cand[0], cand[1]], edges=[list(e) for e in edges], stated={f"{a}-{b}": tables[2][(a, b)] for a, b in edges}, meta=[[list(e), m, nz] for e, m, nz in meta], fired_at=time.time()))
    jp = SamplerV2(mode=be).run(rbc, shots=RB_SHOTS); s2(dict(job_p=jp.job_id())); print("job P (RB) submitted")
    pubs = [tcs[k] for _ in range(COPIES) for k in range(KMAX + 1)]    # copy-major: ladder repeated 4 times in order
    jm = SamplerV2(mode=be).run(pubs, shots=SHOTS); s2(dict(job_main=jm.job_id())); print("main job submitted (no waiting between P and main: they are independent); use --fetch then --analyze")

def mode_fetch():
    st = s2(); svc = get_service(); out = {}
    for key in ("job_p", "job_main"):
        j = svc.job(st[key]); print(key, j.status())
        if "DONE" not in str(j.status()): return
        out[key] = j.result()
    cl = [counts_of(r) for r in out["job_p"]]
    hits = [[counts_of(out["job_main"][c * (KMAX + 1) + k]).get("1", 0) for k in range(KMAX + 1)] for c in range(COPIES)]
    s2(dict(rb_counts=cl, hits=hits)); print("saved. hits", hits)

def mode_analyze():
    st = s2(); be = get_service().backend(D.BACKEND); cand = tuple(st["cand"]); tcs = ladder(be, cand)
    meta = [(tuple(e), m, nz) for e, m, nz in st["meta"]]; meas = rb_fit(st["rb_counts"], meta)
    stated = {tuple(int(x) for x in k.split("-")): v for k, v in st["stated"].items()}
    print("pair: stated / RB-measured / ratio today:", [(e, round(stated[e], 5), round(meas[e], 5), round(meas[e] / stated[e], 2)) for e in sorted(stated)])
    res = three_fits(st["hits"], tcs, stated, meas); head(); print(summarize(res)); print(residuals(res, SHOTS * COPIES))

def mode_reanalyze_v1():
    if D.BACKEND not in D.RB_RATIO: sys.exit(f"v1 reanalysis is kingston/fez only (no hardware-sourced RB_RATIO for {D.BACKEND})")
    st = json.load(open(os.path.join(HERE, "state.json")))
    try: be = get_service().backend(D.BACKEND); src = "live backend tables"
    except Exception: be = fake_backend(); src = "fake backend tables"
    tables = tgt_tables(be); ratio = D.RB_RATIO[D.BACKEND]; lines = [f"v1 saved counts re-fit, zero QPU ({src}); N no fade, S stated CZ error, O stated x {ratio} (the October ratio; v1 had no per-pair measurement)", f"exact price {OPT['price']:.4f}"]
    for arm in ("client", "ours"):
        cand = tuple(st[arm]); tcs = ladder_v1(be, cand); edges = edges_of(tcs); stated = {e: tables[2][e] for e in edges}
        measured = {e: v * ratio for e, v in stated.items()}
        h = [st["hits"][arm]]
        res = three_fits(h, tcs, stated, measured)
        lines.append(f"--- v1 {arm} arm, objective q{cand[0]} (shots 4000, single copy: no interval)")
        for f, nm in (("N", "no fade"), ("S", "stated fade"), ("O", "x1.305 fade")):
            a = res[f]["pooled"]; lines.append(f"  {f} {nm}: a={a:.4f} price {price_of(a):.4f} error {abs(price_of(a)-OPT['price']):.4f}")
        lines.append(residuals(res, SHOTS))
    out = "\n".join(lines); print(out); open(os.path.join(HERE, "reanalysis_v1.text"), "w").write(out + "\n")

def ladder_v1(be, cand): return ladder(be, cand)   # identical transpile settings to v1 (opt 3, seed 7)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    for m in ("test", "dry", "fire", "fetch", "analyze", "reanalyze-v1"): ap.add_argument("--" + m, action="store_true")
    a = ap.parse_args()
    if a.test: mode_test()
    elif a.dry: mode_dry()
    elif a.fire: mode_fire()
    elif a.fetch: mode_fetch()
    elif a.analyze: mode_analyze()
    elif getattr(a, "reanalyze_v1"): mode_reanalyze_v1()
    else: ap.print_help()
