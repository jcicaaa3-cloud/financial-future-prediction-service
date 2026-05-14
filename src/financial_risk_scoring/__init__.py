from __future__ import annotations

import os

# Keep local tests/CI deterministic and prevent BLAS/OpenMP thread shutdown hangs
# in constrained environments. Users can override these before importing the package.
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

__all__ = ["__version__"]
__version__ = "0.5.0"
