#! /usr/bin/env bash

function blue_assistant_chat() {
    local options=$1
    local do_dryrun=$(abcli_option_int "$options" dryrun 0)
    local do_download=$(abcli_option_int "$options" download 0)
    local do_upload=$(abcli_option_int "$options" upload $(abcli_not $do_dryrun))

    local chat_options=$2
    local interactive=$(abcli_option_int "$options" interact 1)

    local object_name=$(abcli_clarify_object $3 chat-$(abcli_string_timestamp))
    [[ "$do_download" == 1 ]] &&
        abcli_download - $object_name

    abcli_eval dryrun=$do_dryrun \
        python3 -m blue_assistant.chat \
        chat \
        --object_name $object_name \
        --interactive $interactive \
        "${@:4}"
    [[ $? -ne 0 ]] && return 1

    [[ "$do_upload" == 1 ]] &&
        abcli_upload - $object_name

    return 0
}
