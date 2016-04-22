find -name ".hg" -exec rm -rf {} \+
for dir in student*
do
	pushd $dir
	hg init
	hg add *
	hg commit -m "Creating repo"
	popd
done
