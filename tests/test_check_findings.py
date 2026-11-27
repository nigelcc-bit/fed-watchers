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
  hypothesis: "The October minutes mark the peak of the Fed's tough stance."
  verdict: killed
  finding: "Not the peak: markets price about 41bp of the 50bp floated."
  key_stats:
    - "about 41bp of a possible 50bp priced by January"
  confidence: "55%"
  numbers: ["40.9bp", "41bp", "50bp"]
  source_file: domestic/quantitative/2026-11-demo/RESULT.md
  run_date: 2026-11-25
  valid_until: 2026-12-08
  owner: fx-115
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
  hypothesis: "The Fed has reached peak toughness."
  verdict: killed
  finding: "Not the peak: markets still expect more tightening."
  key_stats:
    - "about 41bp of tightening still priced"
  confidence: null
  numbers: ["41bp"]
  source_file: domestic/qualitative/2026-11-25-demo-note.md
  run_date: 2026-11-25
  valid_until: null
  owner: fx-115
  links_to: [fw-2026-11-demo-h1]
  people: []
```
"""


def make_repo(tmp_path, findings=GOOD):
    s = tmp_path / "domestic" / "quantitative" / "2026-11-demo"
    s.mkdir(parents=True)
    (s / "RESULT.md").write_text("Cumulative priced: **40.9bp** (about 41bp) vs 50bp floated.\n")
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
    errors, _ = run(make_repo(tmp_path, GOOD.replace('"40.9bp", "41bp"', '"40.9bp", "40bp"')))
    assert any("'40bp' not found verbatim" in e for e in errors)


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
    errors, _ = run(make_repo(tmp_path, GOOD.replace("owner: fx-115", "owner: vera", 1)))
    assert any("owner must be a bot id" in e for e in errors)


def test_unparseable_yaml_fails(tmp_path):
    errors, _ = run(make_repo(tmp_path, GOOD.replace('numbers: ["40.9bp", "41bp", "50bp"]', 'numbers: ["40.9bp", "41bp", "50bp"')))
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


def test_long_hypothesis_fails(tmp_path):
    long_text = " ".join(["word"] * 31)
    errors, _ = run(make_repo(tmp_path, GOOD.replace("The Fed has reached peak toughness.", long_text)))
    assert any("hypothesis has 31 words" in e for e in errors)


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


# ---------- schema v2 rules: one failing case per new rule ----------

@pytest.mark.parametrize("field", ["hypothesis", "finding", "key_stats", "owner"])
def test_new_required_field_missing_fails(tmp_path, field):
    lines = GOOD.splitlines(keepends=True)
    out, skipping = [], False
    removed = False
    for ln in lines:
        if not removed and ln.startswith(f"  {field}:"):
            removed, skipping = True, field == "key_stats"
            continue
        if skipping and ln.startswith("    - "):
            continue
        skipping = False
        out.append(ln)
    errors, _ = run(make_repo(tmp_path, "".join(out)))
    assert any(f"missing field(s) ['{field}']" in e for e in errors)


def test_old_field_names_fail(tmp_path):
    bad = GOOD.replace("  hypothesis:", "  claim:", 1).replace("owner: fx-115", "owner_bot: fx-115", 1)
    errors, _ = run(make_repo(tmp_path, bad))
    assert any("missing field(s) ['hypothesis', 'owner']" in e for e in errors)
    assert any("unknown field(s) ['claim', 'owner_bot']" in e for e in errors)


@pytest.mark.parametrize("owner", ["Vera", "vera", "fx-1150", "fx-11", "zx-115", "fx_115"])
def test_owner_must_be_bot_id(tmp_path, owner):
    errors, _ = run(make_repo(tmp_path, GOOD.replace("owner: fx-115", f"owner: {owner}", 1)))
    assert any("owner must be a bot id" in e for e in errors)


def test_cx_owner_allowed(tmp_path):
    errors, _ = run(make_repo(tmp_path, GOOD.replace("owner: fx-115", "owner: cx-001", 1)))
    assert errors == []


def test_long_finding_fails(tmp_path):
    long_text = " ".join(["word"] * 31)
    errors, _ = run(make_repo(tmp_path, GOOD.replace("Not the peak: markets still expect more tightening.", long_text)))
    assert any("finding has 31 words" in e for e in errors)


def test_number_in_finding_missing_from_numbers_fails(tmp_path):
    bad = GOOD.replace("Not the peak: markets still expect more tightening.", "Not the peak: markets still expect 75bp more.")
    errors, _ = run(make_repo(tmp_path, bad))
    assert any("'75bp'" in e and "does not appear in numbers" in e for e in errors)


def test_number_in_key_stats_missing_from_numbers_fails(tmp_path):
    bad = GOOD.replace('"about 41bp of tightening still priced"', '"about 42bp of tightening still priced"')
    errors, _ = run(make_repo(tmp_path, bad))
    assert any("'42bp'" in e and "does not appear in numbers" in e for e in errors)


def test_numeric_match_is_by_token_not_substring(tmp_path):
    # "9" is a substring of "40.9bp" but not a token of it, so it must fail.
    bad = GOOD.replace("Not the peak: markets price about 41bp of the 50bp floated.",
                       "Not the peak: markets price about 41bp of the 50bp floated, 9 analysts said.")
    errors, _ = run(make_repo(tmp_path, bad))
    assert any("'9'" in e and "does not appear in numbers" in e for e in errors)


def test_sign_does_not_block_match(tmp_path):
    # numbers holds "+41bp" (verbatim from source); the finding says "41bp" without a sign.
    root = make_repo(tmp_path, GOOD.replace('numbers: ["41bp"]', 'numbers: ["+41bp"]'))
    (root / "domestic" / "qualitative" / "2026-11-25-demo-note.md").write_text("Markets price +41bp of tightening.\n")
    errors, _ = run(root)
    assert errors == []


def test_bare_number_key_stat_fails(tmp_path):
    bad = GOOD.replace('"about 41bp of tightening still priced"', '"41bp"')
    errors, _ = run(make_repo(tmp_path, bad))
    assert any("needs a plain-English label" in e for e in errors)


def test_too_many_key_stats_fails(tmp_path):
    extra = '    - "about 41bp of tightening still priced"\n' * 3
    bad = GOOD.replace('    - "about 41bp of tightening still priced"\n', '    - "about 41bp of tightening still priced"\n' + extra)
    errors, _ = run(make_repo(tmp_path, bad))
    assert any("key_stats must be a list of 1-3" in e for e in errors)


# ---------- moved sections (study moved to another repo) ----------
MOVED = "\n## quick-lookups/2026-11-27-gone\nMoved to https://github.com/nigelcc-bit/useless-data/tree/main/quick-lookups/2026-11-27-gone\n"


def test_moved_section_passes(tmp_path):
    errors, _ = run(make_repo(tmp_path, GOOD + MOVED))
    assert errors == []


def test_moved_section_with_extra_content_fails(tmp_path):
    bad = GOOD + MOVED + "Status: complete | Run: 2026-11-27 | Source: x/RESULT.md\n"
    errors, _ = run(make_repo(tmp_path, bad))
    assert any("a moved section must contain only" in e for e in errors)


def test_moved_pointer_must_be_github_url(tmp_path):
    bad = GOOD + "\n## quick-lookups/2026-11-27-gone\nMoved to somewhere else\n"
    errors, _ = run(make_repo(tmp_path, bad))
    assert any("path does not exist" in e for e in errors)


def test_moved_section_still_counts_for_coverage(tmp_path):
    root = make_repo(tmp_path, GOOD.replace("## domestic/quantitative/2026-11-demo\n",
                                            "## domestic/quantitative/2026-11-demo-old\n", 1) + MOVED)
    errors, _ = run(root)
    assert any("no FINDINGS.md section for 'domestic/quantitative/2026-11-demo'" in e for e in errors)
