"""General utility functions for the astrodata_gemini package."""

import math
import re
from functools import wraps

import numpy as np
from astropy import coordinates
from astropy import units as u

# The unitDict dictionary defines the factors for the function
# convert_units
unitDict = {"meters": 0, "micrometers": -6, "nanometers": -9, "angstroms": -10}


def isBlank(bstring):
    """Return True if the input string is None or empty."""
    return not (bstring and bstring.strip())


def removeComponentID(input_string):
    """
    Remove a component ID from a filter name.

    Parameters
    ----------
    input_string : str
        The filter name.

    Returns
    -------
    str or None
        The filter name with the component ID removed, or `None` if the
        input is not a valid string.
    """
    try:
        m = re.match(r"(?P<filt>.*?)_G(.*?)", input_string)
    except TypeError:
        return None

    if not m:
        # There was no "_G" in the input string. Return the input string
        ret_str = str(input_string)
    else:
        ret_str = str(m.group("filt"))
    return ret_str


def getComponentID(input_string):
    """
    Return the ID in a component name.

    Parameters
    ----------
    input_string : str
        The filter name.

    Returns
    -------
    str or None
        The filter ID with the rest removed, or `None` if the input is not
        a valid filter name with an ID.
    """
    try:
        m = re.match(r".*_(?P<id>G\d{4})", input_string)
    except TypeError:
        return None

    if not m:
        ret_str = None
    else:
        ret_str = str(m.group("id"))

    return ret_str


def parse_percentile(input_string):
    """
    Return the integer percentile from a site condition header string.

    Parameters
    ----------
    input_string : str
        The type of string that ought to be present in the site condition
        headers, e.g. "Any" or "70-percentile".

    Returns
    -------
    int or None
        The percentile number ("Any" is the 100th percentile), or `None` if
        the string is not recognized.
    """
    # Is it 'Any' - ie 100th percentile?
    if input_string == "Any":
        return 100

    # Is it a xx-percentile string?
    try:
        m = re.match(r"^(\d\d)-percentile$", input_string)
    except TypeError:
        return None

    if m:
        return int(m.group(1))

    # We didn't recognise it
    return None


def convert_units(input_units, input_value, output_units):
    """
    Convert a wavelength value from one unit to another.

    Parameters
    ----------
    input_units : str
        The units of the value specified by `input_value`.  Possible values
        are 'meters', 'micrometers', 'nanometers' and 'angstroms'.
    input_value : float or None
        The input value to be converted from `input_units` to
        `output_units`.
    output_units : str
        The units of the returned value.  Possible values are 'meters',
        'micrometers', 'nanometers' and 'angstroms'.

    Returns
    -------
    float or None
        The converted value of `input_value` from `input_units` to
        `output_units`, or `None` if `input_value` is `None`.
    """
    # Determine the factor required to convert the input_value from the
    # input_units to the output_units
    power = unitDict[input_units] - unitDict[output_units]
    factor = math.pow(10, power)

    # Return the converted output value
    if input_value is not None:
        return input_value * factor


def return_requested_units(input_units="nm"):
    """
    Decorate a wavelength descriptor with the unit conversion arguments.

    Replaces the repeated code for asMicrometers, asNanometers, asAngstroms.
    Should be replaced by a "units='nm'" parameter, but time is limited.

    Parameters
    ----------
    input_units : str
        The units of the value returned by the decorated function, as
        understood by `astropy.units.Unit`.

    Returns
    -------
    callable
        The decorator.  The decorated function accepts the additional
        boolean keyword arguments ``asMicrometers``, ``asNanometers`` and
        ``asAngstroms`` and returns a Python `float` (or a list thereof)
        with the same number of digits as np.float32, to avoid excessive
        precision.  The default output unit is meters.
    """

    def inner_decorator(fn):
        @wraps(fn)
        def gn(
            instance,
            asMicrometers=False,
            asNanometers=False,
            asAngstroms=False,
            **kwargs,
        ):
            unit_arg_list = [asMicrometers, asNanometers, asAngstroms]
            output_units = u.m  # By default
            if unit_arg_list.count(True) == 1:
                # Just one of the unit arguments was set to True. Return the
                # central wavelength in these units
                if asMicrometers:
                    output_units = u.um
                elif asNanometers:
                    output_units = u.nm
                else:
                    output_units = u.AA

            # Ensure we return a list, not an array
            # nm are the "standard" DRAGONS wavelength unit
            retval = fn(instance, **kwargs)
            if retval is None:
                return retval
            if isinstance(retval, list):
                return [
                    None
                    if v is None
                    else float(
                        str(
                            np.float32(
                                (v * u.Unit(input_units))
                                .to(output_units)
                                .value
                            )
                        )
                    )
                    for v in retval
                ]
            return float(
                str(
                    np.float32(
                        (retval * u.Unit(input_units)).to(output_units).value
                    )
                )
            )

        return gn

    return inner_decorator


def toicrs(frame, ra, dec, equinox=2000.0, ut_datetime=None):
    """
    Convert an RA and Dec to ICRS.

    The coordinates are in the specified reference frame and equinox at
    `ut_datetime`.  This is used by the ra and dec descriptors.

    Parameters
    ----------
    frame : str
        The reference frame of the input coordinates, e.g. 'APPT', 'FK5',
        'ICRS'.
    ra : float
        Right Ascension, in degrees.
    dec : float
        Declination, in degrees.
    equinox : float, optional
        The equinox, as a Julian year.
    ut_datetime : datetime.datetime, optional
        The date and time of the observation.

    Returns
    -------
    tuple of float
        The ICRS Right Ascension and Declination, in degrees.
    """
    # Assume equinox is julian calendar
    equinox = "J{}".format(equinox)

    # astropy doesn't understand APPT coordinates. However, it does understand
    # CIRS coordinates, and we can convert from APPT to CIRS by adding the
    # equation of origins to the RA. We can get that using ERFA.
    # To proceed with this, we first let astopy construct the CIRS frame, so
    # that we can extract the obstime object from that to pass to erfa.
    appt_frame = frame == "APPT"
    if frame == "APPT":
        frame = "cirs"
    if frame == "FK5":
        frame = "fk5"

    # Try this with the passed frame but, if it doesn't work, convert to "cirs"
    # If that doesn't work, then raise an error
    try:
        coords = coordinates.SkyCoord(
            ra=ra * u.degree,
            dec=dec * u.degree,
            frame=frame,
            equinox=equinox,
            obstime=ut_datetime,
        )
    except ValueError:
        frame = "cirs"
        coords = coordinates.SkyCoord(
            ra=ra * u.degree,
            dec=dec * u.degree,
            frame=frame,
            equinox=equinox,
            obstime=ut_datetime,
        )

    if appt_frame:
        # Call ERFA.apci13 to get the Equation of Origin (EO).
        # We just discard the astrom context return
        try:
            # With astropy 4.2 erfa becomes a dependency and lives in an
            # independent Python package: https://github.com/liberfa/pyerfa
            import erfa
        except ImportError:
            from astropy import _erfa as erfa

        astrom, eo = erfa.apci13(coords.obstime.jd1, coords.obstime.jd2)
        # eo comes back as a single element array in radians
        eo = float(eo)
        eo = eo * u.radian
        # re-create the coords frame object with the corrected ra
        coords = coordinates.SkyCoord(
            ra=coords.ra + eo,
            dec=coords.dec,
            frame=coords.frame.name,
            equinox=coords.equinox,
            obstime=coords.obstime,
        )

    # Now we can just convert to ICRS...
    icrs = coords.icrs

    # And return values in degrees
    return (icrs.ra.degree, icrs.dec.degree)


def detsec_to_pixels(ad, detx, dety):
    """
    Convert a "detector section" location to extension pixels.

    Converts a location in "detector section pixels" to an image extension
    and real pixels on that extension.

    Parameters
    ----------
    ad : AstroData
        The AstroData object.
    detx : int or float
        The x location, in detector section pixels.
    dety : int or float
        The y location, in detector section pixels.

    Returns
    -------
    tuple of (int, int, int) or None
        The extension index and the x and y pixel locations on that
        extension, or `None` if the location is not in any extension.
    """
    xbin, ybin = ad.detector_x_bin(), ad.detector_y_bin()
    for i, detsec in enumerate(ad.detector_section()):
        if (
            detx < detsec.x1
            or detx >= detsec.x2
            or dety < detsec.y1
            or dety >= detsec.y2
        ):
            continue
        datasec = ad.data_section()[i]
        return (
            i,
            datasec.x1 + (detx - detsec.x1) // xbin,
            datasec.y1 + (dety - detsec.y1) // ybin,
        )
    return None
