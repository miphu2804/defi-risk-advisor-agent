# Feature 00: Project Foundation

## Status: DONE (with deviations noted below)

## Goal

Create a reproducible UV-managed Python project foundation that future features can build on.

## Scope

Included:

- UV project setup.
- Python version pin.
- Flat package layout under `src/`.
- Configuration entrypoint via `app_config.py`.
- `.env` and `.env_example` for secrets management.
- Kaggle-based dataset downloader.
- Basic utilities for project path resolution.
- Pre-commit hooks for formatting.
- Basic test setup.

Not included:

- API implementation.
- ML model training.
- Agent logic.
- `defi_risk_advisor` subpackage (flat `src/` used instead).

## Files (actual)

```text
.python-version          # pinned to 3.11
.gitignore               # ignores .env, .venv, data/, models/, __pycache__, etc.
.env_example             # DATASET_NAME + DATASET_FILE placeholders
.env                     # actual secrets (git-ignored)
pyproject.toml           # UV-managed, dependencies already added
uv.lock                  # committed lockfile
.pre-commit-config.yaml  # isort + black hooks
main.py                  # starter "Hello from defi-risk-advisor-agent!"
notebooks/eda.ipynb      # raw-data EDA notebook
reports/eda-summary.md   # EDA decision artifact
src/
  __init__.py
  app_config.py           # pydantic-settings based, loads DATASET_NAME, DATASET_FILE
  utils.py                # get_project_root, get_project_path, get_data_path, get_file_path
  downloader/
    __init__.py
    kaggle.py             # KaggleDownloader class using kagglehub
scripts/
  download_dataset.py     # CLI script: downloads dataset from Kaggle to data/raw/
test/
  test_utils.py
  test_kaggle_downloader.py
data/
  raw/                    # downloaded .parquet dataset
```

## Implementation Steps (what was done)

1. Pinned Python to 3.11 via `.python-version`.
2. Created flat `src/` package (no `defi_risk_advisor` subpackage).
3. Added `app_config.py` using `pydantic-settings` with `DATASET_NAME` and `DATASET_FILE`.
4. Added `.env_example` with dataset placeholders.
5. Added `.gitignore` covering `.env`, `.venv`, `data/`, `models/`, `__pycache__/`.
6. Added runtime dependencies: `pandas`, `pyarrow`, `kaggle`, `kagglehub`, `pydantic-settings`, `matplotlib`, `seaborn`, `ipykernel`, `pytest`, `black`, `isort`, `pip`.
7. Added dev dependencies: `black`, `isort`, `pre-commit`.
8. Set up `.pre-commit-config.yaml` with `isort` (profile=black) and `black` (python3.11).
9. Created `src/utils.py` with path helpers (`get_project_root`, `get_data_path`, etc.).
10. Created `src/downloader/kaggle.py` with `KaggleDownloader` class.
11. Created `scripts/download_dataset.py` as CLI entrypoint for data download.
12. Added tests in `test/` for utils and kaggle downloader.
13. Ran `uv sync` and committed `uv.lock`.

## Deviations from Original Plan

| Original Plan | Actual | Reason |
|---|---|---|
| `src/defi_risk_advisor/` subpackage | Flat `src/` layout | Simpler; subpackage can be introduced later when API surface grows |
| `tests/` directory | `test/` directory | Inconsistent naming; kept as-is |
| `.env.example` | `.env_example` | Underscore variant used |
| Empty deps, add later | Dependencies added upfront | Needed for kaggle downloader and EDA notebook |
| Dev: `pytest pytest-cov ruff mypy` | Dev: `black isort pre-commit` | Chose black+isort over ruff; pytest in main deps |
| `ruff check .` for linting | `black` + `isort` via pre-commit | Same goal, different tools |

## Current Notes

- Raw-data EDA was completed before normalized schema and adapter work.
- `pytest`, `black`, and `isort` still live in main dependencies, so dependency cleanup remains open.
- The project uses `test/` rather than `tests/`, and current feature plans should verify against `test/`.

## Review Checklist

- [x] No `requirements.txt` (not needed yet).
- [x] No secrets in `.env_example`.
- [x] `uv sync` and `uv run` work.
- [x] Package imports work from `src/`.
- [x] `uv.lock` committed.
- [ ] `pytest` should be moved to dev deps (currently in main).
- [ ] `black` and `isort` duplicated in main and dev — clean up.

## Verification

```bash
uv sync
uv run python main.py
uv run pytest test
```

## Done Criteria

- [x] New developer can clone, run `uv sync`, then run the starter command.
- [x] Project metadata describes the DeFi risk advisor.
- [x] Folder structure supports data download and EDA.
- [ ] `pytest` not in main deps (cleanup task).
