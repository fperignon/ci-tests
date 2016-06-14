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
set(PROJECT_NAME ci-tests)
set(PROJECT_NAME_CAP ci-tests)


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
    set(DOCKER_REPOSITORY ci-tests)
    set(DOCKER_CMAKE_FLAGS ${CMAKE_ARGS_FROM_CACHE};-DWITH_DOCKER=0;-V)
    include(Docker)
    
    add_docker_targets(
      DOCKER_IMAGE ${DOCKER_IMAGE}
      DOCKER_TEMPLATE ${DOCKER_TEMPLATE}
      DOCKER_IMAGE_DIR ${DOCKER_IMAGE_DIR}
      DOCKER_REPOSITORY ${DOCKER_REPOSITORY}
      DOCKER_CMAKE_FLAGS ${DOCKER_CMAKE_FLAGS}
      DOCKER_SHARED_DIRECTORIES ${DOCKER_SHARED_DIRECTORIES})
      
    project(${PROJECT_NAME} NONE)
  else()
    message(FATAL_ERROR "Cannot find docker.")
  endif()
endif()
