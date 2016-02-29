#!/bin/bash

setup_git() {
	dir=$1
	rm -rf $dir
	mkdir -p $dir
	pushd $dir
	git init
	git config user.name "John Doe"
	git config user.email "testing@example.com"
	add_files .
	git add .
	git commit -m 'first commit'
	popd
}

setup_hg() {
	dir=$1
	rm -rf $dir
	mkdir -p $dir
	pushd $dir
	hg init 
	add_files .
	hg add .
	hg commit --config=ui.username="John Doe" -m 'first commit'
	popd
}
setup_svn() {
	dir=$1
	rm -rf $dir
	rm -rf test/svn-test
	mkdir -p test
	svnadmin create test/svn-test
	svn co file://$(readlink -f test/svn-test) $dir
	pushd $dir
	add_files .
	svn add *
	svn commit -m 'First commit'
	popd
}

add_files() {
	mkdir -p $1
	echo "testing 123" > $1/test.in
	echo "testing 456" > $1/test2.in
	mkdir $1/test
	echo "testing 789" > $1/test/test3.in
}

change_files() {
	echo "123456" >> $1/test.in
	echo "testing abc" > $1/test4.in
	mkdir $1/test2
	mkdir $1/test3
	echo "testing 789" > $1/test/test5.in
}
$1 $2
