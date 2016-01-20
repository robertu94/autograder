#!/bin/bash

if [ "$1" == "pass" ]; then
	echo "stdout"
	echo "stderr" >&2
	exit 0
elif [ "$1" == "fail" ]; then
	echo "stdout"
	echo "stderr" >&2
	exit 1
elif [ "$1" == "timeout" ]; then
	echo "stdout"
	echo "stderr" >&2
	for i in {1..10}; do sleep 1; done
fi
