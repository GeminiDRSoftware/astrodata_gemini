tags_data = {
    #   GMOS Bias
    ('GMOS', 'N20160407S0076.fits'): ['AT_ZENITH', 'AZEL_TARGET', 'BIAS', 'CAL', 'GEMINI', 'GMOS', 'NON_SIDEREAL',
                                      'NORTH', 'RAW', 'UNPREPARED'],
    # S20261001S0185_bias: processed bias
    ('GMOS', 'S20261001S0185_bias.fits'): ['BIAS', 'CAL', 'GEMINI', 'GMOS', 'OVERSCAN_SUBTRACTED', 'OVERSCAN_TRIMMED',
                                           'PREPARED', 'PROCESSED', 'SOUTH'],

    #   GMOS Dark
    # N20160106S0653: MOS dark
    ('GMOS', 'N20160106S0653.fits'): ['AT_ZENITH', 'AZEL_TARGET', 'CAL', 'DARK', 'GEMINI', 'GMOS', 'NON_SIDEREAL',
                                      'NORTH', 'RAW', 'UNPREPARED'],
    # S20160905S0003: N&S dark
    ('GMOS', 'S20160905S0003.fits'): ['AT_ZENITH', 'AZEL_TARGET', 'CAL', 'DARK', 'GEMINI', 'GMOS', 'NODANDSHUFFLE',
                                      'NON_SIDEREAL', 'RAW', 'SOUTH', 'UNPREPARED'],

    #   GMOS Imaging (flats, acquisitions and the Hartmann file with IMAGE are listed here)
    ('GMOS', 'S20111120S0478.fits'): ['GEMINI', 'GMOS', 'IMAGE', 'RAW', 'SIDEREAL', 'SOUTH', 'UNPREPARED'],
    # N20110718S0294: twilight flat
    ('GMOS', 'N20110718S0294.fits'): ['CAL', 'FLAT', 'GEMINI', 'GMOS', 'IMAGE', 'NORTH', 'RAW', 'SIDEREAL',
                                      'TWILIGHT', 'UNPREPARED'],
    # S20251207S0094_flat: processed twilight flat
    ('GMOS', 'S20251207S0094_flat.fits'): ['CAL', 'FLAT', 'GEMINI', 'GMOS', 'IMAGE', 'OVERSCAN_SUBTRACTED',
                                           'OVERSCAN_TRIMMED', 'PREPARED', 'PROCESSED', 'SIDEREAL', 'SOUTH',
                                           'TWILIGHT'],
    # N20190216S0039: Hartmann file (weird)
    ('GMOS', 'N20190216S0039.fits'): ['CAL', 'FLAT', 'GCALFLAT', 'GEMINI', 'GMOS', 'IMAGE', 'NORTH', 'RAW',
                                      'THRUSLIT', 'UNPREPARED'],
    # N20160708S0085: acquisition, MOS thru-slit
    ('GMOS', 'N20160708S0085.fits'): ['ACQUISITION', 'GEMINI', 'GMOS', 'IMAGE', 'MOS', 'NORTH', 'RAW', 'SIDEREAL',
                                      'THRUSLIT', 'UNPREPARED'],
    # N20160620S0317: acquisition, IFU ONESLIT_RED
    ('GMOS', 'N20160620S0317.fits'): ['ACQUISITION', 'GEMINI', 'GMOS', 'IFU', 'IMAGE', 'NORTH', 'ONESLIT_RED', 'RAW',
                                      'SIDEREAL', 'THRUSLIT', 'UNPREPARED'],

    #   GMOS Fringe
    # N20110927S0170_fringe: Those will only be recognized as PROCESSED FRINGE.  As raw, they cannot be recognized.
    ('GMOS', 'N20110927S0170_fringe.fits'): ['CAL', 'FRINGE', 'GEMINI', 'GMOS', 'IMAGE', 'NORTH',
                                             'OVERSCAN_SUBTRACTED', 'OVERSCAN_TRIMMED', 'PREPARED', 'PROCESSED',
                                             'SIDEREAL'],

    #   GMOS Longslit (flats and arcs with SPECT are listed here)
    # N20160726S0179: standard
    ('GMOS', 'N20160726S0179.fits'): ['CAL', 'GEMINI', 'GMOS', 'LS', 'NORTH', 'RAW', 'SIDEREAL', 'SPECT', 'STANDARD',
                                      'UNPREPARED'],
    # S20091217S0032: N&S
    ('GMOS', 'S20091217S0032.fits'): ['GEMINI', 'GMOS', 'LS', 'NODANDSHUFFLE', 'RAW', 'SIDEREAL', 'SOUTH', 'SPECT',
                                      'UNPREPARED'],
    # N20160722S0284: slit illumination
    ('GMOS', 'N20160722S0284.fits'): ['CAL', 'GEMINI', 'GMOS', 'LS', 'NORTH', 'RAW', 'SIDEREAL', 'SLITILLUM', 'SPECT',
                                      'TWILIGHT', 'UNPREPARED'],
    # N20160726S0180: flat
    ('GMOS', 'N20160726S0180.fits'): ['CAL', 'FLAT', 'GCALFLAT', 'GEMINI', 'GMOS', 'LS', 'NORTH', 'RAW', 'SIDEREAL',
                                      'SPECT', 'UNPREPARED'],
    # S20160724S0218: arc
    ('GMOS', 'S20160724S0218.fits'): ['ARC', 'CAL', 'GEMINI', 'GMOS', 'LS', 'RAW', 'SIDEREAL', 'SOUTH', 'SPECT',
                                      'UNPREPARED'],

    #   GMOS MOS (flats and arcs with SPECT are listed here)
    # S20150417S0092: N&S
    ('GMOS', 'S20150417S0092.fits'): ['GEMINI', 'GMOS', 'MOS', 'NODANDSHUFFLE', 'RAW', 'SIDEREAL', 'SOUTH', 'SPECT',
                                      'UNPREPARED'],
    # N20160605S0099: slit illumination
    ('GMOS', 'N20160605S0099.fits'): ['CAL', 'GEMINI', 'GMOS', 'MOS', 'NORTH', 'RAW', 'SIDEREAL', 'SLITILLUM',
                                      'SPECT', 'TWILIGHT', 'UNPREPARED'],
    # S20190217S0211: flat
    ('GMOS', 'S20190217S0211.fits'): ['AT_ZENITH', 'AZEL_TARGET', 'CAL', 'FLAT', 'GCALFLAT', 'GEMINI', 'GMOS', 'MOS',
                                      'NON_SIDEREAL', 'RAW', 'SOUTH', 'SPECT', 'UNPREPARED'],
    # N20160721S0351: arc
    ('GMOS', 'N20160721S0351.fits'): ['ARC', 'AT_ZENITH', 'AZEL_TARGET', 'CAL', 'GEMINI', 'GMOS', 'MOS',
                                      'NON_SIDEREAL', 'NORTH', 'RAW', 'SPECT', 'UNPREPARED'],

    #   GMOS IFU (flats and arcs with SPECT are listed here)
    # S20060130S0079: N&S, TWOSLIT
    ('GMOS', 'S20060130S0079.fits'): ['GEMINI', 'GMOS', 'IFU', 'NODANDSHUFFLE', 'RAW', 'SIDEREAL', 'SOUTH', 'SPECT',
                                      'TWOSLIT', 'UNPREPARED'],
    # S20051225S0084: ONESLIT_BLUE
    ('GMOS', 'S20051225S0084.fits'): ['GEMINI', 'GMOS', 'IFU', 'ONESLIT_BLUE', 'RAW', 'SIDEREAL', 'SOUTH', 'SPECT',
                                      'UNPREPARED'],
    # N20160620S0373: slit illumination, ONESLIT_RED
    ('GMOS', 'N20160620S0373.fits'): ['CAL', 'GEMINI', 'GMOS', 'IFU', 'NORTH', 'ONESLIT_RED', 'RAW', 'SIDEREAL',
                                      'SLITILLUM', 'SPECT', 'TWILIGHT', 'UNPREPARED'],
    # N20111124S0203: flat, ONESLIT_RED
    ('GMOS', 'N20111124S0203.fits'): ['CAL', 'FLAT', 'GCALFLAT', 'GEMINI', 'GMOS', 'IFU', 'NORTH', 'ONESLIT_RED',
                                      'RAW', 'SIDEREAL', 'SPECT', 'UNPREPARED'],
    # S20060131S0131: arc, ONESLIT_BLUE
    ('GMOS', 'S20060131S0131.fits'): ['ARC', 'CAL', 'GEMINI', 'GMOS', 'IFU', 'ONESLIT_BLUE', 'RAW', 'SIDEREAL',
                                      'SOUTH', 'SPECT', 'UNPREPARED'],

    # NIRI Data
    #   NIRI Darks
    ('NIRI', 'N20131215S0503.fits'): ['AT_ZENITH', 'AZEL_TARGET', 'CAL', 'DARK', 'GEMINI', 'NIRI', 'NON_SIDEREAL',
                                      'NORTH', 'RAW', 'UNPREPARED'],
    ('NIRI', 'N20130409S0105_dark.fits'): ['AT_ZENITH', 'AZEL_TARGET', 'CAL', 'DARK', 'GEMINI', 'NIRI',
                                           'NON_SIDEREAL', 'NORTH', 'PREPARED', 'PROCESSED'],

    #   NIRI Imaging (flats with IMAGE are listed here)
    ('NIRI', 'N20131215S0178.fits'): ['GEMINI', 'IMAGE', 'NIRI', 'NORTH', 'RAW', 'SIDEREAL', 'UNPREPARED'],
    ('NIRI', 'N20131215S0427.fits'): ['AT_ZENITH', 'AZEL_TARGET', 'CAL', 'FLAT', 'GCALFLAT', 'GCAL_IR_OFF', 'GEMINI',
                                      'IMAGE', 'LAMPOFF', 'NIRI', 'NON_SIDEREAL', 'NORTH', 'RAW', 'UNPREPARED'],
    ('NIRI', 'N20131215S0428.fits'): ['AT_ZENITH', 'AZEL_TARGET', 'CAL', 'FLAT', 'GCALFLAT', 'GCAL_IR_ON', 'GEMINI',
                                      'IMAGE', 'LAMPON', 'NIRI', 'NON_SIDEREAL', 'NORTH', 'RAW', 'UNPREPARED'],

    #   NIRI Longslit (flats with SPECT are listed here)
    ('NIRI', 'N20120505S0147.fits'): ['GEMINI', 'LS', 'NIRI', 'NORTH', 'RAW', 'SIDEREAL', 'SPECT', 'UNPREPARED'],
    ('NIRI', 'N20100620S0126.fits'): ['ARC', 'GEMINI', 'LS', 'NIRI', 'NORTH', 'RAW', 'SIDEREAL', 'SPECT',
                                      'UNPREPARED'],
    ('NIRI', 'N20120505S0564.fits'): ['AT_ZENITH', 'AZEL_TARGET', 'CAL', 'FLAT', 'GCALFLAT', 'GCAL_IR_OFF', 'GEMINI',
                                      'LAMPOFF', 'LS', 'NIRI', 'NON_SIDEREAL', 'NORTH', 'RAW', 'SPECT', 'UNPREPARED'],
    ('NIRI', 'N20120505S0552.fits'): ['AT_ZENITH', 'AZEL_TARGET', 'CAL', 'FLAT', 'GCALFLAT', 'GCAL_IR_ON', 'GEMINI',
                                      'LAMPON', 'LS', 'NIRI', 'NON_SIDEREAL', 'NORTH', 'RAW', 'SPECT', 'UNPREPARED'],

    # GNIRS Data
    #   GNIRS Darks
    ('GNIRS', 'N20190214S0058.fits'): ['CAL', 'DARK', 'GEMINI', 'GNIRS', 'NORTH', 'RAW', 'UNPREPARED'],
    # N20140812S0142_dark: processed dark
    ('GNIRS', 'N20140812S0142_dark.fits'): ['AT_ZENITH', 'AZEL_TARGET', 'CAL', 'DARK', 'GEMINI', 'GNIRS',
                                            'NON_SIDEREAL', 'NORTH', 'PREPARED', 'PROCESSED'],

    #   GNIRS Imaging (flats and acquisitions with IMAGE are listed here)
    ('GNIRS', 'N20120117S0019.fits'): ['GEMINI', 'GNIRS', 'IMAGE', 'NORTH', 'RAW', 'SIDEREAL', 'UNPREPARED'],
    # N20120117S0042: flat, lamp off
    ('GNIRS', 'N20120117S0042.fits'): ['CAL', 'FLAT', 'GCALFLAT', 'GCAL_IR_OFF', 'GEMINI', 'GNIRS', 'IMAGE',
                                       'LAMPOFF', 'NORTH', 'RAW', 'SIDEREAL', 'UNPREPARED'],
    # N20120117S0041: flat, lamp on
    ('GNIRS', 'N20120117S0041.fits'): ['CAL', 'FLAT', 'GCALFLAT', 'GCAL_IR_ON', 'GEMINI', 'GNIRS', 'IMAGE', 'LAMPON',
                                       'NORTH', 'RAW', 'SIDEREAL', 'UNPREPARED'],
    # N20131222S0070_flat: processed flat
    ('GNIRS', 'N20131222S0070_flat.fits'): ['CAL', 'FLAT', 'GCALFLAT', 'GEMINI', 'GNIRS', 'IMAGE', 'NORTH',
                                            'PREPARED', 'PROCESSED', 'SIDEREAL'],
    # N20160624S0264: acquisition
    ('GNIRS', 'N20160624S0264.fits'): ['ACQUISITION', 'GEMINI', 'GNIRS', 'IMAGE', 'NORTH', 'RAW', 'SIDEREAL',
                                       'UNPREPARED'],
    # N20140717S0232: acquisition, thru-slit
    ('GNIRS', 'N20140717S0232.fits'): ['ACQUISITION', 'GEMINI', 'GNIRS', 'IMAGE', 'LS', 'NORTH', 'RAW', 'SIDEREAL',
                                       'THRUSLIT', 'UNPREPARED'],

    #   GNIRS Longslit (flats and arcs with SPECT are listed here)
    ('GNIRS', 'N20241216S0168.fits'): ['GEMINI', 'GNIRS', 'LS', 'NON_SIDEREAL', 'NORTH', 'RAW', 'SPECT',
                                       'UNPREPARED'],
    # N20240116S0138: telluric
    ('GNIRS', 'N20240116S0138.fits'): ['GEMINI', 'GNIRS', 'LS', 'NORTH', 'RAW', 'SIDEREAL', 'SPECT', 'UNPREPARED'],
    # N20190216S0092: flat, lamp off
    ('GNIRS', 'N20190216S0092.fits'): ['CAL', 'FLAT', 'GCALFLAT', 'GCAL_IR_OFF', 'GEMINI', 'GNIRS', 'LAMPOFF', 'LS',
                                       'NORTH', 'RAW', 'SIDEREAL', 'SPECT', 'UNPREPARED'],
    # N20130814S0231: arc
    ('GNIRS', 'N20130814S0231.fits'): ['ARC', 'CAL', 'GEMINI', 'GNIRS', 'LS', 'NORTH', 'RAW', 'SIDEREAL', 'SPECT',
                                       'UNPREPARED'],

    #   GNIRS Cross-dispersed (flats, arcs and pinholes with SPECT are listed here)
    ('GNIRS', 'N20190206S0279.fits'): ['GEMINI', 'GNIRS', 'NORTH', 'RAW', 'SIDEREAL', 'SPECT', 'UNPREPARED', 'XD'],
    # N20160726S0260: flat, lamp on
    ('GNIRS', 'N20160726S0260.fits'): ['CAL', 'FLAT', 'GCALFLAT', 'GCAL_IR_ON', 'GEMINI', 'GNIRS', 'LAMPON', 'NORTH',
                                       'RAW', 'SIDEREAL', 'SPECT', 'UNPREPARED', 'XD'],
    # N20160722S0232: arc
    ('GNIRS', 'N20160722S0232.fits'): ['ARC', 'CAL', 'GEMINI', 'GNIRS', 'NORTH', 'RAW', 'SIDEREAL', 'SPECT',
                                       'UNPREPARED', 'XD'],
    # N20160726S0301: pinhole
    ('GNIRS', 'N20160726S0301.fits'): ['AT_ZENITH', 'AZEL_TARGET', 'CAL', 'GEMINI', 'GNIRS', 'NON_SIDEREAL', 'NORTH',
                                       'PINHOLE', 'RAW', 'SPECT', 'UNPREPARED', 'XD'],
    # S20060507S0125: pinhole, south
    ('GNIRS', 'S20060507S0125.fits'): ['AZEL_TARGET', 'CAL', 'GEMINI', 'GNIRS', 'NON_SIDEREAL', 'PINHOLE', 'RAW',
                                       'SOUTH', 'SPECT', 'UNPREPARED', 'XD'],

    #   GNIRS IFU
    # N20240330S0209: LR-IFU
    ('GNIRS', 'N20240330S0209.fits'): ['GEMINI', 'GNIRS', 'IFU', 'NORTH', 'RAW', 'SIDEREAL', 'SPECT', 'UNPREPARED'],
    # S20070102S0073: IFU, south
    ('GNIRS', 'S20070102S0073.fits'): ['GEMINI', 'GNIRS', 'IFU', 'RAW', 'SIDEREAL', 'SOUTH', 'SPECT', 'UNPREPARED'],
    # N20240129S0380: arc, HR-IFU
    ('GNIRS', 'N20240129S0380.fits'): ['ARC', 'CAL', 'GEMINI', 'GNIRS', 'IFU', 'NORTH', 'RAW', 'SPECT', 'UNPREPARED'],

    # NIFS Data
    #   NIFS Darks
    ('NIFS', 'N20160428S0174.fits'): ['AT_ZENITH', 'AZEL_TARGET', 'CAL', 'DARK', 'GEMINI', 'NIFS', 'NON_SIDEREAL',
                                      'NORTH', 'RAW', 'UNPREPARED'],

    #   NIFS Flats
    ('NIFS', 'N20160705S0221.fits'): ['AT_ZENITH', 'AZEL_TARGET', 'CAL', 'FLAT', 'GCALFLAT', 'GCAL_IR_OFF', 'GEMINI',
                                      'IFU', 'LAMPOFF', 'NIFS', 'NON_SIDEREAL', 'NORTH', 'RAW', 'RONCHI', 'SPECT',
                                      'UNPREPARED'],
    ('NIFS', 'N20160727S0079.fits'): ['AZEL_TARGET', 'CAL', 'FLAT', 'GCALFLAT', 'GCAL_IR_ON', 'GEMINI', 'IFU',
                                      'LAMPON', 'NIFS', 'NON_SIDEREAL', 'NORTH', 'RAW', 'SPECT', 'UNPREPARED'],

    #   NIFS Arcs
    ('NIFS', 'N20160727S0078.fits'): ['ARC', 'AT_ZENITH', 'AZEL_TARGET', 'CAL', 'GEMINI', 'IFU', 'NIFS',
                                      'NON_SIDEREAL', 'NORTH', 'RAW', 'SPECT', 'UNPREPARED'],

    #   NIFS Acquisition
    ('NIFS', 'N20160708S0119.fits'): ['ACQUISITION', 'GEMINI', 'IFU', 'NIFS', 'NORTH', 'RAW', 'SIDEREAL', 'SPECT',
                                      'UNPREPARED'],

    #   NIFS IFU science
    ('NIFS', 'N20160708S0134.fits'): ['GEMINI', 'IFU', 'NIFS', 'NORTH', 'RAW', 'SIDEREAL', 'SPECT', 'UNPREPARED'],

    # F2 Data
    #   F2 Darks
    ('F2', 'S20150516S0373.fits'): ['AT_ZENITH', 'AZEL_TARGET', 'CAL', 'DARK', 'F2', 'GEMINI', 'NON_SIDEREAL', 'RAW',
                                    'SOUTH', 'UNPREPARED'],
    ('F2', 'S20141031S0274_dark.fits'): ['AT_ZENITH', 'AZEL_TARGET', 'CAL', 'DARK', 'F2', 'GEMINI', 'NON_SIDEREAL',
                                         'PREPARED', 'PROCESSED', 'SOUTH'],

    #   F2 Imaging (flats and acquisitions with IMAGE are listed here)
    ('F2', 'S20150511S0168.fits'): ['F2', 'GEMINI', 'IMAGE', 'RAW', 'SIDEREAL', 'SOUTH', 'UNPREPARED'],
    ('F2', 'S20190214S0576.fits'): ['AT_ZENITH', 'AZEL_TARGET', 'CAL', 'F2', 'FLAT', 'GCALFLAT', 'GCAL_IR_OFF', 'GEMINI',
                                    'IMAGE', 'LAMPOFF', 'NON_SIDEREAL', 'RAW', 'SOUTH', 'UNPREPARED'],
    ('F2', 'S20160317S0053.fits'): ['ACQUISITION', 'F2', 'GEMINI', 'IMAGE', 'RAW', 'SIDEREAL', 'SOUTH', 'UNPREPARED'],
    ('F2', 'S20160317S0055.fits'): ['ACQUISITION', 'F2', 'GEMINI', 'IMAGE', 'LS', 'RAW', 'SIDEREAL', 'SOUTH',
                                    'THRUSLIT', 'UNPREPARED'],
    ('F2', 'S20150622S0004.fits'): ['ACQUISITION', 'F2', 'GEMINI', 'IMAGE', 'MOS', 'RAW', 'SIDEREAL', 'SOUTH',
                                    'THRUSLIT', 'UNPREPARED'],

    #   F2 Longslit (flats and arcs with SPECT are listed here)
    ('F2', 'S20140217S0036.fits'): ['F2', 'GEMINI', 'LS', 'RAW', 'SIDEREAL', 'SOUTH', 'SPECT', 'UNPREPARED'],
    ('F2', 'S20160616S0071.fits'): ['ARC', 'CAL', 'F2', 'GEMINI', 'LS', 'RAW', 'SIDEREAL', 'SOUTH', 'SPECT',
                                    'UNPREPARED'],

    #   F2 MOS (flats and arcs with SPECT are listed here)
    ('F2', 'S20150622S0005.fits'): ['F2', 'GEMINI', 'MOS', 'NON_SIDEREAL', 'RAW', 'SOUTH', 'SPECT', 'UNPREPARED'],
    ('F2', 'S20150629S0244.fits'): ['ARC', 'AT_ZENITH', 'AZEL_TARGET', 'CAL', 'F2', 'GEMINI', 'MOS', 'NON_SIDEREAL',
                                    'RAW', 'SOUTH', 'SPECT', 'UNPREPARED'],
    ('F2', 'S20150624S0172.fits'): ['CAL', 'F2', 'FLAT', 'GCALFLAT', 'GCAL_IR_ON', 'GEMINI', 'LAMPON', 'MOS',
                                    'NON_SIDEREAL', 'RAW', 'SOUTH', 'SPECT', 'UNPREPARED'],

    # GSAOI Data
    #   GSAOI Darks
    ('GSAOI', 'S20160422S0150.fits'): ['AT_ZENITH', 'AZEL_TARGET', 'CAL', 'DARK', 'GEMINI', 'GSAOI', 'NON_SIDEREAL',
                                       'RAW', 'SOUTH', 'UNPREPARED'],

    #   GSAOI Flats
    ('GSAOI', 'S20160613S0316.fits'): ['AZEL_TARGET', 'CAL', 'DOMEFLAT', 'FLAT', 'GEMINI', 'GSAOI', 'IMAGE', 'LAMPOFF',
                                       'NON_SIDEREAL', 'RAW', 'SOUTH', 'UNPREPARED'],
    # This is a processed image, so we don't care about LAMPON, but it's harmless, and easier to just keep it there
    ('GSAOI', 'S20130524S0081_flat.fits'): ['CAL', 'DOMEFLAT', 'FLAT', 'GEMINI', 'GSAOI', 'IMAGE', 'LAMPON',
                                            'NON_SIDEREAL', 'PREPARED', 'PROCESSED', 'SOUTH'],
    ('GSAOI', 'S20150531S0009.fits'): ['CAL', 'FLAT', 'GEMINI', 'GSAOI', 'IMAGE', 'RAW', 'SIDEREAL', 'SOUTH',
                                       'TWILIGHT', 'UNPREPARED'],

    #   GSAOI Imaging science
    ('GSAOI', 'S20150110S0142.fits'): ['GEMINI', 'GSAOI', 'IMAGE', 'RAW', 'SIDEREAL', 'SOUTH', 'UNPREPARED'],

    # BHROS Data
    ('BHROS', 'S20070112S0081.fits'): ['BHROS', 'GEMINI', 'RAW', 'SIDEREAL', 'SOUTH', 'SPECT', 'UNPREPARED'],
    ('BHROS', 'S20070131S0030.fits'): ['BHROS', 'CAL', 'FLAT', 'GCALFLAT', 'GCAL_IR_OFF', 'GEMINI', 'LAMPOFF', 'RAW',
                                       'SIDEREAL', 'SOUTH', 'SPECT', 'UNPREPARED'],
    ('BHROS', 'S20070131S0152.fits'): ['AT_ZENITH', 'AZEL_TARGET', 'BHROS', 'GEMINI', 'NON_SIDEREAL', 'RAW', 'SOUTH',
                                       'SPECT', 'UNPREPARED'],

    # GPI Data
    ('GPI', 'S20160523S0215.fits'): ['DARK', 'GEMINI', 'GPI', 'IFU', 'NON_SIDEREAL', 'RAW', 'SOUTH', 'SPECT',
                                     'UNPREPARED'],
    ('GPI', 'S20161014S0043.fits'): ['GEMINI', 'GPI', 'H_CORON', 'IFU', 'RAW', 'SIDEREAL', 'SOUTH', 'SPECT',
                                     'UNPREPARED'],

    # GRACES Data
    ('GRACES', 'N20190116G0054i.fits'): ['GEMINI', 'GRACES', 'RAW', 'SPECT', 'UNPREPARED'],

    # MICHELLE Data
    ('MICHELLE', 'N20050116S0119.fits'): ['GEMINI', 'IMAGE', 'MICHELLE', 'NORTH', 'RAW', 'SIDEREAL', 'UNPREPARED'],
    ('MICHELLE', 'N20111112S0316.fits'): ['GEMINI', 'LS', 'MICHELLE', 'NORTH', 'RAW', 'SIDEREAL', 'SPECT',
                                          'UNPREPARED'],

    # NICI Data
    ('NICI', 'S20091206S0101.fits'): ['AT_ZENITH', 'AZEL_TARGET', 'CAL', 'FLAT', 'GCAL_IR_OFF', 'GEMINI', 'IMAGE',
                                      'LAMPOFF', 'NICI', 'NON_SIDEREAL', 'RAW', 'SOUTH', 'UNPREPARED'],
    ('NICI', 'S20130607S0258.fits'): ['ADI_R', 'GEMINI', 'IMAGE', 'NICI', 'RAW', 'SIDEREAL', 'SOUTH', 'UNPREPARED'],
    ('NICI', 'S20130607S0592.fits'): ['AZEL_TARGET', 'CAL', 'DARK', 'GEMINI', 'IMAGE', 'NICI', 'NON_SIDEREAL', 'RAW',
                                      'SOUTH', 'UNPREPARED'],
    ('NICI', 'S20130714S0155.fits'): ['CAL', 'FLAT', 'GCALFLAT', 'GCAL_IR_ON', 'GEMINI', 'IMAGE', 'LAMPON', 'NICI',
                                      'RAW', 'SIDEREAL', 'SOUTH', 'UNPREPARED'],
    ('NICI', 'S20130715S0112.fits'): ['GEMINI', 'IMAGE', 'NICI', 'RAW', 'SIDEREAL', 'SOUTH', 'UNPREPARED'],
    ('NICI', 'S20130806S0071.fits'): ['ASDI', 'GEMINI', 'IMAGE', 'NICI', 'RAW', 'SIDEREAL', 'SOUTH', 'UNPREPARED'],

    # TRECS Data
    ('TRECS', 'S20121030S0130.fits'): ['GEMINI', 'IMAGE', 'RAW', 'SIDEREAL', 'SOUTH', 'TRECS', 'UNPREPARED'],
    ('TRECS', 'S20051113S0300.fits'): ['GEMINI', 'RAW', 'SIDEREAL', 'SOUTH', 'SPECT', 'TRECS', 'UNPREPARED'],


        # ('gmos', 'N20160516S0485_bias.fits') : ['GMOS', 'AT_ZENITH', 'GEMINI_NORTH', 'BIAS', 'AZEL_TARGET', 'CAL', 'NON_SIDEREAL', 'PREPARED', 'PROCESSED_BIAS'],
        # ('NIRI', 'N20160523S0471_forStack.fits') : ['NIRI', 'GEMINI_NORTH', 'SIDEREAL', 'IMAGE', 'PREPARED'],

    # GHOST bundle and extracted files
    ('GHOST', 'S20221209S0010.fits'): ['BUNDLE', 'RAW', 'CAL', 'GHOST', 'BIAS', 'UNPREPARED', 'GEMINI', 'SOUTH'],
    ('GHOST', 'S20221209S0012.fits'): ['GCALFLAT', 'RAW', 'CAL', 'GHOST', 'UNPREPARED', 'SOUTH', 'LAMPOFF', 'BUNDLE', 'GCAL_IR_OFF', 'FLAT', 'GEMINI'],
    ('GHOST', 'S20221208S0064.fits'): ['BUNDLE', 'RAW', 'CAL', 'GHOST', 'ARC', 'UNPREPARED', 'GEMINI', 'SOUTH'],
    ('GHOST', 'S20230214S0025.fits'): ['UNPREPARED', 'SOUTH', 'RAW', 'GHOST', 'GEMINI', 'SIDEREAL', 'BUNDLE'],
    ('GHOST', 'S20230214S0025_blue001.fits'): ['BLUE', 'GHOST', 'SIDEREAL', 'UNPREPARED', 'SPECT', 'SOUTH', 'RAW', 'GEMINI', 'XD'],
    ('GHOST', 'S20230214S0025_red002.fits'): ['RED', 'GHOST', 'SIDEREAL', 'UNPREPARED', 'SPECT', 'SOUTH', 'RAW', 'GEMINI', 'XD'],
    ('GHOST', 'S20230214S0025_slit.fits'): ['SLIT', 'GHOST', 'SIDEREAL', 'SLITV', 'UNPREPARED', 'SOUTH', 'IMAGE', 'RAW', 'GEMINI'],

    # IGRINS-2 Data
    #   IGRINS-2 Darks
    ('IGRINS-2', 'N20260228S0506.fits'):  # dark (no DARK?)
        ['BUNDLE', 'GEMINI', 'IGRINS-2', 'NORTH', 'RAW', 'UNPREPARED'],

    #   IGRINS-2 Flats
    ('IGRINS-2', 'N20260303S0290.fits'):  # flat, lamp off
        ['BUNDLE', 'CAL', 'FLAT', 'GCALFLAT', 'GEMINI', 'IGRINS-2', 'LAMPOFF', 'NORTH', 'RAW', 'UNPREPARED'],
    ('IGRINS-2', 'N20260923S0392.fits'):  # flat, lamp on
        ['BUNDLE', 'CAL', 'FLAT', 'GCALFLAT', 'GEMINI', 'IGRINS-2', 'LAMPON', 'NORTH', 'RAW', 'UNPREPARED'],

    #   IGRINS-2 Telluric standards
    ('IGRINS-2', 'N20260228S0200.fits'):  # telluric standard
        ['BUNDLE', 'CAL', 'GEMINI', 'IGRINS-2', 'NORTH', 'RAW', 'SIDEREAL', 'STANDARD', 'UNPREPARED'],

    #   IGRINS-2 Blank sky
    ('IGRINS-2', 'N20260303S0044.fits'):  # blank sky
        ['BUNDLE', 'CAL', 'GEMINI', 'IGRINS-2', 'NORTH', 'RAW', 'SIDEREAL', 'SKY', 'UNPREPARED'],

    #   IGRINS-2 Split pieces (H and K bands are separate files cut from a bundle)
    ('IGRINS-2', 'N20260303S0289_H.fits'):  # H band piece of the bundle N20260303S0289
        ['GEMINI', 'H', 'IGRINS-2', 'NORTH', 'SPECT', 'UNPREPARED', 'XD'],
}
