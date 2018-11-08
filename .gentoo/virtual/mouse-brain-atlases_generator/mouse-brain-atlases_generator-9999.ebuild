# Copyright 1999-2017 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2

EAPI=6

PYTHON_COMPAT=( python{2_7,3_4,3_5,3_6} )

inherit distutils-r1

DESCRIPTION="Virtual : Generate a package-manager friendly mouse brain atlases collection"
HOMEPAGE="https://github.com/IBT-FMI/mouse-brain-atlases_generator"

SLOT="0"
KEYWORDS=""



src_unpack() {
	cp -r -L "$DOTGENTOO_PACKAGE_ROOT" "$S"
	}

src_compile() {
	return
}

src_install() {
return
}

#python_prepare_all() {
#	find . -type f -exec \
#		sed -i "s:/usr/share/mouse-brain-atlases/:${EPREFIX}/usr/share/mouse-brain-atlases/:g" {} +
#	distutils-r1_python_prepare_all
#		}



# Numpy dependency to circumvent scikits_learn dependency bug:
# https://bugs.gentoo.org/653052
RDEPEND="
	>=dev-python/numpy-1.13.3[${PYTHON_USEDEP}]
	>=sci-biology/fsl-5.0.9
	sci-libs/nibabel[${PYTHON_USEDEP}]
	sci-biology/ants
	sci-biology/nilearn[${PYTHON_USEDEP}]
	>=sci-libs/scikits_image-0.13.0[${PYTHON_USEDEP}]
	media-gfx/blender
	dev-python/pynrrd
	"

