#!/usr/bin/env python3

# Pilberry packages|modules imports
from lib.carrier.Carrier import Carrier

with Carrier() as C:
    C.send('MODES', 'CMD_A1')
