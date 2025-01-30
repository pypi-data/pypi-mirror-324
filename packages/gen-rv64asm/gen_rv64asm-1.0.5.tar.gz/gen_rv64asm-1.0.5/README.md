# Create risc-v 64-bit asm project skeleton

<img align="right" src="https://raw.githubusercontent.com/vroncevic/gen_rv64asm/dev/docs/gen_rv64asm_logo.png" width="25%">

**gen_rv64asm** is tool for creating risc-v 64-bit asm project skeleton.

Developed in **[python](https://www.python.org/)** code.

The README is used to introduce the modules and provide instructions on
how to install the modules, any machine dependencies it may have and any
other information that should be provided before the modules are installed.

[![gen_rv64asm python checker](https://github.com/vroncevic/gen_rv64asm/actions/workflows/gen_rv64asm_python_checker.yml/badge.svg)](https://github.com/vroncevic/gen_rv64asm/actions/workflows/gen_rv64asm_python_checker.yml) [![gen_rv64asm package checker](https://github.com/vroncevic/gen_rv64asm/actions/workflows/gen_rv64asm_package_checker.yml/badge.svg)](https://github.com/vroncevic/gen_rv64asm/actions/workflows/gen_rv64asm_package.yml) [![GitHub issues open](https://img.shields.io/github/issues/vroncevic/gen_rv64asm.svg)](https://github.com/vroncevic/gen_rv64asm/issues) [![GitHub contributors](https://img.shields.io/github/contributors/vroncevic/gen_rv64asm.svg)](https://github.com/vroncevic/gen_rv64asm/graphs/contributors)

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**

- [Installation](#installation)
    - [Install using pip](#install-using-pip)
    - [Install using build](#install-using-build)
    - [Install using py setup](#install-using-py-setup)
    - [Install using docker](#install-using-docker)
- [Dependencies](#dependencies)
- [Tool structure](#tool-structure)
- [Docs](#docs)
- [Contributing](#contributing)
- [Copyright and Licence](#copyright-and-licence)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

### Installation

Used next development environment

![debian linux os](https://raw.githubusercontent.com/vroncevic/gen_rv64asm/dev/docs/debtux.png)

[![gen_rv64asm python3 build](https://github.com/vroncevic/gen_rv64asm/actions/workflows/gen_rv64asm_python3_build.yml/badge.svg)](https://github.com/vroncevic/gen_rv64asm/actions/workflows/gen_rv64asm_python3_build.yml)

Currently there are four ways to install framework
* Install process based on using pip mechanism
* Install process based on build mechanism
* Install process based on setup.py mechanism
* Install process based on docker mechanism

##### Install using pip

Python is located at **[pypi.org](https://pypi.org/project/gen_rv64asm/)**.

You can install by using pip

```bash
#python3
pip3 install gen_rv64asm
```

##### Install using build

Navigate to **[release page](https://github.com/vroncevic/gen_rv64asm/releases)** download and extract release archive.

To install **gen-rv64asm** run

```bash
tar xvzf gen-rv64asm-x.y.z.tar.gz
cd gen-rv64asm-x.y.z
# python3
wget https://bootstrap.pypa.io/get-pip.py
python3 get-pip.py 
python3 -m pip install --upgrade setuptools
python3 -m pip install --upgrade pip
python3 -m pip install --upgrade build
pip3 install -r requirements.txt
python3 -m build -s --no-isolation --wheel
pip3 install dist/gen-rv64asm-x.y.z-py3-none-any.whl
rm -f get-pip.py
```

##### Install using py setup

Navigate to release **[page](https://github.com/vroncevic/gen_rv64asm/releases/)** download and extract release archive.

To install **gen_rv64asm** type the following

```bash
tar xvzf gen_rv64asm-x.y.z.tar.gz
cd gen_rv64asm-x.y.z/
# python3
pip3 install -r requirements.txt
python3 setup.py install_lib
python3 setup.py install_data
python3 setup.py install_egg_info
```

##### Install using docker

You can use Dockerfile to create image/container.

### Dependencies

**gen_rv64asm** requires next modules and libraries

* [ats-utilities - Python App/Tool/Script Utilities](https://vroncevic.github.io/gen_rv64asm)

### Tool structure

**gen_rv64asm** is based on OOP

Generator structure

```bash
    gen_rv64asm/
        ├── conf/
        │   ├── gen_rv64asm.cfg
        │   ├── gen_rv64asm.logo
        │   ├── gen_rv64asm_util.cfg
        │   ├── project.yaml
        │   └── template/
        │       ├── asmflags.template
        │       ├── ldflags.template
        │       ├── main.template
        │       ├── makefile.template
        │       ├── objects.template
        │       └── sources.template
        ├── __init__.py
        ├── log/
        │   └── gen_rv64asm.log
        ├── pro/
        │   ├── __init__.py
        │   ├── read_template.py
        │   └── write_template.py
        ├── py.typed
        └── run/
            └── gen_rv64asm_run.py
```

### Code coverage

| Name | Stmts | Miss | Cover |
|------|-------|------|-------|
| `gen_rv64asm/__init__.py` | 71 | 12 | 83% |
| `gen_rv64asm/pro/__init__.py` | 59 | 2 | 97% |
| `gen_rv64asm/pro/read_template.py` | 53 | 2 | 96% |
| `gen_rv64asm/pro/write_template.py` | 60 | 3 | 95% |
| **Total** | 243 | 19 | 92% |

### Docs

[![Documentation Status](https://readthedocs.org/projects/gen_rv64asm/badge/?version=latest)](https://gen-rv64asm.readthedocs.io/en/latest/?badge=latest)

More documentation and info at

* [gen_rv64asm.readthedocs.io](https://gen-rv64asm.readthedocs.io)
* [www.python.org](https://www.python.org/)

### Contributing

[Contributing to gen_rv64asm](CONTRIBUTING.md)

### Copyright and Licence

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0) [![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

Copyright (C) 2025 by [vroncevic.github.io/gen_rv64asm](https://vroncevic.github.io/gen_rv64asm/)

**gen_rv64asm** is free software; you can redistribute it and/or modify
it under the same terms as Python itself, either Python version 3.x or,
at your option, any later version of Python 3 you may have available.

Lets help and support PSF.

[![Python Software Foundation](https://raw.githubusercontent.com/vroncevic/gen_rv64asm/dev/docs/psf-logo-alpha.png)](https://www.python.org/psf/)

[![Donate](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.python.org/psf/donations/)
