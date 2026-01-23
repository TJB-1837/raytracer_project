Raytracing Project

Author: MARMOL Antoine / PITOLET Alex
--------------------------------------------
Description
--------------------------------------------

This project implements a simple raytracer in Python.
It renders static images of 3D scenes composed of spheres,
rectangular walls and multiple light sources.

The output is one (or multiple) bitmap image(s) in the PPM (Portable Pixmap) format.


--------------------------------------------
Features
--------------------------------------------
- Ray-sphere and ray-rectangle intersections
- Diffuse and specular lighting 
- Shadows
- Reflections (recursive ray tracing)
- Scene loaded from a text file
- Output image(s) in PPM format
- Basic user interactions 

--------------------------------------------
Requirements
--------------------------------------------
Python 3.x

Required packages:
- numpy
- json
- pyray (for Vector3 structure only)

--------------------------------------------
How to run
--------------------------------------------
1. Make sure Python 3 is installed.
2. Install required packages if needed:
   pip install numpy pyray json
3. Place a scene description file (e.g. scene.json) in the project directory.
4. Run:
   python main.py
5. Chose your rendering type : "i" for an image and "a" for animation
5.5. If image rendering selected, you will have to provide an angle (in radian) and an axis for the camera rotation : follow the displayed instructions to make sure no error will occur.

5. The rendered image(s) will be saved as:
   - output.ppm (if image rendering)
   - frame_0x.ppm (30 frames generated for animation rendering, with these images you will be able to create a gif online)

--------------------------------------------
Scene file format
--------------------------------------------
Scene description is provided in JSON format (scene.json),
which is a structured text format.

Supported objects:
- camera x y z
- sphere x y z radius r g b specular reflective
- rectangle cx cy cz nx ny nz width height r g b specular reflective
- ambient intensity
- point intensity x y z (MANDATORY to be declared as the second light in your json file if you want the animation feature to work)
- directional intensity dx dy dz

Lines starting with # are comments.

--------------------------------------------
Output
--------------------------------------------
The program generates PPM image(s) (ASCII P3 format),
which can be opened with most image viewers or converted
using tools such as GIMP.

--------------------------------------------