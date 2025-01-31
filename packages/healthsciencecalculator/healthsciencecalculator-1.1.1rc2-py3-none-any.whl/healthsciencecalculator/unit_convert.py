def unit_convert(value: float, input_unit: str, output_unit: str):
    """Converts values from one unit to another.

    Supported measurement units:
    - Weight: kg, g, lb, stone
    - Length: m, cm, feet, inch
    - Temperature: C, F
    - Concentration: mg/dL, mmol/L
    - Volume: L, mL

    Parameters
    ----------
    value : float
        The numeric value to be converted.

    input_unit : str
        The unit of input value.

    output_unit : str
        The desired unit of output value.
    

    Returns
    -------
    float
        The output value in desired unit.

    Examples
    --------
    >>> unit_convert(1, "m", "cm")
    100
    """
    
    category = {
        "kg":0,"g":0,"lb":0,"stone":0,
        "m":1,"cm":1,"feet":1,"inch":1,
        "C":2,"F":2,
        "mg/dL":3,"mmol/L":3,
        "L":4,"mL":4
        }
    cal = {
        "kg":1000.0,"g":1.0,"lb":453.59237,"stone":6350.29318,
        "m":100.0,"cm":1.0,"feet":30.48,"inch":2.54,
        "mg/dL":1.0,"mmol/L":18.0,
        "L":1000.0,"mL":1.0
    }

    # validate input
    if (not isinstance(value, float)) & (not isinstance(value, int)):
        raise TypeError("Value must be a number")
    if not isinstance(input_unit, str):
        raise TypeError("Input unit must be string")
    if not isinstance(output_unit, str):
        raise TypeError("output unit must be string")

    # validate category
    if not input_unit in category:
        raise ValueError("Input unit does not exist")
    if not output_unit in category:
        raise ValueError("Output unit does not exist")
    if category[input_unit] != category[output_unit]:
        raise ValueError("Input unit and output unit do not in the same category")

    # no need to convert
    if input_unit == output_unit:
        return value

    # convert temperature
    if input_unit == "C":
        return round(value * 1.8 + 32, 2)
    if input_unit == "F":
        return round((value - 32) / 1.8, 2)

    # convert others
    return round(value * cal[input_unit] / cal[output_unit], 2)
        
    
