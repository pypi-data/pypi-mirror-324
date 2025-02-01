cmake_minimum_required(VERSION 3.15...3.26)
project(${SKBUILD_PROJECT_NAME} LANGUAGES CXX)

set(PYBIND11_FINDPYTHON ON)
find_package(pybind11 CONFIG REQUIRED)
find_package(OpenCL REQUIRED)

pybind11_add_module(_core MODULE src/core/main.cpp)
pybind11_add_module(_core_double MODULE src/core_double/main.cpp)

target_include_directories(_core PRIVATE ${OpenCL_INCLUDE_DIRS})
target_include_directories(_core_double PRIVATE ${OpenCL_INCLUDE_DIRS})
target_link_libraries(_core PRIVATE ${OpenCL_LIBRARIES})
target_link_libraries(_core_double PRIVATE ${OpenCL_LIBRARIES})
message(STATUS "OpenCL Include Directory: ${OpenCL_INCLUDE_DIRS}")
message(STATUS "OpenCL Library: ${OpenCL_LIBRARIES}")

install(TARGETS _core _core_double DESTINATION ${SKBUILD_PROJECT_NAME})
