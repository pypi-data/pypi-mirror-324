"""
Quantum-inspired Random Number Generator (QRNG) for Python.
"""
import os
import atexit
from typing import Optional, Union
from _qrng import lib, ffi

__version__ = "1.1.0"

class QrngError(Exception):
    """Exception raised for QRNG-related errors."""
    pass

class Qrng:
    """
    Python interface to the Quantum Random Number Generator (QRNG).
    It manages the underlying C QRNG context.

    Args:
        seed (bytes, optional): Seed data for the QRNG. If None, uses system entropy.

    Raises:
        TypeError: If seed is not bytes
        QrngError: If QRNG initialization fails
    """
    def __init__(self, seed: Optional[bytes] = None):
        if seed is None:
            seed = os.urandom(32)
        if not isinstance(seed, bytes):
            raise TypeError("Seed must be bytes")

        self._seed = seed
        self._ctx_ptr = ffi.new("qrng_ctx **")
        res = lib.qrng_init(self._ctx_ptr, self._seed, len(self._seed))

        if res != lib.QRNG_SUCCESS:
            raise QrngError(f"Failed to initialize QRNG: {ffi.string(lib.qrng_error_string(res)).decode()}")

        self._ctx = self._ctx_ptr[0]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        """Explicitly free the QRNG context."""
        if hasattr(self, "_ctx") and self._ctx:
            lib.qrng_free(self._ctx)
            self._ctx = ffi.NULL

    def __del__(self):
        self.close()

    def uint64(self) -> int:
        """Return a random 64-bit unsigned integer."""
        if not self._ctx:
            raise QrngError("QRNG context has been closed")
        return lib.qrng_uint64(self._ctx)

    def random(self) -> float:
        """Return a random floating point number in [0, 1)."""
        if not self._ctx:
            raise QrngError("QRNG context has been closed")
        return lib.qrng_double(self._ctx)

    def randint(self, a: int, b: int) -> int:
        """
        Return a random integer N such that a <= N <= b.

        Args:
            a: Lower bound (inclusive)
            b: Upper bound (inclusive)

        Raises:
            ValueError: If a > b
            QrngError: If QRNG context has been closed
        """
        if not self._ctx:
            raise QrngError("QRNG context has been closed")
        if a > b:
            raise ValueError("Lower bound must be less than or equal to upper bound")

        if a < 0 or b < 0:
            return lib.qrng_range32(self._ctx, int(a), int(b))
        return lib.qrng_range64(self._ctx, int(a), int(b))

    def version(self) -> str:
        """Return the version string of the underlying QRNG implementation."""
        return ffi.string(lib.qrng_version()).decode('utf-8')

# Module-level interface
_default_instance = None

def _cleanup():
    global _default_instance
    if _default_instance is not None:
        _default_instance.close()
        _default_instance = None

atexit.register(_cleanup)

def get_default() -> Qrng:
    """Get or create the default QRNG instance."""
    global _default_instance
    if _default_instance is None:
        _default_instance = Qrng()
    return _default_instance

def uint64() -> int:
    """Return a random 64-bit unsigned integer using the default QRNG."""
    return get_default().uint64()

def random() -> float:
    """Return a random floating point number in [0, 1) using the default QRNG."""
    return get_default().random()

def randint(a: int, b: int) -> int:
    """Return a random integer N such that a <= N <= b using the default QRNG."""
    return get_default().randint(a, b)

def version() -> str:
    """Return the version string of the underlying QRNG implementation."""
    return get_default().version()

__all__ = ['Qrng', 'QrngError', 'uint64', 'random', 'randint', 'version']