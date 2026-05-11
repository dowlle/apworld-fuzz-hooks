# apworld-fuzz-hooks

Bananium-style validation hooks for [Eijebong/Archipelago-fuzzer](https://github.com/Eijebong/Archipelago-fuzzer).
Used as the fuzz gate for [dowlle/Archipelago-index](https://github.com/dowlle/Archipelago-index)
under the [Archipelago Pie](https://ap-pie.com) umbrella, and on a separate
worker host for local runs.

## What's here

`hooks/` — nine Python hook modules that plug into `fuzz.py --hook hooks.<name>:Hook`.
A tenth "check" is the default (hook-less) fuzz pass.

| Check | Hook module | Run count at 1.0x |
|---|---|---|
| default | _(none)_ | 5000 |
| no-restrictive-starts | `no_rs:Hook` | 5000 |
| check-determinism | `determinism:Hook` | 500 |
| check-collect-accessibility | `collect_accessibility_test:Hook` | 500 |
| check-item-location-count | `item_location_count:Hook` | 500 |
| check-placement-refs | `check_placement_item_location_references:Hook` | 500 |
| check-lambda-capture | `detect_rule_variable_capture_issues:Hook` | 500 |
| check-static-output | `detect_output_placement_changes:Hook` | 500 |
| check-indirect-conditions | `indirect_conditions:Hook` | 500 |
| check-ut | `with_empty:Hook` | 500 |

`empty.apworld` — the [Eijebong/empty-apworld](https://github.com/Eijebong/empty-apworld)
build pinned to the version `no_rs` and `with_empty` expect. Pre-place into the AP
install's `worlds/` folder before invoking `fuzz.py`.

## How callers use this

Both fuzz environments check this repo out, copy `hooks/` next to `fuzz.py`, and
copy `empty.apworld` into `<AP_DIR>/worlds/` before running. They then invoke
`fuzz.py --hook hooks.<name>:Hook ...` once per check.

- **GHA workflow** on `dowlle/Archipelago-index` (`.github/workflows/fuzz.yml`):
  one matrix job per check, parallel, free tier.
- **Worker-host script** for local sequential runs.

## Provenance

Hooks adapted from the Bananium team's fuzz collection. Two hooks
(`no_rs.py`, `with_empty.py`) had hardcoded paths inherited from the
original `ap-yaml-checker` container layout; both were refactored to assume
`empty.apworld` is pre-placed by the caller, so the hooks are portable.

## License

MIT.
