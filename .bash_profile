#!/bin/bash

if [ -f ~/.bashrc ]; then
   source ~/.bashrc
fi

export PATH="$PATH:/usr/local/mysql/bin:/usr/local/git/bin"