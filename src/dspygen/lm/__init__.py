"""
Language Model backends for dspygen

Compatible with DSPy 3.1.3+
"""

from dspygen.lm.groq_lm_v3 import Groq, init_groq

__all__ = ["Groq", "init_groq"]

