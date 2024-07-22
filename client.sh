#! env bash

[ $# -ge 2 ] || {
    echo "syntax $0 name description"
    exit 1
}

SERVER=http://127.0.0.1:5000
ENDPOINT=${SERVER}/drinks
CONTENT_JSON='Content-Type: application/json'

NAME=${1}
DESCRIPTION=${2}

curl "${ENDPOINT}" -X POST --header "${CONTENT_JSON}" --data @- <<EOF
{ 
  "name": "${NAME}",
  "description": "${DESCRIPTION}"
} 
EOF