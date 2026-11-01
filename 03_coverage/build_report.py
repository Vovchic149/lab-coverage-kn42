import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).parent
ENV = dict(os.environ, PYTHONUTF8="1", PYTHONIOENCODING="utf-8", NO_COLOR="1")

STEPS = {
    "VERSION": [["coverage", "--version"]],
    "UNITTEST": [
        ["coverage", "erase"],
        ["coverage", "run", "-m", "unittest", "discover"],
        ["coverage", "report", "-m"],
    ],
    "PYTEST": [
        ["coverage", "erase"],
        ["coverage", "run", "-m", "pytest"],
        ["coverage", "report", "-m"],
    ],
    "PYTESTCOV": [
        ["pytest", "--cov=app", "--cov-branch", "--cov-report=term-missing", "-v"],
    ],
    "BEFORE": [
        ["coverage", "erase"],
        ["coverage", "run", "-m", "pytest", "before_examples/test_triangle_only.py"],
        ["coverage", "report", "-m"],
    ],
    "FAIL_BEFORE": [
        [
            "pytest",
            "before_examples/test_triangle_only.py",
            "--cov=app",
            "--cov-branch",
            "--cov-fail-under=90",
            "-q",
        ],
    ],
    "FAIL_AFTER": [
        ["pytest", "--cov=app", "--cov-branch", "--cov-fail-under=90", "-q"],
    ],
    "NOPRAGMA": [
        ["coverage", "erase"],
        ["coverage", "run", "-m", "pytest"],
        ["coverage", "report", "-m", "--rcfile=coveragerc_no_pragma"],
    ],
    "NOASSERT": [
        ["coverage", "erase"],
        ["coverage", "run", "-m", "pytest", "before_examples/test_no_assert.py"],
        ["coverage", "report", "-m"],
    ],
    "HTML": [
        ["coverage", "erase"],
        ["coverage", "run", "-m", "pytest"],
        ["coverage", "html"],
    ],
    "XML": [["coverage", "xml"]],
}


def run(args, cwd):
    result = subprocess.run(
        [sys.executable, "-m", *args],
        cwd=cwd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=ENV,
    )
    return (result.stdout + result.stderr).strip()


def run_steps(steps, cwd=ROOT):
    parts = []
    for args in steps:
        parts.append("> py -m " + " ".join(args))
        output = run(args, cwd)
        if output:
            parts.append(output)
    return "\n".join(parts)


def bug_demo():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = pathlib.Path(tmp)
        source = (ROOT / "app.py").read_text(encoding="utf-8")
        (tmp / "app.py").write_text(source.replace("return 3", "return 30"), encoding="utf-8")
        shutil.copy(ROOT / ".coveragerc", tmp / ".coveragerc")
        shutil.copy(ROOT / "before_examples" / "test_no_assert.py", tmp / "test_no_assert.py")
        shutil.copy(ROOT / "test_app.py", tmp / "test_app.py")
        without_assert = run_steps(
            [
                ["coverage", "erase"],
                ["coverage", "run", "-m", "pytest", "test_no_assert.py"],
                ["coverage", "report", "-m"],
            ],
            tmp,
        )
        with_assert = run_steps([["pytest", "test_app.py", "--tb=short", "-q"]], tmp)
    return without_assert, with_assert


def total(output):
    found = re.findall(r"TOTAL\s+\d+\s+\d+\s+\d+\s+\d+\s+(\d+)%", output)
    return f"{found[-1]}%" if found else "н/д"


def main():
    try:
        import coverage
        import pytest
        import pytest_cov
    except ImportError:
        print("Не вистачає пакетів. Виконайте: py -m pip install coverage pytest pytest-cov")
        sys.exit(1)

    outputs = {name: run_steps(steps) for name, steps in STEPS.items()}
    xml_path = ROOT / "coverage.xml"
    xml_head = ""
    if xml_path.exists():
        xml_head = "\n".join(xml_path.read_text(encoding="utf-8").splitlines()[:12])
    outputs["XMLHEAD"] = xml_head
    outputs["BUG_NOASSERT"], outputs["BUG_ASSERT"] = bug_demo()

    passed = re.search(r"(\d+) passed", outputs["PYTEST"])
    if passed and " failed" not in outputs["PYTEST"]:
        status = f"Усі {passed.group(1)} тестів проходять."
    else:
        status = "Не всі тести пройшли, див. вивід запусків вище."
        print("Увага: запуск тестів завершився не повністю успішно. Перевірте вивід.")

    text = (ROOT / "README.template.md").read_text(encoding="utf-8")
    text = re.sub(r"\{\{CMD:(\w+)\}\}", lambda m: outputs[m.group(1)], text)
    text = re.sub(
        r"\{\{FILE:([^}]+)\}\}",
        lambda m: (ROOT / m.group(1)).read_text(encoding="utf-8").rstrip("\n"),
        text,
    )
    text = re.sub(r"\{\{TOTAL:(\w+)\}\}", lambda m: total(outputs[m.group(1)]), text)

    def image(match):
        path, alt = match.group(1).split("|")
        if (ROOT / path).exists():
            return f"![{alt}]({path})\n\n"
        return ""

    text = re.sub(r"\{\{IMG:([^}]+)\}\}\n?", image, text)
    text = text.replace("{{STATUS}}", status)
    text = re.sub(r"\n{3,}", "\n\n", text)
    (ROOT / "README.md").write_text(text, encoding="utf-8", newline="\n")
    print("README.md створено")


if __name__ == "__main__":
    main()
