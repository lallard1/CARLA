import glob
import os
import sys
import pandas as pd
#import xlsxwriter

try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import carla

camera_pos_log = []# ['x', 'y', 'z', 'roll', 'pitch', 'yaw']]

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

    finally:
        pass
        


if __name__ == '__main__':

    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        filename = 'Camera_pos.xlsx'
        #Save output to easily readable Excel File 
        df = pd.DataFrame(camera_pos_log)
        writer = pd.ExcelWriter(filename, engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Camera Positions from Spectator', index=False)
        writer.save()
        print('\n Camera positions have been saved to the file:', filename)
