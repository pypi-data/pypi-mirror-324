from dataclasses import dataclass

@dataclass
class BMIResult:
    bmi: float
    category: str


def get_bmi(
    weight: float,
    height: float,
) -> BMIResult:
    """Calculate Body Mass Index (BMI) and return detailed classification information.

    BMI is calculated as weight (kg) divided by height (m) squared.

    Parameters
    ----------
    weight : float
        Weight in kilograms
    height : float
        Height in meters

    Returns
    -------
    BMIResult
        A dataclass containing:
        - bmi (float): The calculated BMI value
        - category (str): BMI category, one of:
            - 'underweight' (BMI < 18.5)
            - 'healthy' (BMI 18.5-24.9)
            - 'overweight' (BMI 25-29.9)
            - 'class 1 obesity' (BMI 30-34.9)
            - 'class 2 obesity' (BMI 35-39.9)
            - 'class 3 obesity' (BMI >= 40)


    Example
    ------
    >>> get_bmi(weight=70.0, height=1.75)
    BMIResult(bmi=22.9, category='healthy')

    Raises
    ------
    ValueError
        If weight or height is not positive
    TypeError
        If weight or height is not a number
    """
    # Input validation
    if not isinstance(weight, (int, float)) or not isinstance(height, (int, float)):
        raise TypeError("Weight and height must be numbers")
    if weight <= 0:
        raise ValueError("Weight must be positive")
    if height <= 0:
        raise ValueError("Height must be positive")

    #Rounding after calculation to ensure calculation is accurate first
    bmi = round(weight / (height ** 2), 1)
    
    if bmi < 18.5:
        category = "underweight"
    elif bmi < 25:
        category = "healthy"
    elif bmi < 30:
        category = "overweight"
    elif bmi < 35:
        category = "class 1 obesity"
    elif bmi < 40:
        category = "class 2 obesity"
    else:
        category = "class 3 obesity"
    
    return BMIResult(bmi=bmi, category=category)

