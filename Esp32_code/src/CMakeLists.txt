# This file was automatically generated for projects
# without default 'CMakeLists.txt' file.

FILE(GLOB_RECURSE app_sources ${CMAKE_SOURCE_DIR}/src/*.*)
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -w")
idf_component_register(SRCS ${app_sources})
