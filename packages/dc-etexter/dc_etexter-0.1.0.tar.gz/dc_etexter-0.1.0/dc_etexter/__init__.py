# This file makes `dc_etexter/` an importable package.

# Import the function from `etexter.py` in the same directory
from .etexter import send_text

# Define what is available when using "from dc_etexter import *"
__all__ = ["send_text"]
