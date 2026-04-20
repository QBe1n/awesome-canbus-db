# SQL Query Cookbook

14 battle-tested queries for `awesome_canbus.db`. Copy-paste into `sqlite3`, DB Browser, Datasette, or any client.

## 1. Top-20 by stars

```sql
SELECT name, category, language, stars, activity
FROM v_projects
WHERE is_github = 1
ORDER BY stars DESC
LIMIT 20;
```

## 2. Highly-recommended projects (🔝 from upstream)

```sql
SELECT name, category, stars, language, description
FROM v_top_recommended;
```

## 3. All OBD-II tools

```sql
SELECT name, stars, language, description, url
FROM v_projects
WHERE subcategory = 'OBD-II tools'
ORDER BY stars DESC NULLS LAST;
```

## 4. Active Python libraries

```sql
SELECT name, stars, days_since_push, description
FROM v_projects
WHERE language = 'Python' AND activity IN ('Очень активен', 'Активен')
ORDER BY stars DESC;
```

## 5. Reverse-engineering toolkits

```sql
SELECT name, stars, language, url
FROM v_projects
WHERE category = 'Hacking and Reverse Engineering tools'
ORDER BY stars DESC;
```

## 6. License distribution

```sql
SELECT license, COUNT(*) AS projects, SUM(stars) AS total_stars
FROM v_projects
WHERE license IS NOT NULL
GROUP BY license
ORDER BY total_stars DESC;
```

## 7. Projects by GitHub topic

```sql
SELECT p.name, p.stars, p.gh_full_name
FROM project p
JOIN project_topic pt ON pt.project_id = p.id
JOIN topic t          ON t.id = pt.topic_id
WHERE t.name = 'automotive'
ORDER BY p.stars DESC;
```

## 8. Keyword search in descriptions

```sql
SELECT name, category, stars, description
FROM v_projects
WHERE description LIKE '%UDS%' OR description LIKE '%ISO-TP%'
ORDER BY stars DESC;
```

## 9. ESP32-based hardware

```sql
SELECT name, stars, description, url
FROM v_projects
WHERE category = 'Hardware' AND subcategory LIKE '%Espressif%'
ORDER BY stars DESC NULLS LAST;
```

## 10. Most active in the last month

```sql
SELECT name, category, stars, days_since_push, gh_full_name
FROM v_projects
WHERE days_since_push < 30
ORDER BY stars DESC NULLS LAST;
```

## 11. Abandoned but still popular

```sql
SELECT name, stars, days_since_push, description
FROM v_stale
LIMIT 20;
```

## 12. Category × language matrix

```sql
SELECT category, language, COUNT(*) AS n
FROM v_projects
WHERE is_github = 1 AND language IS NOT NULL
GROUP BY category, language
ORDER BY category, n DESC;
```

## 13. CAN-FD-capable projects

```sql
SELECT name, stars, category, description
FROM v_projects
WHERE description LIKE '%CAN-FD%' OR description LIKE '%CANFD%'
ORDER BY stars DESC NULLS LAST;
```

## 14. All projects from one author

```sql
SELECT gh_full_name, name, stars, category
FROM v_projects
WHERE gh_owner = 'collin80'
ORDER BY stars DESC;
```
