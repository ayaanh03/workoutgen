# Apple Watch `.workout` file format (reverse-engineered)

A `.workout` file is an Apple Watch custom workout: the file the iPhone Workout app shares and imports. Inside is a WorkoutKit custom workout (`WorkoutPlan`) serialized as binary [protocol buffers](https://protobuf.dev/programming-guides/encoding/). Apple publishes no schema, and its developer forums say these files can only be imported and exported in binary ([thread](https://developer.apple.com/forums/thread/750557)).

The layout below was worked out from real exports. Each one is kept in [fixtures/](fixtures/), and `test_workoutgen.py` rebuilds it byte-for-byte from its text spec. [workoutgen.py](workoutgen.py) implements it in one standard-library Python file.

**Status:** running, outdoor, with time / distance / open goals and pace, heart-rate, cadence and power alerts. Anything else is unknown until someone exports one ([CONTRIBUTING.md](CONTRIBUTING.md)).

## Messages

Field numbers are protobuf tags. Wire types: varint, `double` (64-bit), and length-delimited (string or nested message).

### File (top level)

| Field | Type | Meaning |
|---|---|---|
| 9 | string | Plan UUID, uppercase |
| 11 | Workout | The workout |
| 1000 | varint | Always `1` (format/version marker) |
| 1002 | varint | Always `5` (format/version marker) |

### Workout

| Field | Type | Meaning |
|---|---|---|
| 1 | varint | Activity type, the HKWorkoutActivityType raw value: `37` = running |
| 2 | varint | Location: `3` = outdoor |
| 3 | string | Display name |
| 4 | Step | Warmup (optional) |
| 5 | Block | Repeated, in order. A standalone step is a block with 1 iteration |
| 6 | Step | Cooldown (optional) |

### Block and IntervalStep

| Message | Field | Type | Meaning |
|---|---|---|---|
| Block | 1 | IntervalStep | Repeated, in order |
| Block | 2 | varint | Iterations |
| IntervalStep | 1 | varint | Purpose: `1` = work, `2` = recovery |
| IntervalStep | 2 | Step | The step |

### Step, Goal, Quantity

| Message | Field | Type | Meaning |
|---|---|---|---|
| Step | 1 | Goal | |
| Step | 2 | Alert | Optional, at most one |
| Goal | 1 | varint | `1` = time, `3` = distance, `4` = open |
| Goal | 2 | Quantity | Time goal. Units: `1` = seconds, `2` = minutes |
| Goal | 4 | Quantity | Distance goal. Units: `1` = meters, `2` = kilometers, `5` = miles |
| Quantity | 1 | varint | Unit |
| Quantity | 2 | double | Value |

### Alert

| Field | Type | Meaning |
|---|---|---|
| 1 | varint | Kind: `1` average pace, `2` current pace, `3` current cadence, `4` current power, `5` heart rate, `6` average power |
| 2 | varint | Shape: `1` single target, `2` range, `3` heart-rate zone |
| 4 / 5 / 6 / 7 | message | Payload for pace / cadence / power / heart rate |

Payload by shape: single → `{1: Value}`, range → `{2: {1: low Value, 2: high Value}}`, zone → `{1: {1: zone 1–5}}`.

| Value | Encoding |
|---|---|
| Pace | `{1: Quantity meters, 2: Quantity 1 second}`, i.e. speed in m/s. In a range, the low value is the slower speed |
| Cadence | `{1: varint steps, 2: Quantity 1 minute}` |
| Power | Quantity, unit `1` = watts |
| Heart rate | `{1: double bpm}` |

Seen so far: average pace (single, range), current pace (single, range), heart rate (range, zone; the app offers no single value), cadence (single, range), average power (range), current power (single).

## Example

[fixtures/10-07.workout](fixtures/10-07.workout), a real export. `workoutgen.py decode` gives:

```
name: 10/07
warmup: open
repeat 3
  work: 1mi @ 7:40/mi
  recovery: 1:30
cooldown: open
```

`workoutgen.py dump` shows the raw fields (7:40/mi = 1609.344 m / 460 s = 3.4986 m/s):

```
9: '54E3D6EB-2BEF-42AB-AE78-5E09EC55799A'
11 {
  1: 37
  2: 3
  3: '10/07'
  4 {
    1 {
      1: 4
    }
  }
  5 {
    1 {
      1: 1
      2 {
        1 {
          1: 3
          4 {
            1: 5
            2: 1.0 (double)
          }
        }
        2 {
          1: 1
          2: 1
          4 {
            1 {
              1 {
                1: 1
                2: 3.4985739130434785 (double)
              }
              2 {
                1: 1
                2: 1.0 (double)
              }
            }
          }
        }
      }
    }
    1 {
      1: 2
      2 {
        1 {
          1: 1
          2 {
            1: 1
            2: 90.0 (double)
          }
        }
      }
    }
    2: 3
  }
  6 {
    1 {
      1: 4
    }
  }
}
1000: 1
1002: 5
```

## Not mapped yet

Other activity types and locations (including swimming), WorkoutKit's pacer and swim-bike-run workouts, speed alerts, and any field not listed above. `workoutgen.py` refuses them rather than guessing. One export of each is enough to map it ([CONTRIBUTING.md](CONTRIBUTING.md)).
