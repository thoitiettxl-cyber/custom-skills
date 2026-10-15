#!/usr/bin/env python3
"""Self-test for the linkage-checks skill scaffold and templates.

stdlib unittest, no deps. Run: python3 tests/test_scaffold.py
Every script is invoked via `bash <path>`; nothing relies on exec bits.
"""
import os
import re
import shutil
import stat
import subprocess
import tempfile
import unittest

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCAFFOLD = os.path.join(SKILL_DIR, "bin", "new-linkage-check")
TEMPLATE = os.path.join(SKILL_DIR, "assets", "check-template.sh")

TOY_CONFIG = {
    'THINGS = "FILL:things"': 'THINGS = "widgets"',
    'WHERE = "FILL:where"': 'WHERE = "a USE reference"',
    'MARKER = "FILL:NO_X"': 'MARKER = "NO_USE"',
    'DIRECTION = "FILL:a2b|b2a|both"': 'DIRECTION = "both"',
    'A_DEF_RE = r"FILL:"': r'A_DEF_RE = r"^DEFINE:\s*([a-z0-9_]+)\s*$"',
    'B_GLOBS = ("FILL:*.ext",)': 'B_GLOBS = ("*.txt",)',
    'B_REF_RE = r"FILL:"': r'B_REF_RE = r"USE:\s*([a-z0-9_]+)"',
    '$REPO_ROOT/FILL:path/to/definitions': '$REPO_ROOT/defs.txt',
    '$REPO_ROOT/FILL:path/to/usages': '$REPO_ROOT/use',
}


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def bash(*args, **kw):
    return run(["bash", *args], **kw)


def fill_toy(text, overrides=None):
    """Fill the template for a toy pair: `DEFINE: <name>` lines in defs.txt
    must appear as `USE: <name>` in *.txt under use/ (and vice versa).
    Hatch: `# NO_USE: <reason>` in the comment block attached above."""
    cfg = dict(TOY_CONFIG, **(overrides or {}))
    for k, v in cfg.items():
        assert k in text, k
        text = text.replace(k, v)
    # Header/comment FILL markers: the filler documents and removes them.
    out = []
    for line in text.splitlines(keepends=True):
        if line.lstrip().startswith("#") and "FIL[L]" not in line:
            line = line.replace("FILL:", "filled:")
        out.append(line)
    text = "".join(out)
    assert "FILL:" not in text, [l for l in text.splitlines() if "FILL:" in l]
    return text


def make_toy_check(repo, overrides=None, path=None):
    with open(TEMPLATE, encoding="utf-8") as f:
        filled = fill_toy(f.read(), overrides)
    path = path or os.path.join(repo, "scripts", "checks", "toy.sh")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(filled)
    return path


def write_fixture(base, defs_text, uses):
    os.makedirs(os.path.join(base, "use"), exist_ok=True)
    with open(os.path.join(base, "defs.txt"), "w", encoding="utf-8") as f:
        f.write(defs_text)
    for i, u in enumerate(uses):
        with open(os.path.join(base, "use", "f%d.txt" % i), "w",
                  encoding="utf-8") as f:
            f.write(u)


def write(path, text):
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


class TempRepo(unittest.TestCase):
    def setUp(self):
        self.repo = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.repo, ignore_errors=True)

    def assertMisconfig(self, r):
        self.assertEqual(r.returncode, 2, r.stdout + r.stderr)
        self.assertNotIn("Traceback", r.stdout + r.stderr)
        self.assertNotIn("FAIL:", r.stdout)
        self.assertIn("error:", r.stderr)


class ScaffoldTest(TempRepo):
    def test_scaffold_creates_script_runner_and_fixtures(self):
        r = bash(SCAFFOLD, "demo-check", "--repo", self.repo)
        self.assertEqual(r.returncode, 0, r.stderr)
        script = os.path.join(self.repo, "scripts", "checks", "demo-check.sh")
        fix = os.path.join(self.repo, "scripts", "checks", "tests",
                           "fixtures", "demo-check")
        with open(script, encoding="utf-8") as f:
            body = f.read()
        self.assertIn("FILL:", body)  # still needs filling
        self.assertIn("set -euo pipefail", body)
        self.assertTrue(os.path.isfile(os.path.join(fix, "run-fixtures.sh")))
        for fx in ("pass", "fail", "exempt"):
            self.assertTrue(os.path.isfile(os.path.join(fix, fx, "fixture.env")))
            self.assertTrue(os.path.isfile(os.path.join(fix, fx, "README.md")))
        self.assertTrue(os.path.isfile(os.path.join(fix, "fail", "EXPECT_OFFENDER")))
        self.assertTrue(os.path.isfile(os.path.join(fix, "exempt", "EXPECT_EXEMPT")))
        self.assertIn("native validation", r.stdout)

    def test_scaffold_rejects_bad_name(self):
        r = bash(SCAFFOLD, "Bad_Name", "--repo", self.repo)
        self.assertEqual(r.returncode, 2)

    def test_scaffold_refuses_overwrite(self):
        self.assertEqual(bash(SCAFFOLD, "x", "--repo", self.repo).returncode, 0)
        r = bash(SCAFFOLD, "x", "--repo", self.repo)
        self.assertEqual(r.returncode, 2)
        self.assertIn("already exists", r.stderr)

    def test_repo_flag_without_value_is_usage(self):
        for args in (["x", "--repo"], ["--repo"], ["x", "--repo", ""]):
            r = bash(SCAFFOLD, *args, cwd=self.repo)
            self.assertEqual(r.returncode, 2, args)
            self.assertIn("usage:", r.stderr, args)

    def test_unknown_flag_and_missing_repo_exit_2(self):
        self.assertEqual(bash(SCAFFOLD, "x", "--bogus").returncode, 2)
        r = bash(SCAFFOLD, "x", "--repo", os.path.join(self.repo, "nope"))
        self.assertEqual(r.returncode, 2)

    def test_unfilled_check_exits_2_without_traceback(self):
        bash(SCAFFOLD, "raw", "--repo", self.repo)
        script = os.path.join(self.repo, "scripts", "checks", "raw.sh")
        write(os.path.join(self.repo, "a.txt"), "x\n")
        # Even with valid inputs (CI-like env), an unfilled template is misconfig.
        env = dict(os.environ, A_FILE=os.path.join(self.repo, "a.txt"),
                   B_DIR=self.repo)
        for e in (env, dict(os.environ)):
            r = bash(script, env=e)
            self.assertMisconfig(r)
            self.assertIn("unfilled template", r.stderr)

    def test_unfilled_runner_exits_2(self):
        bash(SCAFFOLD, "raw", "--repo", self.repo)
        runner = os.path.join(self.repo, "scripts", "checks", "tests",
                              "fixtures", "raw", "run-fixtures.sh")
        r = bash(runner)
        self.assertEqual(r.returncode, 2, r.stdout + r.stderr)
        self.assertIn("unfilled", r.stderr)


class TemplateBehaviorTest(TempRepo):
    def setUp(self):
        super().setUp()
        self.script = make_toy_check(self.repo)
        self.fx = os.path.join(self.repo, "fx")
        os.makedirs(self.fx)

    def run_check(self, name, *args, **envx):
        base = os.path.join(self.fx, name)
        env = dict(os.environ, A_FILE=os.path.join(base, "defs.txt"),
                   B_DIR=os.path.join(base, "use"), **envx)
        env.pop("LINKAGE_DIRECTION", None) if "LINKAGE_DIRECTION" not in envx else None
        return bash(self.script, *args, env=env)

    def fixture(self, name, defs, uses):
        write_fixture(os.path.join(self.fx, name), defs, uses)
        return name

    # --- core pass / fail / exempt
    def test_pass(self):
        r = self.run_check(self.fixture("p", "DEFINE: alpha\nDEFINE: beta\n",
                                        ["USE: alpha\n", "USE: beta\n"]))
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("PASS:", r.stdout)

    def test_fail_names_offender(self):
        r = self.run_check(self.fixture("f", "DEFINE: alpha\nDEFINE: gamma\n",
                                        ["USE: alpha\n"]))
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        self.assertIn("FAIL:", r.stdout)
        self.assertIn("- gamma", r.stdout)
        self.assertNotIn("- alpha", r.stdout)

    def test_exempt(self):
        r = self.run_check(self.fixture(
            "e", "DEFINE: alpha\n# NO_USE: internal only\nDEFINE: beta\n",
            ["USE: alpha\n"]))
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("exempt: beta (internal only)", r.stdout)

    # --- escape-hatch scope
    def test_marker_wrong_scope_does_not_exempt(self):
        r = self.run_check(self.fixture(
            "s", "DEFINE: alpha\n# NO_USE: internal only\n\nDEFINE: beta\n",
            ["USE: alpha\n"]))
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("- beta", r.stdout)

    def test_marker_in_multiline_attached_block_exempts(self):
        defs = ("DEFINE: alpha\n"
                "# Beta is wired by the plugin loader.\n"
                "# NO_USE: loaded reflectively\n"
                "# (see loader docs)\n"
                "DEFINE: beta\n")
        r = self.run_check(self.fixture("m", defs, ["USE: alpha\n"]))
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("exempt: beta (loaded reflectively)", r.stdout)

    def test_multiline_block_broken_by_blank_line_does_not_exempt(self):
        defs = ("# NO_USE: loaded reflectively\n"
                "# more words\n"
                "\n"
                "# unrelated comment\n"
                "DEFINE: beta\n")
        r = self.run_check(self.fixture("mb", defs, []))
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        self.assertIn("- beta", r.stdout)

    def test_block_of_previous_definition_does_not_leak(self):
        defs = ("# header\n# NO_USE: only alpha\nDEFINE: alpha\nDEFINE: beta\n")
        r = self.run_check(self.fixture("leak", defs, []))
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        self.assertIn("- beta", r.stdout)
        self.assertNotIn("- alpha", r.stdout)

    def test_marker_without_reason_is_misconfig(self):
        r = self.run_check(self.fixture("nr", "# NO_USE:\nDEFINE: beta\n", []))
        self.assertMisconfig(r)
        self.assertIn("without a reason", r.stderr)

    # --- exit-code contract: misconfig is 2, never 1
    def test_empty_definitions_is_misconfiguration(self):
        self.assertMisconfig(self.run_check(self.fixture("empty", "nothing\n", ["x\n"])))

    def test_missing_file_a_exits_2(self):
        self.fixture("ma", "DEFINE: a\n", ["USE: a\n"])
        os.remove(os.path.join(self.fx, "ma", "defs.txt"))
        r = self.run_check("ma")
        self.assertMisconfig(r)
        self.assertIn("A_FILE", r.stderr)

    def test_missing_b_dir_exits_2(self):
        self.fixture("mbd", "DEFINE: a\n", [])
        shutil.rmtree(os.path.join(self.fx, "mbd", "use"))
        r = self.run_check("mbd")
        self.assertMisconfig(r)
        self.assertIn("B_DIR", r.stderr)

    def test_missing_env_vars_exit_2(self):
        # No overrides and the REPO_ROOT defaults don't exist in this repo.
        env = {k: v for k, v in os.environ.items() if k not in ("A_FILE", "B_DIR")}
        r = bash(self.script, env=env)
        self.assertMisconfig(r)
        env["A_FILE"] = ""  # empty counts as unset
        self.assertMisconfig(bash(self.script, env=env))

    def test_internal_error_exits_2_traceback_only_with_debug(self):
        bad = make_toy_check(self.repo, {'A_DEF_RE = r"FILL:"': 'A_DEF_RE = r"("'},
                             path=os.path.join(self.repo, "scripts", "checks", "bad.sh"))
        self.fixture("ie", "DEFINE: a\n", ["USE: a\n"])
        base = os.path.join(self.fx, "ie")
        env = dict(os.environ, A_FILE=os.path.join(base, "defs.txt"),
                   B_DIR=os.path.join(base, "use"))
        self.assertMisconfig(bash(bad, env=env))
        r = bash(bad, env=dict(env, LINKAGE_DEBUG="1"))
        self.assertEqual(r.returncode, 2)
        self.assertIn("Traceback", r.stderr)

    def test_python_syntax_error_exits_2(self):
        with open(self.script, encoding="utf-8") as f:
            body = f.read().replace("def strip_comments(text):", "def strip_comments(text) oops:")
        bad = os.path.join(self.repo, "scripts", "checks", "syn.sh")
        write(bad, body)
        self.fixture("se", "DEFINE: a\n", ["USE: a\n"])
        base = os.path.join(self.fx, "se")
        env = dict(os.environ, A_FILE=os.path.join(base, "defs.txt"),
                   B_DIR=os.path.join(base, "use"))
        self.assertMisconfig(bash(bad, env=env))

    def test_bad_flags_exit_2(self):
        self.fixture("bf", "DEFINE: a\n", ["USE: a\n"])
        for args in (["--bogus"], ["--direction"], ["--direction", "sideways"]):
            r = self.run_check("bf", *args)
            self.assertEqual(r.returncode, 2, args)
            self.assertNotIn("Traceback", r.stderr)
        self.assertEqual(self.run_check("bf", LINKAGE_DIRECTION="up").returncode, 2)

    # --- directions
    def test_b2a_dangling_reference(self):
        self.fixture("d", "DEFINE: alpha\n", ["USE: alpha\nUSE: ghost\n"])
        r = self.run_check("d")  # default both
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("undefined widgets", r.stdout)
        self.assertIn("- ghost (f0.txt:2)", r.stdout)
        self.assertEqual(self.run_check("d", "--direction", "b2a").returncode, 1)
        r = self.run_check("d", "--direction", "a2b")
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertEqual(self.run_check("d", LINKAGE_DIRECTION="a2b").returncode, 0)

    def test_b2a_mode_ignores_unreferenced_definition(self):
        self.fixture("d2", "DEFINE: alpha\nDEFINE: lonely\n", ["USE: alpha\n"])
        self.assertEqual(self.run_check("d2", "--direction", "b2a").returncode, 0)
        self.assertEqual(self.run_check("d2", "--direction", "a2b").returncode, 1)

    # --- comment stripping at B (documented behavior)
    def test_reference_only_in_comment_does_not_count(self):
        self.fixture("c", "DEFINE: alpha\nDEFINE: beta\n",
                     ["USE: alpha\n# USE: beta  (commented-out code)\n"])
        r = self.run_check("c")
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("- beta", r.stdout)

    def test_trailing_comment_stripped_and_dangling_in_comment_ignored(self):
        self.fixture("c2", "DEFINE: alpha\n",
                     ["USE: alpha  # USE: ghost\n#USE: ghost2\n"])
        r = self.run_check("c2")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_block_comments_when_configured(self):
        blk = make_toy_check(self.repo, {
            'B_BLOCK_COMMENT = None': r'B_BLOCK_COMMENT = (r"/\*", r"\*/")'},
            path=os.path.join(self.repo, "scripts", "checks", "blk.sh"))
        self.fixture("bc", "DEFINE: alpha\nDEFINE: beta\n",
                     ["USE: alpha\n/* USE: beta\n   still comment */\nUSE: zed_not\n"])
        base = os.path.join(self.fx, "bc")
        env = dict(os.environ, A_FILE=os.path.join(base, "defs.txt"),
                   B_DIR=os.path.join(base, "use"))
        r = bash(blk, env=env)
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        self.assertIn("- beta", r.stdout)
        self.assertIn("- zed_not (f0.txt:4)", r.stdout)  # line numbers preserved


class GeneratedRunnerTest(TempRepo):
    """Scaffold a real check into a temp repo, fill it, run run-fixtures.sh."""

    def setUp(self):
        super().setUp()
        r = bash(SCAFFOLD, "toy-pair", "--repo", self.repo)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.script = os.path.join(self.repo, "scripts", "checks", "toy-pair.sh")
        with open(self.script, encoding="utf-8") as f:
            write(self.script, fill_toy(f.read()))
        self.fix = os.path.join(self.repo, "scripts", "checks", "tests",
                                "fixtures", "toy-pair")
        self.runner = os.path.join(self.fix, "run-fixtures.sh")
        envtxt = "A_FILE={fixture}/defs.txt\nB_DIR={fixture}/use\n"
        write_fixture(os.path.join(self.fix, "pass"),
                      "DEFINE: alpha\nDEFINE: beta\n", ["USE: alpha\nUSE: beta\n"])
        write_fixture(os.path.join(self.fix, "fail"),
                      "DEFINE: alpha\nDEFINE: gamma\n", ["USE: alpha\n"])
        write_fixture(os.path.join(self.fix, "exempt"),
                      "DEFINE: alpha\n# NO_USE: reflective\nDEFINE: beta\n",
                      ["USE: alpha\n"])
        for fx in ("pass", "fail", "exempt"):
            write(os.path.join(self.fix, fx, "fixture.env"), envtxt)
        write(os.path.join(self.fix, "fail", "EXPECT_OFFENDER"), "gamma\n")
        write(os.path.join(self.fix, "exempt", "EXPECT_EXEMPT"), "beta\n")

    def test_green(self):
        r = bash(self.runner)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("PASS: 3 fixtures for toy-pair", r.stdout)
        # Real repo defaults also work (REPO_ROOT resolution): runs from anywhere.
        write(os.path.join(self.repo, "defs.txt"), "DEFINE: a\n")
        os.makedirs(os.path.join(self.repo, "use"))
        write(os.path.join(self.repo, "use", "x.txt"), "USE: a\n")
        r = bash(self.script, cwd="/")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_broken_fail_fixture_goes_red(self):
        # Offender accidentally referenced: check passes, fixture must not.
        write(os.path.join(self.fix, "fail", "use", "f1.txt"), "USE: gamma\n")
        r = bash(self.runner)
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        self.assertIn("NOT OK fail", r.stdout)

    def test_wrong_expected_offender_goes_red(self):
        write(os.path.join(self.fix, "fail", "EXPECT_OFFENDER"), "delta\n")
        r = bash(self.runner)
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        self.assertIn("offender 'delta' not named", r.stdout)

    def test_broken_exempt_fixture_goes_red(self):
        write(os.path.join(self.fix, "exempt", "defs.txt"),
              "DEFINE: alpha\n# NO_USE: reflective\n\nDEFINE: beta\n")
        r = bash(self.runner)
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        self.assertIn("NOT OK exempt", r.stdout)

    def test_broken_pass_fixture_goes_red(self):
        write(os.path.join(self.fix, "pass", "defs.txt"), "DEFINE: alpha\nDEFINE: nope\n")
        r = bash(self.runner)
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        self.assertIn("NOT OK pass", r.stdout)

    def test_unfilled_expectation_is_misconfig(self):
        write(os.path.join(self.fix, "fail", "EXPECT_OFFENDER"), "FILL:x\n")
        self.assertEqual(bash(self.runner).returncode, 2)
        os.remove(os.path.join(self.fix, "exempt", "EXPECT_EXEMPT"))
        write(os.path.join(self.fix, "fail", "EXPECT_OFFENDER"), "gamma\n")
        self.assertEqual(bash(self.runner).returncode, 2)


class NoExecBitTest(unittest.TestCase):
    def test_skill_works_without_exec_bits(self):
        tmp = tempfile.mkdtemp()
        try:
            skill = os.path.join(tmp, "skill")
            shutil.copytree(SKILL_DIR, skill)
            for root, _, files in os.walk(skill):
                for fn in files:
                    p = os.path.join(root, fn)
                    os.chmod(p, os.stat(p).st_mode & ~(stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH))
            repo = os.path.join(tmp, "repo")
            os.makedirs(repo)
            r = bash(os.path.join(skill, "bin", "new-linkage-check"), "nx", "--repo", repo)
            self.assertEqual(r.returncode, 0, r.stderr)
            for root, _, files in os.walk(repo):
                for fn in files:
                    p = os.path.join(root, fn)
                    os.chmod(p, os.stat(p).st_mode & ~(stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH))
            runner = os.path.join(repo, "scripts", "checks", "tests", "fixtures", "nx", "run-fixtures.sh")
            r = bash(runner)  # unfilled, but must reach the contract (2), not EACCES
            self.assertEqual(r.returncode, 2, r.stderr)
            self.assertNotIn("Permission denied", r.stderr)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    unittest.main(verbosity=2)
