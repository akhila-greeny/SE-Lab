# Reflection

## 1. Which issues were the easiest and which were the hardest to fix?

The easiest were the Flake8 formatting issues (missing spaces after commas,
blank lines, a line over 79 characters) and the Pylint docstring and naming
warnings. They were mechanical and did not change how the program behaves.
The hardest were the Bandit security findings, because each one needed a
design decision. Replacing `subprocess.call(..., shell=True)` meant switching
to `shutil.copy`, and the MD5 fix had to keep the job card id unchanged
(`353ee89f`) so the program output stayed the same.

## 2. Did the static analysis tools report any false positives?

Yes, partly. Bandit flagged MD5 as a high-severity weak hash, but here it only
generates a short job card id and is not used for security. The right fix was
`usedforsecurity=False`, not a stronger algorithm, so the warning was valid in
general but not a real vulnerability in this context. The hardcoded password
(B105) was a low-severity finding, and the value was an unused demo string, but
it is still bad practice. I treated it as valid and moved it to an environment
variable.

## 3. How would you integrate static analysis into a regular development workflow?

I would run Flake8, Pylint and Bandit automatically on every commit with
pre-commit hooks, and again in a CI pipeline such as GitHub Actions on every
pull request. The pipeline would fail if Bandit finds a high-severity issue,
if Flake8 reports anything, or if the Pylint score drops below a set threshold
such as 9.5. Catching problems at commit time is cheaper than finding them in
code review or production.

## 4. What tangible improvements did you see in the code after the fixes?

- **Security:** the command injection risk and the weak hash warning were
  removed, and Bandit went from 4 issues (2 High, 2 Low) to 0.
- **Quality:** the Pylint score went from 4.66/10 to 10.00/10.
- **Bug fixed:** the mutable default `history=[]` was shared between calls and
  kept growing. It now defaults to `None` and the list is created per call.
- **Readability:** snake_case names, docstrings, and PEP 8 formatting (Flake8
  now reports nothing) make the code easier to read and maintain.
- **Behavior preserved:** the program output was identical before and after.