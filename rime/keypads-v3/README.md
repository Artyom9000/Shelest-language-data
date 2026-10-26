# Exact nine-key Pinyin data v3

Adds native exact Roman syllables alongside telephone spelling. Fuzzy aliases apply only to the unresolved digit spelling. All four v2 modes are retained. Dictionaries and official compiler remain pinned in models.json. The application supplies reviewed schemas; language packs contain only compiled data.

Build on Windows with Python 3: `python build.py --output /path/to/packs --compiler-root /path/to/pinned/compiler`.

The uppercase canonical branch is derived before fuzzy transformations, then restored after numeric transliteration. No dictionary entries or candidate pages are filtered by the application. This package contains data, build recipes, provenance and licenses only.
