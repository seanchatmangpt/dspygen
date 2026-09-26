"""
DEPRECATED: This module uses DSPy 2.x API and is no longer maintained.

Please use dspygen.lm.groq_lm_v3 for DSPy 3.1.3+ support.

Migration guide:
    OLD (DSPy 2.x):
        from dspygen.lm.groq_lm import Groq
        lm = Groq(model="llama3-70b-8192")

    NEW (DSPy 3.x):
        from dspygen.lm.groq_lm_v3 import Groq, init_groq
        lm = init_groq(model="llama3-70b-8192")
        # OR
        lm = Groq(model="llama3-70b-8192")
        import dspy
        dspy.settings.configure(lm=lm)

This file is kept for backward compatibility only.
"""

import warnings

warnings.warn(
    "dspygen.lm.groq_lm is deprecated. Use dspygen.lm.groq_lm_v3 for DSPy 3.1.3+ support.",
    DeprecationWarning,
    stacklevel=2,
)

# Import from new module for backward compatibility
from dspygen.lm.groq_lm_v3 import Groq, init_groq

__all__ = ["Groq", "init_groq"]

