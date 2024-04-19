#!/bin/sh

# Loads env variables
set -o allexport
eval $(cat '.env' | sed -e '/^#/d;/^\s*$/d' -e 's/\(\w*\)[ \t]*=[ \t]*\(.*\)/\1=\2/' -e "s/=['\"]\(.*\)['\"]/=\1/g" -e "s/'/'\\\''/g" -e "s/=\(.*\)/='\1'/g")
set +o allexport

echo "💿 Loading $MODEL_NAME \n\n"

# Load the model to nitro
curl -s --location 'http://localhost:3928/inferences/llamacpp/loadModel' \
--header 'Content-Type: application/json' \
--data "{
    \"llama_model_path\": \"$(pwd)/models/$MODEL_NAME\",
    \"ctx_len\": 2048,
    \"ngl\": 32,
    \"embedding\": false
}"
