# Shelest language data

Public, data-only language resources for offline input. Application source and native binaries are not distributed in this repository.

## Japanese OSS model

Release `mozc-24.11-c4b2aef` contains `mozc.data`, built from Google Mozc commit `c4b2aef7c65e61be394bacadaec200eb5b97f91c` using its official OSS data target. Internal data version: `24.11.oss`. Size: 19,001,738 bytes.

SHA-256: `7a47a2b3958baeb0796345aec2c3f380b1d783d6fa399c8a0c358a197bee6046`. The accompanying notices preserve the Google/Mozc, IPAdic/NAIST/ICOT, Okinawa and Japanese Usage Dictionary notices. Upstream credits also list optional desktop components; this release contains only a data file.

## Reproduce

Use Linux, Python 3.13 and Bazelisk. Clone https://github.com/google/mozc, checkout the exact commit above, then run in `src/`:

```sh
python3 build_tools/update_deps.py
bazelisk build --config oss_linux --config release_build --jobs=3 //data_manager/oss:mozc_dataset_for_oss
sha256sum bazel-bin/data_manager/oss/mozc.data
```

Upstream pins its build dependencies. The expected output hash is recorded above and in `model.json`; do not substitute a dataset merely because its format version matches. The model was verified with a native Mozc engine built from the same source revision.

## Chinese Pinyin models

Release [rime-1.17-v2-keypads](https://github.com/Artyom9000/Shelest-language-data/releases/tag/rime-1.17-v2-keypads) contains complete Simplified and Traditional Pinyin data with normal, fuzzy, nine-key and combined spelling prisms. See [pinned sources, reviewed schemas, build recipe and licenses](rime/keypads-v2/README.md). The original [v1 data](rime/README.md) remains available for older applications.
