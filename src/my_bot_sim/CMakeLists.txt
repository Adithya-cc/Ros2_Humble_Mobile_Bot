cmake_minimum_required(VERSION 3.8)
project(my_bot_sim)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclpy REQUIRED)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  set(ament_cmake_copyright_FOUND TRUE)
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

install(DIRECTORY 
  launch
  urdf
  rviz
  worlds
  config
  DESTINATION share/${PROJECT_NAME}
)
install(PROGRAMS
scripts/lidar_filter.py
scripts/finding_obstracle.py
scripts/object_follow.py
scripts/ball_move.py
scripts/obj_type.py
DESTINATION lib/${PROJECT_NAME}
)
ament_package()
