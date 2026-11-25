"""Tests for scripts/check_findings.py. Each test builds a small throwaway repo in tmp_path."""
import datetime as dt
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import check_findings as cf  # noqa: E402

TODAY = dt.date(2026, 11, 25)

GOOD = """# Findings: fed-watchers
Last updated: 2026-11-25

## domestic/quantitative/2026-11-demo
Status: complete | Run: 2026-11-25 | Source: domestic/quantitative/2026-11-demo/RESULT.md
```yaml
- id: fw-2026-11-demo-h1
  study: domestic/quantitative/2026-11-demo
  type: quant
  region: US
  topic: fed-policy
  claim: "Markets price less tightening than one governor floated."
  verdict: killed
  confidence: "55%"
  numbers: ["40.9bp", "50bp"]
  source_file: domestic/quantitative/2026-11-demo/RESULT.md
  run_date: 2026-11-25
  valid_until: 2026-12-08
  owner_bot: vera
  links_to: [fw-2026-11-25-demo-note-camp]
  people: []
```

## domestic/qualitative/2026-11-25-demo-note.md
Status: complete | Run: 2026-11-25 | Source: domestic/qualitative/2026-11-25-demo-note.md
```yaml
- id: fw-2026-11-25-demo-note-camp
  study: domestic/qualitative/2026-11-25-demo-note.md
  type: qual
  region: US
  topic: fed-policy
  claim: "One camp argued the Fed has peaked."
  verdict: killed
  confidence: null
  numbers: ["41bp"]
  source_file: domestic/qualitative/2026-11-25-demo-note.md
  run_date: 2026-11-25
  valid_until: null
  owner_bot: vera
  links_to: [fw-2026-11-demo-h1]
  people: []
```
"""


def make_repo(tmp_path, findings=GOOD):
    s = tmp_path / "domestic" / "quantitative" / "2026-11-demo"
    s.mkdir(parents=True)
    (s / "RESULT.md").write_text("Cumulative priced: **40.9bp** vs 50bp floated.\n")
    q = tmp_path / "domestic" / "qualitative"
    q.mkdir(parents=True)
    (q / "_TEMPLATE.md").write_text("# template\n")
    (q / "2026-11-25-demo-note.md").write_text("Markets price 41bp of tightening.\n")
    (tmp_path / "FINDINGS.md").write_text(findings)
    return tmp_path


def run(root, today=TODAY):
    return cf.check(root, today)


def test_good_file_passes(tmp_path):
    errors, warnings = run(make_repo(tmp_path))
    assert errors == []
    assert warnings == []


def test_cli_exit_codes(tmp_path):
    root = make_repo(tmp_path)
    assert cf.main(["--root", str(root), "--today", "2026-11-25"]) == 0
    (root / "FINDINGS.md").write_text(GOOD.replace('"40.9bp"', '"41.0bp"'))
    assert cf.main(["--root", str(root), "--today", "2026-11-25"]) == 1


def test_missing_number_fails(tmp_path):
    errors, _ = run(make_repo(tmp_path, GOOD.replace('"40.9bp"', '"40.90bp"')))
    assert any("not found verbatim" in e and "40.90bp" in e for e in errors)


def test_rounded_number_fails(tmp_path):
    errors, _ = run(make_repo(tmp_path, GOOD.replace('"40.9bp"', '"41bp"')))
    assert any("'41bp' not found verbatim" in e for e in errors)


def test_duplicate_id_fails(tmp_path):
    bad = GOOD.replace("- id: fw-2026-11-25-demo-note-camp", "- id: fw-2026-11-demo-h1")
    errors, _ = run(make_repo(tmp_path, bad))
    assert any("duplicate id" in e for e in errors)


def test_missing_section_fails(tmp_path):
    root = make_repo(tmp_path)
    extra = root / "international" / "quantitative" / "2026-12-other"
    extra.mkdir(parents=True)
    (extra / "RESULT.md").write_text("result\n")
    errors, _ = run(root)
    assert any("no FINDINGS.md section for 'international/quantitative/2026-12-other'" in e for e in errors)


def test_missing_note_section_fails(tmp_path):
    root = make_repo(tmp_path)
    (root / "domestic" / "qualitative" / "2026-12-01-new-note.md").write_text("note\n")
    errors, _ = run(root)
    assert any("2026-12-01-new-note.md" in e for e in errors)


def test_template_is_not_required(tmp_path):
    errors, _ = run(make_repo(tmp_path))
    assert not any("_TEMPLATE" in e for e in errors)


def test_missing_field_fails(tmp_path):
    errors, _ = run(make_repo(tmp_path, GOOD.replace("  people: []\n", "", 1)))
    assert any("missing field(s) ['people']" in e for e in errors)


def test_invalid_enum_fails(tmp_path):
    errors, _ = run(make_repo(tmp_path, GOOD.replace("verdict: killed", "verdict: holds", 1)))
    assert any("verdict must be one of" in e for e in errors)


def test_bad_owner_fails(tmp_path):
    errors, _ = run(make_repo(tmp_path, GOOD.replace("owner_bot: vera", "owner_bot: otto", 1)))
    assert any("owner_bot" in e for e in errors)


def test_unparseable_yaml_fails(tmp_path):
    errors, _ = run(make_repo(tmp_path, GOOD.replace('numbers: ["40.9bp", "50bp"]', 'numbers: ["40.9bp", "50bp"')))
    assert any("yaml does not parse" in e for e in errors)


def test_duplicate_section_fails(tmp_path):
    first = GOOD.split("\n## domestic/qualitative")[0]
    dup = first.split("## domestic/quantitative/2026-11-demo")[1].replace("fw-2026-11-demo-h1", "fw-2026-11-demo-h1b")
    bad = GOOD + "\n## domestic/quantitative/2026-11-demo" + dup
    errors, _ = run(make_repo(tmp_path, bad))
    assert any("duplicate section" in e for e in errors)


def test_unknown_link_fails(tmp_path):
    errors, _ = run(make_repo(tmp_path, GOOD.replace("links_to: [fw-2026-11-demo-h1]", "links_to: [fw-nope]")))
    assert any("links_to 'fw-nope'" in e for e in errors)


def test_long_claim_fails(tmp_path):
    long_claim = " ".join(["word"] * 31)
    errors, _ = run(make_repo(tmp_path, GOOD.replace("One camp argued the Fed has peaked.", long_claim)))
    assert any("claim has 31 words" in e for e in errors)


def test_unquoted_number_fails(tmp_path):
    errors, _ = run(make_repo(tmp_path, GOOD.replace('numbers: ["41bp"]', "numbers: [41]")))
    assert any("numbers must be a list of quoted strings" in e for e in errors)


def test_stale_valid_until_warns_only(tmp_path):
    root = make_repo(tmp_path)
    errors, warnings = run(root, today=dt.date(2026, 12, 10))
    assert errors == []
    assert any("valid_until 2026-12-08 is in the past" in w for w in warnings)
    assert cf.main(["--root", str(root), "--today", "2026-12-10"]) == 0


def test_real_repo_findings_pass():
    errors, _ = cf.check(REPO, TODAY)
    assert errors == [], errors
