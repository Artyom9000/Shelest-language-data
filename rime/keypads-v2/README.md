# Chinese input data v2

Release `rime-1.17-v2-keypads` adds nine-key Pinyin and fuzzy Pinyin, independently or together, for Simplified and Traditional Chinese. It retains the complete pinned v1 dictionaries. Each format-3 pack contains the table, reverse dictionary and four spelling prisms; no executable, plugin or schema is downloaded by the app.

Fuzzy pairs: zh/z, ch/c, sh/s, n/l, f/h, an/ang, en/eng, in/ing. The nine-key prism maps letters to telephone digits 2–9 using Rime spelling algebra. Apostrophe separates syllables. All eight reviewed runtime schemas are included here; the application supplies identical schemas.

Build on Windows with `python rime/keypads-v2/build.py --output release-v2`. The script verifies the official compiler and dictionary pins. Use `--compiler-root PATH` for the already extracted pinned compiler. System 7z is needed when downloading the compiler. Sources and notices accompany the immutable published artifacts. `models.json` identifies the exact published bytes; rebuilds create new hashes and are not claimed to be byte-identical.

Published packs were compiled using the pinned official librime DLL through its C API `deploy_schema`. The public recipe uses the official deployer with that same DLL and pinned inputs. Native tests validated normal, fuzzy, nine-key and combined fuzzy/nine-key input for both scripts.
