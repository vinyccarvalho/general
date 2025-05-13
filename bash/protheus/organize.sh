#!/bin/bash

ini_file=$1

ini_content="$(cat $ini_file | dos2unix | tr '[:upper:]' '[:lower:]' | sed -r 's|\\|\\\\|g')"

ini_sessions=$(grep -E '^\[' <<< "$ini_content" | sort)

while read session; do
        unset session_content

        while read line; do
                if grep -Eq '^\[' <<< $line; then

                        if [[ "$session" == "$line" ]]; then
                                show_line=1 && continue
                        else
                                show_line=0
                        fi
                fi

                [[ $show_line == 1 ]] && [[ "$line" != "" ]] && session_content+="$line"$'\n'

        done <<< "$ini_content"

        session_content_sort=$(sort <<< "$session_content")
        echo -n "$session"
        #echo "$session_content_sort"
        printf "%s\n" "$session_content_sort"
        echo

done <<< "$ini_sessions"

