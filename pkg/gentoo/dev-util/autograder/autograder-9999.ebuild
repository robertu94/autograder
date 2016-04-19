# Copyright 1999-2016 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2
# $Id$

EAPI=5

PYTHON_COMPAT=( python{3_3,3_4,3_5} )

inherit distutils-r1

if [[ "${PV}" == "9999" ]]; then
	EGIT_REPO_URI="https://github.com/robertu94/autograder.git"
	inherit git-r3
else
	SRC_URI="https://github.com/robertu94/autograder/archive/${PV}.tar.gz -> ${P}.tar.gz"
	KEYWORDS="~amd64 ~x86"
fi

DESCRIPTION="A automatic testing and grading framework in python"
HOMEPAGE="https://www.cs.clemson.edu/acm"

LICENSE="BSD"
SLOT="0"
IUSE="doc docker git mail mercurial subversion"

RDEPEND="
	docker? ( app-emulation/docker )
	git? ( dev-vcs/git )
	mail? ( virtual/mta )
	mercurial? ( dev-vcs/mercurial )
	subversion? ( dev-vcs/subversion )

	doc? ( app-text/pandoc )
"
DEPEND=""

src_prepare() {
	if use doc; then
		pandoc -t html -s docs/architecture.markdown -o docs/architecture.html
		pandoc -t html -s docs/developer.markdown -o docs/developer.html
	fi

	distutils-r1_src_prepare
}

src_install() {
	if use doc; then
		dodoc docs/architecture.html
		dodoc docs/developer.html
	fi

	distutils-r1_src_install
}
