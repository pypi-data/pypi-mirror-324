#define Real double
#define OpenCLWrapper OpenCLWrapper_double
#define MODULE _core_double
#define VERY_SMALL_NUMBER 1e-10

#ifdef __OPENCL_VERSION__
#define Size ulong
#define Int int
#else
#define Size uint64_t
#define Int int32_t
#endif
