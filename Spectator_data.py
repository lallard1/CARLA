import glob
import os
import sys
import pandas as pd
import yaml 
import carla

try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

def let_user_pick(options):
    print("Please choose sensor type:")

    for idx, element in enumerate(options):
        print("{}) {}".format(idx + 1, element))

    i = input("Enter number: ")
    try:
        if 0 < int(i) <= len(options):
            return options[int(i) - 1]
    except:
        pass
    return None


camera_pos_log = []# ['x', 'y', 'z', 'roll', 'pitch', 'yaw']]
all_sensors = []

# filepath = 'configs/camera_pos.yaml'
# with open(filepath, 'r') as stream:
#     try:
#         d = yaml.safe_load(stream)
#         print(d)
#     except yaml.YAMLError as e:
#         print(e)




def main():
    
    try:
        client = carla.Client('localhost', 2000)
        client.set_timeout(2.0)
        world = client.get_world()

        while True:

            location =[]
            input("Press enter to record the Spectator's position. Press ctrl + c to quit...")
            spectator = world.get_spectator()
            pos = spectator.get_transform()
            print("\nThe spectator's position is:" , pos.location, "and it's rotation angles are:" , pos.rotation)
            location.append(pos.location.x)
            location.append(pos.location.y)
            location.append(pos.location.z)
            location.append(pos.rotation.roll)
            location.append(pos.rotation.pitch)
            location.append(pos.rotation.yaw)
            camera_pos_log.append(location)    

            # Get sensor types for location
            num_sensors = int(input("How many sensors in this location? "))
            type_sensors = []
            options = ["sensor.camera.rgb", "sensor.camera.instance_segmentation", "sensor.camera.depth"] # add other sensor types later
            for i in range(num_sensors):
                res = let_user_pick(options)    
                type_sensors.append(res)
            all_sensors.append(type_sensors)

    finally:
        pass
        #final_dict = create_dict(camera_pos_log, all_sensors, sensor_dict)
        
# for each location in camera_pos_log, add key/value pairs to sensor dict for the sensors specified
def create_dict(camera_pos_log, all_sensors):
    sensor_dict = {'spawn_actors': []} # {'spawn_actors': [{'blueprint': {...}, 'transform': {...}}]} 
    for i, pos in enumerate(camera_pos_log):
        for sensor in all_sensors[i]:
            sensor_dict['spawn_actors'].append(
                {'blueprint': {'name': sensor, 'attr': {'image_size_x': '1280', 'image_size_y': '960'}}, 
                'transform': {'location': {'x': pos[0], 'y': pos[1], 'z': pos[2]}, 'rotation': {'roll': pos[3],
                    'pitch': pos[4], 'yaw': pos[5]}}})  
            
            # {('spawn_actors', [ ... ])})

    return(sensor_dict)


if __name__ == '__main__':

    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        
        filename = 'sensor_pos.xlsx' 
        df = pd.DataFrame(camera_pos_log)
        writer = pd.ExcelWriter(filename, engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Sensor Positions from Spectator', index=False)
        writer.save()

        final_dict = create_dict(camera_pos_log, all_sensors)
        #del final_dict['spawn_actors'][0]
        with open(r'sensor_pos.yaml', 'w') as file:
            documents = yaml.dump(final_dict, file)
        print('\n Sensor positions have been saved to the excel file:', filename, 'and the config file has been saved as sensor_pos.yaml file')

