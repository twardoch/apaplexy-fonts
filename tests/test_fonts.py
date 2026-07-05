# this_file: tests/test_fonts.py
"""Validity tests for the shipped font binaries.

The font files are the product. Before any release we prove that every
OTF and TTF master parses as a real OpenType font and carries a sane name
table. If one of these assertions fails, a font is corrupt or mislabelled
and must not ship.

Run locally:

    uv run --with fonttools --with pytest pytest tests/test_fonts.py

CI runs the same command (see .github/workflows/validate-fonts.yml).
"""

from __future__ import annotations

from pathlib import Path

import pytest
from fontTools.ttLib import TTFont

REPO_ROOT = Path(__file__).resolve().parent.parent
PACKAGES = REPO_ROOT / "packages"

# Required tables for any usable OpenType font.
REQUIRED_TABLES = ("name", "cmap", "head", "hhea", "maxp", "OS/2", "post")

# Name IDs we insist on: family, subfamily, full name, PostScript name.
REQUIRED_NAME_IDS = (1, 2, 4, 6)


def _discover_fonts() -> list[Path]:
    """Collect every OTF/TTF master under packages/*/fonts/complete/."""
    fonts: list[Path] = []
    for ext in ("otf", "ttf"):
        fonts.extend(sorted(PACKAGES.glob(f"*/fonts/complete/{ext}/*.{ext}")))
    return fonts


FONTS = _discover_fonts()


def test_fonts_were_discovered() -> None:
    """A green run over zero fonts would be a silent lie."""
    assert FONTS, f"No OTF/TTF masters found under {PACKAGES}"


@pytest.mark.parametrize("font_path", FONTS, ids=lambda p: str(p.relative_to(REPO_ROOT)))
def test_font_parses_and_name_table_is_sane(font_path: Path) -> None:
    rel = font_path.relative_to(REPO_ROOT)

    # Parses as a real font, lazily so we only pay for what we touch.
    font = TTFont(font_path, lazy=True)

    for table in REQUIRED_TABLES:
        assert table in font, f"{rel}: missing required table {table!r}"

    assert font["maxp"].numGlyphs > 0, f"{rel}: font has no glyphs"

    # Exactly one outline flavour: TrueType (glyf) or CFF (OTF).
    has_glyf = "glyf" in font
    has_cff = "CFF " in font or "CFF2" in font
    assert has_glyf ^ has_cff, f"{rel}: expected exactly one of glyf/CFF outlines"

    name = font["name"]
    for name_id in REQUIRED_NAME_IDS:
        record = name.getDebugName(name_id)
        assert record and record.strip(), f"{rel}: empty/missing name ID {name_id}"

    # The PostScript name (ID 6) must be a single token — no spaces allowed.
    postscript = name.getDebugName(6)
    assert " " not in postscript, f"{rel}: PostScript name {postscript!r} contains a space"

    font.close()
