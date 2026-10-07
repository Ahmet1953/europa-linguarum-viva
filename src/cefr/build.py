"""Build cefr.html prototype from plans/klasik2/category-list.md."""
import re, json, html, sys
from pathlib import Path

src = Path(sys.argv[1]).read_text()
font_css = sys.argv[2]
out = Path(sys.argv[3])

# status overrides (verified against repo on 2026-10-07)
FINAL = {("A1.1", n) for n in range(1, 17)} | {("A1.2", 1), ("A1.2", 3), ("A1.2", 4)}
REVIEW = {("A1.2", 2), ("A1.2", 5)}  # Directions and Transport, Health and Body: staging

blocks = []
cur = None
for line in src.splitlines():
    m = re.match(r"^## ([ABC][12]\.[12])\b", line)
    if m:
        cur = {"id": m.group(1), "core": [], "extra": []}
        blocks.append(cur); section = None; continue
    if cur is None:
        continue
    if line.startswith("**Çekirdek 10"):
        section = "core"; continue
    if line.startswith("**Almanca'ya özel"):
        section = "extra"; continue
    m = re.match(r"^(\d+)\. (.+)$", line)
    if m and section:
        name = re.split(r" — | \*\(| \(≈", m.group(2))[0].strip()
        cur[section].append((int(m.group(1)), name))

assert len(blocks) == 12, len(blocks)
for b in blocks:
    exp = {"A": 6, "B": 4, "C": 2}[b["id"][0]]
    assert len(b["core"]) == 10 and len(b["extra"]) == exp, (b["id"], len(b["core"]), len(b["extra"]))

data = []
for b in blocks:
    cats = []
    for n, name in b["core"] + b["extra"]:
        st = "final" if (b["id"], n) in FINAL else "review" if (b["id"], n) in REVIEW else "planned"
        cats.append({"n": n, "name": name, "core": n <= 10, "st": st})
    data.append({"id": b["id"], "cats": cats})

LEVELS = {"A1": ("Breakthrough", "Einstieg"), "A2": ("Waystage", "Grundlegende Kenntnisse"),
          "B1": ("Threshold", "Fortgeschrittene Sprachverwendung"), "B2": ("Vantage", "Selbständige Sprachverwendung"),
          "C1": ("Effective proficiency", "Fachkundige Sprachkenntnisse"), "C2": ("Mastery", "Annähernd muttersprachliche Kenntnisse")}

page = Path(__file__).with_name("template.html").read_text()
page = page.replace("/*FONTS*/", font_css).replace("__DATA__", json.dumps(data, ensure_ascii=False)).replace("__LEVELS__", json.dumps(LEVELS, ensure_ascii=False))
out.write_text(page)
tot = sum(len(b["cats"]) for b in data)
print("blocks", len(data), "categories", tot, "final", sum(c["st"] == "final" for b in data for c in b["cats"]))
