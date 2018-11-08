# Copyright 1999-2017 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2

EAPI=6

DESCRIPTION="Virtual : Generate a package-manager friendly mouse brain atlases collection"

SLOT="0"
KEYWORDS=""

RDEPEND="
	>=dev-python/numpy-1.13.3
	>=sci-biology/fsl-5.0.9
	sci-libs/nibabel
	sci-biology/ants
	sci-biology/nilearn
	>=sci-libs/scikits_image-0.13.0
	media-gfx/blender
	dev-python/pynrrd
	"
