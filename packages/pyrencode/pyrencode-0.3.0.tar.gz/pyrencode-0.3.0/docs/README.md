# pyrencode: rencode in pure python

[![build][build_badge]][build_url]
[![lint][lint_badge]][lint_url]
[![tests][tests_badge]][tests_url]
[![license][licence_badge]][licence_url]
[![codecov][codecov_badge]][codecov_url]
[![readthedocs][readthedocs_badge]][readthedocs_url]
[![pypi][pypi_badge]][pypi_url]
[![downloads][pepy_badge]][pepy_url]
[![code style: black][black_badge]][black_url]
[![build automation: yam][yam_badge]][yam_url]
[![Lint: ruff][ruff_badge]][ruff_url]

`pyrencode` is a python rewrite of the original
[rencode](https://github.com/aresch/rencode) by aresch, avoiding the
cython dependency, so that it can be used with PyPy. Even though there
in no cython code, the performance is comparable to the original, and in
many cases it\'s even better.

## Links

-   [Documentation]
-   [Changelog]

[build_badge]: https://github.com/spapanik/pyrencode/actions/workflows/build.yml/badge.svg
[build_url]: https://github.com/spapanik/pyrencode/actions/workflows/build.yml
[lint_badge]: https://github.com/spapanik/pyrencode/actions/workflows/lint.yml/badge.svg
[lint_url]: https://github.com/spapanik/pyrencode/actions/workflows/lint.yml
[tests_badge]: https://github.com/spapanik/pyrencode/actions/workflows/tests.yml/badge.svg
[tests_url]: https://github.com/spapanik/pyrencode/actions/workflows/tests.yml
[licence_badge]: https://img.shields.io/pypi/l/pyrencode
[licence_url]: https://pyrencode.readthedocs.io/en/stable/LICENSE/
[codecov_badge]: https://codecov.io/github/spapanik/pyrencode/graph/badge.svg?token=Q20F84BW72
[codecov_url]: https://codecov.io/github/spapanik/pyrencode
[readthedocs_badge]: https://readthedocs.org/projects/pyrencode/badge/?version=latest
[readthedocs_url]: https://pyrencode.readthedocs.io/en/latest/
[pypi_badge]: https://img.shields.io/pypi/v/pyrencode
[pypi_url]: https://pypi.org/project/pyrencode
[pepy_badge]: https://pepy.tech/badge/pyrencode
[pepy_url]: https://pepy.tech/project/pyrencode
[black_badge]: https://img.shields.io/badge/code%20style-black-000000.svg
[black_url]: https://github.com/psf/black
[yam_badge]: https://img.shields.io/badge/build%20automation-yamk-success
[yam_url]: https://github.com/spapanik/yamk
[ruff_badge]: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v1.json
[ruff_url]: https://github.com/charliermarsh/ruff
[Documentation]: https://pyrencode.readthedocs.io/en/stable/
[Changelog]: https://pyrencode.readthedocs.io/en/stable/CHANGELOG/
