---
layout: post
title: How to run Pytest with coverage
seo: Ways - How to run Pytest with coverage
tag: ways
permalink: /ways/run-pytest-with-coverage
date: 2026-03-01

---

Run the following in Terminal to execute Pytest with coverage reporting.

```bash
pytest --cov=. --cov-report=html
```

This command will run all tests in the current directory and generate an HTML report showing the code coverage. You can open the `htmlcov/index.html` file in your browser to view the coverage details.

Add htmlcov to .gitignore to avoid committing coverage reports to version control.
