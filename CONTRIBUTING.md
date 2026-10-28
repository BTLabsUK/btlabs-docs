# Contributing

Thank you for improving the documentation.

1. Read [WRITING.md](WRITING.md): the format and word rules every page follows.
2. Edit the pages in `site/docs/`. Keep one change per commit and stage files by name.
3. Check the build: `cd site && npm ci && npm run build` (a broken link fails it). Builds run on
   your own machine; there is no hosted CI.
4. Sign your commits off (`git commit -s`): by adding `Signed-off-by` you certify the
   [DCO 1.1](https://developercertificate.org/) for your change under the Apache License 2.0.

The wikis of the code projects are generated from these pages (`tools/wiki-sync.py`): edit here,
never in a wiki.

This project follows the [Contributor Covenant](CODE_OF_CONDUCT.md).
