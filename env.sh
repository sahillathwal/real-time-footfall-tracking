#rtft_docker_interface
export RTFT_DOCKER_PATH=$(realpath $(dirname "${BASH_SOURCE[0]:-$0}"))
rdi() { python3 $RTFT_DOCKER_PATH/scripts/docker_interface.py "$@" ; }