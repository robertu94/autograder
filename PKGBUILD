# Maintainer: Robert Underwood <rr.underwood at gamil.com>
pkgname=autograder-git
pkgver=0.0.1
pkgrel=1
pkgdesc="An autograding framework written in python"
arch=('i686' 'x86_64')
url="http://www.cs.clemson.edu/acm"
licence=('BSD')
depends=("python")
optdepends=("git: for git repository support" \
	        "svn: for svn repository support" \
	        "mercurial: for hg repository support" \
	        "docker: for containerized test support")
md5sums=()

_gitname="autograder"
_gitrepo="git@github.com:robertu94/autograder.git"

build() {
	cd $srcdir
	if [[ -d "$_gitname" ]]; then
		cd "$_gitname" && git pull origin
	else
		git clone "$_gitrepo" "$_gitname"
	fi
	rm -rf "$srcdir/$_gitname-build"
	git clone $srcdir/$_gitname "$srcdir/$_gitname-build"
	cd $srcdir/$_gitname
}

package() {
	cd $srcdir/$_gitname-build
	python setup.py install --root="$pkgdir/" --optimize=1
}
