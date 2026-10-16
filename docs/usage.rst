.. usage.rst

.. _usage:

*****
Usage
*****

``astrodata_gemini`` is a plugin for the |astrodata| package.  You
must first install |astrodata|. To use it, you need to import ``astrodata``
and then import the plugin:

.. code-block:: python

    >>> import astrodata
    >>> import astrodata_gemini



Then you can use ``astrodata`` to open Gemini data files, and the plugin will
automatically handle the Gemini-specific metadata and data structures.

.. code-block:: python

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