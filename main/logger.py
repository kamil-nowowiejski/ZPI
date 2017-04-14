import cv2
import httplib
import base64
from datetime import datetime
from resources import res


def agent_registration(agent, protocol=None, request_type=None, language="SL", action_receiver_id=None,
                       action_sender_id=None):
    json = _agent_registration_json(agent, protocol, request_type, language, action_receiver_id, action_sender_id)
    return _send_json_to_server(res('logger\\url\\agents'), json)


def presence_request(agent, presence_type, protocol=None, request_type=None, language="SL", action_receiver_id=None,
                     action_sender_id=None):
    json = _presence_request_json(agent, presence_type, protocol, request_type, language, action_receiver_id,
                                  action_sender_id)
    return _send_json_to_server(res('logger\\url\\presence_requests'), json)


def object_registration(object_name, object_description, protocol=None, request_type=None, language="SL",
                        action_receiver_id=None, action_sender_id=None):
    json = _object_registration_json(object_name, object_description, protocol, request_type, language,
                                     action_receiver_id, action_sender_id)
    return _send_json_to_server(res('logger\\url\\objects'), json)


def feature_registration(feature_name, protocol=None, request_type=None, language="SL", action_receiver_id=None,
                         action_sender_id=None):
    json = _feature_registration_json(feature_name, protocol, request_type, language, action_receiver_id,
                                      action_sender_id)
    return _send_json_to_server(res('logger\\url\\features'), json)


def assessment_creation(assessment_value, object, feature, protocol=None, request_type=None, language="SL",
                        action_receiver_id=None, action_sender_id=None):
    json = _assessment_creation_json(assessment_value, object, feature, protocol, request_type, language,
                                     action_receiver_id, action_sender_id)
    return _send_json_to_server(res('logger\\url\\assessments'), json)


def communication_action_passing(protocol=None, request_type=None, language="SL", action_receiver_id=None,
                                 action_sender_id=None):
    json = _communication_action_passing_json(protocol, request_type, language, action_receiver_id, action_sender_id)
    return _send_json_to_server(res('logger\\url\\communicative_actions'), json)


def location_inform(x_position, y_position, protocol=None, request_type=None, language="SL", action_receiver_id=None,
                    action_sender_id=None):
    json = _location_inform_json(x_position, y_position, protocol, request_type, language, action_receiver_id,
                                 action_sender_id)
    return _send_json_to_server(res('logger\\url\\locations'), json)


def sensor_readout(readout_value, sensor, protocol=None, request_type=None, language="SL", action_receiver_id=None,
                   action_sender_id=None):
    json = _sensor_readout_json(readout_value, sensor, protocol, request_type, language, action_receiver_id, action_sender_id)
    return _send_json_to_server(res('logger\\url\\readouts'), json)


def graphical_readout(image, sensor, protocol=None, request_type=None, language="SL", action_receiver_id=None,
                      action_sender_id=None):
    json = _graphical_readout_json(image, sensor, protocol, request_type, language, action_receiver_id, action_sender_id)
    return _send_json_to_server(res('logger\\url\\graphical_readouts'), json)


def _send_json_to_server(relative_address, json):
    connection = httplib.HTTPConnection(res('logger\\url\\base'))
    headers = {'content-type': 'application/json'}
    connection.request("POST", relative_address, json, headers)
    return connection.getresponse()


def _agent_registration_json(agent, protocol, request_type, language, action_receiver_id, action_sender_id):
    return _create_complete_json(_agent_to_string(agent), protocol, request_type, language, action_receiver_id,
                                 action_sender_id)


def _presence_request_json(agent, presence_type, protocol, request_type, language, action_receiver_id,
                           action_sender_id):
    content = 'presenceStatus:' + presence_type + ',agent:' + agent.name
    return _create_complete_json(content, protocol, request_type, language, action_receiver_id, action_sender_id)


def _object_registration_json(object_name, object_description, protocol, request_type, language, action_receiver_id,
                              action_sender_id):
    content = 'objectName:' + object_name + ',objectDescription:' + object_description
    return _create_complete_json(content, protocol, request_type, language, action_receiver_id, action_sender_id)


def _feature_registration_json(feature_name, protocol, request_type, language, action_receiver_id, action_sender_id):
    content = 'featureName:' + feature_name
    return _create_complete_json(content, protocol, request_type, language, action_receiver_id, action_sender_id)


def _assessment_creation_json(assessment_value, object, feature, protocol, request_type, language, action_receiver_id,
                              action_sender_id):
    content = 'assessmentValue:' + str(assessment_value) + ',object:' + object.name + ',feature:' + feature
    return _create_complete_json(content, protocol, request_type, language, action_receiver_id, action_sender_id)


def _communication_action_passing_json(protocol, request_type, language, action_receiver_id, action_sender_id):
    return _create_complete_json(protocol, request_type, language, action_receiver_id, action_sender_id)


def _location_inform_json(x_position, y_position, protocol, request_type, language, action_receiver_id,
                          action_sender_id):
    content = 'xPosition:' + str(x_position) + ',yPosition:' + str(y_position)
    return _create_complete_json(content, protocol, request_type, language, action_receiver_id, action_sender_id)


def _sensor_readout_json(readout_value, sensor, protocol, request_type, language, action_receiver_id, action_sender_id):
    content = 'readoutValue:' + str(readout_value) + ',sensorName:' + sensor.name
    return _create_complete_json(content, protocol, request_type, language, action_receiver_id, action_sender_id)


def _graphical_readout_json(image, sensor, protocol, request_type, language, action_receiver_id, action_sender_id):
    img_str = base64.b64encode(cv2.imencode('.jpg', image)[1])
    content = 'image:' + img_str + ',sensor:' + sensor.name
    return _create_complete_json(content, protocol, request_type, language, action_receiver_id, action_sender_id)


def _agent_to_string(agent):
    result = 'agentName:' + agent.name + ',' \
           + 'agentDescription:' + agent.description + ','\
           + 'agentType:' + agent.type + ','\
           + 'sensors:'
    for sensor in agent.sensor_list:
        result += _sensor_to_string(sensor) + ';'
    if len(agent.sensor_list) != 0:
        result = result[0:len(result) - 1]
    return result


def _sensor_to_string(sensor):
    return 'sensorName-' + sensor.name \
         + ' sensorAccuracy-' + str(sensor.accuracy) \
         + ' unitType-' + sensor.unit_type \
         + ' sensorType-' + sensor.type


def _create_complete_json(content, protocol, request_type, language, action_receiver_id, action_sender_id):
    return '{' \
           + _create_communication_action_header(protocol, request_type, language, action_receiver_id, action_sender_id) \
           + ',' \
           + '"content":"' + content \
           + '"}'


def _create_communication_action_header(protocol, request_type, language, action_receiver_id, action_sender_id):
    result = ''
    result += _action_protocol(protocol) + ','
    result += _action_request_type(request_type) + ','
    result += _language(language) + ','
    result += _action_receiver(action_receiver_id) + ','
    result += _action_sender(action_sender_id) + ','
    result += _action_time()
    return result


def _action_protocol(protocol):
    if protocol is None:
        return '"action_protocol":null'
    return '"action_protocol":' + protocol + '"'


def _action_request_type(request_type):
    if request_type is None:
        return '"action_requesttype":null'
    return '"action_requesttype:' + request_type + '"'


def _language(language):
    return '"language":"' + language + '"'


def _action_receiver(action_receiver_id):
    if action_receiver_id is None:
        return '"action_receiver":null'
    return '"action_receiver":{"id":' + str(action_receiver_id) + '}'


def _action_sender(action_sender_id):
    if action_sender_id is None:
        return '"action_sender":null'
    return '"action_sender":{"id":' + str(action_sender_id) + '}'


def _action_time():
    return'"actionTime":"' + datetime.now().strftime('%Y-%m-%d' + 'T' + '%H:%M:%S') + '"'
