# Install script for directory: /home/wellyowo/locobot_sim/locobot_ws/src/ThirdParty/ecl/ecl_core/ecl_streams/src/lib

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/home/wellyowo/locobot_sim/locobot_ws/install/ecl_streams")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

# Set default install directory permissions.
if(NOT DEFINED CMAKE_OBJDUMP)
  set(CMAKE_OBJDUMP "/usr/bin/objdump")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libecl_streams.so.1.2.1" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libecl_streams.so.1.2.1")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libecl_streams.so.1.2.1"
         RPATH "")
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE SHARED_LIBRARY FILES "/home/wellyowo/locobot_sim/locobot_ws/build/ecl_streams/src/lib/libecl_streams.so.1.2.1")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libecl_streams.so.1.2.1" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libecl_streams.so.1.2.1")
    file(RPATH_CHANGE
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libecl_streams.so.1.2.1"
         OLD_RPATH "/home/wellyowo/locobot_sim/locobot_ws/install/ecl_devices/lib:/home/wellyowo/locobot_sim/locobot_ws/install/ecl_formatters/lib:/home/wellyowo/locobot_sim/locobot_ws/install/ecl_threads/lib:/home/wellyowo/locobot_sim/locobot_ws/install/ecl_time/lib:/home/wellyowo/locobot_sim/locobot_ws/install/ecl_time_lite/lib:/home/wellyowo/locobot_sim/locobot_ws/install/ecl_exceptions/lib:/home/wellyowo/locobot_sim/locobot_ws/install/ecl_errors/lib:/home/wellyowo/locobot_sim/locobot_ws/install/ecl_type_traits/lib:"
         NEW_RPATH "")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libecl_streams.so.1.2.1")
    endif()
  endif()
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libecl_streams.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libecl_streams.so")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libecl_streams.so"
         RPATH "")
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE SHARED_LIBRARY FILES "/home/wellyowo/locobot_sim/locobot_ws/build/ecl_streams/src/lib/libecl_streams.so")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libecl_streams.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libecl_streams.so")
    file(RPATH_CHANGE
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libecl_streams.so"
         OLD_RPATH "/home/wellyowo/locobot_sim/locobot_ws/install/ecl_devices/lib:/home/wellyowo/locobot_sim/locobot_ws/install/ecl_formatters/lib:/home/wellyowo/locobot_sim/locobot_ws/install/ecl_threads/lib:/home/wellyowo/locobot_sim/locobot_ws/install/ecl_time/lib:/home/wellyowo/locobot_sim/locobot_ws/install/ecl_time_lite/lib:/home/wellyowo/locobot_sim/locobot_ws/install/ecl_exceptions/lib:/home/wellyowo/locobot_sim/locobot_ws/install/ecl_errors/lib:/home/wellyowo/locobot_sim/locobot_ws/install/ecl_type_traits/lib:"
         NEW_RPATH "")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libecl_streams.so")
    endif()
  endif()
endif()

