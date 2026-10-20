#!/usr/bin/env python3
"""Regression test for workoutgen.py against real Workout app exports.

Every fixture in fixtures/ is a `.workout` exported from the iPhone Workout app
plus its `.txt` spec. For each one: decoding must give the spec, building the
spec (with the export's UUID) must give the export byte-for-byte, builds must
be deterministic, and `dump` must read it. Run: python3 test_workoutgen.py
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import workoutgen  # noqa: E402

FIXTURES = pathlib.Path(__file__).parent / "fixtures"


def main():
    files = sorted(FIXTURES.glob("*.workout"))
    if not files:
        sys.exit(f"no fixtures in {FIXTURES}")
    failures = 0
    for wf in files:
        exported = wf.read_bytes()
        spec = wf.with_suffix(".txt").read_text(encoding="utf-8")
        plan, plan_uuid = workoutgen.decode(exported)
        # Spelling out the default activity/location must change nothing.
        explicit = spec.replace("\n", "\nactivity: running\nlocation: outdoor\n", 1)
        checks = {
            "decodes to spec": workoutgen.to_spec(plan) == spec,
            "rebuilds byte-identical": workoutgen.encode(workoutgen.parse_spec(spec), plan_uuid) == exported,
            "deterministic": workoutgen.encode(workoutgen.parse_spec(spec))
                             == workoutgen.encode(workoutgen.parse_spec(spec)),
            "explicit defaults": workoutgen.encode(workoutgen.parse_spec(explicit), plan_uuid) == exported,
            "dumps": bool(workoutgen.dump(exported)),
        }
        bad = [k for k, ok in checks.items() if not ok]
        failures += bool(bad)
        print(f"{'FAIL' if bad else 'ok  '} {wf.name}" + (f"  ({', '.join(bad)})" if bad else ""))
    if failures:
        sys.exit(f"{failures} fixture(s) failed")


if __name__ == "__main__":
    main()
