# cmake_minimum_required(VERSION 3.23)

# project(OcaSDKToPython)
# set(PYBIND11_NEWPYTHON ON)

# find_package(orcaSDK REQUIRED PATHS C:/Users/JakeTaranov/pyActuator/orcaSDK/build)

# add_subdirectory(third_party/pybind11 pybind11)

# pybind11_add_module(pyActuator
#     bindings/PyActuator.cpp
# )

# target_link_libraries(pyActuator PRIVATE orcaSDK::core)



# install(TARGETS pyActuator LIBRARY DESTINATION pyActuator)



cmake_minimum_required(VERSION 3.17...3.27)

# Scikit-build-core sets these values for you, or you can just hard-code the
# name and version.
project(
  ${SKBUILD_PROJECT_NAME}
  VERSION ${SKBUILD_PROJECT_VERSION}
  DESCRIPTION "C++ bindings for Iris Dynamics orcaSDK"
  LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 14)

find_package(orcaSDK REQUIRED PATHS C:/Users/JakeTaranov/pyActuator/orcaSDK/build)


add_subdirectory(third_party/pybind11 pybind11)

pybind11_add_module(_pyActuator
    bindings/PyActuator.cpp
)

target_link_libraries(_pyActuator PRIVATE orcaSDK::core)

install(TARGETS _pyActuator LIBRARY DESTINATION pyActuator)
