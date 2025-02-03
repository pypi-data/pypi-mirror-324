#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
# author： NearlyHeadlessJack
# email: wang@rjack.cn
# datetime： 2025/1/26 22:42
# ide： PyCharm
# file: initialize.py
from wavelogpostmanager.utils.create_toml import create_toml
import os
import sys


def init() -> None:
    try:
        os.makedirs("wdw")
    except FileExistsError:
        print("-wdw already exists")
        sys.exit(1)
    os.makedirs("wdw/ssl", exist_ok=True)
    from wavelogpostmanager.constants.default_config import default_config

    create_toml(path="wdw/wdw.toml", config=default_config)
    os.makedirs("wdw/templates", exist_ok=True)
    os.makedirs("wdw/docx", exist_ok=True)
    os.makedirs("wdw/log", exist_ok=True)


if __name__ == "__main__":
    init()
