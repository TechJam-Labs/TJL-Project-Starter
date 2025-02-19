#compdef tjl-project tjl

# Zsh completion for TJL Project Setup Tool
# Author: Ben Adenle
# Email: ben@techjamlabs.com

_tjl_project() {
    local curcontext="$curcontext" state line ret=1
    typeset -A opt_args

    _arguments -C \
        '1: :->command' \
        '*: :->args' && ret=0

    case $state in
        command)
            _path_files -/ && ret=0
            ;;
        args)
            local opts=(
                '--path[Specify base path for project creation]:directory:_path_files -/'
                '--environments[Specify comma-separated list of environments]:environments:(local,dev,staging,prod dev,staging,prod local,dev,qa,staging,prod)'
                '--template[Select project template]:template:(basic microservice webapp library)'
                '--help[Show help message]'
                '--version[Show version information]'
            )
            _describe -t opts 'options' opts && ret=0
            ;;
    esac

    return ret
}

_tjl_project "$@"