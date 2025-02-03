# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pioemu', 'pioemu.instructions']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'rp2040-pio-emulator',
    'version': '0.84.0',
    'description': 'RP2040 emulator for the testing and debugging of PIO programs',
    'long_description': '# Emulator for the PIO Blocks within the RP2040 Microcontroller (Python Edition)\n\n![Build Status](https://github.com/NathanY3G/rp2040-pio-emulator/actions/workflows/package-ci.yml/badge.svg) ![Coverage](./docs/images/coverage-badge.svg) [![PyPI](https://img.shields.io/pypi/v/rp2040-pio-emulator?color=informational)](https://pypi.org/project/rp2040-pio-emulator/)\n\n## Introduction\nAn emulator for the Programmable Input/Output (PIO) blocks that are present\nwithin the Raspberry Pi Foundation\'s RP2040 Microcontroller. It is designed\nto assist in the analysis of PIO programs and to help you by:\n\n* Enabling unit tests to be written.\n* Answering questions such as: How many clock cycles are being consumed?\n* Supporting the visualization of GPIO outputs over time.\n* Providing alternatives to debugging on real hardware, which can be time consuming.\n\n## Quick Start\nBelow is a slight variation of the example used within the [Quick Start Guide](./docs/Quick%20Start%20Guide.md).\n\n```python\nfrom pioemu import emulate\n\nprogram = [0xE029, 0x0041, 0x2080]  # Count down from 9 using X register\n\ngenerator = emulate(program, stop_when=lambda _, state: state.x_register < 0)\n\nfor before, after in generator:\n  print(f"X register: {before.x_register} -> {after.x_register}")\n```\n\n## Documentation\nA [Tour of pioemu](./docs/Tour%20of%20pioemu.md) provides a more detailed explanation than the\n[Quick Start Guide](./docs/Quick%20Start%20Guide.md) offers. In addition, there is a\n[FAQ](./docs/FAQ.md) available that might contain an answer to your question. However, if none\nof these provides you with the necessary information then please consider creating a\n[new issue](https://github.com/NathanY3G/rp2040-pio-emulator/issues) - thanks!\n\n## Additional Examples\nSome additional examples are available within the [rp2040-pio-emulator-examples](https://github.com/NathanY3G/rp2040-pio-emulator-examples)\nrepository, including:\n\n1. [TDD](https://en.wikipedia.org/wiki/Test-driven_development) example for the\n   [Pimoroni Blinkt!](https://shop.pimoroni.com/products/blinkt)\n\n1. Tool to create Fast Signal Trace (FST) files suitable for analysis by\n   [GTKWave](https://gtkwave.sourceforge.net/)\n\n1. Visualisation of square wave program using a\n   [Jupyter Notebook](https://jupyter-notebook.readthedocs.io/en/latest/)\n\n## Supported Instructions\n\nInstruction | Supported                         | Notes\n:-----------| :---------------------------------| :----\nJMP         | :heavy_check_mark:                | \nWAIT        | :heavy_check_mark: :warning:      | IRQ variant is not supported\nIN          | :heavy_check_mark:                |\nOUT         | :heavy_check_mark: :construction: | EXEC destination not implemented\nPUSH        | :heavy_check_mark:                | \nPULL        | :heavy_check_mark:                | \nMOV         | :heavy_check_mark: :construction: | Some variants and operations not implemented\nIRQ         | :heavy_multiplication_x:          |\nSET         | :heavy_check_mark:                |\n\n## Known Limitations\nThis software is under development and currently has limitations - the notable ones are:\n\n1. Not all of the available instructions are supported - please refer to the table above.\n\n1. No support for pin-sets associated with `OUT`, `SET` or `IN`; all pin numbers are with respect to GPIO 0.\n\n1. Pin-sets do not wrap after GPIO 31.\n\n1. `PULL IFEMPTY` and `PUSH IFFULL` do not respect the pull and push thresholds.\n\n1. No direct support for the concurrent running of multiple PIO programs;\n   a single State Machine is emulated and not an entire PIO block.\n\n## Thanks To\n* [aaronjamt](https://github.com/aaronjamt) for contributing features and fixes.\n* [Josverl](https://github.com/Josverl) for contributing features.\n* [winnylourson](https://github.com/winnylourson) for contributing a bug fix.\n',
    'author': 'Nathan Young',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/NathanY3G/rp2040-pio-emulator',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10.13,<4.0.0',
}


setup(**setup_kwargs)
