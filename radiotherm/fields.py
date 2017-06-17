import json

from . import validate

class Field(object):
    """
    Instances of this class act as descriptors on the Thermostat class. They
    define a piece of data from the API that can be accessed with GET and
    optionally with POST.
    """
    def __init__(self, url, name, human_value_map=None, post_url=None, post_name=None):
        """
        :param url:             relative URL to use for GET and POST, except
                                when post_url is defined.
        :param name:            key value for the data point you want. Most
                                responses come as a dictionary, for example
                                {'temp' : 73}, so you would pass 'temp' for
                                this argument.
        :param human_value_map: An optional dictionary where keys are actual
                                values the server might return, and values
                                are a human-readable form. This is useful for
                                example when a return value of "0" actually
                                means "Off". If you pass this argument, make
                                sure it includes all possible values.
        :param post_url:        A few items require you to POST to a different
                                URL than where you GET. Use this argument to
                                specify a POST URL, and the 'url' argument will
                                continue to be used for GETs.
        :param post_name:       A few items that can be set are not available
                                for reading, such as it_heat. Use this argument
                                to specify a POST variable which is different
                                from the GET variable.
        """
        self.url = url
        self.name = name
        self.human_value_map = human_value_map
        self.post_url = post_url
        self.post_name = post_name

    def __get__(self, instance, owner):
        response = instance.get(self.url)
        envelope = json.loads(response.read().decode('utf-8'))
        validate.validate_response(response, envelope)
        return self._build_get_return(envelope)

    def _build_get_return(self, envelope):
        """
        :param envelope:    raw value returned from the thermostat, which
                            usually is a dict. There are some attributes that
                            don't come with an envelope, and are just the raw
                            value by itself. In that case, set name=None.

        :returns:   dict with key 'raw' whose value is the value this Field is
                    setup to return. For example, it might be the current temp.
                    If there is a human_value_map, this dict will have an
                    additional 'human' key whose value is a human-readable
                    version of the raw value.
        """
        # Some URLs, like /tstat, don't have an envelope
        ret = {'raw' : envelope.get(self.name) if self.name else envelope}
        if self.human_value_map:
            ret['human'] = self._convert_to_human(ret['raw'])
        return ret

    def __set__(self, instance, value):
        data = json.dumps({self.post_name or self.name: value}).encode('utf-8')
        response = instance.post(self.post_url or self.url, data)
        validate.validate_response(response)

    def _convert_to_human(self, value):
        """
        :param value:   raw value retrieved from the thermostat and removed
                        from its envelope

        :returns:   human-readable version of the value, as retrieved from
                    self.human_value_map
        """
        try:
            return self.human_value_map[value]
        except KeyError:
            raise AttributeError('Human readable value not known for raw value %s' %
                (str(value)))


class ReadOnlyField(Field):
    """For read-only values like the current temperature"""
    def __set__(self, instance, value):
        raise TypeError('This attribute does not support writes.')


class WriteOnlyField(Field):
    """For write-only values like the remote temperature"""
    def __get__(self, instance, owner):
        raise TypeError('This attribute does not support reads.')
