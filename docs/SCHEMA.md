# Schema reference

3NF. One fact table (`project`), four dimension tables, one junction table (`project_topic`), one meta table, six views.

## Tables

### `project` (fact)

| Column | Type | Notes |
|---|---|---|
| `id` | INTEGER PK | autoincrement |
| `name` | TEXT | as displayed on upstream list |
| `description` | TEXT | from upstream markdown |
| `url` | TEXT UNIQUE | primary link to the project |
| `category_id` | FK → `category` | required |
| `subcategory_id` | FK → `subcategory` | nullable |
| `is_top` | INTEGER | 1 if flagged `🔝` upstream |
| `is_github` | INTEGER | 1 if URL matches `github.com/<owner>/<repo>` |
| `gh_owner`, `gh_repo`, `gh_full_name` | TEXT | parsed from URL |
| `stars`, `open_issues`, `size_kb` | INTEGER | from GitHub API |
| `language_id` | FK → `language` | primary language |
| `license_id` | FK → `license` | SPDX |
| `created_at`, `pushed_at` | TEXT | ISO-8601 UTC |
| `days_since_push` | INTEGER | computed at build time |
| `activity` | TEXT | `Очень активен` / `Активен` / `Умеренная` / `Низкая` / `Заброшен` |
| `archived`, `fork` | INTEGER | booleans from API |

### `category` / `subcategory` / `language` / `license` / `topic`

Pure lookup tables: `id`, `name` (or `spdx` for license). `subcategory` carries a composite unique key `(category_id, name)` to prevent cross-category collisions.

### `project_topic` (junction)

Composite PK `(project_id, topic_id)`. `ON DELETE CASCADE` on both sides.

### `meta`

Key-value store for DB-level metadata:

| Key | Example value |
|---|---|
| `source` | `https://github.com/iDoka/awesome-canbus` |
| `generated_at` | `2026-04-20 21:34 UTC` |
| `total_projects` | `242` |
| `github_projects` | `226` |
| `enriched_projects` | `222` |
| `schema_version` | `1.0` |

## Indexes

- `idx_project_category` on `category_id`
- `idx_project_subcategory` on `subcategory_id`
- `idx_project_language` on `language_id`
- `idx_project_stars` on `stars DESC`
- `idx_project_pushed` on `pushed_at DESC`
- `idx_project_is_top` on `is_top`
- `idx_project_is_github` on `is_github`

## Views

- **`v_projects`** — denormalized project rows with readable category, subcategory, language, license names. Use this for most queries.
- **`v_top_recommended`** — filtered to `is_top = 1`, sorted by stars.
- **`v_category_stats`** — `projects`, `on_github`, `total_stars`, `avg_stars`, `max_stars` grouped by category.
- **`v_language_stats`** — same aggregates grouped by language.
- **`v_active`** — projects whose `activity` is `Очень активен` or `Активен`, sorted by stars.
- **`v_stale`** — 2+ years inactive but still ≥50 stars.

## Regenerating

```bash
curl -sL https://raw.githubusercontent.com/iDoka/awesome-canbus/master/README.md -o awesome_canbus_README.md
python3 scripts/parse_readme.py      # → parsed_entries.json (raw parse)
python3 scripts/enrich.py            # → enriched.json (GitHub API)
python3 scripts/build_db.py          # → awesome_canbus.db (final)
```

Each step is idempotent. `enrich.py` checkpoints every 20 projects, safe to interrupt and resume.
