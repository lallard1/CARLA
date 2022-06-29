#!/usr/bin/env python

# Copyright (c) 2019 Computer Vision Center (CVC) at the Universitat Autonoma de
# Barcelona (UAB).
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.

import glob
from importlib.resources import path
import os
import sys
import pandas as pd
from openpyxl import load_workbook
import xlrd

try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import carla

import random
import time



def main():
    actor_list = []
    #cam_bp =[]
    cam_transform =[]
    cam_actor =[]

    # In this tutorial script, we are going to add a vehicle to the simulation
    # and let it drive in autopilot. We will also create a camera attached to
    # that vehicle, and save all the images generated by the camera to disk.

    try:
        client = carla.Client('localhost', 2000)
        client.set_timeout(2.0)

        world = client.get_world()

        # The world contains the list blueprints that we can use for adding new
        # actors into the simulation.
        blueprint_library = world.get_blueprint_library()

        data_file = 'Camera_pos.xlsx'

        #Read in Spectator_data to get selected camera locations 
        #transform_variables = ['x', 'y', 'z', 'roll', 'pitch', 'yaw']
        df = pd.read_excel(data_file, sheet_name = 'Camera Positions from Spectator') # names = transform_variables)
    

        for row in range(len(df)):

            pos = (list(df.iloc[row,0:3]))
            rot = (list(df.iloc[row,3:6]))

            cam_bp = blueprint_library.find('sensor.camera.rgb')
            cam_bp.set_attribute("image_size_x",str(1920))
            cam_bp.set_attribute("image_size_y",str(1080))
            cam_bp.set_attribute("fov",str(105))
            cam_pos = carla.Location(pos[0],pos[1],pos[2])
            cam_rot = carla.Rotation(rot[1],rot[2],rot[0])
            cam_transform.append(carla.Transform(cam_pos,cam_rot))
            cam_actor.append(world.spawn_actor(cam_bp,cam_transform[row]))
            cam_actor[row].listen(lambda image: image.save_to_disk('recording/cam/%.6d.jpg' % image.frame))

        #for cameras in cam_actor:
            #cameras.listen(lambda image: image.save_to_disk('recording/output/%.6d.jpg' % image.frame))

        time.sleep(5)

    finally:

        print('destroying actors')
        #cam_actor.destroy()
        client.apply_batch([carla.command.DestroyActor(x) for x in cam_actor])
        print('done.')


if __name__ == '__main__':

    main()
