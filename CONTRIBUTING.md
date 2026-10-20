# Contributing

Apple publishes no spec for `.workout` files, so everything here comes from real exports. **A new variant needs one file exported from the Workout app.** That's what keeps every supported feature verified byte-for-byte.

Good first contributions:

- other activities (cycling, walking, swimming…) and indoor locations
- new alerts (speed, other heart-rate shapes) and goals
- a fixture for something mapped but not yet covered (cadence ranges, current power)

## No code? Open an issue

1. In the Workout app, create a custom workout that uses the thing you want supported. Keep everything else simple.
2. Share it to get the `.workout` file.
3. Open a **New workout variant** issue. Attach the file (zip it first; GitHub only accepts some attachment types) and list exactly what you set in the app. A screenshot helps.

## Adding it yourself

1. Export the workout as above, then:
   ```sh
   python3 workoutgen.py decode your.workout   # names the unmapped field or value
   python3 workoutgen.py dump your.workout     # raw protobuf tree
   ```
2. Compare the dump with a fixture that's close to it. If two things changed at once, make another export that changes only one.
3. Map it in `workoutgen.py`:
   - new activity or location: add it to `ACTIVITIES` / `LOCATIONS`
   - new alert kind or shape: `ALERTS`, plus `parse_alert` / `fmt_alert` if it needs new spec syntax
   - new goal type or unit: the `GOAL_*` / `*_UNITS` constants, `parse_step_spec`, `fmt_step`
   - update the field map in the module docstring
4. Add the export as `fixtures/<short-name>.workout`, unmodified. Add `fixtures/<short-name>.txt` holding exactly what `decode` prints, minus its `#` header line.
5. Run `python3 test_workoutgen.py`. Every line must say `ok`.
6. Update the tables in `README.md` and `SKILL.md`, then open a pull request.

Rules: standard library only, one file, never guess a field number or unit (see `AGENTS.md`).

## Privacy

The exports seen so far hold only the workout you built and a random ID. Run `dump` on your file before sharing to check, and rename the workout first if its name is personal.
