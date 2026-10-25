# Chinese language data

Release `rime-1.17-v1` contains complete compiled Simplified and Traditional Pinyin data for librime 1.17. Source revisions, compiler/archive hashes, model hashes and licenses are recorded in `models.json`.

The APK supplies fixed reviewed runtime schemas. Downloads contain only `.table.bin`, `.prism.bin`, `.reverse.bin` and the bounded format-3 manifest. No executable library, plugin or downloaded schema is installed. Complete matching dictionary sources and license copies accompany the release.

Build on Windows using the official pinned Rime compiler: `python rime/build.py --output release`. A system 7z executable is required. The workflow rebuilds data and records new artifact hashes; it does not overwrite the immutable published release. Observed rebuilds differ in dictionary header checksums, so rebuilds are not claimed to be byte-identical. Source and schema pins are verified before compilation.

Provenance clarification: the original release metadata attributed the header differences to process-dependent metadata. That cause has not been established; only the checksum differences were observed. The tracked metadata corrects that wording without replacing any published model bytes or hashes.
