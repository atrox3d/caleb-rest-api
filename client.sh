#! env bash

usage () { echo "How to use"; }
die () { usage;echo "${*}";exit 1; }

DEBUG=true
debug () { $DEBUG && echo "${*}"; }



debug "START: OPTIND=$OPTIND \$#=$#"

# default
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

shift $((OPTIND - 1))
debug "SHIFT: OPTIND=$OPTIND  \$#=$#"

[ $# -eq 0 ] && echo "No positional arguments specified"

process () {
	case "${OP}" in
		GET) [ $# -ge 1 ] && JSON=$(get_drink ${1}) || die "get requires id";;
		ADD) [ $# -ge 2 ] && JSON=$(add_drink "${@}") || die "add requires name, description";;
		DELETE) [ $# -ge 1 ] && JSON=$(delete_drink ${1}) || die "delete requires id";;
		LIST) JSON=$(list_drinks)
  	esac
	echo "${JSON}"
}

SERVER=http://127.0.0.1:5000
ENDPOINT=${SERVER}/drinks
CONTENT_JSON='Content-Type: application/json'

add_drink () {
	NAME=${1}
	DESCRIPTION=${2}

	curl -s "${ENDPOINT}" -X POST --header "${CONTENT_JSON}" --data @- <<-EOF
	{ 
		"name": "${NAME}",
		"description": "${DESCRIPTION}"
	} 
	EOF
}

get_drink () {
	ID=${1}
	curl -s "${ENDPOINT}/${ID}" -X GET
}

delete_drink () {
	ID=${1}
	curl -s "${ENDPOINT}/${ID}" -X DELETE
}

list_drinks () {
	curl -s "${ENDPOINT}" -X GET
}

process "${@}"
