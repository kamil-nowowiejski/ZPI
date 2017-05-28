import Agent.ImageProcessing.size_detection as sd

def test_test_1():
    distance = 30.0
    object_size = (85., 1623.)
    image_resolution = (3120., 4160.)
    print sd.assume_size(distance, object_size, image_resolution, h_fov=80., v_fov=80.0)