from machinery.ci_task import CiTask

siconos_default = CiTask(
    ci_config='default',
    distrib='ubuntu:14.04',
    #pkgs=['build-base', 'gcc', 'gfortran', 'gnu-c++', 'atlas-lapack', 'lpsolve', 'python-env'],
    srcs=['.'],
    targets={'.': ['docker-build', 'docker-ctest']})

siconos_debian_mechanisms = siconos_default.copy()(
    ci_config='with_mechanisms',
    add_pkgs=['wget', 'bash', 'bullet', 'h5py', 'oce-pythonocc-deps'],
    #with_examples=True,
    distrib='debian:latest')


# dispatch based on hostname and distrib type (to min. disk requirement)

known_tasks = {'siconos---vm0':
               (siconos_default,)}
