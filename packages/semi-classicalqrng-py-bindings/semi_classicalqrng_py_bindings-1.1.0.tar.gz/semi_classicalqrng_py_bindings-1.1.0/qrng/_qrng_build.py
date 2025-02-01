from cffi import FFI
ffibuilder = FFI()

# Provide the C declarations from the header file
ffibuilder.cdef("""
    typedef enum {
        QRNG_SUCCESS = 0,
        QRNG_ERROR_NULL_CONTEXT = -1,
        QRNG_ERROR_NULL_BUFFER = -2,
        QRNG_ERROR_INVALID_LENGTH = -3,
        QRNG_ERROR_INSUFFICIENT_ENTROPY = -4,
        QRNG_ERROR_INVALID_RANGE = -5
    } qrng_error;

    typedef struct qrng_ctx_t qrng_ctx;

    const char* qrng_version(void);
    uint64_t qrng_uint64(qrng_ctx *ctx);
    double qrng_double(qrng_ctx *ctx);
    int32_t qrng_range32(qrng_ctx *ctx, int32_t min, int32_t max);
    uint64_t qrng_range64(qrng_ctx *ctx, uint64_t min, uint64_t max);
    qrng_error qrng_init(qrng_ctx **ctx, const uint8_t *seed, size_t seed_len);
    void qrng_free(qrng_ctx *ctx);
    qrng_error qrng_reseed(qrng_ctx *ctx, const uint8_t *seed, size_t seed_len);
    qrng_error qrng_bytes(qrng_ctx *ctx, uint8_t *out, size_t len);
    double qrng_get_entropy_estimate(qrng_ctx *ctx);
    qrng_error qrng_entangle_states(qrng_ctx *ctx, uint8_t *state1, uint8_t *state2, size_t len);
    qrng_error qrng_measure_state(qrng_ctx *ctx, uint8_t *state, size_t len);
    const char* qrng_error_string(qrng_error err);
""")

# The source files (just the one C file here relies on its header and also includes the common header)
ffibuilder.set_source("_qrng",  # name of the output C extension
"""
    #include "quantum_rng.h"
""",
    sources=["src/quantum_rng/quantum_rng.c"],
    include_dirs=["src/quantum_rng", "src/common"],
    libraries=["m"],  # link math library on Unix
)

if __name__ == "__main__":
    ffibuilder.compile(verbose=True)