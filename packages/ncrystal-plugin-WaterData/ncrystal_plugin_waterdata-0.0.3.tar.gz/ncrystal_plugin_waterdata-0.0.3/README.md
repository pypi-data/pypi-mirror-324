ncrystal-plugin-WaterData
=========================

Plugin for NCrystal (release 4 and later), which provides the user with extra
NCMAT data files for light and heavy water, covering a wider range of
temperatures compared to what is found in the NCrystal standard library.

After installation, use for instance `nctool --browse` to see the provided file
names. For instance, to use heavy water at 10C, one would use a cfg-string like
`"plugins::water/LiquidHeavyWaterD2O_T283.6K.ncmat"`.

The data files were based on ENDF/B-VIII.0 CAB scattering kernels, which are
described in:

J.I. Márquez Damián, J.R. Granada, D.C. Malaspina, "CAB models for water: A new
evaluation of the thermal neutron scattering laws for light and heavy water in
ENDF-6 format", Annals of Nuclear Energy, Volume 65 (2014), Pages 280-289,
(https://doi.org/10.1016/j.anucene.2013.11.014).

Please find more references therein, as well as in the headers of the included
NCMAT files (browse with `nctool --extract <filename>` which includes the inline
references from the source ENDF files.

After conversion with ncrystal_endf2ncmat, the files were post-edited manually
to correct the densities to correspond to standard pressure. The headers of the
NCMAT files also contains comments about the source of these density data. Note
that the NCrystal cfg-string `density` parameter, can be used to modify these
hardwire densities, if needed.
