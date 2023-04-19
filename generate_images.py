##########################################################################################
# Imports
##########################################################################################
import pathlib
import sys

# Add base dir to PATH for module discovery within Blender
base_dir = pathlib.Path(__file__).parent
sys.path.append(str(base_dir))

from blenderline.settings import ImageGenerationSettings


##########################################################################################
# Main script
##########################################################################################
def main() -> None:
    settings = ImageGenerationSettings(base_dir, "config/example_beer/image.json")

    # Initialize scene by loading scene assets and configuring camera
    scene_manager = settings.get_scene_manager()
    scene_manager.initialize()


    hdr_manager = settings.get_hdr_manager()
    hdr_manager.initialize()
    hdr_manager.sample()

    background_manager = settings.get_background_manager()
    background_manager.initialize()
    background_manager.sample()


    item_manager = settings.get_item_manager()
    item_manager.initialize()

    item_1 = item_manager.item_collection.sample().spawn((0, 0, 0))
    item_2 = item_manager.item_collection.sample().spawn((0.24, 0, 0))
    item_3 = item_manager.item_collection.sample().spawn((-0.24, 0, 0))

    import bpy

    for i in range(100):
        location, normal_global_xy, normal_local_z = item_manager.path_reference.sample()
        point1 = location
        point2 = location + normal_local_z*0.1

        # Create a new mesh object
        mesh = bpy.data.meshes.new("Line")
        obj = bpy.data.objects.new("Line", mesh)
        bpy.context.collection.objects.link(obj)

        # Create a vertex list
        vertices = [point1, point2]

        # Create a mesh from the vertex list
        edges = []
        faces = []
        mesh.from_pydata(vertices, edges, faces)

        mesh.update()


if __name__ == "__main__":
    main()