cmake_minimum_required(VERSION 2.6)

#### Variable Definitions
set(projectName
    SwarmHost
)

## Version Setting

set (SwarmHost_VERSION_MAJOR 0)
set (SwarmHost_VERSION_MINOR 1)
set (SwarmHost_VERSION_PATCH 0)


#### File Location Includes
include_directories(
    include
    ${PROJECT_BINARY_DIR}
    )
set( SOURCES
    src/main.cpp
    src/arucoTest.cpp
)
set( HEADERFILES
    include/arucoTest.h
)

#### File Configuration 
## Add version numbering to configure file
configure_file(
    "${PROJECT_SOURCE_DIR}/include/SwarmHostConfig.h.in"
    "${PROJECT_BINARY_DIR}/include/SwarmHostConfig.h"
)


#### Library Inclusion
find_package( OpenCV REQUIRED )

include_directories( /usr/include/readline )

#### Build the project

add_executable( ${projectName} ${SOURCES} )
target_link_libraries(${projectName} ${OpenCV_LIBS} readline)
