# Issues Found

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---|---|---|
| subprocess with shell=True (B602) | Security (High) | 61 | User-supplied `folder` is concatenated into a shell command, allowing command injection | Remove subprocess, use `shutil.copy` |
| Weak MD5 hash (B324) | Security (High) | 39 | MD5 is flagged as a weak hash | Pass `usedforsecurity=False` (job card id is not a security feature) |
| Hardcoded password (B105) | Security (Low) | 8 | Password stored in source code | Read from an environment variable |
| Importing subprocess (B404) | Security (Low) | 3 | Import of a risky module | Removed along with the subprocess call |
| Mutable default argument (W0102) | Bug | 12 | `history=[]` is created once and shared across all calls | Default to `None` and create the list inside the function |
| Broad exception (W0718) | Quality | 23 | `except Exception` can hide unrelated errors | Catch `KeyError` only |
| Missing encoding (W1514) | Quality | 50 | `open()` without encoding depends on the platform default | Add `encoding="utf-8"` |
| Naming not snake_case (C0103) | Style | 12-59 | Functions, arguments and variables use camelCase | Rename to snake_case |
| Missing docstrings (C0114, C0116) | Style | 1, 12-64 | Module and all functions undocumented | Add docstrings |
| Missing whitespace after comma (E231) | Style | 7 | `1500,"General"` | Add a space |
| Missing whitespace around operator (E225) | Style | 43 | `best=None` | Write `best = None` |
| Expected 2 blank lines (E302) | Style | 49 | Only 1 blank line before `saveRecords` | Add a second blank line |
| Line too long (E501) | Style | 77 | 83 characters, limit is 79 | Split the print call across lines |