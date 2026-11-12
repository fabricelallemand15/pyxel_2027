"""Vérifie la cohérence des livrables d'un chapitre du cours.

Usage :
    python3 cours/pyxel-platformer/outils/verifier_articles.py

Contrôles, pour chaque dossier de leçon et de chapitre bonus :

- le bloc python de la section « Le code complet » est identique à main.py ;
- le bloc « Code final » du script vidéo est identique à main.py ;
- les blocs de code et les divs Quarto sont appariés ;
- aucune balise HTML ne subsiste hors des blocs de code ;
- les tableaux ont le même nombre de cellules sur chaque ligne ;
- la prose n'utilise que des apostrophes typographiques.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FOLDERS = [
    folder
    for folder in sorted(ROOT.iterdir())
    if (folder / "main.py").exists() and folder.name != "outils"
]
FOLDERS += [
    folder
    for folder in sorted((ROOT / "bonus-cube").iterdir())
    if (folder / "main.py").exists()
]

QUOTED_IDENTIFIERS = re.compile(r"'(?:res\.pyxres|pyxel\.cube)'")
ELISION = re.compile(r"[A-Za-zÀ-ÿ]'[A-Za-zÀ-ÿ]")


def fences(text):
    return re.findall(r"^```(\w*)\n(.*?)^```$", text, re.S | re.M)


def code_block_after(text, heading):
    match = re.search(
        r"^" + heading + r".*?^```python\n(.*?)^```$",
        text,
        re.S | re.M,
    )
    return match.group(1).rstrip("\n") if match else None


def script_code(text):
    match = re.search(r"^### Code final\n.*?^```python\n(.*?)^```$", text, re.S | re.M)
    return match.group(1).rstrip("\n") if match else None


def strip_code(text):
    text = re.sub(r"^```.*?^```$", "", text, flags=re.S | re.M)
    return re.sub(r"`[^`]*`", "", text)


def check_qmd(path, main_py):
    problems = []
    name = path.parent.name
    text = path.read_text(encoding="utf-8")

    block = code_block_after(text, "## Le code complet")
    if block is None:
        problems.append(f"{name}: bloc « Le code complet » absent")
    elif block != main_py:
        problems.append(f"{name}: code de l'article différent de main.py")

    for language, body in fences(text):
        if language != "python" and re.search(r"<[a-zA-Z/][^>]*>", body):
            problems.append(f"{name}: balise HTML dans un bloc {language}")

    prose = strip_code(text)
    for match in re.finditer(r"<[a-zA-Z/][^>]*>", prose):
        problems.append(f"{name}: balise HTML résiduelle {match.group(0)}")

    titles = re.findall(r'title="([^"]*)"', text)
    without_titles = re.sub(r'title="[^"]*"', "", prose)
    for number, line in enumerate(without_titles.splitlines(), 1):
        if QUOTED_IDENTIFIERS.sub("", line).count("'"):
            problems.append(f"{name}:{number}: apostrophe droite")
    for title in titles:
        found = ELISION.search(QUOTED_IDENTIFIERS.sub("", title))
        if found:
            problems.append(f"{name}: élision dans un titre d'encadré : {title}")

    if len(re.findall(r"^::::$", text, re.M)) != 1:
        problems.append(f"{name}: div .lesson mal fermée")
    if len(re.findall(r"^:::: \{\.lesson\}$", text, re.M)) != 1:
        problems.append(f"{name}: div .lesson absente")
    if len(re.findall(r"^::: \{\.lesson-header\}$", text, re.M)) != 1:
        problems.append(f"{name}: en-tête absente")
    opens = len(re.findall(r"^::: \{", text, re.M))
    closes = len(re.findall(r"^:::$", text, re.M))
    if opens != closes:
        problems.append(f"{name}: {opens} divs ouvertes pour {closes} fermées")

    table = []
    for line in text.splitlines() + [""]:
        if line.startswith("|"):
            table.append(line)
            continue
        if table:
            counts = {row.count("|") for row in table}
            if len(counts) != 1:
                problems.append(f"{name}: tableau irrégulier {counts}")
            table = []

    identifiers = re.findall(r"^## .* \{#([^}]+)\}$", text, re.M)
    if len(identifiers) != len(set(identifiers)):
        problems.append(f"{name}: identifiants de section dupliqués")

    return problems


def check_script(path, main_py):
    problems = []
    name = path.parent.name
    text = path.read_text(encoding="utf-8")
    if text.count("```") % 2:
        problems.append(f"{name}: bloc de code non fermé dans le script")
    block = script_code(text)
    if block is None:
        problems.append(f"{name}: bloc « Code final » absent du script")
    elif block != main_py:
        problems.append(f"{name}: script différent de main.py")
    prose = re.sub(r"^```.*?^```$", "", text, flags=re.S | re.M)
    prose = re.sub(r"`[^`]*`", "", prose)
    for number, line in enumerate(prose.splitlines(), 1):
        if QUOTED_IDENTIFIERS.sub("", line).count("'"):
            problems.append(f"{name}:{number}: apostrophe droite dans le script")
    return problems


def check_code(path):
    problems = []
    text = path.read_text(encoding="utf-8")
    for number, line in enumerate(text.splitlines(), 1):
        if len(line) > 79:
            problems.append(f"{path.parent.name}: ligne {number} trop longue")
        if any(ord(char) > 127 for char in line):
            problems.append(f"{path.parent.name}: caractère non ASCII ligne {number}")
    return problems


def main():
    problems = []
    for folder in FOLDERS:
        main_py = (folder / "main.py").read_text(encoding="utf-8").rstrip("\n")
        qmd = folder / "article.qmd"
        script = folder / "script-video.md"
        if not qmd.exists():
            problems.append(f"{folder.name}: article.qmd absent")
        else:
            problems += check_qmd(qmd, main_py)
        if not script.exists():
            problems.append(f"{folder.name}: script-video.md absent")
        else:
            problems += check_script(script, main_py)
        problems += check_code(folder / "main.py")
    print(f"{len(FOLDERS)} dossiers vérifiés")
    for problem in problems:
        print(" -", problem)
    if not problems:
        print("aucun problème")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
