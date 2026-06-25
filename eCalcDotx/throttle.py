# Author: Andrea Locatelli <andrea.locatelli.1997@gmail.com>
# Copyright (c) 2026 Andrea Locatelli

import math
from currentEstimate import estimateCurrent

def estimateThrottleHover(thrust_query, thrust_data, throttle_data=None):
    """
    Estimated throttle (%) required to hold the requested thrust per motor.

    Two modes:
    - If throttle_data is provided and valid (measured throttle column from
      the datasheet), interpolates thrust -> throttle directly. ACCURATE.
    - Otherwise falls back to the quadratic propeller approximation
      throttle ~= sqrt(thrust / thrust_max). APPROXIMATE: ignores ESC curve,
      voltage sag and motor dynamics. Use as an order-of-magnitude figure.

    thrust_query  : required thrust per single motor [g] (e.g. hover)
    thrust_data   : datasheet thrust column [g]
    throttle_data : datasheet throttle column [%], or None / all -1 if absent
    """
    valid_thrust = [t for t in thrust_data if t is not None]
    if not valid_thrust:
        raise ValueError("No valid thrust values in datasheet block")

    # Caso 1: throttle misurato disponibile -> interpolazione vera
    
    if throttle_data is not None and any(
            v is not None and v >= 0 for v in throttle_data):
        return estimateCurrent(thrust_query, thrust_data, throttle_data), True
    
    # Caso 2: fallback quadratico (approssimato)
    thrust_max = max(valid_thrust)
    throttle_pct = math.sqrt(thrust_query / thrust_max) * 100.0
    return throttle_pct, False