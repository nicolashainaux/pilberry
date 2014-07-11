#!/usr/bin/env python3

# Pilberry packages|modules imports
import bootstrap
from lib.carrier.Carrier import Carrier

with Carrier() as C:
    C.send('MODES', 'CMD_A1')
