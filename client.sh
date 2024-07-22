#! env bash

usage () { echo "How to use"; }
die () { usage;echo "${*}";exit 1; }


DEBUG=true
debug () { $DEBUG && echo "${*}"; }

debug "START: OPTIND=$OPTIND \$#=$#"

OP=LIST
options=':adgl'
while getopts $options option
do
    debug "GETOPTS: OPTIND=$OPTIND INDEX=$((OPTIND - 1)) \$option=$option \$#=$#"
    case "$option" in
        a  ) OP=ADD;;
        d  ) OP=DELETE;;
        g  ) OP=GET;;
        l  ) OP=LIST;;
        # j  ) j_arg=$OPTARG;;
        h  ) usage; exit;;
        \? ) echo "Unknown option: -$OPTARG" >&2; exit 1;;
        :  ) echo "Missing option argument for -$OPTARG" >&2; exit 1;;
        *  ) echo "Unimplemented option: -$option" >&2; exit 1;;
    esac
done

debug "END: OPTIND=$OPTIND  \$#=$#"
if ((OPTIND == 1))
then
    echo "No options specified"
    OP=LIST
fi

shift $((OPTIND - 1))
debug "SHIFT: OPTIND=$OPTIND  \$#=$#"

if (($# == 0))
then
    echo "No positional arguments specified"
fi

process () {
  case ${OP} in:
    GET) METHOD=GET; [ $# -ge 1 ] && JSON=$(get_drink ${1}) || die "get requires id";;
    ADD) METHOD=POST; [ $# -ge 2 ] && JSON=$(add_drink "${@}") || die "add requires name, description";;
    DELETE) METHOD=POST; [ $# -ge 2 ] && JSON=$(delete_drink ${1}) || die "delete requires id";;
    LIST) METHOD=GET; JSON=$(list_drinks)
  esac
}

call_server () {
  SERVER=http://127.0.0.1:5000
  ENDPOINT=${SERVER}/drinks
  CONTENT_JSON='Content-Type: application/json'

  # NAME=${1}
  # DESCRIPTION=${2}

  # curl "${ENDPOINT}" -X POST --header "${CONTENT_JSON}" --data @- <<EOF
  # { 
    # "name": "${NAME}",
    # "description": "${DESCRIPTION}"
  # } 
  # EOF
}

