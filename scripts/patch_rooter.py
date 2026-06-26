#!/usr/bin/env python3
"""Patch rooter.py at build time."""
import re

filepath = '/opt/CAPEv2/utils/rooter.py'
with open(filepath, 'r') as f:
    lines = f.readlines()

# Patch 1: sendto — wrapper try/except
patched_sendto = False
for i, line in enumerate(lines):
    if 'server.sendto(' in line and 'json.dumps' in line and 'output' in line:
        indent = len(line) - len(line.lstrip())
        ind = ' ' * indent
        ind_inner = ' ' * (indent + 4)
        lines[i] = (
            f"{ind}try:\n"
            f"{ind_inner}{line.lstrip()}"
            f"{ind}except (FileNotFoundError, OSError):\n"
            f"{ind_inner}pass\n"
        )
        patched_sendto = True
        print(f'rooter sendto patch applied at line {i+1}')
        break
if not patched_sendto:
    print('WARNING: sendto pattern not found')

# Patch 2: chmod socket -> 0o666
patched_chmod = False
for i, line in enumerate(lines):
    if 'os.chmod(settings.socket' in line and 'stat.' in line:
        lines[i] = re.sub(
            r'os\.chmod\(settings\.socket,\s*[^)]+\)',
            'os.chmod(settings.socket, 0o666)',
            line
        )
        patched_chmod = True
        print(f'rooter chmod patch applied at line {i+1}')
        break
if not patched_chmod:
    print('WARNING: chmod pattern not found')

with open(filepath, 'w') as f:
    f.writelines(lines)