# LiquidSig — Cell-free RNA signatures

[![PyPI](https://img.shields.io/pypi/v/liquidsig.svg)][pypi status]
[![Status](https://img.shields.io/pypi/status/liquidsig.svg)][pypi status]
[![Python Version](https://img.shields.io/pypi/pyversions/liquidsig)][pypi status]
[![License](https://img.shields.io/pypi/l/liquidsig)][license]

[![Documentation](https://github.com/semenko/liquidsig/actions/workflows/docs.yml/badge.svg)][documentation]
[![Tests](https://github.com/semenko/liquidsig/actions/workflows/tests.yml/badge.svg)][tests]
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=semenko_liquidsig&metric=coverage)][sonarcov]
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=semenko_liquidsig&metric=alert_status)][sonarquality]

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)][poetry]

[pypi status]: https://pypi.org/project/liquidsig/
[documentation]: https://semenko.github.io/liquidsig
[tests]: https://github.com/semenko/liquidsig/actions?workflow=Tests

[sonarcov]: https://sonarcloud.io/summary/overall?id=semenko_liquidsig
[sonarquality]: https://sonarcloud.io/summary/overall?id=semenko_liquidsig
[pre-commit]: https://github.com/pre-commit/pre-commit
[black]: https://github.com/psf/black
[poetry]: https://python-poetry.org/

## Features

- Deconvolute cfRNA data
- Derive tissue & organ-specific signatures
    - For early malignancy detection & MRD
    - For predicting tissue of origin
    - For identification of end-organ damage (e.g., in sepsis)

## Requirements

- Python 3.10+
- Quantified transcripts (from cfRNA), in . format

## Installation

You can install _Liquidsig_ via [pip] from [PyPI]:

```console
pip install liquidsig
```

## Usage

Please see the [Reference Guide] for details.

## Contributing

Contributions are very welcome.
To learn more, see the [Contributor Guide].

## License

For non-commercial use only. Copyright &copy; Nick Semenkovich & Medical College of Wisconsin 2024-2025

## Issues

If you encounter any problems,
please [file an issue] along with a detailed description.

## Credits

This project was generated from [Statistics Norway]'s [SSB PyPI Template].

[statistics norway]: https://www.ssb.no/en
[pypi]: https://pypi.org/
[ssb pypi template]: https://github.com/statisticsnorway/ssb-pypitemplate
[file an issue]: https://github.com/semenko/liquidsig/issues
[pip]: https://pip.pypa.io/

<!-- github-only -->

[license]: https://github.com/semenko/liquidsig/blob/main/LICENSE
[contributor guide]: https://github.com/semenko/liquidsig/blob/main/CONTRIBUTING.md
[reference guide]: https://semenko.github.io/liquidsig/reference.html
