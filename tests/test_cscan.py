"""Unit tests for tools/cscan.py (stdlib unittest, no third-party deps).

Run from the repo root:  python -m unittest discover -s tests -v
"""
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest

REPO_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
CSCAN = os.path.join(REPO_ROOT, "tools", "cscan.py")
TEMPLATE = os.path.join(REPO_ROOT, "templates", "compliance-scan-report-template.md")


def run_cscan(*args, cwd=None):
    proc = subprocess.run(
        [sys.executable, CSCAN] + list(args),
        cwd=cwd or REPO_ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        timeout=120,
    )
    return proc.returncode, proc.stdout


def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(content)


def read_json(path):
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def read_text(path):
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


class CscanTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.target = self.tmp.name
        subprocess.run(["git", "init", "-q"], cwd=self.target, check=True)
        subprocess.run(["git", "config", "user.email", "t@example.com"],
                       cwd=self.target, check=True)
        subprocess.run(["git", "config", "user.name", "t"], cwd=self.target, check=True)
        write(os.path.join(self.target, "app", "auth.py"),
              'API_TOKEN = "x"\n# TODO: rotate\ndef login(u, password):\n    return u\n')
        write(os.path.join(self.target, "app", "main.py"), 'print("ok")\n')
        write(os.path.join(self.target, "README.md"), "# fixture\n")
        write(os.path.join(self.target, "secrets", ".env"), "DB_PASSWORD=live-secret\n")
        # Evidence dir itself must not pollute the tracked universe.
        write(os.path.join(self.target, ".gitignore"), ".evidence/\n")
        subprocess.run(["git", "add", "-A"], cwd=self.target, check=True)
        subprocess.run(["git", "commit", "-qm", "fixture"], cwd=self.target, check=True)
        write(os.path.join(self.target, "notes.txt"), "untracked\n")
        self.evidence = os.path.join(self.target, ".evidence")

    def tearDown(self):
        self.tmp.cleanup()

    def test_freeze_records_head_and_dirty_tree(self):
        out = os.path.join(self.evidence, "00-freeze")
        code, _ = run_cscan("freeze", "--target", self.target, "--out", out)
        self.assertEqual(code, 0)
        data = read_json(os.path.join(out, "freeze.json"))
        head = subprocess.run(["git", "-C", self.target, "rev-parse", "HEAD"],
                              stdout=subprocess.PIPE, universal_newlines=True).stdout.strip()
        self.assertEqual(data["head"], head)
        self.assertTrue(data["dirty"])  # notes.txt is untracked
        self.assertIn("notes.txt", "\n".join(data["status_porcelain"]))

    def test_inventory_counts_reconcile_with_git(self):
        out = os.path.join(self.evidence, "01-inventory")
        code, _ = run_cscan("inventory", "--target", self.target, "--out", out)
        self.assertEqual(code, 0)
        data = read_json(os.path.join(out, "inventory.json"))
        # 4 fixture files + .gitignore = 5 tracked; notes.txt untracked.
        self.assertEqual(data["total_tracked"], 5)
        self.assertEqual(data["total_untracked"], 1)
        self.assertIn("app", data["by_top_directory"])

    def test_search_finds_secret_and_never_opens_excluded(self):
        out = os.path.join(self.evidence, "02-search")
        code, _ = run_cscan("search", "--target", self.target, "--out", out,
                            "--exclude", "secrets/*", "--engine", "python")
        self.assertEqual(code, 0)
        body = read_text(os.path.join(out, "secrets.txt"))
        self.assertIn("app/auth.py:1:", body)
        self.assertNotIn("live-secret", body)  # excluded file never opened
        receipts = read_json(os.path.join(out, "receipts.json"))
        sec = [r for r in receipts if r["group"] == "secrets"][0]
        self.assertEqual(sec["files_skipped_excluded"], ["secrets/.env"])
        self.assertGreater(sec["files_searched"], 0)

    def test_search_negative_result_has_receipt(self):
        out = os.path.join(self.evidence, "02-neg")
        code, _ = run_cscan("search", "--target", self.target, "--out", out,
                            "--group", "datasubject", "--engine", "python")
        self.assertEqual(code, 0)
        receipts = read_json(os.path.join(out, "receipts.json"))
        self.assertEqual(len(receipts), 1)
        self.assertEqual(receipts[0]["matches"], 0)
        self.assertIn("command", receipts[0])
        self.assertIn("started_utc", receipts[0])

    def test_scaffold_fills_and_warns_on_remainder(self):
        report = os.path.join(self.evidence, "SCAN-000000-01.md")
        code, out = run_cscan(
            "scaffold", "--out", report,
            "--set", "TARGET_REPO_URL=https://example.com/o/r.git",
            "--set", "TARGET_BRANCH=main",
            "--set", "SCAN_START_COMMIT=aaa", "--set", "SCAN_END_COMMIT=bbb",
            "--set", "SCOPE_DIRS=./app", "--set", "EXCLUDED_PATHS=secrets/.env",
            "--set", "STANDARDS=ISO 27001:2022", "--set", "SCAN_TYPE=Initial",
            "--set", "OPERATOR=t", "--set", "REVIEWER=r", "--set", "APPROVER=a",
            "--set", "CLASSIFICATION=Confidential",
            "--set", "DOCUMENT_ID=SCAN-000000-01", "--set", "EVIDENCE_DIR=.evidence")
        self.assertEqual(code, 0)
        self.assertIn("WARNING", out)  # finding/matrix rows still need a human
        body = read_text(report)
        self.assertNotIn("<TARGET_REPO_URL>", body)
        self.assertNotIn("<SCAN_START_COMMIT>", body)

    def test_validate_rejects_raw_template(self):
        code, out = run_cscan("validate", "--report", TEMPLATE)
        self.assertEqual(code, 1)
        self.assertIn("FAIL", out)

    def test_validate_accepts_completed_report(self):
        report = os.path.join(self.evidence, "done.md")
        write(report,
              "# R\n\n## Document Control\n\n"
              "| Field | Value |\n|---|---|\n"
              "| Document ID | SCAN-000000-01 |\n| Version | 1.0 |\n"
              "| Classification | Internal |\n| Author | t |\n"
              "| Reviewed by | r |\n| Approved by | a |\n"
              "| Scan date | 2026-09-04 |\n| Commit (start) | aaa |\n"
              "| Commit (end) | bbb |\n| Repository | https://example.com/o/r.git |\n"
              "| Branch | main |\n| Scope | ./app |\n| Standards | ISO 27001:2022 |\n\n"
              "## 3. Findings\n\n#### FINDING F-001: Hardcoded token\n\n"
              "| Field | Value |\n|---|---|\n"
              "| Rating | High |\n| Commitment reference | - |\n"
              "| Standard reference | ISO 27001 Annex A 8.4 |\n"
              "| Evidence location | app/auth.py:1 |\n| Commit | bbb |\n"
              "| Date discovered | 2026-09-04 |\n")
        code, out = run_cscan("validate", "--report", report)
        self.assertEqual(code, 0, out)
        self.assertIn("0 failure(s)", out)

    def test_validate_flags_forbidden_token(self):
        report = os.path.join(self.evidence, "leak.md")
        write(report, "# R\nScope: fayolearn backend\n")
        code, out = run_cscan("validate", "--report", report)
        self.assertEqual(code, 1)
        self.assertIn("forbidden token", out)


class KitHygieneTest(unittest.TestCase):
    """Guards on the kit itself (not on a target repo)."""

    def test_forbidden_token_list_is_canonical(self):
        # tools/cscan.py intentionally contains the prior-engagement token
        # list as a documented leak-guard. Pin its exact contents so any
        # change is deliberate and reviewed (CI leak-guard excludes it).
        spec = importlib.util.spec_from_file_location("cscan_mod", CSCAN)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        self.assertEqual(set(mod.DEFAULT_FORBIDDEN_TOKENS),
                         {"nds-by-nat", "fayolearn", "big-pickle"})


if __name__ == "__main__":
    unittest.main()
