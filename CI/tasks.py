from machinery.ci_task import CiTask

citests_default = CiTask(
    ci_config='default',
    distrib='ubuntu:14.04',
    pkgs=['build-base', 'gcc', 'python-env'],
    srcs=['.'],
    targets={'.': ['docker-build', 'docker-ctest']}
    )
# dispatch based on hostname and distrib type (to min. disk requirement)


debian_oce = citests_default.copy()(
    #ci_config='with_mechanisms',
    add_pkgs=['wget', 'bash', 'bullet', 'h5py', 'oce-pythonocc-deps'],
    #with_examples=True,
    distrib='debian:latest')


known_tasks = {'citests---vm0':
               (citests_default,)}
