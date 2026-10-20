# workoutgen

Turn a few lines of text into an Apple Watch custom workout (`.workout` file), and decode any `.workout` back to text. One Python file, no dependencies.

A `.workout` file is what the iPhone Workout app shares and imports. Apple doesn't publish the format, so this codec was reverse-engineered from real exports, and every feature it supports is checked byte-for-byte against one ([fixtures/](fixtures/)).

## Quick start

```sh
curl -O https://raw.githubusercontent.com/ayaanh03/workoutgen/main/workoutgen.py

cat > intervals.txt <<'EOF'
name: 5x3 min
warmup: 1mi @ 9:15-10:30/mi
repeat 5
  work: 3:00 @ current 7:00-7:15/mi
  recovery: 2:00
cooldown: 1mi @ 9:15-10:30/mi
EOF

python3 workoutgen.py build intervals.txt        # -> intervals.workout
python3 workoutgen.py decode intervals.workout   # prints the spec back
```

Get the `.workout` onto the iPhone paired with your Watch (AirDrop, Files, Messages, a download link) and open it. The Workout app imports it.

Prefer a command? `pipx install git+https://github.com/ayaanh03/workoutgen`, or run it without installing: `uvx --from git+https://github.com/ayaanh03/workoutgen workoutgen build intervals.txt`.

## Spec

| Line | Meaning |
|---|---|
| `name: <text>` | Name shown on the Watch (required) |
| `activity: running` | Optional, default `running` |
| `location: outdoor` | Optional, default `outdoor` |
| `warmup: <goal> [@ <alert>]` | Optional |
| `work: <goal> [@ <alert>]` | A work step; standalone steps run once |
| `recovery: <goal> [@ <alert>]` | A recovery step |
| `repeat N` | The indented `work` / `recovery` lines under it repeat N times |
| `cooldown: <goal> [@ <alert>]` | Optional |
| `# ...` | Comment |

**Goals:** `open`, distance (`400m`, `2km`, `1mi`, `3.11mi`), time (`1:30`, `50:00`, `90s`, `5min`).

**Alerts:**

| Alert | Examples |
|---|---|
| Average pace, single or range | `7:40/mi`, `4:45/km`, `9:10-10:30/mi` |
| Current pace, single or range | `current 7:00/mi`, `current 7:00-7:20/mi` |
| Heart rate, range or zone (no single value) | `120-150bpm`, `zone 3` |
| Current cadence, single or range | `170spm`, `160-190spm` |
| Average power, range | `200-205w` |
| Current power, single | `current 200w` |

Build from stdin with `workoutgen.py build - -o out.workout`. `--uuid` pins the plan UUID; by default it's derived from the content, so the same spec always gives the same bytes.

## What's verified

Running, outdoor, with the goals and alerts above. Files built this way were imported on an iPhone in October 2026. Cadence ranges and current power are mapped but have no fixture yet; adding an export of either is an easy first contribution. Anything else stops with `not mapped yet` instead of writing a file the app might reject.

Want cycling, swimming, indoor runs or another alert? It takes one exported file. See [CONTRIBUTING.md](CONTRIBUTING.md), or open an issue and attach the export.

## For AI agents

- **Skill:** [SKILL.md](SKILL.md) follows the [Agent Skills](https://agentskills.io) standard. For Claude Code: `git clone https://github.com/ayaanh03/workoutgen ~/.claude/skills/workoutgen`.
- **Any agent with a shell:** fetch the single file (see Quick start) and follow [SKILL.md](SKILL.md).
- **Working on the code:** [AGENTS.md](AGENTS.md).

Errors are one line that names the spec line and what to write instead, so an agent can fix its input and retry.

## How it works

The format is protobuf. The field map is in the docstring at the top of [workoutgen.py](workoutgen.py), and `workoutgen.py dump file.workout` prints the raw field tree of any export. Tests: `python3 test_workoutgen.py`.

## License

[MIT](LICENSE). Not affiliated with Apple. Apple Watch is a trademark of Apple Inc.
