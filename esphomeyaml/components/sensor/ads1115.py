import voluptuous as vol

import esphomeyaml.config_validation as cv
from esphomeyaml.components import sensor
from esphomeyaml.components.ads1115 import ADS1115Component
from esphomeyaml.const import CONF_ADS1115_ID, CONF_GAIN, CONF_MULTIPLEXER, CONF_NAME, \
    CONF_UPDATE_INTERVAL
from esphomeyaml.helpers import get_variable

DEPENDENCIES = ['ads1115']

MUX = {
    'A0_A1': sensor.sensor_ns.ADS1115_MULTIPLEXER_P0_N1,
    'A0_A3': sensor.sensor_ns.ADS1115_MULTIPLEXER_P0_N3,
    'A1_A3': sensor.sensor_ns.ADS1115_MULTIPLEXER_P1_N3,
    'A2_A3': sensor.sensor_ns.ADS1115_MULTIPLEXER_P2_N3,
    'A0_GND': sensor.sensor_ns.ADS1115_MULTIPLEXER_P0_NG,
    'A1_GND': sensor.sensor_ns.ADS1115_MULTIPLEXER_P1_NG,
    'A2_GND': sensor.sensor_ns.ADS1115_MULTIPLEXER_P2_NG,
    'A3_GND': sensor.sensor_ns.ADS1115_MULTIPLEXER_P3_NG,
}

GAIN = {
    '6.144': sensor.sensor_ns.ADS1115_GAIN_6P144,
    '4.096': sensor.sensor_ns.ADS1115_GAIN_6P096,
    '2.048': sensor.sensor_ns.ADS1115_GAIN_2P048,
    '1.024': sensor.sensor_ns.ADS1115_GAIN_1P024,
    '0.512': sensor.sensor_ns.ADS1115_GAIN_0P512,
    '0.256': sensor.sensor_ns.ADS1115_GAIN_0P256,
}


def validate_gain(value):
    if isinstance(value, float):
        value = u'{:0.03f}'.format(value)
    elif not isinstance(value, (str, unicode)):
        raise vol.Invalid('invalid gain "{}"'.format(value))

    if value not in GAIN:
        raise vol.Invalid("Invalid gain, options are {}".format(', '.join(GAIN.keys())))
    return value


PLATFORM_SCHEMA = sensor.PLATFORM_SCHEMA.extend({
    cv.GenerateID('ads1115_sensor'): cv.register_variable_id,
    vol.Required(CONF_MULTIPLEXER): vol.All(vol.Upper, cv.one_of(*MUX)),
    vol.Required(CONF_GAIN): validate_gain,
    vol.Optional(CONF_ADS1115_ID): cv.variable_id,
    vol.Optional(CONF_UPDATE_INTERVAL): cv.positive_time_period_milliseconds,
}).extend(sensor.SENSOR_SCHEMA.schema)


def to_code(config):
    hub = get_variable(config.get(CONF_ADS1115_ID), ADS1115Component)

    mux = MUX[config[CONF_MULTIPLEXER]]
    gain = GAIN[config[CONF_GAIN]]
    rhs = hub.get_sensor(config[CONF_NAME], mux, gain, config.get(CONF_UPDATE_INTERVAL))
    sensor.register_sensor(rhs, config)


BUILD_FLAGS = '-DUSE_ADS1115_SENSOR'