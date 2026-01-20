Raytracing Project

Author: MARMOL Antoine / PITOLET Alex
--------------------------------------------
Description
--------------------------------------------

This project implements a simple raytracer in Python.
It renders static images of 3D scenes composed of spheres,
rectangular walls and multiple light sources.

The output is a bitmap image in the PPM (Portable Pixmap) format.

--------------------------------------------
Features
--------------------------------------------
- Ray-sphere and ray-rectangle intersections
- Diffuse and specular lighting 
- Shadows
- Reflections (recursive ray tracing)
- Scene loaded from a text file
- Output image in PPM format

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
   pip install numpy pyray
3. Place a scene description file (e.g. scene.json) in the project directory.
4. Run:
   python main.py
5. The rendered image will be saved as:
   output.ppm

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
- point intensity x y z
- directional intensity dx dy dz

Lines starting with # are comments.

--------------------------------------------
Output
--------------------------------------------
The program generates a PPM image (ASCII P3 format),
which can be opened with most image viewers or converted
using tools such as GIMP.

--------------------------------------------