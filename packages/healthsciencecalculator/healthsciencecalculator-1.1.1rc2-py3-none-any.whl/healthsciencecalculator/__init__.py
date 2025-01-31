# read version from installed package
# from importlib.metadata import version
# from healthsciencecalculator import (
#     get_bmi,
#     get_bmr,
#     get_tdee,
#     unit_convert,
#     BMIResult
# )

# __version__ = version("healthsciencecalculator")

# __all__ = [
#     'get_bmi',
#     'get_bmr',
#     'get_tdee',
#     'unit_convert',
#     'BMIResult'
# ]


from importlib.metadata import version
__version__ = version("healthsciencecalculator")