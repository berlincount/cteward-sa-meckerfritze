#!/bin/bash

ls *.py */*.py|sed -e 's%.py$%%' -e 's%/%.%'|xargs python -m unittest -v
