# generated from ament/cmake/core/templates/nameConfig.cmake.in

# prevent multiple inclusion
if(_kobuki_bumper2pc_CONFIG_INCLUDED)
  # ensure to keep the found flag the same
  if(NOT DEFINED kobuki_bumper2pc_FOUND)
    # explicitly set it to FALSE, otherwise CMake will set it to TRUE
    set(kobuki_bumper2pc_FOUND FALSE)
  elseif(NOT kobuki_bumper2pc_FOUND)
    # use separate condition to avoid uninitialized variable warning
    set(kobuki_bumper2pc_FOUND FALSE)
  endif()
  return()
endif()
set(_kobuki_bumper2pc_CONFIG_INCLUDED TRUE)

# output package information
if(NOT kobuki_bumper2pc_FIND_QUIETLY)
  message(STATUS "Found kobuki_bumper2pc: 1.0.0 (${kobuki_bumper2pc_DIR})")
endif()

# warn when using a deprecated package
if(NOT "" STREQUAL "")
  set(_msg "Package 'kobuki_bumper2pc' is deprecated")
  # append custom deprecation text if available
  if(NOT "" STREQUAL "TRUE")
    set(_msg "${_msg} ()")
  endif()
  # optionally quiet the deprecation message
  if(NOT ${kobuki_bumper2pc_DEPRECATED_QUIET})
    message(DEPRECATION "${_msg}")
  endif()
endif()

# flag package as ament-based to distinguish it after being find_package()-ed
set(kobuki_bumper2pc_FOUND_AMENT_PACKAGE TRUE)

# include all config extra files
set(_extras "")
foreach(_extra ${_extras})
  include("${kobuki_bumper2pc_DIR}/${_extra}")
endforeach()
