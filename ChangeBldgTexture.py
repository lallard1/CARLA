import glob
import os
import sys

# try:
# 	sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
# 		sys.version_info.major,
# 		sys.version_info.minor,
# 		'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
# except IndexError:
# 	pass

import carla
from PIL import Image
import random
import time


def main():

	try:
		# First of all, we need to create the client that will send the requests
		# to the simulator. Here we'll assume the simulator is accepting
		# requests in the localhost at port 2000.
		client = carla.Client('localhost', 2000)
		client.set_timeout(2.0)
		world = client.get_world()

		# Load the modified texture
		image = Image.open('T_Apartment04_D_Opt_Modified.tga')
		height = image.size[1]
		width = image.size[0]

		# Instantiate a carla.TextureColor object and populate
		# the pixels with data from the modified image
		texture = carla.TextureColor(width ,height)
		for x in range(0,width):
			for y in range(0,height):
				color = image.getpixel((x,y))
				r = int(color[0])
				g = int(color[1])
				b = int(color[2])
				a = 255
				texture.set(x, y, carla.Color(r,g,b,a))

		# Now apply the texture to the building asset
		world.apply_color_texture_to_object('BP_Apartment04_v05_Opt_2', carla.MaterialParameter.Diffuse, texture)

		

	finally:

		print('BP_Apartment04_v05_Opt_2 texture changed')


if __name__ == '__main__':

	main()
