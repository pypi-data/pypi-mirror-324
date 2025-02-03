ncrystal-plugin-UraniumOxideData
================================

Plugin for NCrystal (release 4 and later), which provides the user with extra
NCMAT data files for uranium oxide (uraninite, UO2), with phonon densities
optimised for various temperatures.

After installation, use for instance `nctool --browse` to see the provided file
names. For instance, to use the material at 1200K, one would use a cfg-string
like `"plugins::UraniumOxideData/UO2_sg225_UraniumOxide_vdos1200K.ncmat"`.

Phonon density curves in the files are taken from: "Combining density functional
theory and Monte Carlo neutron transport calculations to study the phonon
density of states of UO2 up to 1675 K by inelastic neutron scattering"
G. Noguere, J. P. Scotta, S. Xu, A. Filhol, J. Ollivier, E. Farhi,
Y. Calzavarra, S. Rols, B. Fak, J.-M. Zanotti, and Q. Berrod Phys. Rev. B 102,
134312 - Published 30 October 2020 https://doi.org/10.1103/PhysRevB.102.134312

Crystal structures in the files are based on the cif file of the entry 0011728
in the AMCSD. An additional reference for the structure is: Wyckoff R W G,
Crystal Structures, vol. 1, p. 239-444, 1963
(https://www.crystallography.net/cod/9009049.html).
