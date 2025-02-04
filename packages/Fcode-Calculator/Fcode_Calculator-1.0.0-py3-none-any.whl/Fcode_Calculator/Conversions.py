def freq_converter(value, from_freq, to_freq):
    """Convert frequency between Hz, kHz, MHz, and GHz."""
    metric_dict = {'Hz': 1, 'kHz': 10**3, 'MHz': 10**6, 'GHz': 10**9}
    if from_freq not in metric_dict or to_freq not in metric_dict:
        raise ValueError("Invalid frequency units")
    return value * (metric_dict[from_freq] / metric_dict[to_freq])

def metric_converter(value, from_unit, to_unit):
    """Convert metric units (nano, micro, kilo, etc.)."""
    metric_dict = {'pico': 10**-12, 'nano': 10**-9, 'micro': 10**-6, 'milli': 10**-3,
                   'base': 1, 'Kilo': 10**3, 'Mega': 10**6, 'Giga': 10**9, 'Tera': 10**12}
    if from_unit not in metric_dict or to_unit not in metric_dict:
        raise ValueError("Invalid metric units")
    return value * (metric_dict[from_unit] / metric_dict[to_unit])

def cmyk_to_rgb(c, m, y, k):
    """Convert CMYK color values to RGB."""
    return (round(255 * (1 - c) * (1 - k)),
            round(255 * (1 - m) * (1 - k)),
            round(255 * (1 - y) * (1 - k)))
