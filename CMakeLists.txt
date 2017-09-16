cmake_minimum_required(VERSION 2.8)

project( SwamHost )

find_package( OpenCV REQUIRED )
include_directories( ${OpenCV_INCLUDE_DIRS} )
add_executable( SwarmHost main.cpp )
target_link_libraries( SwarmHost ${OpenCV_LIBS} )
