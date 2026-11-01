# Звіт до роботи

**Тема:** Покриття коду (Coverage)

**Мета роботи:** навчитись вимірювати покриття коду тестами за допомогою `coverage.py` і `pytest-cov`, читати звіт про покриття рядків і розгалужень, налаштовувати вимірювання, виключати код зі звіту та розуміти межі цього показника.

**Виконав:** Бейгул Володимир, група КН-42

## Виконання роботи

### Встановлення

```bash
pip install coverage pytest pytest-cov
```

У моєму середовищі команди запускались через `py -m ...`, це те саме, що виклик без `py -m`. Версія:

```text
> py -m coverage --version
Coverage.py, version 7.17.0 with C extension
Full documentation is at https://coverage.readthedocs.io/en/7.17.0
```

### Структура проєкту

```text
03_coverage/
├── app.py                      клас Figure (властивість get_angles)
├── test_app.py                 pytest-тести
├── test_unittest.py            unittest-тести
├── before_examples/
│   ├── test_triangle_only.py   тест лише для трикутника (стан «до»)
│   └── test_no_assert.py       тести без assert
├── .coveragerc                 налаштування coverage
├── coveragerc_no_pragma        конфігурація для порівняння без pragma
├── pyproject.toml              налаштування pytest та Poetry
├── Makefile
├── .github/workflows/coverage.yml
└── build_report.py             генерує цей звіт зі справжніх запусків
```

### Код прикладу

`app.py` (до прикладу додано точку входу з `# pragma: no cover` для одного із завдань):

```python
class Figure:
    FIGURES = ["квадрат", "прямокутник", "трикутник"]

    def __init__(self, figure_type: str, length: int) -> None:
        assert length > 0, "Довжина має бути більшою за 0!"
        assert figure_type in self.FIGURES, "Невідомий тип фігури"
        self.type = figure_type
        self.length = length

    @property
    def get_angles(self) -> int:
        if self.type in ["квадрат", "прямокутник"]:
            return 4
        if self.type == "трикутник":
            return 3
        return 0

if __name__ == "__main__":  # pragma: no cover
    print(Figure("квадрат", 1).get_angles)
```

`test_app.py` (pytest):

```python
import pytest

from app import Figure

@pytest.mark.parametrize(
    ("figure_type", "expected_angles"),
    [("квадрат", 4), ("прямокутник", 4), ("трикутник", 3)],
)
def test_get_angles(figure_type, expected_angles):
    assert Figure(figure_type, 1).get_angles == expected_angles

def test_invalid_length():
    with pytest.raises(AssertionError):
        Figure("квадрат", 0)

def test_unknown_type_uses_fallback():
    figure = Figure("квадрат", 1)
    figure.type = "коло"

    assert figure.get_angles == 0
```

`test_unittest.py` (unittest):

```python
import unittest

from app import Figure

class TestFigure(unittest.TestCase):
    def test_square_has_four_angles(self):
        self.assertEqual(4, Figure("квадрат", 1).get_angles)

    def test_rectangle_has_four_angles(self):
        self.assertEqual(4, Figure("прямокутник", 1).get_angles)

    def test_triangle_has_three_angles(self):
        self.assertEqual(3, Figure("трикутник", 1).get_angles)

    def test_unknown_type_uses_fallback(self):
        figure = Figure("квадрат", 1)
        figure.type = "коло"

        self.assertEqual(0, figure.get_angles)

    def test_invalid_length_raises_assertion_error(self):
        with self.assertRaises(AssertionError):
            Figure("квадрат", 0)

    def test_invalid_type_raises_assertion_error(self):
        with self.assertRaises(AssertionError):
            Figure("коло", 1)

if __name__ == "__main__":
    unittest.main()
```

### Запуск тестів і окремі вимірювання

Запуск тестів: `pytest -v` (у моєму середовищі `py -m pytest -v`).

Перед кожним вимірюванням виконую `coverage erase`, щоб дані різних запусків не змішувались у файлі `.coverage`.

**Набір unittest** (`coverage run -m unittest discover`):

```text
> py -m coverage erase
> py -m coverage run -m unittest discover
......
----------------------------------------------------------------------
Ran 6 tests in 0.001s

OK
> py -m coverage report -m
Name     Stmts   Miss Branch BrPart  Cover   Missing
----------------------------------------------------
app.py      14      0      4      0   100%
----------------------------------------------------
TOTAL       14      0      4      0   100%
```

**Набір pytest** (`coverage run -m pytest`):

```text
> py -m coverage erase
> py -m coverage run -m pytest
============================= test session starts =============================
platform win32 -- Python 3.15.2, pytest-9.2.0, pluggy-1.7.0
rootdir: D:\Microsoft VS Code\03_coverage
configfile: pyproject.toml
testpaths: .
plugins: cov-7.1.0
collected 11 items

test_app.py .....                                                        [ 45%]
test_unittest.py ......                                                  [100%]

============================= 11 passed in 0.07s ==============================
> py -m coverage report -m
Name     Stmts   Miss Branch BrPart  Cover   Missing
----------------------------------------------------
app.py      14      0      4      0   100%
----------------------------------------------------
TOTAL       14      0      4      0   100%
```

**Плагін pytest-cov** (`pytest --cov=app --cov-branch --cov-report=term-missing -v`):

```text
> py -m pytest --cov=app --cov-branch --cov-report=term-missing -v
============================= test session starts =============================
platform win32 -- Python 3.15.2, pytest-9.2.0, pluggy-1.7.0 -- C:\Users\rrete\AppData\Local\Python\pythoncore-3.15-64\python.exe
cachedir: .pytest_cache
rootdir: D:\Microsoft VS Code\03_coverage
configfile: pyproject.toml
testpaths: .
plugins: cov-7.1.0
collecting ... collected 11 items

test_app.py::test_get_angles[\u043a\u0432\u0430\u0434\u0440\u0430\u0442-4] PASSED [  9%]
test_app.py::test_get_angles[\u043f\u0440\u044f\u043c\u043e\u043a\u0443\u0442\u043d\u0438\u043a-4] PASSED [ 18%]
test_app.py::test_get_angles[\u0442\u0440\u0438\u043a\u0443\u0442\u043d\u0438\u043a-3] PASSED [ 27%]
test_app.py::test_invalid_length PASSED                                  [ 36%]
test_app.py::test_unknown_type_uses_fallback PASSED                      [ 45%]
test_unittest.py::TestFigure::test_invalid_length_raises_assertion_error PASSED [ 54%]
test_unittest.py::TestFigure::test_invalid_type_raises_assertion_error PASSED [ 63%]
test_unittest.py::TestFigure::test_rectangle_has_four_angles PASSED      [ 72%]
test_unittest.py::TestFigure::test_square_has_four_angles PASSED         [ 81%]
test_unittest.py::TestFigure::test_triangle_has_three_angles PASSED      [ 90%]
test_unittest.py::TestFigure::test_unknown_type_uses_fallback PASSED     [100%]

=============================== tests coverage ================================
_______________ coverage: platform win32, python 3.15.2-final-0 _______________

Name     Stmts   Miss Branch BrPart  Cover   Missing
----------------------------------------------------
app.py      14      0      4      0   100%
----------------------------------------------------
TOTAL       14      0      4      0   100%
============================= 11 passed in 0.09s ==============================
```

### Як читати звіт

- `Stmts` кількість виконуваних операторів, `Miss` скільки з них не виконано;
- `Branch` кількість можливих переходів між гілками умов, `BrPart` скільки з умов пройдено не в усі боки;
- `Cover` загальний відсоток, `Missing` номери рядків, які варто перевірити.

**Покриття рядків і покриття розгалужень.** Line coverage показує, чи був рядок виконаний хоча б раз. Branch coverage перевіряє кожен напрямок умовного переходу окремо: для `if` потрібні і випадок «істина», і випадок «хиба». Тест може виконати рядок з `if`, але пройти лише в один бік, тоді рядки покриті, а гілки ні.

### ⭐ Розгалуження: покриття до і після

У наданому прикладі вже є тести для квадрата, прямокутника й трикутника. Щоб показати стан до додавання тестів, я створив `before_examples/test_triangle_only.py`, де перевіряється лише трикутник:

```python
from app import Figure

def test_triangle_angles():
    assert Figure("трикутник", 1).get_angles == 3
```

Вимірювання **до** (лише тест для трикутника), покриття 78%:

```text
> py -m coverage erase
> py -m coverage run -m pytest before_examples/test_triangle_only.py
============================= test session starts =============================
platform win32 -- Python 3.15.2, pytest-9.2.0, pluggy-1.7.0
rootdir: D:\Microsoft VS Code\03_coverage
configfile: pyproject.toml
plugins: cov-7.1.0
collected 1 item

before_examples\test_triangle_only.py .                                  [100%]

============================== 1 passed in 0.05s ==============================
> py -m coverage report -m
Name     Stmts   Miss Branch BrPart  Cover   Missing
----------------------------------------------------
app.py      14      2      4      2    78%   13, 16
----------------------------------------------------
TOTAL       14      2      4      2    78%
```

Пояснення: тест для трикутника виконує конструктор, перевірку `if self.type in ["квадрат", "прямокутник"]` (вона хибна) і `return 3`. Не виконуються:

- `return 4`, бо умова для квадрата й прямокутника жодного разу не була істинною;
- `return 0` (запасний варіант для невідомого типу), бо до нього тест не доходить.

Номери цих рядків видно у стовпці `Missing`. За гілками перша умова жодного разу не була істинною, а друга жодного разу не була хибною, тому в `BrPart` є часткові переходи.

Після використання повного набору тестів (квадрат, прямокутник, трикутник і запасний варіант) покриття 100%, див. вивід `coverage run -m pytest` вище.

### Налаштування `.coveragerc`

```ini
[run]
source = .
branch = true

[report]
omit =
    test_*.py
    */test_*.py
    */tests/*
    */__init__.py
    */.venv/*
    build_report.py
```

Файл зберігає налаштування у проєкті, тож не треба щоразу передавати параметри в командному рядку.

- `[run] source = .` задає аналіз Python-файлів у поточній папці;
- `branch = true` вмикає вимірювання розгалужень (звідси стовпці `Branch` і `BrPart`);
- `[report] omit` виключає зі звіту тести та службові файли. До наведеного прикладу я додав `*/test_*.py` (тести у підпапках, наприклад `before_examples`) і `build_report.py`, бо при `source = .` coverage показує навіть файли, які тести не імпортують, з покриттям 0%.

⭐ **Перевірка меж вимірювання:** у стовпці `Name` усіх таблиць вище лише `app.py`, тобто `source` охоплює програму, а тестові файли та `build_report.py` до звіту не потрапляють.

Ті самі налаштування можна зберегти й у `pyproject.toml` у секціях `[tool.coverage.run]` і `[tool.coverage.report]`. Якщо одночасно є `.coveragerc`, coverage читає його, тому я залишив лише один спосіб.

### ⭐ HTML та XML-звіти

HTML-звіт (`coverage html`):

```text
> py -m coverage erase
> py -m coverage run -m pytest
============================= test session starts =============================
platform win32 -- Python 3.15.2, pytest-9.2.0, pluggy-1.7.0
rootdir: D:\Microsoft VS Code\03_coverage
configfile: pyproject.toml
testpaths: .
plugins: cov-7.1.0
collected 11 items

test_app.py .....                                                        [ 45%]
test_unittest.py ......                                                  [100%]

============================= 11 passed in 0.07s ==============================
> py -m coverage html
Wrote HTML report to htmlcov\index.html
```

Файл `htmlcov/index.html` відкривається в браузері; у ньому по кожному файлу видно рядки, підсвічені як виконані або пропущені.

XML-звіт (`coverage xml`):

```text
> py -m coverage xml
Wrote XML report to coverage.xml
```

Початок файлу `coverage.xml`:

```xml
<?xml version="1.0" ?>
<coverage version="7.17.0" timestamp="1793546552895" lines-valid="14" lines-covered="14" line-rate="1" branches-valid="4" branches-covered="4" branch-rate="1" complexity="0">
	<!-- Generated by coverage.py: https://coverage.readthedocs.io/en/7.17.0 -->
	<!-- Based on https://raw.githubusercontent.com/cobertura/web/master/htdocs/xml/coverage-04.dtd -->
	<sources>
		<source>D:\Microsoft VS Code\03_coverage</source>
	</sources>
	<packages>
		<package name="." line-rate="1" branch-rate="1" complexity="0">
			<classes>
				<class name="app.py" filename="app.py" complexity="0" line-rate="1" branch-rate="1">
					<methods/>
```

**Призначення форматів.** HTML-звіт призначений для людини: зручно переглядати у браузері, які саме рядки не покриті. XML-звіт призначений для інструментів: CI-системи та сервіси аналізу покриття читають його автоматично. Папка `htmlcov/` і `coverage.xml` додані до `.gitignore`, бо це згенеровані файли, які не треба комітити.

### ⭐ `pragma: no cover` для точки входу

У кінець `app.py` додано блок запуску:

```python
if __name__ == "__main__":  # pragma: no cover
    print(Figure("квадрат", 1).get_angles)
```

Тести імпортують модуль, тому умова `__name__ == "__main__"` у них хибна і блок ніколи не виконується. Порівняння з тими самими даними вимірювання: **з** `pragma: no cover` покриття 100% (вивід `coverage run -m pytest` вище), **без** виключення, коли `pragma` не враховується, покриття 91%:

```text
> py -m coverage erase
> py -m coverage run -m pytest
============================= test session starts =============================
platform win32 -- Python 3.15.2, pytest-9.2.0, pluggy-1.7.0
rootdir: D:\Microsoft VS Code\03_coverage
configfile: pyproject.toml
testpaths: .
plugins: cov-7.1.0
collected 11 items

test_app.py .....                                                        [ 45%]
test_unittest.py ......                                                  [100%]

============================= 11 passed in 0.06s ==============================
> py -m coverage report -m --rcfile=coveragerc_no_pragma
Name     Stmts   Miss Branch BrPart  Cover   Missing
----------------------------------------------------
app.py      16      1      6      1    91%   20
----------------------------------------------------
TOTAL       16      1      6      1    91%
```

Різниця виникає через рядок `print(...)` і перехід умови `if __name__ == "__main__"`, які без `pragma` рахуються пропущеними.

🔥 **Коректне та некоректне виключення.** Коректний приклад це саме точка входу `if __name__ == "__main__":`. Вона лише запускає програму, а логіка (`get_angles`, перевірки в конструкторі) вже перевірена тестами, тому виключення не приховує важливу поведінку й не змінює покриття важливої логіки. Некоректно ставити `pragma: no cover` на гілку `return 0` у `get_angles`: це реальна логіка, і її треба перевіряти тестом (як у `test_unknown_type_uses_fallback`), а не ховати від звіту заради відсотка.

### 🔥 Мінімальний поріг покриття

Встановив поріг 90% через `--cov-fail-under=90`. З одним тестом для трикутника поріг не досягається (команда завершується з помилкою):

```text
> py -m pytest before_examples/test_triangle_only.py --cov=app --cov-branch --cov-fail-under=90 -q
.
ERROR: Coverage failure: total of 78 is less than fail-under=90
                                                                         [100%]
=============================== tests coverage ================================
_______________ coverage: platform win32, python 3.15.2-final-0 _______________

Name     Stmts   Miss Branch BrPart  Cover
------------------------------------------
app.py      14      2      4      2    78%
------------------------------------------
TOTAL       14      2      4      2    78%
FAIL Required test coverage of 90% not reached. Total coverage: 77.78%
1 passed in 0.04s
```

Після доповнення тестів поріг досягнуто:

```text
> py -m pytest --cov=app --cov-branch --cov-fail-under=90 -q
...........                                                              [100%]
=============================== tests coverage ================================
_______________ coverage: platform win32, python 3.15.2-final-0 _______________

Name     Stmts   Miss Branch BrPart  Cover
------------------------------------------
app.py      14      0      4      0   100%
------------------------------------------
TOTAL       14      0      4      0   100%
Required test coverage of 90% reached. Total coverage: 100.00%
11 passed in 0.05s
```

### 🔥 Перевірка coverage у CI

Додав workflow `.github/workflows/coverage.yml`: він встановлює залежності, запускає `pytest` з `--cov-fail-under=90`, формує `coverage.xml` і завантажує його як артефакт. Якщо поріг не досягнуто, крок завершується помилкою і статус запуску стає невдалим.

```yaml
name: Coverage

on:
  push:
  pull_request:

jobs:
  coverage:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install coverage pytest pytest-cov
      - run: pytest --cov=app --cov-branch --cov-report=term-missing --cov-report=xml --cov-fail-under=90
      - uses: actions/upload-artifact@v4
        with:
          name: coverage-xml
          path: coverage.xml
```

Результат запусків видно у вкладці **Actions** репозиторію.

### Чого coverage не доводить

Тести без `assert` (`before_examples/test_no_assert.py`) лише викликають `get_angles` для всіх фігур і для запасного варіанта:

```python
import pytest

from app import Figure

@pytest.mark.parametrize("figure_type", Figure.FIGURES)
def test_get_angles_without_assert(figure_type):
    Figure(figure_type, 1).get_angles

def test_fallback_without_assert():
    figure = Figure("квадрат", 1)
    figure.type = "коло"
    figure.get_angles
```

Покриття цього набору 100%:

```text
> py -m coverage erase
> py -m coverage run -m pytest before_examples/test_no_assert.py
============================= test session starts =============================
platform win32 -- Python 3.15.2, pytest-9.2.0, pluggy-1.7.0
rootdir: D:\Microsoft VS Code\03_coverage
configfile: pyproject.toml
plugins: cov-7.1.0
collected 4 items

before_examples\test_no_assert.py ....                                   [100%]

============================== 4 passed in 0.06s ==============================
> py -m coverage report -m
Name     Stmts   Miss Branch BrPart  Cover   Missing
----------------------------------------------------
app.py      14      0      4      0   100%
----------------------------------------------------
TOTAL       14      0      4      0   100%
```

Тепер у тимчасовій копії проєкту навмисно внесено помилку: для трикутника `get_angles` повертає 30 замість 3. Тести без `assert` усе одно проходять і показують повне покриття:

```text
> py -m coverage erase
> py -m coverage run -m pytest test_no_assert.py
============================= test session starts =============================
platform win32 -- Python 3.15.2, pytest-9.2.0, pluggy-1.7.0
rootdir: C:\Users\rrete\AppData\Local\Temp\tmpeneq3ia7
plugins: cov-7.1.0
collected 4 items

test_no_assert.py ....                                                   [100%]

============================== 4 passed in 0.10s ==============================
> py -m coverage report -m
Name     Stmts   Miss Branch BrPart  Cover   Missing
----------------------------------------------------
app.py      14      0      4      0   100%
----------------------------------------------------
TOTAL       14      0      4      0   100%
```

А тести з перевіркою очікуваного значення (`test_app.py`) помилку виявляють:

```text
> py -m pytest test_app.py --tb=short -q
..F..                                                                    [100%]
================================== FAILURES ===================================
__ test_get_angles[\u0442\u0440\u0438\u043a\u0443\u0442\u043d\u0438\u043a-3] __
test_app.py:11: in test_get_angles
    assert Figure(figure_type, 1).get_angles == expected_angles
E   AssertionError: assert 30 == 3
E    +  where 30 = <app.Figure object at 0x00000181816B20D0>.get_angles
E    +    where <app.Figure object at 0x00000181816B20D0> = Figure('трикутник', 1)
=========================== short test summary info ===========================
FAILED test_app.py::test_get_angles[\u0442\u0440\u0438\u043a\u0443\u0442\u043d\u0438\u043a-3]
1 failed, 4 passed in 0.11s
```

**Висновок із порівняння:** тест без `assert` гарантує лише, що код виконується без винятків, а тест із перевіркою гарантує правильний результат. 100% line coverage означає, що кожен рядок хоча б раз виконався, але не що результат правильний: покриття не перевіряє значення, не показує сценарії, для яких тестів немає взагалі, і не виявляє помилки в самій логіці.

## Висновок

Виконав завдання роботи, включно з ⭐ та 🔥: окремі вимірювання для unittest і pytest, `pytest-cov`, порівняння покриття до й після додавання тестів, налаштування `.coveragerc`, HTML та XML-звіти, `pragma: no cover`, поріг покриття, workflow для CI та приклад, чому покриття не гарантує якість. Усі 11 тестів проходять.

Мети роботи досягнуто: навчився вимірювати покриття, читати стовпці звіту, відрізняти покриття рядків від покриття розгалужень, налаштовувати вимірювання і виключення та розуміти, що відсоток покриття не доводить правильність тестів.

Складності: потрібно було розібратись, що при `source = .` у звіт потрапляють і непроімпортовані файли (0%), тому довелося додати їх до `omit`.

Feedback: формат здачі через посилання на репозиторій зручний, бо код, налаштування та звіт лежать разом.

Suggestions: у прикладі `app.py` немає точки входу, тому для завдання з `pragma: no cover` її довелося додавати самостійно. Було б корисно мати її в прикладі.
