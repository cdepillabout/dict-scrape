

#!/bin/bash

if [ -d 'test' ]; then
    dir='test'
else
    dir='.'
fi

if [ x$coverage != x ]; then
    args="--with-coverage"
else
    args=""
    echo "Call with coverage=1 to run coverage tests"
fi
#(cd $dir && nosetests2 -vs $args --cover-package=anki $@)
PYTHONPATH="$PYTHONPATH:.:.." (set && cd $dir && nosetests2 -vs $args $@)
