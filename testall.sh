#!/bin/bash

ls *.py */*.py|sed -e 's%.py$%%' -e 's%/%.%'|xargs python -m unittest -v
RESULT=$?

CHECKCOUNT=`ls checks/[^_]*.py|wc -l`
CHECKCOUNT_SUCCESS=`grep -l test_success checks/[^_]*.py|wc -l`
CHECKCOUNT_FAIL=`grep -l test_fail checks/[^_]*.py|wc -l`

if [ ${CHECKCOUNT_SUCCESS} -lt ${CHECKCOUNT} ]; then
    echo "Not all checks have tests for success cases (${CHECKCOUNT_SUCCESS}/${CHECKCOUNT})."
    RESULT=1
fi

if [ ${CHECKCOUNT_FAIL} -lt ${CHECKCOUNT} ]; then
    echo "Not all checks have tests for failure cases (${CHECKCOUNT_FAIL}/${CHECKCOUNT})."
    RESULT=1
fi

exit $RESULT
