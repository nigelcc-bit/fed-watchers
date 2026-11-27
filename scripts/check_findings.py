#!/usr/bin/env python3
"""Check FINDINGS.md against its schema and the files it cites.

Exit 1 on any error:
  - a section header, Status line or yaml block is malformed, or a yaml block does not parse
  - a finding is missing a field or has an invalid value (enums, dates, id format, owner id,
    hypothesis or finding over 30 words, key_stats not 1-3 labelled strings)
  - a numeric token in `finding` or `key_stats` does not appear among the tokens of `numbers`
  - an id is duplicated, or a section path appears twice (re-runs must replace, not append)
  - a string in `numbers` is not found verbatim in its `source_file`
  - a links_to id does not exist
  - a complete study or note has no section: any folder under domestic/ or international/
    containing a RESULT.md, or any non-template .md under */qualitative/
Warn (exit 0) when valid_until is in the past.

A section whose whole body is one line "Moved to https://github.com/<owner>/<repo>/..." marks a study that
moved to another repo: it is accepted without a yaml block or a local path, and still counts for coverage.

Usage: python3 scripts/check_findings.py [--root PATH] [--today YYYY-MM-DD]
"""
import argparse
import datetime as dt
import re
import sys
from pathlib import Path

import yaml

FIELDS = ["id", "study", "type", "region", "topic", "hypothesis", "verdict", "finding", "key_stats", "confidence",
          "numbers", "source_file", "run_date", "valid_until", "owner", "links_to", "people"]
TYPES = {"quant", "qual"}
VERDICTS = {"supported", "killed", "weak", "prior-only", "inconclusive", "interim"}
STATUSES = {"complete", "interim"}
OWNER_RE = re.compile(r"^(?:fx|cx)-\d{3}$")  # bot ids only, never names
MAX_WORDS = 30
MAX_KEY_STATS = 3
# A numeric token: digits with optional thousands commas, decimals and a unit suffix (%, bp, pp).
# Signs and trailing punctuation are not part of the token, so "+139bp" and "139bp" match.
NUM_RE = re.compile(r"\d+(?:,\d{3})*(?:\.\d+)?(?:%|bp|pp)?")
WORD_RE = re.compile(r"[A-Za-z]{2,}")
RESEARCH_ROOTS = ("domestic", "international")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
ID_RE = re.compile(r"^fw-[a-z0-9]+(?:-[a-z0-9]+)*$")
CONF_RE = re.compile(r"^\d{1,3}%$")
STATUS_RE = re.compile(r"^Status: (\S+) \| Run: (\S+) \| Source: (\S+)\s*$")
# A study moved to another repo: the section body is exactly one line pointing at its new home.
MOVED_RE = re.compile(r"^Moved to https://github\.com/[\w.-]+/[\w.-]+/\S+$")
BLOCK_RE = re.compile(r"```yaml\n(.*?)```", re.S)


def _date(v):
    """Accept a YAML date or a YYYY-MM-DD string; return a date or None."""
    if isinstance(v, dt.datetime):
        return v.date()
    if isinstance(v, dt.date):
        return v
    if isinstance(v, str) and DATE_RE.match(v):
        try:
            return dt.date.fromisoformat(v)
        except ValueError:
            return None
    return None


def required_sections(root):
    """Paths (relative, posix) of complete studies and notes that must have a FINDINGS section."""
    req = set()
    for top in RESEARCH_ROOTS:
        base = root / top
        if not base.is_dir():
            continue
        for res in base.rglob("RESULT.md"):
            req.add(res.parent.relative_to(root).as_posix())
    for note in root.glob("*/qualitative/**/*.md"):
        if note.name.startswith("_") or note.name.lower() == "readme.md":
            continue
        req.add(note.relative_to(root).as_posix())
    return req


def parse_sections(text):
    """Split on '## ' headings. Returns list of (path, body, line_no)."""
    out = []
    lines = text.splitlines(keepends=True)
    cur, body, start = None, [], 0
    for i, ln in enumerate(lines, 1):
        if ln.startswith("## "):
            if cur is not None:
                out.append((cur, "".join(body), start))
            cur, body, start = ln[3:].strip(), [], i
        elif cur is not None:
            body.append(ln)
    if cur is not None:
        out.append((cur, "".join(body), start))
    return out


def check(root, today=None):
    root = Path(root)
    today = today or dt.date.today()
    errors, warnings = [], []
    fpath = root / "FINDINGS.md"
    if not fpath.exists():
        return ["FINDINGS.md not found"], warnings
    text = fpath.read_text(encoding="utf-8")
    if not text.startswith("# Findings: fed-watchers"):
        errors.append("FINDINGS.md must start with '# Findings: fed-watchers'")
    m = re.search(r"^Last updated: (\S+)\s*$", text, re.M)
    if not m or not _date(m.group(1)):
        errors.append("missing or invalid 'Last updated: YYYY-MM-DD' line")

    sections = parse_sections(text)
    seen_sections, ids, findings = set(), {}, []
    for path, body, ln in sections:
        where = f"section '{path}' (line {ln})"
        if path in seen_sections:
            errors.append(f"{where}: duplicate section; a re-run must replace its section, not add another")
        seen_sections.add(path)
        lines = [l.strip() for l in body.splitlines() if l.strip()]
        if any(MOVED_RE.match(l) for l in lines):
            if len(lines) != 1:
                errors.append(f"{where}: a moved section must contain only the 'Moved to <GitHub URL>' line")
            continue  # findings live in the destination repo; no yaml or path checks here
        if not (root / path).exists():
            errors.append(f"{where}: path does not exist")
        first = next((l for l in body.splitlines() if l.strip()), "")
        sm = STATUS_RE.match(first)
        if not sm:
            errors.append(f"{where}: first line must be 'Status: complete|interim | Run: YYYY-MM-DD | Source: <path>'")
            sec_run = None
        else:
            status, run, src = sm.groups()
            if status not in STATUSES:
                errors.append(f"{where}: invalid status '{status}'")
            sec_run = _date(run)
            if not sec_run:
                errors.append(f"{where}: invalid Run date '{run}'")
            if not (root / src).is_file():
                errors.append(f"{where}: Source file '{src}' does not exist")
        blocks = BLOCK_RE.findall(body)
        if len(blocks) != 1:
            errors.append(f"{where}: expected exactly one ```yaml block, found {len(blocks)}")
            continue
        try:
            items = yaml.safe_load(blocks[0])
        except yaml.YAMLError as e:
            errors.append(f"{where}: yaml does not parse: {e}")
            continue
        if not isinstance(items, list) or not items:
            errors.append(f"{where}: yaml block must be a non-empty list of findings")
            continue
        for j, f in enumerate(items):
            fwhere = f"{where} finding #{j + 1}"
            if not isinstance(f, dict):
                errors.append(f"{fwhere}: not a mapping")
                continue
            fid = f.get("id")
            if isinstance(fid, str):
                fwhere = f"{where} '{fid}'"
            missing = [k for k in FIELDS if k not in f]
            extra = [k for k in f if k not in FIELDS]
            if missing:
                errors.append(f"{fwhere}: missing field(s) {missing} (use null where not applicable)")
            if extra:
                errors.append(f"{fwhere}: unknown field(s) {extra}")
            if missing:
                continue
            if not isinstance(fid, str) or not ID_RE.match(fid):
                errors.append(f"{fwhere}: id must match fw-<study-slug>-<short-key> (lowercase, digits, hyphens)")
            elif fid in ids:
                errors.append(f"{fwhere}: duplicate id (also in section '{ids[fid]}')")
            else:
                ids[fid] = path
            if f["study"] != path:
                errors.append(f"{fwhere}: study '{f['study']}' does not match its section '{path}'")
            if f["type"] not in TYPES:
                errors.append(f"{fwhere}: type must be one of {sorted(TYPES)}")
            if f["verdict"] not in VERDICTS:
                errors.append(f"{fwhere}: verdict must be one of {sorted(VERDICTS)}")
            for k in ("region", "topic", "hypothesis", "finding"):
                if not isinstance(f[k], str) or not f[k].strip():
                    errors.append(f"{fwhere}: {k} must be a non-empty string")
            for k in ("hypothesis", "finding"):
                if isinstance(f[k], str) and len(f[k].split()) > MAX_WORDS:
                    errors.append(f"{fwhere}: {k} has {len(f[k].split())} words (max {MAX_WORDS})")
            ks = f["key_stats"]
            if not isinstance(ks, list) or not all(isinstance(x, str) and x.strip() for x in ks) or not 1 <= len(ks) <= MAX_KEY_STATS:
                errors.append(f"{fwhere}: key_stats must be a list of 1-{MAX_KEY_STATS} non-empty strings")
                ks = [x for x in ks if isinstance(x, str)] if isinstance(ks, list) else []
            for x in ks:
                if len(WORD_RE.findall(x)) < 2:
                    errors.append(f"{fwhere}: key_stat '{x}' needs a plain-English label, not a bare number")
            if f["confidence"] is not None and not (isinstance(f["confidence"], str) and CONF_RE.match(f["confidence"])):
                errors.append(f"{fwhere}: confidence must be a quoted string like \"55%\" or null")
            if not isinstance(f["owner"], str) or not OWNER_RE.match(f["owner"]):
                errors.append(f"{fwhere}: owner must be a bot id like fx-115 or cx-001, never a name (got {f['owner']!r})")
            rd = _date(f["run_date"])
            if not rd:
                errors.append(f"{fwhere}: run_date must be YYYY-MM-DD")
            elif sec_run and rd != sec_run:
                errors.append(f"{fwhere}: run_date {rd} differs from section Run {sec_run}")
            vu = f["valid_until"]
            if vu is not None:
                vd = _date(vu)
                if not vd:
                    errors.append(f"{fwhere}: valid_until must be YYYY-MM-DD or null")
                elif vd < today:
                    warnings.append(f"{fwhere}: valid_until {vd} is in the past; re-run and replace this section")
            for k in ("links_to", "people"):
                if not isinstance(f[k], list) or not all(isinstance(x, str) for x in f[k]):
                    errors.append(f"{fwhere}: {k} must be a list of strings (use [] if none)")
            nums = f["numbers"]
            if not isinstance(nums, list) or not all(isinstance(x, str) for x in nums):
                errors.append(f"{fwhere}: numbers must be a list of quoted strings")
                nums = []
            num_tokens = {t for n in nums for t in NUM_RE.findall(n)}
            spoken = ([f["finding"]] if isinstance(f["finding"], str) else []) + ks
            for text_ in spoken:
                for t in NUM_RE.findall(text_):
                    if t not in num_tokens:
                        errors.append(f"{fwhere}: '{t}' in \"{text_}\" does not appear in numbers")
            sf = f["source_file"]
            if not isinstance(sf, str) or not (root / sf).is_file():
                errors.append(f"{fwhere}: source_file '{sf}' does not exist")
            else:
                src_text = (root / sf).read_text(encoding="utf-8")
                for n in nums:
                    if n not in src_text:
                        errors.append(f"{fwhere}: number '{n}' not found verbatim in {sf}")
            findings.append((fwhere, f))

    for fwhere, f in findings:
        if isinstance(f.get("links_to"), list):
            for link in f["links_to"]:
                if link not in ids:
                    errors.append(f"{fwhere}: links_to '{link}' is not a known id")

    for req in sorted(required_sections(root) - seen_sections):
        errors.append(f"no FINDINGS.md section for '{req}'")
    return errors, warnings


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", default=Path(__file__).resolve().parents[1])
    ap.add_argument("--today", type=dt.date.fromisoformat, default=None)
    a = ap.parse_args(argv)
    errors, warnings = check(a.root, a.today)
    for w in warnings:
        print(f"WARNING: {w}")
    for e in errors:
        print(f"ERROR: {e}")
    if errors:
        print(f"FAILED: {len(errors)} error(s), {len(warnings)} warning(s)")
        return 1
    print(f"OK: FINDINGS.md passes ({len(warnings)} warning(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main())
