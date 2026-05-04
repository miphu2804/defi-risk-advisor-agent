# Feature 00: Project Foundation

## Goal

Create a reproducible UV-managed Python project foundation that future features can build on.

## Scope

Included:

- UV project setup.
- Python version pin.
- Package layout.
- Configuration entrypoint.
- Basic README setup.
- Empty but intentional folder structure.

Not included:

- API implementation.
- ML model training.
- Data ingestion.
- Agent logic.

## Files

Create or update:

```text
.python-version
.gitignore
.env.example
pyproject.toml
uv.lock
README.md
src/defi_risk_advisor/__init__.py
src/defi_risk_advisor/app_config.py
tests/
```

## Implementation Steps

1. Confirm Python version is pinned:

   ```bash
   uv python pin 3.11
   ```

2. Keep dependencies empty until code needs them.
3. Add runtime dependencies with `uv add`, not manual `pyproject.toml` edits.
4. Add dev dependencies only when first tests/lint are introduced:

   ```bash
   uv add --dev pytest pytest-cov ruff mypy
   ```

5. Create importable package at `src/defi_risk_advisor/`.
6. Add `app_config.py` as the single environment/config entrypoint.
7. Add `.env.example` with placeholders only.
8. Ensure `.env*` is ignored, except `.env.example`.
9. Update README with UV setup commands.
10. Run `uv sync` and commit `uv.lock`.

## Config Guideline

All environment variables go through `app_config.py`.

Rules:

- Load `.env` once in config.
- Validate env values once in config.
- Other modules import config values instead of calling `os.getenv`.
- Never log secret values.

## Review Checklist

- No `requirements.txt` unless exported for a specific deployment target.
- No secrets in `.env.example`.
- README uses `uv sync` and `uv run`.
- Package imports work from `src/`.
- `uv.lock` exists after dependencies are introduced.

## Verification

```bash
uv sync
uv run python main.py
```

When tests exist:

```bash
uv run python -m compileall src tests
uv run pytest
uv run ruff check .
```

## Done Criteria

- New developer can clone, run `uv sync`, then run the starter command.
- Project metadata describes the DeFi risk advisor.
- Folder structure supports the next feature.

## Unresolved Questions

1. Should package mode use `hatchling`, `uv_build`, or stay virtual initially?
2. Should lint settings be added now or when first source modules exist?
3. Should Docker be deferred until API exists?
