---
name: workoutgen
description: Create Apple Watch custom workouts as .workout files (the format the iPhone Workout app shares and imports) from a short text spec, or decode a .workout back to text. Use when someone wants a structured run on their Apple Watch (warmup, intervals, repeats, recoveries, cooldown, pace / heart-rate / cadence / power alerts), or wants to read or edit a .workout file. Python 3, no dependencies.
license: MIT
compatibility: Requires Python 3.8+. The output is imported by the iPhone Workout app and synced to a paired Apple Watch.
---

# workoutgen

Turns a workout into a `.workout` file that the user opens on their iPhone.

## Steps

1. Write the workout as a spec file (syntax below).
2. Build it:
   `python3 ${CLAUDE_SKILL_DIR}/workoutgen.py build workout.txt -o workout.workout`
   (`${CLAUDE_SKILL_DIR}` is the folder holding this file. Outside Claude Code, use the path to `workoutgen.py` next to it. Or pipe the spec in: `build - -o workout.workout`.)
3. Check it: `python3 .../workoutgen.py decode workout.workout` prints the spec back.
4. Give the user the `.workout` file and tell them to open it on the iPhone paired with their Watch.

## Spec

```
name: 5x1K                         # shown on the Watch; keep it short
warmup: 1mi @ 9:15-10:30/mi        # average-pace range alert
repeat 5
  work: 1km @ current 7:00-7:15/mi # current-pace range alert
  recovery: 1:30                   # no alert
cooldown: 10:00 @ 9:15-10:30/mi    # time goal + average-pace range
```

- **Goals:** `open`, distance (`400m`, `2km`, `1mi`), time (`1:30`, `50:00`, `90s`, `5min`). Use a distance goal when the plan gives a distance, a time goal when it gives a time, and `open` only when it gives neither.
- **Alerts** (optional, after `@`, one per step):
  - average pace `7:40/mi` or `9:10-10:30/mi`
  - current pace `current 7:00-7:20/mi`
  - heart rate `120-150bpm` or `zone 3` (never a single bpm)
  - cadence `170spm` or `160-190spm`
  - average power `200-205w` (range only)
  - current power `current 200w` (single only)
- Pace ranges can be written in either order. Paces per km work too (`4:45/km`).
- `repeat N` repeats the indented `work` / `recovery` lines under it. Unindented steps run once, in order.
- Optional `activity:` / `location:` lines default to `running` / `outdoor`, the only verified values so far.

## Rules

- The tool only builds what it has verified against a real export. If it answers `not mapped yet`, don't work around it. Drop that alert or step (or use a verified one), and tell the user what you dropped.
- Errors name the spec line. Fix the line and rerun; don't hand-edit `.workout` bytes.
- To add support for something new (another sport, indoor, a new alert), the user needs to export one from the Workout app. See `CONTRIBUTING.md`.
