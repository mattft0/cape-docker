#!/usr/bin/env python3
import os

# 1. Patch settings.py: make init_rooter() and init_routing() non-fatal in cape-web
path_settings = '/opt/CAPEv2/web/web/settings.py'
if os.path.exists(path_settings):
    with open(path_settings) as f:
        content = f.read()

    old1 = 'init_rooter()'
    new1 = 'try:\n    init_rooter()\nexcept Exception:\n    pass'
    if old1 in content:
        content = content.replace(old1, new1, 1)
        print('init_rooter patch applied')

    old2 = 'init_routing()'
    new2 = 'try:\n    init_routing()\nexcept Exception:\n    pass'
    if old2 in content:
        content = content.replace(old2, new2, 1)
        print('init_routing patch applied')

    with open(path_settings, 'w') as f:
        f.write(content)

# 2. Patch startup.py: disable init_rooter() and init_routing() entirely in Docker
path_startup = '/opt/CAPEv2/lib/cuckoo/core/startup.py'
if os.path.exists(path_startup):
    with open(path_startup) as f:
        content = f.read()

    # Strategy A: disable function bodies
    old1 = 'def init_rooter():'
    new1 = 'def init_rooter(): return  # Disabled in Docker\ndef _init_rooter_disabled():'
    if old1 in content:
        content = content.replace(old1, new1, 1)
        print('init_rooter disabled patch applied')

    old2 = 'def init_routing():'
    new2 = 'def init_routing(): return  # Disabled in Docker\ndef _init_routing_disabled():'
    if old2 in content:
        content = content.replace(old2, new2, 1)
        print('init_routing disabled patch applied')

    # Strategy B (fallback): make rt_available check non-fatal
    old_rt = '                is_rt_available = rooter("rt_available", entry.rt_table)["output"]\n                if not is_rt_available:'
    new_rt = '                try:\n                    is_rt_available = rooter("rt_available", entry.rt_table)["output"]\n                except Exception:\n                    is_rt_available = True\n                if not is_rt_available:'
    if old_rt in content:
        content = content.replace(old_rt, new_rt, 1)
        print('startup rt_available patch applied')

    with open(path_startup, 'w') as f:
        f.write(content)
