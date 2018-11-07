# Copyright 1999-2017 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2

EAPI=6

PYTHON_COMPAT=( python{2_7,3_4,3_5,3_6} )

inherit distutils-ir1

DESCRIPTION="Generate a package-manager friendly mouse brain atlases collection"
HOMEPAGE="https://github.com/IBT-FMI/mouse-brain-atlases_generator"

LICENSE="GPL-3"
SLOT="0"
IUSE="+atlases labbookdb test"
KEYWORDS=""

# Numpy dependency to circumvent scikits_learn dependency bug:
# https://bugs.gentoo.org/653052
RDEPEND="
	>=dev-python/numpy-1.13.3[${PYTHON_USEDEP}]
	>=sci-biology/fsl-5.0.9
	sci-libs/nibabel[${PYTHON_USEDEP}]
	sci-biology/ants
	sci-biology/nilearn[${PYTHON_USEDEP}]
	>=sci-libs/scikits_image-0.13.0[${PYTHON_USEDEP}]
	>=media-gfx/blender
	dev-python/pynrrd
	"

src_unpack() {
	cp -r -L "$DOTGENTOO_PACKAGE_ROOT" "$S"
}

python_prepare_all() {
	find . -type f -exec \
		sed -i "s:/usr/share/mouse-brain-atlases/:${EPREFIX}/usr/share/mouse-brain-atlases/:g" {} +
	distutils-r1_python_prepare_all
}

python_test() {
	distutils_install_for_testing
	export MPLBACKEND="agg"
	export PATH=${TEST_DIR}/scripts:$PATH
	export PYTHONIOENCODING=utf-8
	pytest || die
	for i in examples/*.py; do
		echo "Executing ${EPYTHON} ${i}"
		${EPYTHON} "$i" || die "Example Python script $i failed with ${EPYTHON}"
	done
	./test_scripts.sh || die "Test scripts failed."
}
