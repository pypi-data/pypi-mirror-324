import math
import cmath
import sympy
import re
def _pse(x):
    if x.imag == 0:return float(x.real)
    return complex(x)
def sin(x):
    return _pse(cmath.sin(x))
def cos(x):
    return _pse(cmath.cos(x))
def tan(x):
    return _pse(cmath.tan(x))
def sinh(x):
    return _pse(cmath.sinh(x))
def cosh(x):
    return _pse(cmath.cosh(x))
def tanh(x):
    return _pse(cmath.tanh(x))
def asin(x):
    return _pse(cmath.asin(x))
def acos(x):
    return _pse(cmath.acos(x))
def atan(x):
    return _pse(cmath.atan(x))
def asinh(x):
    return _pse(cmath.asinh(x))
def acosh(x):
    return _pse(cmath.acosh(x))
def atanh(x):
    return _pse(cmath.atanh(x))
def factorial(x):
    return _pse(sympy.factorial(x))
def root(x,y=2):
    return x**(1/y)
def expand_formula(formula):
    """
    Преобразует строку типа 'CO2' в 'COO' или 'NH3' в 'NHHH'.

    Args:
        formula (str): Химическая формула в строковом формате.

    Returns:
        str: Развернутая формула.
    """
    def replace_match(match):
        char = match.group(1)  # Символ перед цифрой
        num = int(match.group(2)) if match.group(2) else 1   # Количество повторений
        return char * num

    expanded_formula = re.sub(r'([A-Za-z])(\d*)', replace_match, formula)
    return expanded_formula
