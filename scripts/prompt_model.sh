#!/bin/sh

curl -s --location 'http://localhost:3928/v1/chat/completions' \
--header 'Content-Type: application/json' \
--data "{
        "messages": [
            {"content": "$1"},
        ],
        "stream": true,
        "max_tokens": 100,
        "stop": ["hello"],
        "frequency_penalty": 0,
        "presence_penalty": 0,
        "temperature": 0.7
    }"