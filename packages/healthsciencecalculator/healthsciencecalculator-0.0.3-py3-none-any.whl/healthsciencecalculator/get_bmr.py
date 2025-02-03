def get_bmr(
        weight: float,
        height:float,
        age:int,
        sex:str
) -> float:
    """
    Computes Basal Metabolic Rate (BMR) using the Harris-Benedict equation.

    The BMR is an estimate of the number of calories your body needs to perform
    basic life-sustaining functions, such as breathing, circulation, and cell production.

    Parameters
    ----------
    weight : float
        Weight of the individual in kilograms.
    height : float
        Height of the individual in centimeters.
    age : int
        Age of the individual in years.
    sex : str
        Biological sex of the individual. Accepted values are "male" or "female".

    Returns
    -------
    float
        The estimated BMR value in calories per day.

    Notes
    -----
    The Harris-Benedict equation is used to calculate BMR:
    - For males: BMR = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    - For females: BMR = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)

    Examples
    --------
    >>> get_bmr(70, 175, 25, "male")
    1668.872
    >>> get_bmr(60, 165, 30, "female")
    1392.247
    """
    if weight <= 0:
        raise ValueError("Weight must be positive")
    if height <= 0:
        raise ValueError("Height must be positive")
    if age < 0 or not isinstance(age, int):
        raise ValueError("Age must be positive integer")

    if sex.lower() == "male":
        bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    elif sex.lower() == "female":
        bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
    else:
        raise ValueError('Invalid value for sex. Use "male" or "female".')
    
    return round(bmr, 4)
    
