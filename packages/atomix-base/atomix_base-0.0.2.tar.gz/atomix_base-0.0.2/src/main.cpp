#include <pybind11/pybind11.h>
#define STRINGIFY(x) #x
#define MACRO_STRINGIFY(x) STRINGIFY(x)

#if defined(_M_ARM64EC) || defined(_M_ARM64) || defined(__aarch64__) || defined(__arm64__) || defined(__ARM_ARCH) || defined(__ARM_ARCH_ISA_A64)
    #define USE_ATOMIC
    #else
    #if defined(__x86_64__) || defined(__amd64__) || defined(_M_X64) || defined(_M_AMD64) || defined(__amd64) || defined(__x86_64)
        #if defined(__GNUC__) || defined(__clang__)
            #define USE_GCC
        #elif defined(_MSC_VER)
            #define USE_MSVC
        #endif
    #else
        #define USE_ATOMIC
    #endif
#endif

// uncomment these to test USE_ATOMIC
// #undef USE_GCC
// #undef USE_MSVC
// #define USE_ATOMIC

#if defined(USE_ATOMIC)
#include <atomic>
#endif

class AtomicInt {
public:
    AtomicInt(int64_t value) : value(value) {}
#if defined(USE_MSVC)
    int64_t load() { return _InterlockedExchangeAdd64(&value, 0); }
    void store(int64_t new_val) { _InterlockedExchange64(&value, new_val); }
    int64_t increment() { return _InterlockedIncrement64(&value); }
    int64_t decrement() { return _InterlockedDecrement64(&value); }
    int64_t add(int64_t new_val) { return _InterlockedExchangeAdd64(&value, new_val) + new_val; }
    int64_t subtract(int64_t new_val) { return _InterlockedExchangeAdd64(&value, -new_val) - new_val; }
    int64_t exchange(int64_t new_val) { return _InterlockedExchange64(&value, new_val); }
    bool compare_exchange(int64_t expected_val, int64_t new_val) { 
        const __int64 val = _InterlockedCompareExchange64(&value, new_val, expected_val);
        return (val == expected_val);
        }
    bool compare_exchange_weak(int64_t expected_val, int64_t new_val) { 
        const __int64 val = _InterlockedCompareExchange64(&value, new_val, expected_val);
        return (val == expected_val);
        }
#elif defined(USE_GCC)
    int64_t load() { return __atomic_load_n(&value, __ATOMIC_SEQ_CST); }
    void store(int64_t new_val) { __atomic_store_n(&value, new_val, __ATOMIC_SEQ_CST); }
    int64_t increment() { return __atomic_add_fetch(&value, 1, __ATOMIC_SEQ_CST); }
    int64_t decrement() { return __atomic_sub_fetch(&value, 1, __ATOMIC_SEQ_CST); }
    int64_t add(int64_t new_val) { return __atomic_add_fetch(&value, new_val, __ATOMIC_SEQ_CST); }
    int64_t subtract(int64_t new_val) { return __atomic_sub_fetch(&value, new_val, __ATOMIC_SEQ_CST); }
    int64_t exchange(int64_t new_val) { return __atomic_exchange_n(&value, new_val, __ATOMIC_SEQ_CST); }
    bool compare_exchange(int64_t expected_val, int64_t new_val) { 
        return __atomic_compare_exchange_n(&value, &expected_val, new_val, false, __ATOMIC_SEQ_CST, __ATOMIC_SEQ_CST);
        }
    bool compare_exchange_weak(int64_t expected_val, int64_t new_val) { 
        return __atomic_compare_exchange_n(&value, &expected_val, new_val, true, __ATOMIC_SEQ_CST, __ATOMIC_SEQ_CST);
        }
#elif defined(USE_ATOMIC)
    int64_t load() { return value.load(); }
    void store(int64_t new_val) { value.store(new_val); }
    int64_t increment() { return value.fetch_add(1) + 1; }
    int64_t decrement() { return value.fetch_sub(1) - 1; }
    int64_t add(int64_t new_val) { return value.fetch_add(new_val) + new_val; }
    int64_t subtract(int64_t new_val) { return value.fetch_sub(new_val) - new_val; }
    int64_t exchange(int64_t new_val) { return value.exchange(new_val); }
    bool compare_exchange(int64_t expected_val, int64_t new_val) { 
        return value.compare_exchange_strong(expected_val, new_val);
        }
    bool compare_exchange_weak(int64_t expected_val, int64_t new_val) { 
        return value.compare_exchange_weak(expected_val, new_val);
        }
#endif

private:
#if defined(USE_ATOMIC)
    std::atomic<int64_t> value;
#else
    int64_t value;
#endif
};

namespace py = pybind11;

PYBIND11_MODULE(atomix_base, m) {
    py::class_<AtomicInt>(m, "AtomicInt")
        .def(py::init<int64_t>())
        .def("load", &AtomicInt::load)
        .def("store", &AtomicInt::store)
        .def("increment", &AtomicInt::increment)
        .def("decrement", &AtomicInt::decrement)
        .def("add", &AtomicInt::add)
        .def("subtract", &AtomicInt::subtract)
        .def("exchange", &AtomicInt::exchange)
        .def("compare_exchange", &AtomicInt::compare_exchange)
        .def("compare_exchange_weak", &AtomicInt::compare_exchange_weak);
#ifdef VERSION_INFO
    m.attr("__version__") = MACRO_STRINGIFY(VERSION_INFO);
#else
    m.attr("__version__") = "dev";
#endif
}
