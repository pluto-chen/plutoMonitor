#!/usr/bin/env python
# -*- coding:utf-8 -*-


import os
import sys
from core import main

BaseDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(BaseDir)


if __name__ == '__main__':

    client = main.Argv_Handler(sys.argv)


