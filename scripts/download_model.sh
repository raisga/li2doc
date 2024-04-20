#!/bin/sh

# Loads env variables
set -o allexport
eval $(cat '.env' | sed -e '/^#/d;/^\s*$/d' -e 's/\(\w*\)[ \t]*=[ \t]*\(.*\)/\1=\2/' -e "s/=['\"]\(.*\)['\"]/=\1/g" -e "s/'/'\\\''/g" -e "s/=\(.*\)/='\1'/g")
set +o allexport

# Check if /models/$MODEL_NAME exists, if not, download it
if [[ ! -f "./" ]]; then
    echo "📩 Downloading $MODEL_NAME \n\n"
    wget $MODEL_URL -O ./$MODEL_NAME
fi
