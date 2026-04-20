```text
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║    █████╗ ██╗    ██╗███████╗███████╗ ██████╗ ███╗   ███╗███████╗             ║
║   ██╔══██╗██║    ██║██╔════╝██╔════╝██╔═══██╗████╗ ████║██╔════╝             ║
║   ███████║██║ █╗ ██║█████╗  ███████╗██║   ██║██╔████╔██║█████╗               ║
║   ██╔══██║██║███╗██║██╔══╝  ╚════██║██║   ██║██║╚██╔╝██║██╔══╝               ║
║   ██║  ██║╚███╔███╔╝███████╗███████║╚██████╔╝██║ ╚═╝ ██║███████╗             ║
║   ╚═╝  ╚═╝ ╚══╝╚══╝ ╚══════╝╚══════╝ ╚═════╝ ╚═╝     ╚═╝╚══════╝             ║
║                                                                              ║
║    ██████╗ █████╗ ███╗   ██╗██████╗ ██╗   ██╗███████╗      ██████╗ ██████╗   ║
║   ██╔════╝██╔══██╗████╗  ██║██╔══██╗██║   ██║██╔════╝      ██╔══██╗██╔══██╗  ║
║   ██║     ███████║██╔██╗ ██║██████╔╝██║   ██║███████╗█████╗██║  ██║██████╔╝  ║
║   ██║     ██╔══██║██║╚██╗██║██╔══██╗██║   ██║╚════██║╚════╝██║  ██║██╔══██╗  ║
║   ╚██████╗██║  ██║██║ ╚████║██████╔╝╚██████╔╝███████║      ██████╔╝██████╔╝  ║
║    ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝  ╚═════╝ ╚══════╝      ╚═════╝ ╚═════╝   ║
║                                                                              ║
║              242 tools.  1 SQLite.  Query the whole CAN universe.            ║
║                                                                              ║
║                                  v1.0-beta                                   ║
║                                                                              ║
║                   Authors: Mikhail Kubalskiy (@QBe1n)                        ║
║                                                                              ║
║                                                                              ║
║                ⠀⠀⠀⠀⠀⠀⠀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀                          ║
║                ⠀⠀⠀⠀⣠⠶⠛⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠙⠶⣄⠀⠀⠀⠀⠀     Get them bytes.....   ║
║                ⠀⢀⣠⠞⠁⠀⠀⠀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⠀⠀⠀⠀⠈⠳⣄⡀⠀⠀                         ║
║                ⢸⣏⣀⣀⣀⣀⡴⠚⠉⠀⠀⠀⠀⠀⠀⠀⠀⠉⠙⢦⣀⣀⣀⣀⣹⠀⠀                         ║
║                ⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⠀⠀                         ║
║                ⢸⡀⢠⣶⣶⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣶⣶⡄⢀⡇⠀⠀                         ║
║                ⠀⠙⠶⠿⠿⠷⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠾⠿⠿⠷⠞⠀⠀⠀                         ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

# AWESOME-CANBUS-DB — 242 CAN Bus tools. 1 SQLite database.

[![SQLite](https://img.shields.io/badge/SQLite-3.x-003B57?logo=sqlite&logoColor=white)](https://sqlite.org)
[![Source](https://img.shields.io/badge/source-awesome--canbus-blue)](https://github.com/iDoka/awesome-canbus)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Data: CC-BY-4.0](https://img.shields.io/badge/Data-CC--BY--4.0-green.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://python.org)

---

**Authors:** Mikhail Kubalskiy ([@QBe1n](https://github.com/QBe1n))

**License:** MIT (code) + CC-BY-4.0 (data, per upstream awesome-canbus)

**Source of truth:** [iDoka/awesome-canbus](https://github.com/iDoka/awesome-canbus)

**Repository:** https://github.com/QBe1n/awesome-canbus-db

**Dependencies:** Python 3.10+, `gh` CLI (for enrichment), stdlib only (`sqlite3`, `re`, `json`)

---

## What is AWESOME-CANBUS-DB?

A queryable SQLite database built from every project listed in the excellent [awesome-canbus](https://github.com/iDoka/awesome-canbus) — a curated index of tools, libraries, hardware, and resources for working with the CAN bus. The upstream list is a well-organized markdown file. This repo turns it into something you can `JOIN`, filter, rank, and plug into other pipelines.

Every GitHub-hosted project is enriched with live metadata: stars, primary language, SPDX license, last push date, open issues, archived flag, and GitHub topics. Activity is classified into human-readable buckets so you can instantly tell "maintained" from "last touched in 2017".

1. **Parses** the full awesome-canbus README into 242 structured entries
2. **Extracts** 6 categories and 24 subcategories faithfully from the source
3. **Preserves** the `🔝` highly-recommended flag on 18 top projects
4. **Enriches** 222 GitHub repos via the `gh` CLI with stars, language, license, activity
5. **Normalizes** languages, licenses, and topics into dedicated tables (3NF)
6. **Links** projects to 388 GitHub topics via a many-to-many junction table
7. **Classifies** each repo's activity (`Очень активен` / `Активен` / `Умеренная` / `Низкая` / `Заброшен`)
8. **Indexes** the hot paths: `stars DESC`, `pushed_at DESC`, category, language
9. **Exposes** 6 pre-built views: top-recommended, category stats, language stats, active, stale, and a denormalized `v_projects`
10. **Ships** the parser, enricher, and builder as three tiny Python scripts — reproducible end-to-end

**Disclaimer: It's a quick hack, and we can't live without it**:
It was vibecoded in one session on top of Perplexity Comet agents. The database is a snapshot — rerun the scripts whenever you want fresh numbers. Don't point dashboards at this without refreshing it first. Early release, PRs welcome.

---

## What's unique about AWESOME-CANBUS-DB?

- **Single file, zero dependencies to read.** Any SQLite client works. Drop it into a Python notebook, Datasette, DBeaver, DB Browser for SQLite, or sqlite3 on your terminal.
- **Real normalized schema, not a glorified CSV.** Categories, subcategories, languages, licenses, and topics live in their own tables — join, group, and rank them freely.
- **Live GitHub metadata.** 222/226 GitHub projects carry stars, language, license, and last-push timestamps as of the generation date.
- **Reproducible.** Three scripts (`parse_readme.py` → `enrich.py` → `build_db.py`) regenerate the DB from scratch. Safe to rerun — the build script drops and recreates the file cleanly.
- **Respects upstream.** Source URL and generation timestamp are persisted in the `meta` table. Data is attributed to awesome-canbus under CC-BY-4.0.

### Recent improvements (v1.0-beta)

- **Initial release.** 242 projects, 6 views, 7 indexes, 388 topics.
- **Smart dedup.** Projects cited in multiple sections are stored once, keyed by URL.
- **Activity buckets.** Not just `days_since_push` — an opinionated label in a first-class column.
- **Incremental enrichment.** `enrich.py` checkpoints every 20 repos, safe to resume after rate limits.

---

## Quick Start

```bash
# 1. Clone
git clone https://github.com/QBe1n/awesome-canbus-db.git
cd awesome-canbus-db

# 2. Open the database
sqlite3 awesome_canbus.db

# 3. Get the top 10 by stars
sqlite> SELECT name, category, stars FROM v_projects
        WHERE is_github = 1
        ORDER BY stars DESC LIMIT 10;

# 4. Or regenerate from scratch (requires gh CLI authenticated)
curl -sL https://raw.githubusercontent.com/iDoka/awesome-canbus/master/README.md \
  -o awesome_canbus_README.md
python3 scripts/parse_readme.py
python3 scripts/enrich.py
python3 scripts/build_db.py
```

---

## Available Queries

Pre-built views cover the most common questions. Always prefer them over raw joins.

```sql
-- Discovery
SELECT * FROM v_projects          -- everything, human-readable names
SELECT * FROM v_top_recommended   -- 18 projects flagged 🔝 upstream
SELECT * FROM v_active            -- push date < 180 days
SELECT * FROM v_stale             -- 2+ years inactive, 50+ stars

-- Aggregates
SELECT * FROM v_category_stats    -- project count, total/avg stars per category
SELECT * FROM v_language_stats    -- same but per language
```

```sql
-- Narrow searches on v_projects
WHERE category     = 'Hacking and Reverse Engineering tools'
WHERE subcategory  = 'OBD-II tools'
WHERE language     = 'Python' AND activity = 'Активен'
WHERE description LIKE '%UDS%'
WHERE gh_owner     = 'collin80'
```

```sql
-- Many-to-many on topics
SELECT p.name, p.stars
FROM project p
JOIN project_topic pt ON pt.project_id = p.id
JOIN topic t          ON t.id = pt.topic_id
WHERE t.name = 'automotive'
ORDER BY p.stars DESC;
```

---

## Architecture

3NF relational schema. One fact table, four dimension tables, one junction table, six views.

- **Fact table**
  - `project` — 242 rows. `id`, `name`, `description`, `url`, FKs, `stars`, `pushed_at`, `days_since_push`, `activity`, etc.
- **Dimension tables**
  - `category` (6) — top-level sections from the awesome list
  - `subcategory` (24) — nested sections, scoped to a category
  - `language` (20) — normalized GitHub primary language
  - `license` (12) — SPDX identifiers
  - `topic` (388) — GitHub topics
- **Junction**
  - `project_topic` — many-to-many, `ON DELETE CASCADE`
- **Views** — `v_projects`, `v_top_recommended`, `v_category_stats`, `v_language_stats`, `v_active`, `v_stale`
- **Indexes** — `stars DESC`, `pushed_at DESC`, `category_id`, `subcategory_id`, `language_id`, `is_top`, `is_github`
- **Meta** — source URL, generation timestamp, schema version, project counts

**See:** `docs/SCHEMA.md` for column-by-column details (in repo).

---

## Database Snapshot

| Category | Projects | ⭐ Total |
|----------|---------:|---------:|
| **Utils** | 73 | 22,797 |
| **Hacking and Reverse Engineering tools** | 22 | 18,904 |
| **Hardware** | 91 | 12,425 |
| **Protocols** | 29 | 6,804 |
| **CAN Database** | 25 | 4,927 |
| **Test equipment and simulators** | 2 | 758 |

| Coverage | Status |
|----------|--------|
| Parsed from upstream README | ✅ 242 projects |
| Enriched via GitHub API | ✅ 222 / 226 GitHub projects |
| Flagged `🔝` (highly recommended) | ✅ 18 |
| Broken / renamed upstream URLs | ⚠️ 4 projects with `stars=NULL` |
| Non-GitHub sources (SourceForge, personal sites) | ⚠️ 16 with metadata skipped |

---

## Environment Variables

None required for querying. For regenerating the DB:

- `GH_TOKEN` — personal access token for the `gh` CLI (read-only `public_repo` scope is enough)

---

## Documentation

### User Guides
- `README.md` — this file
- `docs/QUERIES.md` — 14 battle-tested SQL recipes

### Architecture & Development
- `docs/SCHEMA.md` — table-by-table breakdown
- `scripts/parse_readme.py` — markdown → JSON
- `scripts/enrich.py` — GitHub API fan-out with checkpoints
- `scripts/build_db.py` — schema + data load

---

## Contribute

PRs are warmly welcomed. A few directions this could grow:

- Your idea here
- Your second idea here
- Fuzzy search across `description` via FTS5 virtual table
- Weekly GitHub Action that rebuilds the DB and commits the artifact
- Datasette deployment for a public web UI on top of the file
- Sibling databases for `awesome-embedded-rust`, `awesome-automotive`, etc.
- Language coverage fixes for the 4 projects stuck at `stars=NULL`

Open an issue or ping me at [@QBe1n](https://github.com/QBe1n).

---

## License

**Code:** MIT License — Copyright (c) 2026 Mikhail Kubalskiy

**Data:** CC-BY-4.0, inherited from upstream [awesome-canbus](https://github.com/iDoka/awesome-canbus). Attribution required.

See `LICENSE` file for full text.

---

## Support

- **Issues:** https://github.com/QBe1n/awesome-canbus-db/issues
- **Repository:** https://github.com/QBe1n/awesome-canbus-db
- **Upstream data:** https://github.com/iDoka/awesome-canbus
- **Author:** [@QBe1n](https://github.com/QBe1n)
