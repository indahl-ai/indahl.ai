#!/usr/bin/env python
"""FINANCE DEMO v3: v2 plus ONE frozen fade scale per chip (an exponent on the RB-based fade), as simulation v3 does.
 N = no fade (client)   S = stated-CZ fade ** SCALE   O = our RB-measured-CZ fade ** SCALE   (same SCALE for S and O, fairness).
SCALE is calibrated ONCE per chip on that chip's EARLIER v2 hardware job (its saved per-copy hits, anchored on that job's own
RB-measured errors, so it captures the RB-to-signal mapping, not the stated-vs-measured gap) and FROZEN in SCALE_FROZEN below
before any v3 shot. It is never fitted on the shots it scores. Job P (fresh RB) and main are fired fresh.
Modes: --test --calibrate --power --dry --fire --fetch --analyze.  Never prints keys/CRNs."""
import os, sys, json, math, argparse
import numpy as np
import demo as D
import demo_v2 as V2
from demo import OPT, price_of, KMAX, mlae, n2q, tgt_tables, candidates, fake_backend, get_service, usage_remaining
from demo_v2 import ladder, edges_of, rb_circuits, rb_fit, retention, edge_err, summarize, residuals, tq, head, COPIES, SHOTS, RB_SHOTS

HERE = D.HERE
D.MAX_SECONDS = 400
STATE3 = os.path.join(HERE, f"state_v3_{D.BACKEND}.json")
V2.STATE2 = STATE3                      # reuse v2's s2()/mode_fetch against the v3 state file
V2_STATE = {"ibm_kingston": "state_v2.json", "ibm_fez": "state_v2_ibm_fez.json", "ibm_marrakesh": "state_v2_ibm_marrakesh.json"}
V2_JOBS = {"ibm_kingston": ("dbv7h7darooc73fl2b30", "dbv7h7larooc73fl2b3g"), "ibm_fez": ("dbv7a7782tmc73dugtu0", "dbv7a7ff8rhs73bnd5a0"), "ibm_marrakesh": (None, None)}
# FROZEN per-chip fade scale (fade = retention ** SCALE). Calibrated by --calibrate on the v2 job above (EARLIER job, own RB-measured errors),
# frozen 19 Nov before any v3 shot. None = not calibrated yet -> --fire refuses.
SCALE_FROZEN = {"ibm_kingston": 0.63, "ibm_fez": 1.35, "ibm_marrakesh": 1.5}   # marrakesh sits on the 1.5 grid bound (error still falling at 6: a layout fault, not a fade); flagged, not a real calibration
GRID = np.round(np.arange(0.05, 1.5001, 0.005), 4)
ROBUST = (0.8, 1.0, 1.25)   # measured-error factors for the power cross-check (a fresh job P will not equal v2's)

def load_v2(chip):
    st = json.load(open(os.path.join(HERE, V2_STATE[chip])))
    stated = {tuple(int(x) for x in k.split("-")): v for k, v in st["stated"].items()}
    meta = [(tuple(e), m, nz) for e, m, nz in st["meta"]]
    return st, stated, rb_fit(st["rb_counts"], meta)

def vis_arms(tcs, stated, measured, scale):
    fs, fo = float(np.mean(list(stated.values()))), float(np.mean(list(measured.values())))
    return {"N": [1.0] * (KMAX + 1), "S": [v ** scale for v in retention(tcs, stated, fs)], "O": [v ** scale for v in retention(tcs, measured, fo)]}

def fits(hits, vis):
    pooled = [sum(h[k] for h in hits) for k in range(KMAX + 1)]
    res = {"vis": vis, "pooled_hits": pooled}
    for f in "NSO":
        res[f] = {"copies": [mlae(h, SHOTS, vis[f]) for h in hits], "pooled": mlae(pooled, SHOTS * len(hits), vis[f])}
    return res

def copy_errs(hits, vis):
    return np.abs(np.array([price_of(mlae(h, SHOTS, vis)) for h in hits]) - OPT["price"])

def v2_context(chip, scale_pair=None):
    st, stated, meas = load_v2(chip)
    try: be = get_service().backend(chip)
    except Exception: be = fake_backend()
    tcs = ladder(be, tuple(st["cand"]) if not isinstance(st["cand"], tuple) else st["cand"])
    tcs = ladder(be, (st["cand"][0], list(st["cand"][1])))
    return st, stated, meas, tcs

def calibrate(chip):
    """s minimizing mean abs price error of the O arm over the v2 job's copies, O fade from that job's own RB-measured CZ error."""
    st, stated, meas, tcs = v2_context(chip); hits = st["hits"]
    errs = []
    for s in GRID:
        v = vis_arms(tcs, stated, meas, float(s))["O"]; errs.append(copy_errs(hits, v).mean())
    i = int(np.argmin(errs)); return float(GRID[i]), float(errs[i]), (st, stated, meas, tcs)

def mode_calibrate():
    for chip in V2_STATE:
        if chip == "ibm_marrakesh":
            pass
        D.BACKEND = chip
        s, e, (st, stated, meas, tcs) = calibrate(chip)
        print(f"{chip}: frozen scale {s:.3f} (O mean abs error {e:.4f} on v2 job {V2_JOBS[chip][1] or 'marrakesh v2 main'}, in-sample); at scale 1.0: {copy_errs(st['hits'], vis_arms(tcs, stated, meas, 1.0)['O']).mean():.4f}")

def power_for(chip, scale, quiet=False):
    """In-sample (labelled): frozen scale applied to the v2 per-copy hits. Returns (ratio_ON, ratio_OS, lines)."""
    st, stated, meas, tcs = v2_context(chip); hits = st["hits"]; n = len(hits); t = tq(n)
    L = [f"{chip}: frozen scale {scale:.3f}; v2 job {V2_JOBS[chip][1] or 'marrakesh v2 main'} ({n} copies, same planned count {COPIES}); IN-SAMPLE (scale was calibrated on these hits)"]
    rON, rOS = [], []
    for fac in ROBUST:
        m = {e: v * fac for e, v in meas.items()}
        vis = vis_arms(tcs, stated, m, scale)
        eN, eS, eO = (copy_errs(hits, vis[f]) for f in "NSO")
        for nm, d, store in (("O-N", eO - eN, rON), ("O-S", eO - eS, rOS)):
            half = t * d.std(ddof=1) / math.sqrt(n); sig = abs(d.mean()); store.append(sig / half if half > 0 else float("inf"))
            L.append(f"  measured x{fac:.2f}: errors N {eN.mean():.4f} S {eS.mean():.4f} O {eO.mean():.4f}; {nm} {d.mean():+.4f}, paired {int(100*0.99)}% half-width {half:.4f}, ratio {sig/half:.2f}")
    L.append(f"  {chip} smallest ratio over measured factors: O vs N {min(rON):.2f}, O vs S {min(rOS):.2f}")
    if not quiet:
        for l in L: print(l)
    return min(rON), min(rOS), L

def get_scale_or_none(): return SCALE_FROZEN.get(D.BACKEND)

def mode_power():
    rs = []
    for chip in V2_STATE:
        D.BACKEND = chip; sc = SCALE_FROZEN[chip]
        if sc is None: print(chip, "scale not frozen"); continue
        rs.append(power_for(chip, sc)[:2])
    if rs: print(f"POWER RATIO: {min(r[0] for r in rs):.2f}   (O vs N, smallest over chips and measured factors)\nPOWER RATIO (O vs S): {min(r[1] for r in rs):.2f}")

def mode_test():
    """Code smoke test only (fake backend, Aer): no headline, no number from it is used anywhere."""
    head(); be = fake_backend(); print("[SIMULATION SMOKE TEST ONLY] fake", D.BACKEND)
    st, stated, meas = load_v2(D.BACKEND)
    tcs = ladder(be, (st["cand"][0], list(st["cand"][1])))
    for sc in (0.5, 1.0):
        res = fits(st["hits"][:4], vis_arms(tcs, stated, meas, sc)); print(f"scale {sc}: ok, O pooled price {price_of(res['O']['pooled']):.3f}")
    print("test ok; no job submitted")

def mode_dry():
    head(); sc = get_scale_or_none(); print("frozen scale:", sc)
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
    print(f"TOTAL estimate {est_p+est_m:.1f} s (limit {D.MAX_SECONDS}); state file {os.path.basename(STATE3)}")
    print("runtime options at fire: dynamical_decoupling off, twirling off (gates, measure), no mitigation; read back from the job after submit")
    return est_p + est_m

def set_options_off(sampler):
    o = sampler.options
    o.dynamical_decoupling.enable = False
    o.twirling.enable_gates = False; o.twirling.enable_measure = False

def readback(job, tag):
    try:
        opts = job.inputs.get("options", job.inputs) if hasattr(job, "inputs") else {}
        flat = json.dumps(opts, default=str)
        dd = opts.get("dynamical_decoupling", {}); tw = opts.get("twirling", {})
        print(f"{tag} options read back: dynamical_decoupling={dd}, twirling={tw}")
        return {"dd": dd, "twirling": tw}
    except Exception as e:
        print(f"{tag} options read-back failed: {type(e).__name__}"); return {}

def mode_fire():
    from qiskit_ibm_runtime import SamplerV2
    head(); sc = get_scale_or_none()
    if sc is None: sys.exit(f"REFUSED: no frozen fade scale for {D.BACKEND} (run --calibrate, freeze in SCALE_FROZEN and the plan)")
    svc = get_service(); be = svc.backend(D.BACKEND); tables = tgt_tables(be); cand = candidates(*tables)[0]
    tcs = ladder(be, cand); edges = edges_of(tcs); rbc, meta = rb_circuits(be, edges)
    est = 6.0 + sum(RB_SHOTS * (0.0006 + 1e-6 * c.depth()) for c in rbc) + COPIES * sum(SHOTS * (0.0006 + 1e-6 * t.depth()) for t in tcs)
    rem = usage_remaining(svc); print(f"estimate {est:.1f} s, remaining {rem:.0f} s, frozen scale {sc}")
    if est > D.MAX_SECONDS or est > rem: sys.exit(f"REFUSED: estimate exceeds {D.MAX_SECONDS} s or remaining usage")
    V2.s2(dict(scale=sc, cand=[cand[0], cand[1]], edges=[list(e) for e in edges], stated={f"{a}-{b}": tables[2][(a, b)] for a, b in edges}, meta=[[list(e), m, nz] for e, m, nz in meta], fired_at=__import__("time").time()))
    sp = SamplerV2(mode=be); set_options_off(sp); jp = sp.run(rbc, shots=RB_SHOTS); V2.s2(dict(job_p=jp.job_id())); print("job P (RB) submitted")
    ob_p = readback(jp, "job P")
    sm = SamplerV2(mode=be); set_options_off(sm)
    pubs = [tcs[k] for _ in range(COPIES) for k in range(KMAX + 1)]
    jm = sm.run(pubs, shots=SHOTS); V2.s2(dict(job_main=jm.job_id())); ob_m = readback(jm, "main")
    V2.s2(dict(options_readback=dict(p=ob_p, main=ob_m))); print("main job submitted; use --fetch then --analyze")

def mode_analyze():
    st = V2.s2(); sc = st.get("scale", SCALE_FROZEN.get(D.BACKEND))
    be = get_service().backend(D.BACKEND); tcs = ladder(be, tuple(st["cand"])); meta = [(tuple(e), m, nz) for e, m, nz in st["meta"]]
    meas = rb_fit(st["rb_counts"], meta); stated = {tuple(int(x) for x in k.split("-")): v for k, v in st["stated"].items()}
    print("pair: stated / RB-measured / ratio today:", [(e, round(stated[e], 5), round(float(meas[e]), 5), round(float(meas[e] / stated[e]), 2)) for e in sorted(stated)])
    print(f"frozen scale {sc} (calibrated on the chip's EARLIER v2 job, applied unchanged to S and O; nothing fitted on these shots)")
    res = fits(st["hits"], vis_arms(tcs, stated, meas, sc)); head(); print(summarize(res)); print(residuals(res, SHOTS * COPIES))

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    for m in ("test", "calibrate", "power", "dry", "fire", "fetch", "analyze"): ap.add_argument("--" + m, action="store_true")
    a = ap.parse_args()
    if a.test: mode_test()
    elif a.calibrate: mode_calibrate()
    elif a.power: mode_power()
    elif a.dry: mode_dry()
    elif a.fire: mode_fire()
    elif a.fetch: V2.mode_fetch()
    elif a.analyze: mode_analyze()
    else: ap.print_help()
