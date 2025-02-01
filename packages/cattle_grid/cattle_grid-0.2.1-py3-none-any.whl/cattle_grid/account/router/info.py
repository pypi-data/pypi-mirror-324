from cattle_grid.model.account import NameAndVersion
from cattle_grid.version import __version__


def protocol_and_backend():
    protocol = NameAndVersion(name="CattleDrive", version="0.1.0")
    backend = NameAndVersion(name="cattle_grid", version=__version__)

    return dict(protocol=protocol, backend=backend)
