#!/usr/bin/env bats

@test "testcase 1" {
	run ./fizzbuzz 1
	[ "$status" -eq 0 ]
	[ "$output" = "" ]
}
@test "testcase 2" {
	run ./fizzbuzz 2
	[ "$status" -eq 0 ]
	[ "$output" = "buzz" ]
}
@test "testcase 3" {
	run ./fizzbuzz 3
	[ "$status" -eq 0 ]
	[ "$output" = "fizz" ]
}
@test "testcase 4" {
	run ./fizzbuzz 4
	[ "$status" -eq 0 ]
	[ "$output" = "buzz" ]
}
@test "testcase 5" {
	run ./fizzbuzz 5
	[ "$status" -eq 0 ]
	[ "$output" = "" ]
}
@test "testcase 6" {
	run ./fizzbuzz 6
	[ "$status" -eq 0 ]
	[ "$output" = "fizzbuzz" ]
}
@test "testcase invalid" {
	run ./fizzbuzz fizzbuzz
	[ "$status" -eq 1 ]
	[ "$output" = "" ]
}
@test "testcase no args" {
	run ./fizzbuzz 
	[ "$status" -eq 1 ]
	[ "$output" = "" ]
}
