# MBIplotter
This python program creates a 2D Material Budget map from a TH3D containing the scattering angles of single tracks on a x-y-grid.

### Preparation:

Provide a TH3D with the kink angles in the specified rootfile, e.g. from EUTelescope.

In EUTelescope, this could look like this:
```
histo3D = AIDAProcessor::histogramFactory(this)->
  createHistogram3D( "histo3D", 200, -10, 10, 100, -5, 5, 2000, -40, 40 );
histo3D->setTitle( "kink angle x&y at DUT, medium binning;x_DUT [mm];y_DUT [mm];kink [mrad]" );
```
and
```
histo3D->fill( -xA, -yA, kinkx );
histo3D->fill( -xA, -yA, kinky );
```
with kinkx/kinky being the track's kink angles in mrad.

### Usage:

```
MBIplotter.py ROOTFILE HISTO [-r rebin] [-c cut] [-q quant]
```
