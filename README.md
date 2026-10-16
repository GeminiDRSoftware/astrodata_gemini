[DRAGONS link]: https://github.com/GeminiDRSoftware/DRAGONS
[astrodata]: https://geminidrsoftware.github.io/astrodata/
[astrodata docs]: https://geminidrsoftware.github.io/astrodata/
[astrodata repo]: https://github.com/GeminiDRSoftware/astrodata/
[documentation]: https://astrodata-gemini.readthedocs.io/en/latest/
[pypi link]: https://pypi.org/project/astrodata-gemini
<!-- [citation link]: https://github.com/GeminiDRSoftware/astrodata_gemini/blob/main/CITATION.md -->
[DRAGONS citation]: https://zenodo.org/records/10841622
<!-- [zenodo DOI link]: -->

<!--
[coverage badge]: https://geminidrsoftware.github.io/astrodata_gemini/badges/coverage.svg
[docs build badge]: https://github.com/GeminiDRSoftware/astrodata_gemini/actions/workflows/documentation.yml/badge.svg
[pypi packaging badge]: https://github.com/GeminiDRSoftware/astrodata_gemini/actions/workflows/publish_pypi.yml/badge.svg
[pypi package version badge]: https://img.shields.io/pypi/v/astrodata_gemini
[source test status badge]: https://github.com/GeminiDRSoftware/astrodata_gemini/actions/workflows/source_tests.yml/badge.svg
[build test status badge]: https://github.com/GeminiDRSoftware/astrodata_gemini/actions/workflows/build_tests.yml/badge.svg
[zenodo DOI badge]: https://img.shields.io/badge/DOI-10.5281%2Fzenodo.14804282-blue.svg <- FIX
-->

<!--
<p align="center">
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/GeminiDRSoftware/astrodata_gemini/main/docs/static/logo_dark.svg">
  <img
  alt="A logo of a stylized blue dragon inside a similarly blue shell. A yellow star lies at the center, together with the dragon shape forming a stylized letter A."
  src="https://raw.githubusercontent.com/GeminiDRSoftware/astrodata_gemini/main/docs/static/logo_dark.svg"
  style="display: block; width: 20%; height: auto; float: center"
  >
</p>
-->

astrodata_gemini
================
[![Project Status: Development – The project being refactored,.](https://www.repostatus.org/badges/latest/wip.svg)](https://www.repostatus.org/#wip)
![Supported python versions -- 3.11, 3.12, 3.13, and 3.14](https://img.shields.io/badge/3.11|3.12|3.13|3.14-%234b8bbe?logo=Python&logoColor=%234b8bbe&label=For%20Python%3A)
<!--[![DOI Badge][zenodo DOI badge]][zenodo DOI link]-->

### Tests
<!-- ![A badge displaying the testing coverage percentage of this repository.][coverage badge]
![Source test status badge][source test status badge]
![Build/Release test status badge][build test status badge] -->


### Building & Publishing
<!-- ![Documentation build status badge][docs build badge]
![pypi packaging status badge][pypi packaging badge]
[![PyPI version badge][pypi package version badge]][pypi package version badge] -->

<!-- Clearing the logo for the next header -->
<br clear="left">

Description
-----------
`astrodata_gemini` is an [astrodata] plugin for accessing data from the 
Gemini Observatory instruments through the [astrodata] uniform interface.

Installation
------------

`astrodata_gemini` is available on the [Python Package Index][pypi link] and
can be installed using `pip`:

```
python -m pip install astrodata_gemini
```

Documentation
-------------
Documentation for `astrodata_gemini` is available at 
[https://astrodata-gemini.readthedocs.io/en/latest/][documentation].

Usage
-----
`astrodata_gemini` is a plugin for the [astrodata] package.  You 
must first install [astrodata]. To use it, you need to import `astrodata` 
and then import the plugin:

```python
>>> import astrodata
>>> import astrodata_gemini
```

Then you can use `astrodata` to open Gemini data files, and the plugin will
automatically handle the Gemini-specific metadata and data structures.

```python
>>> ad = astrodata.open('N20180114S0121_arc.fits')
>>> ad.info()
Filename: N20180114S0121_arc.fits
Tags: ARC CAL GEMINI GNIRS LS NORTH PREPARED PROCESSED SIDEREAL SPECT

Pixels Extensions
Index  Content                  Type              Dimensions     Format
[ 0]   science                  NDAstroData       (1022, 1024)   float32
          .variance             ADVarianceUncerta (1022, 1024)   float32
          .mask                 ndarray           (1022, 1024)   uint16
          .FITCOORD             Table             (2, 16)        n/a
          .WAVECAL              Table             (45, 4)        n/a

Other Extensions
               Type        Dimensions
.HISTORY       Table       (11, 4)
.MDF           Table       (1, 4)
.PROVENANCE    Table       (6, 4)

>>> ad.tags
{'PROCESSED', 'PREPARED', 'ARC', 'SPECT', 'SIDEREAL', 'GNIRS', 'GEMINI', 'LS', 'NORTH', 'CAL'}

>>> ad.descriptors
'('airmass', 'amp_read_area', 'ao_seeing', 'array_name', 'array_section', 
'azimuth', 'binning', 'calibration_key', 'camera', 'cass_rotator_pa', 
'central_wavelength', 'coadds', 'data_label', 'data_section', 'dec', 'decker', 
'detector_name', 'detector_roi_setting', 'detector_rois_requested', 
'detector_section', 'detector_x_bin', 'detector_x_offset', 'detector_y_bin', 
'detector_y_offset', 'disperser', 'dispersion', 'dispersion_axis', 
'effective_wavelength', 'elevation', 'exposure_time', 'filter_name', 
'focal_plane_mask', 'gain_setting', 'gcal_lamp', 'group_id', 'instrument', 
'is_ao', 'is_coadds_summed', 'is_in_adu', 'local_time', 'lyot_stop', 
'mdf_row_id', 'nominal_atmospheric_extinction', 
'nominal_photometric_zeropoint', 'object', 'observation_class', 
'observation_epoch', 'observation_id', 'observation_type', 'overscan_section', 
'pixel_scale', 'position_angle', 'program_id', 'pupil_mask', 'qa_state', 'ra', 
'raw_bg', 'raw_cc', 'raw_iq', 'raw_wv', 'read_mode', 'read_speed_setting', 
'requested_bg', 'requested_cc', 'requested_iq', 'requested_wv', 'slit', 
'slit_width', 'target_dec', 'target_ra', 'telescope', 'telescope_x_offset', 
'telescope_y_offset', 'ut_date', 'ut_datetime', 'ut_time', 'wavefront_sensor', 
'wavelength_band', 'wcs_dec', 'wcs_ra', 'well_depth_setting')

>>> ad.filter_name()
'Open&L_G0527'
>>> ad.filter_name(pretty=True)
'L'
```

<!--
Installing development dependencies
-----------------------------------

Contributing
------------

License
-------

Citations
---------

-->