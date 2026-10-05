#!/usr/bin/env python3
"""Build the public CV PDF for the website from External_Files/CV/main.tex.

The source is copied to a temporary directory and adjusted there; the original
is never modified. Adjustments:
  * fill in the website and GitHub URLs,
  * open without the bookmarks sidebar,
  * silence the tailoring notes (\\cvnote),
  * drop the sections flagged "include only for Lab positions".

Usage:  python3 scripts/build_cv.py
Output: files/John_Turnage_CV.pdf
"""
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "External_Files" / "CV" / "main.tex"
OUTPUT = ROOT / "files" / "John_Turnage_CV.pdf"
LATEXMK = shutil.which("latexmk") or "/Library/TeX/texbin/latexmk"

WEBSITE = "https://john-turnage.github.io"
GITHUB = "https://github.com/John-Turnage"


def replace_once(text, old, new):
    if old not in text:
        sys.exit(f"build_cv: expected to find {old!r} in main.tex; update this script.")
    return text.replace(old, new, 1)


def main():
    tex = SOURCE.read_text()
    tex = replace_once(tex, r"\newcommand{\websiteURL}{}", r"\newcommand{\websiteURL}{%s}" % WEBSITE)
    tex = replace_once(tex, r"\newcommand{\githubURL}{}", r"\newcommand{\githubURL}{%s}" % GITHUB)

    # Open without the bookmarks sidebar (hyperref's default is UseOutlines).
    tex = replace_once(tex, r"\begin{document}", "\\hypersetup{pdfpagemode=UseNone}\n\\begin{document}")

    # Silence tailoring notes: \cvnote prints nothing.
    tex, n = re.subn(r"^\\newcommand\{\\cvnote\}\[1\]\{.*\}$",
                     lambda m: r"\newcommand{\cvnote}[1]{}", tex, count=1, flags=re.M)
    if n != 1:
        sys.exit("build_cv: could not find the \\cvnote definition; update this script.")

    # Drop every section whose heading carries a "Lab positions" note, up to the next section marker.
    tex, n = re.subn(r"%-+[A-Z ]+-+\n\\section\{[^\n]*\\cvnote\{include only for Lab positions\}\}.*?(?=%-+[A-Z ]+-+\n)",
                     "", tex, flags=re.S)
    print(f"build_cv: removed {n} lab-only section(s)")

    if r"\todo{" in tex.split(r"\begin{document}", 1)[1]:
        sys.exit("build_cv: main.tex still contains a \\todo{...}; resolve it before publishing.")

    with tempfile.TemporaryDirectory() as tmp:
        (Path(tmp) / "main.tex").write_text(tex)
        result = subprocess.run([LATEXMK, "-pdf", "-interaction=nonstopmode", "-halt-on-error", "main.tex"],
                                cwd=tmp, capture_output=True, text=True)
        if result.returncode != 0:
            sys.stdout.write(result.stdout[-3000:])
            sys.exit("build_cv: LaTeX failed (log tail above).")
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(Path(tmp) / "main.pdf", OUTPUT)
    print(f"build_cv: wrote {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
