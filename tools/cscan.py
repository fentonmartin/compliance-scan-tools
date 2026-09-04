#!/usr/bin/env python3
"""CSCAN Tools — evidence collector and report helper.

Stdlib-only (Python 3.8+). No third-party dependencies, so it runs on any
project checkout with Python and git. Every subcommand writes machine- and
human-readable output plus a *receipt* (what ran, where, when, on which
files) that can be pasted into Appendix B of the scan report.

Existence discipline: this tool never asserts absence from silence. A
"NOT FOUND" verdict is only valid with a receipt proving an exhaustive
search (patterns x file universe x exclusions). See
compliance/scan-methodology.md, "The existence protocol".

Subcommands:
  freeze      record evidence-freeze point (HEAD, branch, status, versions)
  inventory   Phase 1 file inventory (tracked/untracked, by ext/dir, large)
  search      pattern-library search with per-group receipts
  scaffold    fill templates/compliance-scan-report-template.md variables
  validate    pre-release checks on a completed report

Run `cscan <subcommand> --help` for options.
"""

import argparse
import datetime
import fnmatch
import json
import os
import re
import subprocess
import sys

VERSION = "1.2.0"
TEMPLATE_REL = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..",
    "templates",
    "compliance-scan-report-template.md",
)

# ---------------------------------------------------------------------------
# Pattern library (mirrors compliance/scan-methodology.md section 8).
# `.` is a regex dot on purpose: it matches `_`, `-`, `.`, etc.
# ---------------------------------------------------------------------------
PATTERN_GROUPS = {
    "secrets": r"password|secret|api_key|apikey|token|credential|passwd",
    "techdebt": r"TODO|FIXME|HACK|XXX|TEMP|WORKAROUND",
    "auth": r"auth|login|session|jwt|bearer|permission|role|policy",
    "dataprotection": r"encrypt|decrypt|hash|pseudonym|anonymize|redact|mask|crypto-shred",
    "datasubject": r"DSAR|data.subject|erasure|right.to.forget|consent|retention|breach|purge|legal.hold",
    "destructive": r"DELETE|DROP|TRUNCATE|CASCADE|soft.delete|hard.delete",
    "network": r"https?://|Access-Control|Content-Security-Policy|cors|csrf",
}

DEFAULT_FORBIDDEN_TOKENS = [
    # Prior-engagement leak-guard for THIS kit's own history. These are names
    # from the project this kit was extracted from; they must never appear in
    # kit files or in a finished report except inside quoted target evidence
    # or this documented list. Extend per organisation via --forbidden-file.
    "nds-by-nat",
    "fayolearn",
    "big-pickle",
]

MAX_MATCHES_PER_FILE = 500


def utcnow():
    return (
        datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    )


def run_git(root, *args):
    proc = subprocess.run(
        ["git", "-C", root] + list(args),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )
    return proc.returncode, proc.stdout.strip(), proc.stderr.strip()


def repo_root(target):
    code, out, err = run_git(target, "rev-parse", "--show-toplevel")
    if code != 0:
        raise SystemExit("error: '%s' is not inside a git repository (%s)" % (target, err))
    return os.path.normpath(out)


def tracked_files(root):
    code, out, _ = run_git(root, "ls-files", "-z")
    if code != 0 or not out:
        return []
    return [p for p in out.split("\x00") if p]


def untracked_files(root):
    code, out, _ = run_git(root, "ls-files", "--others", "--exclude-standard", "-z")
    if code != 0 or not out:
        return []
    return [p for p in out.split("\x00") if p]


def tool_version(cmd, version_args="--version"):
    try:
        proc = subprocess.run(
            [cmd, version_args],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            timeout=15,
        )
        line = (proc.stdout or "").strip().splitlines()
        return line[0] if line else "unknown"
    except (OSError, subprocess.SubprocessError):
        return None


def to_posix(path):
    return path.replace(os.sep, "/")


def excluded_match(rel_posix, patterns):
    return any(fnmatch.fnmatch(rel_posix, pat) for pat in patterns)


def ensure_out(path):
    if path and not os.path.isdir(path):
        os.makedirs(path, exist_ok=True)


# ---------------------------------------------------------------------------
# freeze
# ---------------------------------------------------------------------------
def cmd_freeze(args):
    root = repo_root(args.target)
    code, head, _ = run_git(root, "rev-parse", "HEAD")
    code_b, branch, _ = run_git(root, "branch", "--show-current")
    _, status, _ = run_git(root, "status", "--porcelain")
    data = {
        "tool": "cscan",
        "tool_version": VERSION,
        "repo_root": root,
        "branch": branch if code_b == 0 and branch else "(detached HEAD or unknown)",
        "head": head,
        "status_porcelain": status.splitlines() if status else [],
        "dirty": bool(status),
        "frozen_at_utc": utcnow(),
        "versions": {
            "git": tool_version("git"),
            "python": sys.version.split()[0],
            "rg": tool_version("rg"),
            "grep": tool_version("grep"),
        },
    }
    ensure_out(args.out)
    if args.out:
        with open(os.path.join(args.out, "freeze.json"), "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2)
        with open(os.path.join(args.out, "freeze.md"), "w", encoding="utf-8") as fh:
            fh.write(
                "# Evidence freeze\n\n"
                "- repo: `%s`\n- branch: `%s`\n- HEAD: `%s`\n"
                "- dirty tree: `%s`\n- frozen at (UTC): `%s`\n"
                % (data["repo_root"], data["branch"], data["head"],
                   data["dirty"], data["frozen_at_utc"])
            )
            if data["status_porcelain"]:
                fh.write("\n## git status --porcelain\n\n```\n")
                fh.write("\n".join(data["status_porcelain"]) + "\n```\n")
    print(json.dumps(data, indent=2))
    return 0


# ---------------------------------------------------------------------------
# inventory
# ---------------------------------------------------------------------------
def cmd_inventory(args):
    root = repo_root(args.target)
    tracked = tracked_files(root)
    untracked = untracked_files(root)
    by_ext = {}
    by_topdir = {}
    large = []
    total_lines = 0
    for rel in tracked:
        posix = to_posix(rel)
        ext = os.path.splitext(posix)[1].lower() or "(no extension)"
        by_ext[ext] = by_ext.get(ext, 0) + 1
        top = posix.split("/")[0] if "/" in posix else "[root]"
        entry = by_topdir.setdefault(top, {"files": 0, "lines": 0, "bytes": 0})
        entry["files"] += 1
        ap = os.path.join(root, rel)
        try:
            size = os.path.getsize(ap)
        except OSError:
            size = -1
        entry["bytes"] += max(size, 0)
        if size > args.large_bytes:
            large.append({"path": posix, "bytes": size})
        try:
            with open(ap, "r", encoding="utf-8", errors="replace") as fh:
                nlines = sum(1 for _ in fh)
        except OSError:
            nlines = -1
        if nlines >= 0:
            entry["lines"] += nlines
            total_lines += nlines
    large.sort(key=lambda d: d["bytes"], reverse=True)
    data = {
        "tool": "cscan",
        "tool_version": VERSION,
        "repo_root": root,
        "head": run_git(root, "rev-parse", "HEAD")[1],
        "scanned_at_utc": utcnow(),
        "total_tracked": len(tracked),
        "total_untracked": len(untracked),
        "total_lines_approx": total_lines,
        "by_extension": dict(sorted(by_ext.items(), key=lambda kv: kv[1], reverse=True)),
        "by_top_directory": by_topdir,
        "large_files_over_bytes": args.large_bytes,
        "large_files": large,
        "untracked": [to_posix(p) for p in untracked],
    }
    ensure_out(args.out)
    if args.out:
        with open(os.path.join(args.out, "tracked.txt"), "w", encoding="utf-8") as fh:
            fh.write("\n".join(sorted(to_posix(p) for p in tracked)) + ("\n" if tracked else ""))
        with open(os.path.join(args.out, "untracked.txt"), "w", encoding="utf-8") as fh:
            fh.write("\n".join(sorted(to_posix(p) for p in untracked)) + ("\n" if untracked else ""))
        with open(os.path.join(args.out, "inventory.json"), "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2)
    print(json.dumps(data, indent=2))
    return 0


# ---------------------------------------------------------------------------
# search
# ---------------------------------------------------------------------------
def python_engine_search(root, universe, pattern, excludes):
    """Search tracked files in pure Python. Returns (hits, skipped, unreadable)."""
    rx = re.compile(pattern, re.IGNORECASE)
    hits, skipped, unreadable = [], [], []
    for rel in universe:
        posix = to_posix(rel)
        if excluded_match(posix, excludes):
            skipped.append(posix)  # name only: never open excluded paths
            continue
        ap = os.path.join(root, rel)
        try:
            with open(ap, "rb") as fh:
                head = fh.read(8192)
                if b"\x00" in head:
                    unreadable.append(posix + " (binary)")
                    continue
                rest = fh.read()
            text = (head + rest).decode("utf-8", errors="replace")
        except OSError:
            unreadable.append(posix + " (unreadable)")
            continue
        count = 0
        for lineno, line in enumerate(text.splitlines(), 1):
            if rx.search(line):
                count += 1
                if count <= MAX_MATCHES_PER_FILE:
                    hits.append({"path": posix, "line": lineno, "text": line.rstrip()[:1000]})
        if count > MAX_MATCHES_PER_FILE:
            hits.append({"path": posix, "line": -1,
                         "text": "... truncated: %d matches, showing first %d ..."
                         % (count, MAX_MATCHES_PER_FILE)})
    return hits, skipped, unreadable


def external_engine_search(root, universe_set, pattern, excludes, engine):
    """rg/grep over the tree, then filter to the tracked universe + excludes."""
    if engine == "rg":
        cmd = ["rg", "-n", "--no-heading", "-I", "-i", "-e", pattern, "--", root]
    else:
        cmd = ["grep", "-rnI", "-i", "-E", "-e", pattern, "--", root]
    try:
        proc = subprocess.run(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            universal_newlines=True, errors="replace", timeout=600,
        )
    except FileNotFoundError:
        return None, "engine '%s' not installed" % engine
    raw_hits, filtered_out = [], 0
    for line in proc.stdout.splitlines():
        m = re.match(r"^(.*?):(\d+):(.*)$", line)
        if not m:
            continue
        apath, lineno, text = m.group(1), int(m.group(2)), m.group(3)
        try:
            rel = os.path.relpath(apath, root)
        except ValueError:
            filtered_out += 1
            continue
        posix = to_posix(rel)
        if posix not in universe_set or excluded_match(posix, excludes):
            filtered_out += 1
            continue
        raw_hits.append({"path": posix, "line": lineno, "text": text[:1000]})
    skipped = sorted(p for p in (to_posix(u) for u in universe_set)
                     if excluded_match(p, excludes))
    return {"hits": raw_hits, "filtered_out": filtered_out,
            "skipped_excluded": skipped, "command": " ".join(cmd)}, None


def cmd_search(args):
    root = repo_root(args.target)
    universe = tracked_files(root)
    universe_set = set(to_posix(p) for p in universe)
    groups = args.group or sorted(PATTERN_GROUPS)
    unknown = [g for g in groups if g not in PATTERN_GROUPS]
    if unknown:
        raise SystemExit("error: unknown pattern group(s): %s (choose from %s)"
                         % (", ".join(unknown), ", ".join(sorted(PATTERN_GROUPS))))
    engine = args.engine
    if engine == "auto":
        engine = "rg" if tool_version("rg") else ("grep" if tool_version("grep") else "python")
    ensure_out(args.out)
    receipts = []
    for group in groups:
        pattern = PATTERN_GROUPS[group]
        started = utcnow()
        receipt = {
            "group": group, "pattern": pattern, "engine": engine,
            "engine_version": tool_version(engine) if engine != "python"
            else ("python " + sys.version.split()[0]),
            "cwd": root, "started_utc": started,
            "case_sensitive": False,
            "file_universe": "git tracked files",
            "files_listed": len(universe),
        }
        if engine == "python":
            receipt["command"] = (
                "cscan search --engine python --group %s (universe: git ls-files, %d files)"
                % (group, len(universe))
            )
            hits, skipped, unreadable = python_engine_search(root, universe, pattern, args.exclude)
            receipt.update({
                "files_searched": len(universe) - len(skipped) - len(unreadable),
                "files_skipped_excluded": skipped,
                "files_unreadable_or_binary": unreadable,
                "matches": len([h for h in hits if h["line"] != -1]),
                "truncated": any(h["line"] == -1 for h in hits),
            })
        else:
            result, err = external_engine_search(root, universe_set, pattern, args.exclude, engine)
            if err:
                raise SystemExit("error: " + err)
            hits = result["hits"]
            receipt.update({
                "command": result["command"],
                "files_searched": len(universe_set) - len(result["skipped_excluded"]),
                "files_skipped_excluded": result["skipped_excluded"],
                "files_unreadable_or_binary": ["(handled by engine -I flag)"],
                "matches": len(hits),
                "traversal_filtered_to_tracked": result["filtered_out"],
                "truncated": False,
            })
        out_file = None
        if args.out:
            out_file = os.path.join(args.out, group + ".txt")
            with open(out_file, "w", encoding="utf-8") as fh:
                for h in hits:
                    fh.write("%s:%s:%s\n" % (h["path"], h["line"], h["text"]))
        receipt["output_file"] = out_file
        receipt["finished_utc"] = utcnow()
        receipts.append(receipt)
        print("%s: %d match(es) across %d searched file(s) [%s]"
              % (group, receipt["matches"], receipt["files_searched"], engine))
    if args.out:
        with open(os.path.join(args.out, "receipts.json"), "w", encoding="utf-8") as fh:
            json.dump(receipts, fh, indent=2)
        print("receipts written to %s" % os.path.join(args.out, "receipts.json"))
    return 0


# ---------------------------------------------------------------------------
# scaffold
# ---------------------------------------------------------------------------
def cmd_scaffold(args):
    template = args.template or TEMPLATE_REL
    if not os.path.isfile(template):
        raise SystemExit("error: template not found: %s" % template)
    with open(template, "r", encoding="utf-8") as fh:
        text = fh.read()
    values = {}
    for item in args.set:
        if "=" not in item:
            raise SystemExit("error: --set expects KEY=VALUE, got '%s'" % item)
        key, val = item.split("=", 1)
        values[key.strip()] = val
    if "SCAN_DATE" not in values:
        values["SCAN_DATE"] = datetime.datetime.now(
            datetime.timezone.utc).strftime("%Y-%m-%d")
    for key, val in values.items():
        text = text.replace("<%s>" % key, val)
    remaining = sorted(set(re.findall(r"<[A-Za-z][A-Za-z0-9 _/.\-]{1,60}>", text)))
    parent = os.path.dirname(os.path.abspath(args.out))
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as fh:
        fh.write(text)
    print("report scaffold written to %s" % args.out)
    if remaining:
        print("WARNING: %d unfilled placeholder(s) remain: %s"
              % (len(remaining), ", ".join(remaining)))
    return 0


# ---------------------------------------------------------------------------
# validate
# ---------------------------------------------------------------------------
DOC_CONTROL_FIELDS = [
    "Document ID", "Version", "Classification", "Author", "Reviewed by",
    "Approved by", "Scan date", "Commit (start)", "Commit (end)",
    "Repository", "Branch", "Scope", "Standards",
]

FINDING_REQUIRED_ROWS = ["Evidence location", "Commit", "Date discovered"]


def cmd_validate(args):
    if not os.path.isfile(args.report):
        raise SystemExit("error: report not found: %s" % args.report)
    with open(args.report, "r", encoding="utf-8") as fh:
        lines = fh.read().splitlines()
    failures, warnings = [], []

    # 1. Unfilled placeholders / sentinel values.
    allowed = set(args.allow or [])
    for i, line in enumerate(lines, 1):
        for token in re.findall(r"<[A-Za-z][A-Za-z0-9 _/.\\-]{1,60}>", line):
            if token.strip("<>") not in allowed:
                failures.append("line %d: unfilled placeholder %s" % (i, token))
        if "YYYY-MM-DD" in line:
            failures.append("line %d: sentinel date YYYY-MM-DD still present" % i)
        if "SCAN-YYMMDD-NN" in line:
            failures.append("line %d: sentinel document ID SCAN-YYMMDD-NN still present" % i)

    # 2. Document control completeness.
    joined = "\n".join(lines)
    for field in DOC_CONTROL_FIELDS:
        if not re.search(r"\|\s*%s\s*\|" % re.escape(field), joined):
            failures.append("document control: missing field '%s'" % field)

    # 3. Every FINDING block carries evidence + commit + date.
    finding_starts = [i for i, l in enumerate(lines)
                      if re.match(r"####\s+FINDING\s+", l)]
    if not finding_starts:
        warnings.append("no '#### FINDING' blocks found — a report with zero findings "
                        "must justify that in the Executive Summary")
    for idx, start in enumerate(finding_starts):
        end = finding_starts[idx + 1] if idx + 1 < len(finding_starts) else len(lines)
        block = "\n".join(lines[start:end])
        title = lines[start].strip()
        for row in FINDING_REQUIRED_ROWS:
            m = re.search(r"\|\s*%s\s*\|\s*(.*?)\s*\|" % re.escape(row), block)
            if not m or not m.group(1).strip() or m.group(1).strip().startswith("<"):
                failures.append("%s: row '%s' missing or unfilled" % (title, row))

    # 4. Prior-engagement leak-guard.
    forbidden = list(DEFAULT_FORBIDDEN_TOKENS)
    if args.forbidden_file:
        with open(args.forbidden_file, "r", encoding="utf-8") as fh:
            forbidden += [l.strip() for l in fh if l.strip() and not l.startswith("#")]
    for i, line in enumerate(lines, 1):
        low = line.lower()
        for token in forbidden:
            if token.lower() in low:
                failures.append("line %d: forbidden token '%s' (prior-engagement leakage?)"
                                % (i, token))

    print("validate: %d finding(s), %d failure(s), %d warning(s)"
          % (len(finding_starts), len(failures), len(warnings)))
    for w in warnings:
        print("  WARNING: " + w)
    for f in failures:
        print("  FAIL: " + f)
    return 1 if failures else 0


# ---------------------------------------------------------------------------
def build_parser():
    parser = argparse.ArgumentParser(
        prog="cscan",
        description="CSCAN Tools evidence collector and report helper.",
    )
    parser.add_argument("--version", action="version", version="CSCAN Tools " + VERSION)
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("freeze", help="record evidence-freeze point")
    p.add_argument("--target", default=".", help="target checkout (default: cwd)")
    p.add_argument("--out", default=None, help="evidence dir for freeze.json/md")
    p.set_defaults(func=cmd_freeze)

    p = sub.add_parser("inventory", help="Phase 1 file inventory")
    p.add_argument("--target", default=".", help="target checkout (default: cwd)")
    p.add_argument("--out", default=None, help="evidence dir for inventory files")
    p.add_argument("--large-bytes", type=int, default=100000,
                   help="large-file threshold in bytes (default: 100000)")
    p.set_defaults(func=cmd_inventory)

    p = sub.add_parser("search", help="pattern-library search with receipts")
    p.add_argument("--target", default=".", help="target checkout (default: cwd)")
    p.add_argument("--out", default=None, help="evidence dir for <group>.txt + receipts.json")
    p.add_argument("--group", action="append", default=None,
                   help="pattern group (repeatable; default: all). Choices: %s"
                   % ", ".join(sorted(PATTERN_GROUPS)))
    p.add_argument("--exclude", action="append", default=[],
                   help="fnmatch pattern (repo-relative) never opened; "
                        "listed by name only (repeatable)")
    p.add_argument("--engine", default="auto", choices=["auto", "python", "rg", "grep"],
                   help="search engine (default: auto -> rg -> grep -> python)")
    p.set_defaults(func=cmd_search)

    p = sub.add_parser("scaffold", help="fill report template variables")
    p.add_argument("--set", action="append", default=[],
                   help="KEY=VALUE filling <KEY> (repeatable)")
    p.add_argument("--template", default=None, help="template path override")
    p.add_argument("--out", required=True, help="report markdown to write")
    p.set_defaults(func=cmd_scaffold)

    p = sub.add_parser("validate", help="pre-release checks on a report")
    p.add_argument("--report", required=True, help="report markdown to check")
    p.add_argument("--forbidden-file", default=None,
                   help="extra forbidden tokens, one per line")
    p.add_argument("--allow", action="append", default=[],
                   help="placeholder name allowed to remain (repeatable)")
    p.set_defaults(func=cmd_validate)

    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
