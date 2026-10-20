# workoutgen: Apple Watch custom workout (.workout) file generator

Create **Apple Watch custom workouts** from a few lines of text: warmup, intervals, repeats, recoveries and cooldown, with pace, heart-rate zone, cadence and power alerts. `workoutgen` writes the `.workout` file that the iPhone **Workout app** imports and syncs to your Watch. No Swift, no Xcode, no iOS app. It also decodes any `.workout` file back to editable text.

It's one Python file using only the standard library. Apple doesn't document the `.workout` format (a binary protobuf of a WorkoutKit `WorkoutPlan`), so it was reverse-engineered from real exports. Every supported feature is checked byte-for-byte against one ([fixtures/](https://github.com/ayaanh03/workoutgen/tree/main/fixtures)); the full field map is in [FORMAT.md](https://github.com/ayaanh03/workoutgen/blob/main/FORMAT.md). AI agents can use it too: see [For AI agents](#for-ai-agents).

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

Prefer a command? `pipx install workoutgen` (from [PyPI](https://pypi.org/project/workoutgen/)), or run it without installing: `uvx workoutgen build intervals.txt`.

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

Want cycling, swimming, indoor runs or another alert? It takes one exported file. See [CONTRIBUTING.md](https://github.com/ayaanh03/workoutgen/blob/main/CONTRIBUTING.md), or open an issue and attach the export.

## For AI agents

- **Skill:** [SKILL.md](https://github.com/ayaanh03/workoutgen/blob/main/SKILL.md) follows the [Agent Skills](https://agentskills.io) standard. For Claude Code: `git clone https://github.com/ayaanh03/workoutgen ~/.claude/skills/workoutgen`.
- **Any agent with a shell:** fetch the single file (see Quick start) and follow [SKILL.md](https://github.com/ayaanh03/workoutgen/blob/main/SKILL.md).
- **Working on the code:** [AGENTS.md](https://github.com/ayaanh03/workoutgen/blob/main/AGENTS.md).

Errors are one line that names the spec line and what to write instead, so an agent can fix its input and retry.

## FAQ

**How do I make an Apple Watch custom workout without Xcode or an app?**
Write the workout as a short spec (above), run `python3 workoutgen.py build spec.txt`, and open the `.workout` on your iPhone.

**How do I import a custom workout into the Apple Watch Workout app from a file?**
Open the `.workout` file on the iPhone paired with the Watch, for example from AirDrop, the Files app, Messages, or a web link. The Workout app takes it from there.

**What is the `.workout` file format?**
A WorkoutKit custom workout (`WorkoutPlan`) serialized as binary protobuf. Apple only supports importing and exporting it in that binary form. [FORMAT.md](https://github.com/ayaanh03/workoutgen/blob/main/FORMAT.md) documents every field mapped so far.

**Can I convert a `.workout` file to text or JSON?**
`workoutgen.py decode file.workout` turns it into the editable text spec, and `workoutgen.py dump file.workout` prints the raw protobuf tree. There's no JSON output.

**Can an AI assistant build Apple Watch workouts for me?**
Yes, if it can run Python: it writes the spec, calls `build` and hands you the file. Claude Code can install it as a skill (above).

**Does it support cycling, swimming, strength or indoor workouts?**
Not yet. Each needs one real export to map; see [CONTRIBUTING.md](https://github.com/ayaanh03/workoutgen/blob/main/CONTRIBUTING.md).

**Does it use WorkoutKit or need an Apple device?**
No. It writes the same file format directly, so it runs anywhere Python 3.8+ does. You only need the iPhone to open the result.

## Related projects

- [WorkoutKit](https://developer.apple.com/documentation/workoutkit): Apple's official Swift API, used from inside an iOS or watchOS app.
- [dotworkout](https://github.com/javierferrersb/dotworkout): TypeScript, with a browser editor and an MCP server.
- [DotnetWorkoutKit](https://github.com/changeforan/DotnetWorkoutKit): a .NET library that writes `.workout` files.

## How it works

The format is protobuf; [FORMAT.md](https://github.com/ayaanh03/workoutgen/blob/main/FORMAT.md) has the field map and a worked example. `workoutgen.py dump file.workout` prints the raw field tree of any export. Tests: `python3 test_workoutgen.py`.

## License

[MIT](https://github.com/ayaanh03/workoutgen/blob/main/LICENSE). Not affiliated with Apple. Apple Watch is a trademark of Apple Inc.
