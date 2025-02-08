#rtftc12_docker_interface
export rtftc12_DOCKER_PATH=$(realpath $(dirname "${BASH_SOURCE[0]:-$0}"))
rdi() { python3 $rtftc12_DOCKER_PATH/scripts/docker_interface.py "$@" ; }