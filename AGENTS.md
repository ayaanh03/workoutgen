# AGENTS.md

`workoutgen.py` is a single-file, stdlib-only codec for the iPhone Workout app's `.workout` format (protobuf, reverse-engineered). `SKILL.md` covers *using* it; this file covers changing it.

## Commands

- Test: `python3 test_workoutgen.py`. Every fixture must print `ok`.
- Raw view of any export: `python3 workoutgen.py dump file.workout`
- What's unmapped in an export: `python3 workoutgen.py decode file.workout`

## Rules

- One file, standard library only, Python 3.8+.
- Never guess a field number, enum value or unit. A mapping lands only together with a real Workout app export in `fixtures/` that decodes to its `.txt` spec and rebuilds byte-for-byte.
- Don't edit existing fixture `.workout` files. They are untouched exports.
- Unknown input must fail loudly with a one-line error (`UNMAPPED`). Never fall back silently.
- Keep the field map (module docstring and `FORMAT.md`) and the README / SKILL.md tables in sync with the code.
- Adding a variant: follow `CONTRIBUTING.md`.
