#* coding: utf-8
from solute.epfl.validators.number import NumberValidator


class FloatValidator(NumberValidator):
    float = True  #: Just set this to True and NumberValidator will do the rest.
