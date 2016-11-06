from .thermostat import (
    Thermostat,
    CommonThermostat,
    CT30v175,
    CT30v192,
    CT30v194,
    CT30v199,
    CT50v109,
    CT50v188,
    CT50v192,
    CT50v194,
    CT80RevB1v100,
    CT80RevB2v100,
    CT80RevB2v103,
    CT80RevB2v109,
    CT80RevB,
    CT30,
    CT50,
    CT80
)
from . import discover
from . import fields

THERMOSTATS = (
    CT30v175,
    CT30v192,
    CT30v194,
    CT30v199,
    CT50v109,
    CT50v188,
    CT50v192,
    CT50v194,
    CT80RevB1v100,
    CT80RevB2v100,
    CT80RevB2v103,
    CT80RevB2v109,
    CT80RevB,
    CT80,
    CT50,
    CT30
)

def get_thermostat_class(model):
    """
    :param model:   string representation of the thermostat's model, in
                    whatever format the thermostat itself returns.
    :type model:    str

    :returns:       subclass of CommonThermostat, or None if there is not a
                    matching subclass found in THERMOSTATS.
    """
    # Look for exact matches first
    for thermostat in THERMOSTATS:
        if issubclass(thermostat, Thermostat) and thermostat.MODEL == model:
            return thermostat

    # Look for partial matches next
    for thermostat in THERMOSTATS:
        if (issubclass(thermostat, Thermostat) and thermostat.MODEL in model):
            return thermostat


def get_thermostat(host_address=None, model=None):
    """
    If a host_address is not passed, auto-discovery will happen. Auto-discovery
    will only succeed then exactly 1 thermostat is on your network.

    :param host_address:    optional address for a thermostat. This can be an
                            IP address or domain name.
    :param model:           optional string representing the model and version
                            number. Available from API resource /tstat/model

    :returns:   instance of a CommonThermostat subclass, or None if a matching
                subclass cannot be found.
    """
    if host_address is None:
        host_address = discover.discover_address()
    if model is None:
        initial = CommonThermostat(host_address)
        model = initial.model.get('raw')
    thermostat_class = get_thermostat_class(model)
    if thermostat_class is not None:
        return thermostat_class(host_address)
