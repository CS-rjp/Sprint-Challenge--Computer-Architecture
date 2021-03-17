#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

if len(sys.argv) > 1:
    with open(sys.argv[1]) as file:
        program = []
        for line in file.readlines():
            # str = line.strip().partition("#")[0]
            str = line.split("#")[0].strip()
            if len(str) == 0:
                continue
            program.append(int(str,2))

        else:
            print(f'Required Arguement: Program Filename')


cpu = CPU()

cpu.load(program)
cpu.run()

