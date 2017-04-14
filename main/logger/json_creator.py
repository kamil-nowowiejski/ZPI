from datetime import datetime


def agent_registration(agent, protocol=None, language="SL", action_receiver_id=None, action_sender_id=None):
    return _create_complete_json(_agent_to_string(agent), protocol, language, action_receiver_id, action_sender_id)


def presence_request(agent, presence_type, protocol=None, language="SL", action_receiver_id=None, action_sender_id=None):
    content = '"presenceStatus:' + presence_type + ',agent:'
    return _create_complete_json()


def object_registration(object_name, object_description, protocol=None, language="SL", action_receiver_id=None, action_sender_id=None):
    content = 'objectName:' + object_name + ',objectDescription:' + object_description
    return _create_complete_json(content, protocol, language, action_receiver_id, action_sender_id)


def feature_registration(feature_name, protocol=None, language="SL", action_receiver_id=None, action_sender_id=None):
    content = 'featureName:' + feature_name
    return _create_complete_json(content, protocol, language, action_receiver_id, action_sender_id)

def

def _agent_to_string(agent):
    result = 'agentName:' + agent.name + ',' \
           + 'agentDescription:' + agent.description + ','\
           + 'agentType:' + agent.type + ','\
           + 'sensors:'
    for sensor in agent.sensor_list:
        result += _sensor_to_string(sensor) + ";"
    return result[0:len(result)-2]


def _sensor_to_string(sensor):
    return 'sensorName-' + sensor.name \
         + 'sensorAccuracy-' + sensor.accuracy \
         + 'unitType-' + sensor.unit_type \
         + 'sensorType-' + sensor.type


def _create_complete_json(content, protocol=None, language="SL", action_receiver_id=None, action_sender_id=None):
    return '{' \
           + _create_communication_action_header(protocol, language, action_receiver_id, action_sender_id) \
           + ',' \
           + '"content":"' + content \
           + '"}'


def _create_communication_action_header(protocol=None, language="SL", action_receiver_id=None, action_sender_id=None):
    result = ''
    result += _action_protocol(protocol)
    result += _language(language)
    result += _action_receiver(action_receiver_id)
    result += _action_sender(action_sender_id)
    result += _action_time()


def _action_protocol(protocol):
    if protocol is None:
         return '"action_protocol":null'
    return '"action_protocol":' + protocol + '"'


def _language(language):
    return '"language":"' + language + '"'


def _action_receiver(action_receiver_id):
    if action_receiver_id is None:
        return '"action_receiver":null'
    return '"action_receiver":{"id":' + action_receiver_id + '}'


def _action_sender(action_sender_id):
    if action_sender_id is None:
        return '"action_sender":null'
    return '"action_sender":{"id":' + action_sender_id + '}'


def _action_time():
    return'"actionTime":"' + datetime.now().isoformat() + '"'
