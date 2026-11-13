cmake_minimum_required(VERSION 3.5)
project(tortoisebot_description)

# Find dependencies
find_package(ament_cmake REQUIRED)
# These are needed if you have C++ nodes, but good to keep for consistency
find_package(rclcpp REQUIRED)
find_package(urdf REQUIRED)

# Install directories
# Note: Removing the trailing slash (e.g., 'urdf' instead of 'urdf/') 
# ensures the folder itself is copied into the destination.
install(
  DIRECTORY
    urdf
    launch
    rviz
  DESTINATION share/${PROJECT_NAME}
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()