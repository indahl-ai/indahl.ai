#!/usr/bin/env python3
"""sandbox.py: the Quantum Idle Audit finance demonstration, run by you, in your own space.

  python3 sandbox.py replay [--run 1|2] [--chip kingston|fez|marrakesh]
        Re-computes our published result from the recorded hardware runs. No key, no network, no IBM time.
        Prints the default (client) fit beside the fit that uses the measured gate error, with the exact price and the intervals.
  python3 sandbox.py check  [--chip ...]
        With YOUR IBM Quantum key: confirms the key works, shows your remaining IBM time and what a live run would use. Submits nothing.
  python3 sandbox.py fire   [--chip ...] --yes
        Runs the demonstration live on your own IBM account. Refuses unless the estimate (about 370 s) is under the 400 s cap and under your remaining time.
  python3 sandbox.py fetch  [--chip ...]       collect the finished jobs
  python3 sandbox.py analyze [--chip ...]      the same comparison, on YOUR run

Your key is read from the IBM_QUANTUM_TOKEN environment variable, used only to talk to IBM, never printed, never written to disk, and never sent anywhere
else. Your runs are saved in ./my_runs/ on this machine. The recorded runs in ./recorded/ are read-only references and are never changed."""
import os, sys, shutil, argparse

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, 'finance'))
CHIPS = {'kingston': 'ibm_kingston', 'fez': 'ibm_fez', 'marrakesh': 'ibm_marrakesh'}


def load(chip):
    os.environ['DEMO_BACKEND'] = CHIPS[chip]            # demo.py reads the chip name at import
    import demo as D, demo_v2 as V2, demo_v3 as V3
    return D, V2, V3


def use_state(V2, V3, path):
    V3.STATE3 = path; V2.STATE2 = path                  # the scripts read and write their state through these two names


def cmd_replay(a):
    D, V2, V3 = load(a.chip)
    src = os.path.join(HERE, 'recorded', 'run%d' % a.run, 'state_v3_%s.json' % CHIPS[a.chip])
    if not os.path.exists(src): sys.exit('no recorded run: ' + src)
    work = os.path.join(HERE, '.replay_tmp'); os.makedirs(work, exist_ok=True)
    tmp = os.path.join(work, os.path.basename(src)); shutil.copyfile(src, tmp)   # the recorded file itself is never opened for writing
    use_state(V2, V3, tmp)
    class Offline:                                       # the analysis only needs the chip's shape to rebuild the circuits, so a fake chip stands in
        def backend(self, name): return D.fake_backend()
    V3.get_service = lambda: Offline()
    print('REPLAY of recorded run %d on %s. Nothing is sent anywhere; no key is used.' % (a.run, CHIPS[a.chip]))
    print('Recorded hardware counts and benchmarking data; the circuits are rebuilt on a stand-in chip only to count depth and two-qubit gates.')
    if a.chip == 'marrakesh': print('NOTE: marrakesh is our layout-fault control. Its fade scale sits on the edge of the search range, so its improvement is not a calibration result.')
    V3.mode_analyze()
    shutil.rmtree(work, ignore_errors=True)


def live(a):
    if not os.environ.get('IBM_QUANTUM_TOKEN', '').strip():
        sys.exit('Set your own IBM Quantum key first:  export IBM_QUANTUM_TOKEN=...   (it stays on this machine)')
    D, V2, V3 = load(a.chip)
    mine = os.path.join(HERE, 'my_runs'); os.makedirs(mine, exist_ok=True)
    use_state(V2, V3, os.path.join(mine, 'state_v3_%s.json' % CHIPS[a.chip]))
    return D, V2, V3


def cmd_check(a):
    D, V2, V3 = live(a); V3.mode_dry()
    print('\nNothing was submitted. To run it live: python3 sandbox.py fire --chip %s --yes' % a.chip)


def cmd_fire(a):
    if not a.yes: sys.exit('This submits jobs on your IBM account and uses your IBM time. Run "check" first, then add --yes to fire.')
    D, V2, V3 = live(a); V3.mode_fire()


def cmd_fetch(a):
    D, V2, V3 = live(a); V2.mode_fetch()


def cmd_analyze(a):
    D, V2, V3 = live(a); V3.mode_analyze()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd', required=True)
    for name, fn in (('replay', cmd_replay), ('check', cmd_check), ('fire', cmd_fire), ('fetch', cmd_fetch), ('analyze', cmd_analyze)):
        p = sub.add_parser(name); p.set_defaults(fn=fn)
        p.add_argument('--chip', choices=sorted(CHIPS), default='kingston')
        if name == 'replay': p.add_argument('--run', type=int, choices=(1, 2), default=2)
        if name == 'fire': p.add_argument('--yes', action='store_true')
    a = ap.parse_args(); a.fn(a)


if __name__ == '__main__':
    main()
