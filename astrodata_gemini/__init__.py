# Import the modules under this package, to trigger any class
# registering that may be needed

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("astrodata_gemini")
except PackageNotFoundError:
    # Running from a source tree that was never installed.
    __version__ = "unknown"

from . import gemini

from . import bhros
from . import cirpass
from . import f2
from . import flamingos
from . import ghost
from . import gmos
from . import gnirs
from . import gpi
from . import graces
from . import gsaoi
from . import hokupaa_quirc
from . import hrwfs
from . import igrins
from . import igrins2
from . import michelle
from . import nici
from . import nifs
from . import niri
from . import oscir
from . import phoenix
from . import texes
from . import trecs
