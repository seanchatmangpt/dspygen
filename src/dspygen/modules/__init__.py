"""DSPyGen module package and bounded legacy compatibility admission."""
from __future__ import annotations

import os

from dspygen.modules.pipeline import install_legacy_pipeline_compat

if os.getenv("DSPYGEN_DISABLE_LEGACY_PIPE_COMPAT") != "1":
    try:
        import dspy
    except ModuleNotFoundError:
        # Generation and static inspection remain available without the optional runtime.
        pass
    else:
        install_legacy_pipeline_compat(dspy.Module)
