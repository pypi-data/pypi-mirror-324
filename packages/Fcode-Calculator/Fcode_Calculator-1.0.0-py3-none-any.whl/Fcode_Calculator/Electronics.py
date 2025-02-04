def ohms_law(type, V=None, I=None, R=None):
    """Calculate Ohm's Law (V = IR). Provide two values to find the third."""
    if type == "Current" and V is not None and R is not None:
        return V / R
    elif type == "Voltage" and I is not None and R is not None:
        return I * R
    elif type == "Resistance" and V is not None and I is not None:
        return V / I
    else:
        raise ValueError("Invalid input, provide exactly two values")

def power_law(type, V=None, I=None, P=None):
    """Calculate Power (P = VI). Provide two values to find the third."""
    if type == "Current" and V is not None and P is not None:
        return P / V
    elif type == "Voltage" and P is not None and I is not None:
        return P / I
    elif type == "Power" and V is not None and I is not None:
        return V * I
    else:
        raise ValueError("Invalid input, provide exactly two values")

def series_resistor(*resistances):
    """Calculate total resistance in a series circuit."""
    return sum(resistances)

def parallel_resistor(*resistances):
    """Calculate total resistance in a parallel circuit."""
    return 1 / sum(1 / r for r in resistances)
