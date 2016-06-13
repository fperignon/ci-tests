from machinery.ci_task import CiTask

citests_default = CiTask(
    ci_config='default',
    distrib='debian:latest',
    pkgs=['build-base', 'gcc', 'python-env'],
    srcs=['.'],
    #targets={'.': ['docker-build', 'docker-ctest']}
    )
# dispatch based on hostname and distrib type (to min. disk requirement)

known_tasks = {'citests---vm0':
               (citests_default,)}
