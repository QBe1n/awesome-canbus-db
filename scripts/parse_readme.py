"""Парсер README awesome-canbus в структурированный JSON."""
import re
import json

with open('/home/user/workspace/canbus_db/awesome_canbus_README.md', 'r') as f:
    text = f.read()

# Строгий regex для записей: * [Name](url) - Description
# Префикс 🔝 опционален
entry_re = re.compile(
    r'^\*\s*(?P<top>🔝)?\[(?P<name>[^\]]+)\]\((?P<url>[^)]+)\)\s*-?\s*(?P<desc>.*?)$',
    re.MULTILINE
)

lines = text.split('\n')

entries = []
current_h2 = None          # ## секция
current_h3 = None          # ### подсекция
# Секции до которых парсим. Contents, Footnotes, Tags, Contributing пропускаем.
skip_sections = {'Contents', 'Contributing', 'Footnotes', 'Tags'}

in_toc = False
current_line_idx = 0

for line in lines:
    current_line_idx += 1
    # Заголовки
    if line.startswith('## '):
        current_h2 = line[3:].strip()
        current_h3 = None
        continue
    if line.startswith('### '):
        current_h3 = line[4:].strip()
        continue
    # Пропускаем Contents и служебные
    if not current_h2 or current_h2 in skip_sections:
        continue
    # Пропускаем lint-комментарии
    if line.strip().startswith('<!--'):
        continue
    # Только буллиты с ссылкой (учитываем 🔝 префикс)
    ls = line.lstrip()
    if not (ls.startswith('* [') or ls.startswith('* 🔝[')):
        continue
    # Игнорируем вложенные буллиты оглавления типа "  * [X](#anchor)"
    m = entry_re.match(line)
    if not m:
        continue
    url = m.group('url').strip()
    if url.startswith('#'):
        continue  # anchor link, пропускаем
    name = m.group('name').strip()
    desc = m.group('desc').strip()
    # Убираем trailing '.'
    if desc.endswith('.'):
        desc = desc[:-1]
    # Определяем, GitHub ли это
    gh_match = re.match(r'https?://github\.com/([^/]+)/([^/#?]+)', url)
    gh_owner = gh_repo = None
    if gh_match:
        gh_owner = gh_match.group(1)
        gh_repo = gh_match.group(2).rstrip('/')
        # Убираем .git
        if gh_repo.endswith('.git'):
            gh_repo = gh_repo[:-4]

    entries.append({
        'name': name,
        'url': url,
        'description': desc,
        'category': current_h2,
        'subcategory': current_h3,
        'is_top': bool(m.group('top')),
        'is_github': gh_owner is not None,
        'gh_owner': gh_owner,
        'gh_repo': gh_repo,
        'gh_full_name': f"{gh_owner}/{gh_repo}" if gh_owner else None,
    })

# Удаляем дубликаты по URL (иногда проект появляется в нескольких секциях — оставим первое)
seen = set()
deduped = []
for e in entries:
    key = e['url']
    if key in seen:
        continue
    seen.add(key)
    deduped.append(e)

# Статистика
print(f"Parsed {len(entries)} raw entries, {len(deduped)} unique")
cats = {}
for e in deduped:
    cats[e['category']] = cats.get(e['category'], 0) + 1
print("\nБy category:")
for c, n in sorted(cats.items(), key=lambda x: -x[1]):
    print(f"  {n:3d}  {c}")
gh_count = sum(1 for e in deduped if e['is_github'])
top_count = sum(1 for e in deduped if e['is_top'])
print(f"\nGitHub-ссылок: {gh_count}")
print(f"🔝 отмеченных: {top_count}")

with open('/home/user/workspace/canbus_db/parsed_entries.json', 'w') as f:
    json.dump(deduped, f, ensure_ascii=False, indent=2)
