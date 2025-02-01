#define Real float
#define MODULE _core
#define VERY_SMALL_NUMBER 1e-10

#ifdef __OPENCL_VERSION__
#define Size ulong
#define Int int
#else
#define Size uint64_t
#define Int int32_t
#endif
