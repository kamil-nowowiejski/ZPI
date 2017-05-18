import json
import cv2
import main.logger as log
from main.resources import res
from main.Agent import Agent, Sensor
from main.object import Object


def test_agent_registration_server_response_empty_strings():
    agent = Agent(1, '', '', '', [])
    response = log.agent_registration(agent, None, None, 'SL', None, None)
    assert response.status != 404 and response.status != 500


def test_agent_registration_server_response():
    sensor1 = Sensor('A222', 21.02, 'second', 'accelerometr')
    sensor2 = Sensor('B333', 56.0003, 'meter', 'mleko')
    agent = Agent(1, 'xxx', 'rrr', 'yyy', [sensor1, sensor2])
    response = log.agent_registration(agent, None, None, 'SL', None, None)
    assert response.status != 404 and response.status != 500


def test_presence_request_server_response_empty_strings():
    agent = Agent(1, '', '', '', [])
    response = log.presence_request(agent, 'mleko', None, None, 'SL', None, None)
    assert response.status != 404 and response.status != 500


def test_presence_request_server_response():
    sensor1 = Sensor('A222', 21.02, 'second', 'accelerometr')
    sensor2 = Sensor('B333', 56.0003, 'meter', 'mleko')
    agent = Agent(1, 'xxx', 'rrr', 'yyy', [sensor1, sensor2])
    response = log.presence_request(agent, 'mleko', None, None, 'SL', None, None)
    assert response.status != 404 and response.status != 500


def test_register_object_server_response_empty_strings():
    response = log.object_registration('', '', None, None, 'SL', None, None)
    assert response.status != 404 and response.status != 500


def test_register_object_server_response():
    response = log.object_registration('fasfs', 'fasfas', None, None, 'SL', None, None)
    assert response.status != 404 and response.status != 500


def test_register_feature_server_response_empty_strings():
    response = log.feature_registration('', None, None, 'SL', None, None)
    assert response.status != 404 and response.status != 500


def test_register_feature_server_response():
    response = log.feature_registration('color red', None, None, 'SL', None, None)
    assert response.status != 404 and response.status != 500


def test_assessment_server_response_empty_strings():
    object = Object(1, '')
    response = log.assessment_creation(0, object, '', None, None, 'SL', None, None)
    assert response.status != 404 and response.status != 500


def test_assessment_server_response():
    object = Object(1, 'fsgfsgd')
    response = log.assessment_creation(0, object, 'red color', None, None, 'SL', None, None)
    assert response.status != 404 and response.status != 500


def test_location_server_response():
    response = log.location_inform(0, 0, None, None, 'SL', None, None)
    assert response.status != 404 and response.status != 500


def test_readout_server_response():
    sensor = Sensor('', 3, '', '')
    response = log.sensor_readout(0, sensor, None, None, 'SL', None, None)
    assert response.status != 404 and response.status != 500


def test_graphical_readout_image_conversion():
    image = cv2.imread('tests\\images\\hsv_color_test.jpg')
    sensor = Sensor('A222', 21.02, 'second', 'accelerometr')
    response = log.graphical_readout(image, sensor, None, None, 'SL', None, 1)
    assert response.status == 201


def test__agent_registration_json_agent_with_sensors():
    agent = Agent(1, 'Adam1', 'Testowy agent', 'agent_mobilny', [])
    sensor1 = Sensor('A222', 21.02, 'second', 'accelerometr')
    sensor2 = Sensor('B333', 56.0003, 'meter', 'mleko')
    agent.sensor_list.append(sensor1)
    agent.sensor_list.append(sensor2)

    result = log._agent_registration_json(agent, protocol=None, request_type=None, language='SL', action_receiver_id=None,
                                          action_sender_id=1)
    json_data = json.loads(result)
    assert json_data['content'] == 'agentName:Adam1,agentDescription:Testowy agent,agentType:agent_mobilny,' \
                                    + 'sensors:sensorName-A222 sensorAccuracy-21.02 ' \
                                    + 'unitType-second sensorType-accelerometr;' \
                                    + 'sensorName-B333 sensorAccuracy-56.0003 unitType-meter sensorType-mleko'
    assert json_data['action_protocol'] is None
    assert json_data['action_requesttype'] is None
    assert json_data['language'] == 'SL'
    assert json_data['action_receiver'] is None
    assert json_data['action_sender']['id'] == 1


def test__agent_registration_json_agent_without_sensors():
    agent = Agent(1, 'Adam1', 'Testowy agent', 'agent_mobilny', [])

    result = log._agent_registration_json(agent, protocol=None, request_type=None, language='SL', action_receiver_id=3,
                                          action_sender_id=None)
    json_data = json.loads(result)
    assert json_data['content'] == 'agentName:Adam1,agentDescription:Testowy agent,agentType:agent_mobilny,sensors:'
    assert json_data['action_protocol'] is None
    assert json_data['action_requesttype'] is None
    assert json_data['language'] == 'SL'
    assert json_data['action_receiver']['id'] == 3
    assert json_data['action_sender'] is None


def test__presence_request_json():
    agent = Agent(1, 'Adam1', 'Testowy agent', 'agent_mobilny', [])

    result = log._presence_request_json(agent, res('logger\\precence_type\\start'), protocol=None, request_type=None,
                                        language='SL', action_receiver_id=3, action_sender_id=None)
    json_data = json.loads(result)

    assert json_data['content'] == 'presenceStatus:start_presence,agent:Adam1'


def test__registered_object_json():
    result = log._object_registration_json('kostka', 'mala kostka', None, None, 'SL', None, None)
    json_data = json.loads(result)

    assert json_data['content'] == 'objectName:kostka,objectDescription:mala kostka'


def test__registered_feature_json():
    result = log._feature_registration_json('red', None, None, 'SL', None, None)
    json_data = json.loads(result)

    assert json_data['content'] == 'featureName:red'


def test__assessment_json():
    object = Object(4, 'mleko')
    result = log._assessment_creation_json(574.342, object, 'czerwony', None, None, 'SL', None, None)
    json_data = json.loads(result)

    assert json_data['content'] == 'assessmentValue:574.342,object:mleko,feature:czerwony'


def test__location_json():
    result = log._location_inform_json(-947.34, -64.3, None, None, 'SL', None, None)
    json_data = json.loads(result)

    assert json_data['content'] == 'xPosition:-947.34,yPosition:-64.3'


def test__readout_json():
    sensor = Sensor('B333', 56.0003, 'meter', 'mleko')

    result = log._sensor_readout_json(54653.45656, sensor, None, None, 'SL', None, None)
    json_data = json.loads(result)

    assert json_data['content'] == 'readoutValue:54653.45656,sensorName:B333'
