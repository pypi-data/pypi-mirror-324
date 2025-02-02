#! /usr/bin/env bash

function test_blue_assistant_chat() {
    local options=$1

    abcli_eval ,$options \
        blue_assistant_chat \
        ~upload,$options \
        ~interact \
        test_blue_assistant_chat-$(abcli_string_timestamp_short) \
        "${@:2}"
}
