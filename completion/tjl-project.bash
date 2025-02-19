# Bash completion for TJL Project Setup Tool
# Author: Ben Adenle
# Email: ben@techjamlabs.com

_tjl_project_completion() {
    local cur prev opts templates environments
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"
    
    # Main options
    opts="--path --environments --template --help --version"
    
    # Available templates
    templates="basic microservice webapp library"
    
    # Common environments
    environments="local,dev,staging,prod"

    case ${prev} in
        --template)
            # Complete template names
            COMPREPLY=( $(compgen -W "${templates}" -- ${cur}) )
            return 0
            ;;
        --path)
            # Complete directory paths
            COMPREPLY=( $(compgen -d -- ${cur}) )
            return 0
            ;;
        --environments)
            # Suggest common environment combinations
            COMPREPLY=( $(compgen -W "${environments}" -- ${cur}) )
            return 0
            ;;
        *)
            # If it starts with a dash, complete from options
            if [[ ${cur} == -* ]] ; then
                COMPREPLY=( $(compgen -W "${opts}" -- ${cur}) )
                return 0
            fi
            
            # Otherwise, suggest directories for project creation
            COMPREPLY=( $(compgen -d -- ${cur}) )
            return 0
            ;;
    esac
}

complete -F _tjl_project_completion tjl-project
complete -F _tjl_project_completion tjl