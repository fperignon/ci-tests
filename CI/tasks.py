from machinery.ci_task import CiTask
import os

#
# 1. where the packages are defined
#
database = os.path.join('config', 'ci-tests.yml')

#
# 2. the default task
#
default = CiTask(
    ci_config='default',
    distrib='ubuntu:14.04',
    pkgs=['build-base', 'gcc', 'gfortran', 'gnu-c++', 'atlas-lapack',
          'lpsolve', 'python-env'],
    srcs=['.'],
    targets={'.': ['docker-build', 'docker-ctest']})


citests_default = default


#
# 4. dispatch based on hostname and distrib type (to min. disk requirement)
#
known_tasks = {'siconos---vm0':
               ci_tests_default,)}
