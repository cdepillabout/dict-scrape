#!/bin/bash

# get the directory this script is being run from
dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

if [ x$coverage != x ]; then
    args="--with-coverage"
else
    args=""
    echo "Call with coverage=1 to run coverage tests"
fi
#(cd $dir && nosetests2 -vs $args --cover-package=anki $@)
(cd $dir && PYTHONPATH="$PYTHONPATH:.:$dir/test/support/words/" nosetests2 -vs $args "$@" )
