#!/usr/bin/env python
"""FINANCE DEMO: European-call pricing by maximum-likelihood amplitude estimation (MLAE).
Client arm: objective qubit chosen from the vendor's published record, MLAE with no noise term.
Our arm:    objective qubit chosen from a fresh readout block, MLAE with a fade term at the
            MEASURED CZ error (RB ratio x stated) and readout correction from that block.
Modes: --test | --dry | --fire | --fetch | --analyze   (see PLAN.md). Never prints keys/CRNs."""
import os, sys, json, math, time, argparse
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import StatePreparation

HERE = os.path.dirname(os.path.abspath(__file__))
FORGE = HERE   # sandbox copy: no house paths
STATE = os.path.join(HERE, "state.json")
BACKEND = os.environ.get("DEMO_BACKEND", "ibm_kingston")
RB_RATIO = {"ibm_kingston": 1.305, "ibm_fez": 1.255}   # measured CZ error / stated (our RB: 1.30-1.31, 1.24-1.27)
KMAX = 3
SHOTS_MAIN = 4000
SHOTS_RO = 2000
NCAND = 12
VMIN = 0.25            # our arm drops rungs whose predicted visibility (true error) is below this
MAX_SECONDS = 300
SIM_INJECT = 0.0489    # test only: record-best qubit delivers this flip (kingston q15 observed: record 0.0034)

# ---------------- option model (log-normal on 4 grid points, call payoff) ----------------
S0, R, SIGMA, T, STRIKE = 100.0, 0.03, 0.25, 0.5, 100.0
def option():
    mu = math.log(S0) + (R - 0.5 * SIGMA**2) * T
    sd = SIGMA * math.sqrt(T)
    lo, hi = mu - 2 * sd, mu + 2 * sd
    x = np.linspace(lo, hi, 4)
    p = np.exp(-0.5 * ((x - mu) / sd) ** 2); p /= p.sum()
    S = np.exp(x)
    pay = np.maximum(S - STRIKE, 0.0); pmax = pay.max()
    f = pay / pmax
    a = float((p * f).sum())
    disc = math.exp(-R * T)
    return dict(p=p, S=S, f=f, a=a, pmax=pmax, disc=disc, price=disc * pmax * a)
OPT = option()
def price_of(a): return OPT["disc"] * OPT["pmax"] * a

def A_gate():
    p, f = OPT["p"], OPT["f"]
    amp = np.zeros(8)
    for i in range(4):
        amp[i] = math.sqrt(p[i] * (1 - f[i])); amp[i + 4] = math.sqrt(p[i] * f[i])  # qubit2 = objective
    return StatePreparation(amp, label="A")

def rung(k):
    """A then k x Q, Q = A S0 A^dag S_psi (S_psi = Z on objective; S0 = reflect about |000>). Measures objective (qubit 2)."""
    A = A_gate(); qc = QuantumCircuit(3, 1)
    qc.append(A, [0, 1, 2])
    for _ in range(k):
        qc.z(2)
        qc.append(A.inverse(), [0, 1, 2])
        qc.x([0, 1, 2]); qc.h(2); qc.ccx(0, 1, 2); qc.h(2); qc.x([0, 1, 2])
        qc.append(A, [0, 1, 2])
    qc.measure(2, 0)
    return qc

# ---------------- backend helpers ----------------
def read_key():
    """Your IBM Quantum API key, from the IBM_QUANTUM_TOKEN environment variable, or from the file DEMO_KEYFILE names. Never printed."""
    t = os.environ.get("IBM_QUANTUM_TOKEN", "").strip()
    if t: return t
    kf = os.environ.get("DEMO_KEYFILE")
    if not kf: sys.exit("no IBM Quantum key: set IBM_QUANTUM_TOKEN (your own key; it stays in this container)")
    return open(kf).read().strip()

def get_service():
    from qiskit_ibm_runtime import QiskitRuntimeService as S
    tok = read_key(); want = os.environ.get("DEMO_INSTANCE", "open-instance")
    base = S(channel="ibm_quantum_platform", token=tok)
    crn = None
    for i in base.instances():
        if want.lower() in str(i.get("name", "")).lower():
            crn = i["crn"]; break
    if crn is None: sys.exit(f"no instance named like '{want}' on this key")
    return S(channel="ibm_quantum_platform", token=tok, instance=crn)

def usage_remaining(svc):
    try: return float(svc.usage().get("usage_remaining_seconds"))
    except Exception as e: sys.exit(f"cannot read usage_remaining_seconds ({type(e).__name__}); refusing")

def fake_backend():
    from qiskit_ibm_runtime.fake_provider import FakeKingston, FakeFez, FakeMarrakesh
    return FakeFez() if "fez" in BACKEND else FakeMarrakesh() if "marrakesh" in BACKEND else FakeKingston()

def tgt_tables(be):
    t = be.target; n = be.num_qubits
    ro = {q: t["measure"][(q,)].error for q in range(n) if (q,) in t["measure"]}
    adj = {q: set() for q in range(n)}; cz = {}
    for (a, b), props in t["cz"].items():
        if props is None or props.error is None: continue
        cz[(a, b)] = props.error; cz[(b, a)] = props.error; adj[a].add(b); adj[b].add(a)
    return ro, adj, cz

def candidates(ro, adj, cz):
    """Candidate objective qubits: lowest RECORDED readout error among qubits with >=2 neighbours."""
    ok = [q for q in ro if len(adj[q]) >= 2 and ro[q] is not None]
    ok.sort(key=lambda q: ro[q])
    out = []
    for q in ok[:NCAND]:
        nb = sorted(adj[q], key=lambda n: cz[(q, n)])[:2]
        out.append((q, nb))
    return out

def layout_for(q, nb): return [nb[0], nb[1], q]   # logical 0,1 uncertainty; logical 2 objective

def transpile_arm(be, cand):
    q, nb = cand
    return [transpile(rung(k), backend=be, initial_layout=layout_for(q, nb), optimization_level=3, seed_transpiler=7) for k in range(KMAX + 1)]

def n2q(tc): return sum(v for g, v in tc.count_ops().items() if g in ("cz", "ecr", "cx"))

def ro_circuits(cands):
    n = len(cands); out = []
    for ones in (False, True):
        qc = QuantumCircuit(n, n)
        if ones: qc.x(range(n))
        qc.measure(range(n), range(n)); out.append(qc)
    return out

def ro_transpile(be, cands):
    lay = [c[0] for c in cands]
    return [transpile(c, backend=be, initial_layout=lay, optimization_level=0) for c in ro_circuits(cands)]

def readout_from_counts(c0, c1, n, shots):
    """returns per-candidate (p01, p10): P(read 1 | prep 0), P(read 0 | prep 1)."""
    res = []
    for i in range(n):
        s01 = sum(v for b, v in c0.items() if b[::-1][i] == "1"); s10 = sum(v for b, v in c1.items() if b[::-1][i] == "0")
        res.append((s01 / shots, s10 / shots))
    return res

def counts_of(pub_result):
    d = pub_result.data
    reg = [getattr(d, a) for a in dir(d) if not a.startswith("_") and hasattr(getattr(d, a), "get_counts")][0]
    return reg.get_counts()

# ---------------- MLAE ----------------
def seconds_est(tcs, shots): return 3.0 + sum(shots * (0.0006 + 1e-6 * tc.depth()) for tc in tcs)

def mlae(hits, shots, vis, ro=None, ks=None):
    """grid ML estimate of a=sin^2(theta). vis[k]: retention of the signal (1 = no fade). ro=(p01,p10) readout to correct."""
    th = np.linspace(1e-4, math.pi / 2 - 1e-4, 20001); ll = np.zeros_like(th)
    for k in (ks if ks is not None else range(len(hits))):
        p = np.sin((2 * k + 1) * th) ** 2
        p = 0.5 + (p - 0.5) * vis[k]
        if ro: p = p * (1 - ro[1]) + (1 - p) * ro[0]
        p = np.clip(p, 1e-9, 1 - 1e-9)
        ll += hits[k] * np.log(p) + (shots - hits[k]) * np.log(1 - p)
    return float(np.sin(th[np.argmax(ll)]) ** 2)

def retention(tcs, be_tables, cand, ratio):
    """per-rung signal retention at the MEASURED CZ error: (1 - 4e/3)^(#2q), edges from the transpiled circuit."""
    _, _, cz = be_tables; vis = []
    for tc in tcs:
        v = 1.0
        for inst in tc.data:
            if inst.operation.name in ("cz", "ecr", "cx"):
                e = cz.get((tc.find_bit(inst.qubits[0]).index, tc.find_bit(inst.qubits[1]).index), np.mean(list(cz.values())))
                v *= 1 - 4 * (e * ratio) / 3
        vis.append(v)
    return vis

def analyze_arm(name, hits, shots, tcs, tables, cand, ratio, ro_meas):
    out = {}
    out["client"] = mlae(hits["client"], shots, [1.0] * (KMAX + 1))
    vis = retention(tcs["ours"], tables, cand["ours"], ratio)
    ks = [k for k in range(KMAX + 1) if vis[k] >= VMIN]
    out["ours"] = mlae(hits["ours"], shots, vis, ro=ro_meas, ks=ks)
    out["ours_rungs"] = ks; out["ours_vis"] = vis
    return out

def report(o):
    ec, eo = abs(price_of(o["client"]) - OPT["price"]), abs(price_of(o["ours"]) - OPT["price"])
    return ec, eo

# ---------------- modes ----------------
def head():
    print(f"backend={BACKEND} exact a={OPT['a']:.6f} exact price={OPT['price']:.5f} (S0={S0},K={STRIKE},sigma={SIGMA},T={T},r={R})")

def mode_dry():
    head()
    try:
        svc = get_service(); be = svc.backend(BACKEND); print("live backend ok; usage_remaining_seconds =", usage_remaining(svc))
    except SystemExit as e: raise
    except Exception as e:
        print("live backend unavailable (", type(e).__name__, ") -> FAKE backend tables for the dry run"); be = fake_backend()
    tables = tgt_tables(be); ro, adj, cz = tables; cands = candidates(*tables)
    print("candidate objective qubits (record readout error):", [(q, round(ro[q], 4)) for q, _ in cands])
    client = cands[0]; print("client arm picks by record: q", client[0], "neighbours", client[1])
    tcs = transpile_arm(be, client); rot = ro_transpile(be, cands)
    total = 0.0
    for k, tc in enumerate(tcs): print(f"rung k={k}: depth={tc.depth()} 2q={n2q(tc)} ops={dict(tc.count_ops())}")
    est_main = 2 * seconds_est(tcs, SHOTS_MAIN); est_ro = seconds_est(rot, SHOTS_RO)
    print(f"readout block: {len(cands)} qubits, 2 circuits x {SHOTS_RO} shots, est {est_ro:.1f} s")
    print(f"main job: 2 arms x {KMAX+1} rungs x {SHOTS_MAIN} shots, est {est_main:.1f} s")
    print(f"TOTAL estimate {est_ro+est_main:.1f} s (limit {MAX_SECONDS})")

def aer_noise(be, tables, delivered, ratio):
    from qiskit_aer.noise import NoiseModel, depolarizing_error, ReadoutError
    ro, adj, cz = tables; nm = NoiseModel(basis_gates=["cz", "sx", "rz", "x", "id"])
    for (a, b), e in cz.items():
        nm.add_quantum_error(depolarizing_error(min(4 * e * ratio / 3, 1.0), 2), ["cz"], [a, b])
    for q in ro:
        nm.add_quantum_error(depolarizing_error(2.5e-4 * 4 / 3 / 2 * 2, 1), ["sx", "x"], [q])
        f = delivered[q]; nm.add_readout_error(ReadoutError([[1 - f, f], [f, 1 - f]]), [q])
    return nm

def sim_run(sim, tcs, nm, shots, seed):
    out = []
    for i, tc in enumerate(tcs):
        r = sim.run(tc, shots=shots, noise_model=nm, seed_simulator=seed * 100 + i).result()
        out.append(r.get_counts())
    return out

def mode_test():
    from qiskit_aer import AerSimulator
    head(); be = fake_backend(); tables = tgt_tables(be); ro, adj, cz = tables
    ratio = RB_RATIO[BACKEND]; cands = candidates(*tables)
    delivered = dict(ro); client = cands[0]; delivered[client[0]] = SIM_INJECT
    print(f"[SIMULATION] Aer noise from fake {BACKEND}: CZ error = {ratio} x stated; record-best readout qubit q{client[0]} record flip {ro[client[0]]:.4f} -> delivered {SIM_INJECT} (injected, from observed q15 case)")
    nm = aer_noise(be, tables, delivered, ratio); sim = AerSimulator()
    # readout block (simulated, analysed before the main arms)
    rot = ro_transpile(be, cands); rc = sim_run(sim, rot, nm, SHOTS_RO, 1)
    meas = readout_from_counts(rc[0], rc[1], len(cands), SHOTS_RO)
    best = min(range(len(cands)), key=lambda i: meas[i][0] + meas[i][1])
    ours = cands[best]
    print("readout block measured flips (p01+p10)/2 per candidate:", [(c[0], round(sum(m) / 2, 4)) for c, m in zip(cands, meas)])
    print(f"client picks q{client[0]} (record {ro[client[0]]:.4f}); ours picks q{ours[0]} (measured {sum(meas[best])/2:.4f}, delivered {delivered[ours[0]]:.4f})")
    tcs = {"client": transpile_arm(be, client), "ours": transpile_arm(be, ours)}
    print("2q gates per rung (client):", [n2q(t) for t in tcs["client"]], " depth:", [t.depth() for t in tcs["client"]])
    rows = []
    for seed in range(1, 11):
        hits = {}
        for arm in ("client", "ours"):
            cs = sim_run(sim, tcs[arm], nm, SHOTS_MAIN, seed)
            hits[arm] = [c.get("1", 0) for c in cs]
        res = analyze_arm("t", hits, SHOTS_MAIN, tcs, tables, {"ours": ours}, ratio, meas[best])
        ec, eo = report(res); rows.append((seed, res["client"], res["ours"], ec, eo))
        print(f"seed {seed:2d}: client a={res['client']:.4f} price err {ec:.4f} | ours a={res['ours']:.4f} price err {eo:.4f} (rungs used {res['ours_rungs']})")
    ec = np.array([r[3] for r in rows]); eo = np.array([r[4] for r in rows])
    print(f"exact price {OPT['price']:.4f}")
    print(f"HEADLINE [SIMULATION, 10 seeds]: mean abs price error client {ec.mean():.4f} vs ours {eo.mean():.4f}; ratio client/ours = {ec.mean()/max(eo.mean(),1e-9):.1f}x; median {np.median(ec):.4f} vs {np.median(eo):.4f}")
    print(f"as % of exact price: client {100*ec.mean()/OPT['price']:.2f}%  ours {100*eo.mean()/OPT['price']:.2f}%")

def save(d):
    s = json.load(open(STATE)) if os.path.exists(STATE) else {}
    s.update(d); json.dump(s, open(STATE, "w"), indent=1)

def wait(job, deadline):
    t0 = time.time()
    while time.time() - t0 < deadline:
        st = str(job.status()); 
        if "DONE" in st or "ERROR" in st or "CANCEL" in st: return st
        time.sleep(5)
    sys.exit(f"deadline {deadline}s passed, job still {job.status()} (id saved in state.json); use --fetch later")

def mode_fire():
    from qiskit_ibm_runtime import SamplerV2
    head(); svc = get_service(); be = svc.backend(BACKEND); tables = tgt_tables(be); ro, adj, cz = tables
    cands = candidates(*tables); client = cands[0]
    rot = ro_transpile(be, cands); tcc = transpile_arm(be, client)
    # our arm's circuits depend on the readout block, so estimate with the client's depth (same family)
    est = seconds_est(rot, SHOTS_RO) + 2 * seconds_est(tcc, SHOTS_MAIN)
    rem = usage_remaining(svc); print(f"estimate {est:.1f} s, remaining {rem:.0f} s")
    if est > MAX_SECONDS or est > rem: sys.exit("REFUSED: estimate exceeds 300 s or remaining usage")
    save(dict(backend=BACKEND, cands=[(int(q), [int(x) for x in nb]) for q, nb in cands], client=[int(client[0]), [int(x) for x in client[1]]],
              record_ro={str(q): ro[q] for q, _ in cands}, fired_at=time.time()))
    jp = SamplerV2(mode=be).run(rot, shots=SHOTS_RO); save(dict(job_p=jp.job_id())); print("job P submitted (readout block)")
    print("job P", wait(jp, 900))
    rp = jp.result(); meas = readout_from_counts(counts_of(rp[0]), counts_of(rp[1]), len(cands), SHOTS_RO)
    best = min(range(len(cands)), key=lambda i: meas[i][0] + meas[i][1]); ours = cands[best]
    print("readout block (p01,p10):", [(c[0], round(m[0], 4), round(m[1], 4)) for c, m in zip(cands, meas)])
    print(f"client q{client[0]} (record {ro[client[0]]:.4f}) vs ours q{ours[0]}")
    tco = transpile_arm(be, ours)
    pubs = []
    for k in range(KMAX + 1): pubs += [tcc[k], tco[k]]       # interleaved: client k, ours k
    jm = SamplerV2(mode=be).run(pubs, shots=SHOTS_MAIN)
    save(dict(job_main=jm.job_id(), ours=[int(ours[0]), [int(x) for x in ours[1]]], readout_meas=meas)); print("main job submitted; use --fetch then --analyze")

def mode_fetch():
    st = json.load(open(STATE)); svc = get_service(); job = svc.job(st["job_main"])
    print("status", job.status())
    if "DONE" not in str(job.status()): return
    r = job.result(); hits = {"client": [], "ours": []}
    for k in range(KMAX + 1):
        hits["client"].append(counts_of(r[2 * k]).get("1", 0)); hits["ours"].append(counts_of(r[2 * k + 1]).get("1", 0))
    save(dict(hits=hits)); print("hits saved", hits)

def mode_analyze():
    st = json.load(open(STATE)); be = fake_backend() if False else get_service().backend(BACKEND)
    tables = tgt_tables(be); ratio = RB_RATIO[BACKEND]
    client = tuple(st["client"]); ours = tuple(st["ours"])
    tcs = {"client": transpile_arm(be, client), "ours": transpile_arm(be, ours)}
    meas = st["readout_meas"]; i = [c[0] for c in st["cands"]].index(ours[0]); m = meas[i]
    res = analyze_arm("live", st["hits"], SHOTS_MAIN, tcs, tables, {"ours": ours}, ratio, tuple(m))
    ec, eo = report(res); head()
    print(f"client (q{client[0]}, no fade): a={res['client']:.4f} price={price_of(res['client']):.4f} error={ec:.4f}")
    print(f"ours   (q{ours[0]}, fade at {ratio}x stated, rungs {res['ours_rungs']}): a={res['ours']:.4f} price={price_of(res['ours']):.4f} error={eo:.4f}")
    print(f"ratio client/ours error = {ec/max(eo,1e-9):.2f}x")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    for m in ("test", "dry", "fire", "fetch", "analyze"): ap.add_argument("--" + m, action="store_true")
    a = ap.parse_args()
    if a.test: mode_test()
    elif a.dry: mode_dry()
    elif a.fire: mode_fire()
    elif a.fetch: mode_fetch()
    elif a.analyze: mode_analyze()
    else: ap.print_help()
