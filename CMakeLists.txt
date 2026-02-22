cmake_minimum_required(VERSION 3.10)
project(gis VERSION 0.1.0)

# generate compile_commands.json so editors like VS Code can pick up include paths
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

#include(CTest)
#enable_testing()

find_package( OpenCV REQUIRED )
# locate PROJ library via pkg-config (Arch provides proj.h)
find_package(PkgConfig REQUIRED)
pkg_check_modules(PROJ REQUIRED proj)

add_executable(gis main.cpp)

target_include_directories(gis PRIVATE ${OpenCV_INCLUDE_DIRS} ${PROJ_INCLUDE_DIRS})
target_link_libraries(gis ${OpenCV_LIBS} ${PROJ_LIBRARIES})


#set(CPACK_PROJECT_NAME ${PROJECT_NAME})
#set(CPACK_PROJECT_VERSION ${PROJECT_VERSION})
#include(CPack)
