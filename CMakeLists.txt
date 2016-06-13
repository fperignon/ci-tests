#===============================================================================

# ============= Global 'standard' cmake Settings =============

# Set minimum version for cmake
cmake_minimum_required(VERSION 3.0.2)

# Set cmake modules directory (i.e. the one which contains all user-defined FindXXX.cmake files among other things)
set(CMAKE_MODULE_PATH ${CMAKE_SOURCE_DIR}/cmake)

# Force out-of-source build
include(OutOfSourcesBuild)


# Get a list of uninitialized cache variables and append
# them to vars.
macro(get_uninitialized_vars vars)
  get_cmake_property(CACHE_VARS CACHE_VARIABLES)
  foreach(CACHE_VAR ${CACHE_VARS})
    get_property(CACHE_VAR_TYPE CACHE ${CACHE_VAR} PROPERTY TYPE)
    if(CACHE_VAR_TYPE STREQUAL "UNINITIALIZED")
      list(APPEND ${vars} -D${CACHE_VAR}=${${CACHE_VAR}})
    endif()
  endforeach()
endmacro()



# Check/set uninitialized cache variables (--> for docker config)
get_uninitialized_vars(CMAKE_ARGS_FROM_CACHE)

# cmake project name
set(PROJECT_NAME testci)
set(PROJECT_NAME_CAP testci)

if(USER_OPTIONS_FILE)
  get_filename_component(input_file ${USER_OPTIONS_FILE} NAME)
  get_filename_component(path_to_file ${USER_OPTIONS_FILE} PATH)
  find_file(filefound NAMES ${input_file}
    PATHS ${path_to_file} ${CMAKE_BINARY_DIR} ${CMAKE_SOURCE_DIR}
    )
  if(NOT ${filefound}-NOTFOUND)
    configure_file(${path_to_file}/${input_file} ${CMAKE_SOURCE_DIR}/${input_file})
  else()
    message(FATAL_ERROR "Cannot find file ${USER_OPTIONS_FILE}")
  endif()
  message("\n !!!!! Load user-defined options set from file ${filefound} !!!!! \n")
  include(${input_file})
  # copy user file to binary dir, just for 'visual' check.
  configure_file(${input_file} ${input_file} COPYONLY)
else()
  include(default_options)
endif()

# Configurations used for continuous integration
if(CI_CONFIG)
  string(REPLACE "," ";" CI_CONFIG_LIST ${CI_CONFIG})
  FOREACH(_CI ${CI_CONFIG_LIST})
    include(CI/config/${_CI}.cmake)
  ENDFOREACH(_CI CI_CONFIG_LIST)
endif()

# ---------- Docker or not docker ... ------------------------
if(WITH_DOCKER)
  find_program(HAVE_DOCKER docker)
  if(HAVE_DOCKER)
    set(DOCKER_MKSENV_COMMAND ${CMAKE_SOURCE_DIR}/CI/machinery/mksenv.py)
    set(DOCKER_MKSENV_INPUT ${CMAKE_SOURCE_DIR}/CI/config/ci-tests.yml)
    set(DOCKER_REPOSITORY ci-test)
    set(DOCKER_CMAKE_FLAGS ${CMAKE_ARGS_FROM_CACHE};-DWITH_DOCKER=0;-V)
    set(DOCKER_CTEST_DRIVER ${CMAKE_SOURCE_DIR}/CI/machinery/CTestDriver.cmake)
    include(Docker)
    
    add_docker_targets(
      DOCKER_IMAGE ${DOCKER_IMAGE}
      DOCKER_TEMPLATE ${DOCKER_TEMPLATE}
      DOCKER_IMAGE_DIR ${DOCKER_IMAGE_DIR}
      DOCKER_REPOSITORY ${DOCKER_REPOSITORY}
      DOCKER_CMAKE_FLAGS ${DOCKER_CMAKE_FLAGS}
      DOCKER_SHARED_DIRECTORIES ${DOCKER_SHARED_DIRECTORIES}
      DOCKER_CTEST_DRIVER ${DOCKER_CTEST_DRIVER})
      
    project(${PROJECT_NAME} NONE)
  else()
    message(FATAL_ERROR "Cannot find docker.")
  endif()
endif()