from healthsciencecalculator import get_bmr

def get_tdee(bmr: float, activity_level: str) -> float:
    """
    Calculate the Total Daily Energy Expenditure (TDEE) based on BMR and activity level.

    Parameters
    ----------
    bmr : float
        The Basal Metabolic Rate (must be positive).
    activity_level : str
        The activity level (allowed values: 'sedentary', 'lightly active', 
        'moderately active', 'very active', 'extra active').

    Returns
    -------
    float
        The calculated TDEE (kcal/day).

    Example 
    -------- 
    >>> get_tdee(bmr = 1500.0, activity_level = 'sedentary')
    1800.0

    Raises
    ------
    ValueError
        If bmr <= 0 or activity_level is not recognized.

    Notes
    -----
    Sample multipliers (you may choose different ones if needed):
      - sedentary: 1.2
      - lightly active: 1.375
      - moderately active: 1.55
      - very active: 1.725
      - extra active: 1.9
    """
    # Defensive checks
    if bmr <= 0:
        raise ValueError("BMR must be a positive number.")
    
    activity_multipliers = {
        "sedentary": 1.2,
        "lightly active": 1.375,
        "moderately active": 1.55,
        "very active": 1.725,
        "extra active": 1.9
    }

    if activity_level not in activity_multipliers:
        raise ValueError(
            f"Invalid activity level. Choose one of: {list(activity_multipliers.keys())}"
        )

    # Calculate TDEE
    tdee = bmr * activity_multipliers[activity_level]
    return tdee
