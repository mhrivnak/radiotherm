import json
from . import fields
from . import validate

try:
    import urllib2 as request
except ImportError:
    from urllib import request

ENABLED_HUMAN_VALUE_MAP = {
    0 : 'Disabled',
    1 : 'Enabled'
}

class Thermostat(object):
    """
    This class implements the most basic functionality of communicating with
    an actual thermostat.
    """
    MODEL = ''
    # The current API doesn't require this header, but it also doesn't hurt,
    # and it's the right thing to do.
    JSON_HEADER = {'Content-Type' : 'application/json'}

    def __init__(self, host):
        self.host = host

    def get(self, relative_url):
        """
        :param relative_url:    The relative URL from the root of the website.

        :returns:   file-like object as returned by urllib[2,.request].urlopen
        """
        url = self._construct_url(relative_url)
        return request.urlopen(url)

    def post(self, relative_url, value):
        """
        :param relative_url:    The relative URL from the root of the website.
        :param value:           Value to set this attribute to

        :returns:   file-like object as returned by urllib[2,.request].urlopen
        """
        url = self._construct_url(relative_url)
        request_instance = request.Request(url, value, self.JSON_HEADER)
        return request.urlopen(request_instance)

    def _construct_url(self, relative_url):
        """
        :param relative_url:    The relative URL from the root of the website

        :returns:   Full URL, for example 'http://192.168.0.2/tstat'
        """
        return 'http://%s/%s' % (self.host, relative_url.lstrip('/'))


class CommonThermostat(Thermostat):
    """
    This class implements the common API features that are available and work
    across all models of thermostat.
    """
    def reboot(self):
        """reboots the thermostat"""
        response = self.post('/sys/command', json.dumps({'command' : 'reboot'}).encode('utf-8'))
        validate.validate_response(response)

    ### tstat subsystem ###
    tstat = fields.ReadOnlyField('/tstat', None)
    model = fields.ReadOnlyField('/tstat/model', 'model')
    version = fields.Field('/tstat/version', 'version')
    temp = fields.ReadOnlyField('/tstat', 'temp')
    tmode = fields.Field('/tstat', 'tmode',
        human_value_map={
            0 : 'Off',
            1 : 'Heat',
            2 : 'Cool',
            3 : 'Auto'
    })
    fmode = fields.Field('/tstat', 'fmode',
        human_value_map={
            0 : 'Auto',
            1 : 'Auto/Circulate',
            2 : 'On'
    })
    override = fields.ReadOnlyField('/tstat', 'override',
        human_value_map=ENABLED_HUMAN_VALUE_MAP)
    hold = fields.Field('/tstat', 'hold', human_value_map=ENABLED_HUMAN_VALUE_MAP)
    t_heat = fields.Field('/tstat/ttemp', 't_heat', post_url='/tstat')
    t_cool = fields.Field('/tstat/ttemp', 't_cool', post_url='/tstat')
    it_heat = fields.Field('/tstat/ttemp', 't_heat', post_url='/tstat', post_name='it_heat')
    it_cool = fields.Field('/tstat/ttemp', 't_cool', post_url='/tstat', post_name='it_cool')

    tstate = fields.ReadOnlyField('/tstat', 'tstate',
        human_value_map={
            0 : 'Off',
            1 : 'Heat',
            2 : 'Cool'
    })
    fstate = fields.ReadOnlyField('/tstat', 'fstate',
        human_value_map={
            0 : 'Off',
            1 : 'On'
    })
    time = fields.Field('/tstat', 'time')
    pump = fields.ReadOnlyField('/tstat/hvac_settings', 'pump',
        human_value_map={
            1 : 'Normal',
            2 : 'Heat Pump'
    })
    aux_type = fields.ReadOnlyField('/tstat/hvac_settings', 'aux_type',
        human_value_map={
            1 : 'Gas',
            2 : 'Electric'
    })

    # LED status values: 1 = green, 2 = yellow, 4 = red
    energy_led = fields.WriteOnlyField('/tstat/led', 'energy_led', None)

    # This isn't documented. It might be postable, but I'm not going to try.
    power = fields.ReadOnlyField('/tstat/power', 'power')

    program_cool = fields.ReadOnlyField('/tstat/program/cool', None)
    program_heat = fields.ReadOnlyField('/tstat/program/heat', None)
    datalog = fields.ReadOnlyField('/tstat/datalog', None)

    # Remote temperature control; posting to rem_temp sets rem_mode to 1
    rem_mode = fields.Field('/tstat/remote_temp', 'rem_mode',
        human_value_map=ENABLED_HUMAN_VALUE_MAP)
    rem_temp = fields.WriteOnlyField('/tstat/remote_temp', 'rem_temp', None)

    ### sys subsystem ###
    sys = fields.ReadOnlyField('/sys', None)
    name = fields.Field('/sys/name', 'name')
    services = fields.ReadOnlyField('/sys/services', None)
    mode = fields.Field('/sys/mode', 'mode', human_value_map={
        0 : 'Provisioning',
        1: 'Normal'
    })
    network = fields.ReadOnlyField('/sys/network', None)
    security = fields.ReadOnlyField('/sys/network', 'security',
        human_value_map = {
            1 : 'WEP',
            3 : 'WPA',
            4 : 'WPA2 Personal'
    })

    ### cloud subsystem ###
    cloud = fields.ReadOnlyField('/cloud', None)

    ### methods ###
    def set_day_program(self, heat_cool, day, program):
        """
        Sets the program for a particular day. See the API docs for details,
        as it is a bit complicated.

        :param heat_cool:   Ether the string 'heat' or 'cool'
        :param day:         One of 'mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun'
        :param program:     See thermostat API docs
        :type program:      dict
        """
        self.post('/tstat/program/%s/%s' % (heat_cool, day), json.dumps(program).encode('utf-8'))


class CT30(CommonThermostat):
    """
    Base model for CT30-based thermostats (including the 3M-50)
    """

    hvac_code = fields.ReadOnlyField('/tstat/hvac_settings', 'hvac_code',
        human_value_map={
            1 : '1 stage heat, 1 stage cool',
            2 : '2 stage heat, 1 stage cool',
            3 : '2 stage heat, 2 stage cool',
            4 : '2 stage heat, 1 stage cool',
            5 : '2 stage heat, 2 stage cool',
            10 : '1 stage pump, 1 stage aux',
            11 : '1 stage pump, 1 stage aux',
            12 : '1 stage pump, no aux',
    })


class CT80(CommonThermostat):
    """
    Base model for CT80-based thermostats
    """

    # These three stages attributes take place of the CT30's hvac_code
    heat_stages = fields.ReadOnlyField('/tstat/hvac_settings', 'heat_stages')
    cool_stages = fields.ReadOnlyField('/tstat/hvac_settings', 'cool_stages')
    aux_stages = fields.ReadOnlyField('/tstat/hvac_settings', 'aux_stages')

    ### (De)humidifier system ###
    humidity = fields.ReadOnlyField('/tstat/humidity', 'humidity')

    humidifier_mode = fields.Field('/tstat/humidifier', 'humidifier_mode',
        human_value_map = {
            0: 'Off',
            1: 'Run only with heat',
            2: 'Run any time (runs fan)',
        })


class CT80RevB(CT80):
    """
    Base model for all Revision B versions of the CT80
    """

    swing = fields.Field('/tstat/tswing', 'tswing')

    # Dehumidifier attributes
    dehumidifier_mode = fields.Field('/tstat/dehumidifier', 'mode',
        human_value_map = {
            0: 'Off',
            1: 'On with fan',
            2: 'On without fan',
    })
    dehumidifier_setpoint = fields.Field('/tstat/dehumidifier', 'setpoint')

    # External dehumidifier
    external_dehumidifier_mode = fields.Field('/tstat/ext_dehumidifier', 'mode',
        human_value_map = {
            0: 'Off',
            1: 'On with fan',
            2: 'On without fan',
    })
    external_dehumidifier_setpoint = fields.Field('/tstat/ext_dehumidifier', 'setpoint')

    # Note: the night light is tricky and will return the last-set intensity even if it's off!
    night_light = fields.Field('/tstat/night_light', 'intensity',
        human_value_map = {
            0: 'Off',
            1: '25%',
            2: '50%',
            3: '75%',
            4: '100%',
        })

    # Note: lock_mode 3 can only be changed remotely
    lock_mode = fields.Field('/tstat/lock', 'lock_mode',
        human_value_map={
            0 : 'Lock disabled',
            1 : 'Partial lock',
            2 : 'Full lock',
            3 : 'Utility lock'
    })

    simple_mode = fields.Field('/tstat/simple_mode', 'simple_mode',
        human_value_map={
            1 : 'Normal mode',
            2 : 'Simple mode'
    })


# Specific model classes
class CT30v175(CT30):
    """
    Defines API features that differ for this specific model from
    CommonThermostat
    """
    MODEL = 'CT30 V1.75'


class CT30v192(CT30):
    """
    Defines API features that differ for this specific model from
    CommonThermostat
    """
    MODEL = 'CT30 V1.92'


class CT30v194(CT30):
    """
    Defines API features that differ for this specific model from
    CommonThermostat4
    """
    MODEL = 'CT30 V1.94'


class CT30v199(CT30):
    """
    Defines API features that differ for this specific model from
    CommonThermostat
    """
    MODEL = 'CT30 V1.99'


class CT50v109(CT30):
    """
    Defines API features that differ for this specific model from
    CommonThermostat
    """
    MODEL = 'CT50 V1.09'


class CT50v188(CT30):
    """
    Defines API features that differ for this specific model from
    CommonThermostat
    """
    MODEL = 'CT50 V1.88'


class CT50v192(CT30):
    """
    Defines API features that differ for this specific model from
    CommonThermostat
    """
    MODEL = 'CT50 V1.92'

    
class CT50v194(CT30):
    """
    Defines API features that differ for this specific model from
    CommonThermostat
    """
    MODEL = 'CT50 V1.94'


class CT80RevB2v103(CT80RevB):
    MODEL = 'CT80 Rev B2 V1.03'


class CT80RevB2v109(CT80RevB):
    MODEL = 'CT80 Rev B2 V1.09'

