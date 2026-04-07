# Contribution Guidelines

## Suggesting a New Resource

Please use the GitHub issue form for new suggestions:

- Open `Suggest a Resource`
- Fill in the category, description, and repository fields as completely as you can
- For papers and articles, use the `Subsection` field for the relevant topic heading

Maintainers can then label the issue and let the automation handle evaluation and PR generation.

## Fixing an Existing Entry

This repository uses a YAML-first workflow:

- `data/*.yaml` is the source of truth
- `README.md` is generated from the YAML data

If you are opening a direct PR:

1. Edit the relevant `data/*.yaml` file, not `README.md`
2. Keep entries in the correct section and order
3. Run `python3 scripts/validate_entries.py`
4. Run `python3 scripts/generate_readme.py`
5. Commit the regenerated `README.md`
6. Sign off commits with `git commit --signoff`

## General Rules

- Search previous suggestions first to avoid duplicates
- Keep descriptions short, factual, and easy to scan
- Use the appropriate category and subsection
- Check spelling and grammar
- Remove trailing whitespace

Thank you for the contribution.
