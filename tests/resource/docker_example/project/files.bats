#!/usr/local/bin/bats -t

@test "Makefile exists" {
	run test -f 'Makefile'
	[ "$status" -eq 0 ]
}

@test "Fizzbuzz.c exists" {
	run test -f 'fizzbuzz.c'
	[ "$status" -eq 0 ]
}
