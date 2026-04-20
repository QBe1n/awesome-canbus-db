"""Собираем SQLite БД из awesome-canbus с нормализованной схемой."""
import json
import sqlite3
import os
from datetime import datetime, timezone

SRC = '/home/user/workspace/canbus_db/enriched.json'
DB = '/home/user/workspace/canbus_db/awesome_canbus.db'

if os.path.exists(DB):
    os.remove(DB)

entries = json.load(open(SRC))
now = datetime.now(timezone.utc)

con = sqlite3.connect(DB)
cur = con.cursor()

# ==== Метаданные БД ====
cur.executescript("""
CREATE TABLE meta (
    key   TEXT PRIMARY KEY,
    value TEXT NOT NULL
);

-- Справочники ------------------------------------------------------------
CREATE TABLE category (
    id   INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE subcategory (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT NOT NULL,
    category_id INTEGER NOT NULL REFERENCES category(id),
    UNIQUE(category_id, name)
);

CREATE TABLE language (
    id   INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE license (
    id    INTEGER PRIMARY KEY AUTOINCREMENT,
    spdx  TEXT NOT NULL UNIQUE
);

-- Основная таблица -------------------------------------------------------
CREATE TABLE project (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    name           TEXT NOT NULL,
    description    TEXT,
    url            TEXT NOT NULL UNIQUE,
    category_id    INTEGER NOT NULL REFERENCES category(id),
    subcategory_id INTEGER          REFERENCES subcategory(id),
    is_top         INTEGER NOT NULL DEFAULT 0,   -- 🔝 highly recommended
    is_github      INTEGER NOT NULL DEFAULT 0,
    gh_owner       TEXT,
    gh_repo        TEXT,
    gh_full_name   TEXT,                         -- owner/repo
    stars          INTEGER,
    language_id    INTEGER REFERENCES language(id),
    license_id     INTEGER REFERENCES license(id),
    created_at     TEXT,                         -- ISO-8601
    pushed_at      TEXT,                         -- дата последнего push
    days_since_push INTEGER,                     -- производное, для удобных запросов
    activity       TEXT,                         -- 'Очень активен' / 'Активен' / ...
    open_issues    INTEGER,
    archived       INTEGER,
    fork           INTEGER,
    size_kb        INTEGER,
    created_ts     TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Топики (many-to-many) --------------------------------------------------
CREATE TABLE topic (
    id   INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE project_topic (
    project_id INTEGER NOT NULL REFERENCES project(id) ON DELETE CASCADE,
    topic_id   INTEGER NOT NULL REFERENCES topic(id)   ON DELETE CASCADE,
    PRIMARY KEY(project_id, topic_id)
);

-- Индексы ----------------------------------------------------------------
CREATE INDEX idx_project_category    ON project(category_id);
CREATE INDEX idx_project_subcategory ON project(subcategory_id);
CREATE INDEX idx_project_language    ON project(language_id);
CREATE INDEX idx_project_stars       ON project(stars DESC);
CREATE INDEX idx_project_pushed      ON project(pushed_at DESC);
CREATE INDEX idx_project_is_top      ON project(is_top);
CREATE INDEX idx_project_is_github   ON project(is_github);
""")

def activity_label(days):
    if days is None:
        return None
    if days < 30:   return 'Очень активен'
    if days < 180:  return 'Активен'
    if days < 365:  return 'Умеренная'
    if days < 730:  return 'Низкая'
    return 'Заброшен'

# Справочники через upsert-кэш
def upsert(cache, sql, key):
    if key in cache:
        return cache[key]
    cur.execute(sql, (key,))
    cache[key] = cur.lastrowid or cur.execute(
        {
            'category': "SELECT id FROM category WHERE name=?",
            'language': "SELECT id FROM language WHERE name=?",
            'license':  "SELECT id FROM license  WHERE spdx=?",
            'topic':    "SELECT id FROM topic    WHERE name=?",
        }.get('category'), (key,)
    ).fetchone()[0]
    return cache[key]

cat_cache, subcat_cache, lang_cache, lic_cache, topic_cache = {}, {}, {}, {}, {}

def get_category_id(name):
    if name in cat_cache: return cat_cache[name]
    cur.execute("INSERT OR IGNORE INTO category(name) VALUES(?)", (name,))
    cur.execute("SELECT id FROM category WHERE name=?", (name,))
    cat_cache[name] = cur.fetchone()[0]
    return cat_cache[name]

def get_subcategory_id(name, cat_id):
    if name is None: return None
    key = (cat_id, name)
    if key in subcat_cache: return subcat_cache[key]
    cur.execute("INSERT OR IGNORE INTO subcategory(name, category_id) VALUES(?,?)", (name, cat_id))
    cur.execute("SELECT id FROM subcategory WHERE category_id=? AND name=?", (cat_id, name))
    subcat_cache[key] = cur.fetchone()[0]
    return subcat_cache[key]

def get_language_id(name):
    if not name: return None
    if name in lang_cache: return lang_cache[name]
    cur.execute("INSERT OR IGNORE INTO language(name) VALUES(?)", (name,))
    cur.execute("SELECT id FROM language WHERE name=?", (name,))
    lang_cache[name] = cur.fetchone()[0]
    return lang_cache[name]

def get_license_id(spdx):
    if not spdx or spdx == 'NOASSERTION': return None
    if spdx in lic_cache: return lic_cache[spdx]
    cur.execute("INSERT OR IGNORE INTO license(spdx) VALUES(?)", (spdx,))
    cur.execute("SELECT id FROM license WHERE spdx=?", (spdx,))
    lic_cache[spdx] = cur.fetchone()[0]
    return lic_cache[spdx]

def get_topic_id(t):
    if not t: return None
    if t in topic_cache: return topic_cache[t]
    cur.execute("INSERT OR IGNORE INTO topic(name) VALUES(?)", (t,))
    cur.execute("SELECT id FROM topic WHERE name=?", (t,))
    topic_cache[t] = cur.fetchone()[0]
    return topic_cache[t]

# Заливаем проекты
for e in entries:
    cat_id = get_category_id(e['category'])
    sub_id = get_subcategory_id(e.get('subcategory'), cat_id)
    lang_id = get_language_id(e.get('language'))
    lic_id = get_license_id(e.get('license'))

    days = None
    if e.get('pushed_at'):
        try:
            pushed = datetime.fromisoformat(e['pushed_at'].replace('Z', '+00:00'))
            days = (now - pushed).days
        except Exception:
            days = None

    cur.execute("""
        INSERT INTO project(
            name, description, url, category_id, subcategory_id,
            is_top, is_github, gh_owner, gh_repo, gh_full_name,
            stars, language_id, license_id,
            created_at, pushed_at, days_since_push, activity,
            open_issues, archived, fork, size_kb
        ) VALUES(?,?,?,?,?, ?,?,?,?,?, ?,?,?, ?,?,?,?, ?,?,?,?)
    """, (
        e['name'], e.get('description'), e['url'], cat_id, sub_id,
        1 if e.get('is_top') else 0,
        1 if e.get('is_github') else 0,
        e.get('gh_owner'), e.get('gh_repo'), e.get('gh_full_name'),
        e.get('stars'), lang_id, lic_id,
        e.get('created_at'), e.get('pushed_at'), days, activity_label(days),
        e.get('open_issues'),
        1 if e.get('archived') else (0 if e.get('archived') is False else None),
        1 if e.get('fork') else (0 if e.get('fork') is False else None),
        e.get('size_kb'),
    ))
    pid = cur.lastrowid
    # topics
    topics_raw = e.get('topics') or ''
    for t in topics_raw.split(','):
        t = t.strip()
        if not t:
            continue
        tid = get_topic_id(t)
        cur.execute("INSERT OR IGNORE INTO project_topic(project_id, topic_id) VALUES(?,?)", (pid, tid))

# ==== Представления ====
cur.executescript("""
-- Проекты + читаемые имена вместо ID
CREATE VIEW v_projects AS
SELECT
    p.id,
    p.name,
    p.description,
    p.url,
    c.name               AS category,
    sc.name              AS subcategory,
    p.is_top,
    p.is_github,
    p.gh_full_name,
    p.stars,
    l.name               AS language,
    lic.spdx             AS license,
    p.pushed_at,
    p.days_since_push,
    p.activity,
    p.open_issues,
    p.archived,
    p.fork
FROM project p
JOIN      category    c   ON c.id  = p.category_id
LEFT JOIN subcategory sc  ON sc.id = p.subcategory_id
LEFT JOIN language    l   ON l.id  = p.language_id
LEFT JOIN license     lic ON lic.id= p.license_id;

-- Топ-проекты (🔝)
CREATE VIEW v_top_recommended AS
SELECT * FROM v_projects WHERE is_top = 1 ORDER BY stars DESC;

-- Статистика по категориям
CREATE VIEW v_category_stats AS
SELECT
    category,
    COUNT(*)                              AS projects,
    SUM(CASE WHEN is_github=1 THEN 1 ELSE 0 END) AS on_github,
    SUM(stars)                            AS total_stars,
    CAST(AVG(stars) AS INTEGER)           AS avg_stars,
    MAX(stars)                            AS max_stars
FROM v_projects
GROUP BY category
ORDER BY total_stars DESC NULLS LAST;

-- Статистика по языкам
CREATE VIEW v_language_stats AS
SELECT
    COALESCE(language, '—') AS language,
    COUNT(*)                AS projects,
    SUM(stars)              AS total_stars,
    CAST(AVG(stars) AS INTEGER) AS avg_stars
FROM v_projects
WHERE is_github = 1
GROUP BY language
ORDER BY total_stars DESC NULLS LAST;

-- Самые активные проекты
CREATE VIEW v_active AS
SELECT * FROM v_projects
WHERE activity IN ('Очень активен','Активен')
ORDER BY stars DESC NULLS LAST;

-- Заброшенные (с какой-то аудиторией: 50+ звёзд)
CREATE VIEW v_stale AS
SELECT * FROM v_projects
WHERE activity IN ('Низкая','Заброшен') AND stars >= 50
ORDER BY stars DESC;
""")

# Метаданные
meta = [
    ('source',               'https://github.com/iDoka/awesome-canbus'),
    ('generated_at',         now.strftime('%Y-%m-%d %H:%M UTC')),
    ('total_projects',       str(len(entries))),
    ('github_projects',      str(sum(1 for e in entries if e['is_github']))),
    ('enriched_projects',    str(sum(1 for e in entries if e.get('stars') is not None))),
    ('schema_version',       '1.0'),
    ('description',          'База данных инструментов, библиотек и ресурсов для работы с CAN-шиной'),
]
cur.executemany("INSERT INTO meta(key, value) VALUES(?,?)", meta)

con.commit()

# Проверка
print("=== Проверка ===")
for q in [
    ("Проектов всего",      "SELECT COUNT(*) FROM project"),
    ("С метаданными GitHub","SELECT COUNT(*) FROM project WHERE stars IS NOT NULL"),
    ("Топ-рекомендованных", "SELECT COUNT(*) FROM project WHERE is_top=1"),
    ("Категорий",           "SELECT COUNT(*) FROM category"),
    ("Подкатегорий",        "SELECT COUNT(*) FROM subcategory"),
    ("Языков",              "SELECT COUNT(*) FROM language"),
    ("Лицензий",            "SELECT COUNT(*) FROM license"),
    ("Топиков",             "SELECT COUNT(*) FROM topic"),
    ("Связей project-topic","SELECT COUNT(*) FROM project_topic"),
]:
    cur.execute(q[1])
    print(f"  {q[0]:25s}: {cur.fetchone()[0]}")

print("\n=== Топ-10 по звёздам ===")
cur.execute("""
    SELECT stars, gh_full_name, category
    FROM v_projects WHERE is_github=1 ORDER BY stars DESC NULLS LAST LIMIT 10
""")
for row in cur.fetchall():
    print(f"  {row[0]:>6}  {row[1]:35s}  [{row[2]}]")

print("\n=== Категории ===")
cur.execute("SELECT category, projects, total_stars FROM v_category_stats")
for row in cur.fetchall():
    print(f"  {row[0]:40s}  {row[1]:4d} проектов  {row[2] or 0:>8} ⭐")

con.close()

size_mb = os.path.getsize(DB) / 1024
print(f"\nDB saved: {DB}  ({size_mb:.1f} KB)")
