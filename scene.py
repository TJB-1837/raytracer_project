import json
from pyray import Vector3
from sphere import Sphere
from rectangle import Rectangle
from light import Light
from color import Color

class Scene:
    def __init__(self,spheres,rectangles,lights):
        self.spheres = spheres
        self.rectangles = rectangles
        self.lights = lights


def load_scene_json(filename):
    with open(filename, "r") as f:
        data = json.load(f)

    # Camera
    cam_pos = data["camera"]["position"]
    camera_pos = Vector3(cam_pos[0], cam_pos[1], cam_pos[2])

    # Spheres
    spheres = []
    for s in data.get("spheres", []):
        spheres.append(
            Sphere(
                Vector3(*s["center"]),
                s["radius"],
                Color(*s["color"]),
                s["specular"],
                s["reflective"]
            )
        )

    # Rectangles
    rectangles = []
    for r in data.get("rectangles", []):
        rectangles.append(
            Rectangle(
                Vector3(*r["center"]),
                Vector3(*r["normal"]),
                r["width"],
                r["height"],
                Color(*r["color"]),
                r["specular"],
                r["reflective"]
            )
        )

    # Lights
    lights = []
    for l in data.get("lights", []):
        if l["type"] == "ambient":
            lights.append(Light("ambient", l["intensity"], None, None))

        elif l["type"] == "point":
            lights.append(
                Light(
                    "point",
                    l["intensity"],
                    Vector3(*l["position"]),
                    None
                )
            )

        elif l["type"] == "directional":
            lights.append(
                Light(
                    "directional",
                    l["intensity"],
                    None,
                    Vector3(*l["direction"])
                )
            )

    return Scene(spheres, rectangles, lights), camera_pos