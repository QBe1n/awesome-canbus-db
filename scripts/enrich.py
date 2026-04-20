"""Обогащение записей GitHub API. Используем уже собранные 27 метаданных где возможно."""
import json, os, subprocess, time, sys

entries = json.load(open('/home/user/workspace/canbus_db/parsed_entries.json'))

# Переиспользуем данные из первого прохода (20 репо + 7 доп)
existing = {}
try:
    prev = json.load(open('/home/user/workspace/data/repos.json'))
    for r in prev:
        existing[r['full_name'].lower()] = r
    print(f"Reusing {len(existing)} repos from previous pass")
except FileNotFoundError:
    pass

enriched_path = '/home/user/workspace/canbus_db/enriched.json'
if os.path.exists(enriched_path):
    enriched = {e['url']: e for e in json.load(open(enriched_path))}
    print(f"Resuming with {len(enriched)} already enriched")
else:
    enriched = {}

def gh_api(path):
    try:
        res = subprocess.run(
            ['gh', 'api', path],
            capture_output=True, text=True, timeout=20
        )
        if res.returncode != 0:
            return None
        return json.loads(res.stdout)
    except Exception:
        return None

total = len(entries)
for i, e in enumerate(entries, start=1):
    if e['url'] in enriched:
        continue
    base = dict(e)
    base['stars'] = None
    base['language'] = None
    base['license'] = None
    base['pushed_at'] = None
    base['created_at'] = None
    base['open_issues'] = None
    base['archived'] = None
    base['fork'] = None
    base['size_kb'] = None
    base['topics'] = None

    if e['is_github'] and e['gh_full_name']:
        key = e['gh_full_name'].lower()
        r = existing.get(key)
        if r:
            base['stars'] = r.get('stars')
            base['language'] = r.get('language')
            base['license'] = r.get('license')
            base['pushed_at'] = r.get('pushed_at')
            base['created_at'] = r.get('created_at')
            base['open_issues'] = r.get('open_issues')
            base['archived'] = r.get('archived')
        else:
            # Запрос к API
            data = gh_api(f"repos/{e['gh_full_name']}")
            if data and 'stargazers_count' in data:
                base['stars'] = data.get('stargazers_count')
                base['language'] = data.get('language')
                base['license'] = (data.get('license') or {}).get('spdx_id')
                base['pushed_at'] = data.get('pushed_at')
                base['created_at'] = data.get('created_at')
                base['open_issues'] = data.get('open_issues_count')
                base['archived'] = data.get('archived')
                base['fork'] = data.get('fork')
                base['size_kb'] = data.get('size')
                base['topics'] = ','.join(data.get('topics') or [])
            # мягкая пауза
            time.sleep(0.05)

    enriched[e['url']] = base

    if i % 20 == 0:
        # Периодически сохраняем
        with open(enriched_path, 'w') as f:
            json.dump(list(enriched.values()), f, ensure_ascii=False, indent=2)
        print(f"  [{i}/{total}] saved checkpoint")

# Финальное сохранение
with open(enriched_path, 'w') as f:
    json.dump(list(enriched.values()), f, ensure_ascii=False, indent=2)

# Статистика
with_stars = sum(1 for v in enriched.values() if v['stars'] is not None)
print(f"\nDONE. Total {len(enriched)}. С метаданными: {with_stars}")
top = sorted([v for v in enriched.values() if v['stars']], key=lambda x: -x['stars'])[:10]
print("\nТоп-10 по звёздам:")
for t in top:
    print(f"  {t['stars']:6d}  {t['gh_full_name']}  [{t['category']}]")
