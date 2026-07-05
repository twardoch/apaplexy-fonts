<!-- this_file: TODO.md -->

# TODO

Bigger ideas parked here, roughly in priority order. The font binaries are the
product — none of these regenerate or edit them.

- [ ] **Reconcile the `v1.0.3` tag.** `v1.0.3` (2025-06-29) sits on a divergent
      side-commit that is not on `master`; `master` carries newer 2026 upstream
      content but is tagged only up to `v1.0.2`. Decide whether `v1.0.3` should
      be retired/re-pointed, and release forward from `master` as `v1.0.4`+ so
      released history is linear again.
- [ ] **Shrink the repo.** `.git` is ~2.4 GB because every font revision is
      committed as a binary. Evaluate Git LFS or shipping binaries only as
      release/CDN artifacts (upstream IBM tracks this in
      [IBM/plex#554](https://github.com/IBM/plex/issues/554)). This is a history
      rewrite — coordinate before doing it.
- [ ] **Extend validation to WOFF/WOFF2.** The current test covers OTF/TTF
      masters. Add an opt-in pass that spot-checks the ~10.8k web fonts (or a
      per-family sample) so derived formats can't silently drift from masters.
- [ ] **Variable-font axis checks.** For `plex-sans-variable` /
      `plex-serif-variable`, assert the `fvar` weight axis range and named
      instances match expectations.
- [ ] **Automate upstream sync.** A scheduled workflow that pulls new IBM Plex
      releases, runs the validation gate, and opens a PR on green.
