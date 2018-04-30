
import numpy as np

import rospy
import actionlib
import pc_pipeline_msgs.msg


def ros_mesh_msg_to_daefile(mesh, dae_filepath):
    import mcubes

    vs = []
    for vert in mesh.vertices:
        vs.append((vert.x, vert.y, vert.z))
    vertices = np.array(vs)

    ts = []
    for tri in mesh.triangles:
        ts.append(tri.vertex_indices)
    triangles = np.array(ts)

    mcubes.export_mesh(vertices, triangles, dae_filepath, "model")


def ros_mesh_msg_to_plyfile(mesh_msg, ply_filepath):
    # vertex = numpy.array([(0, 0, 0),
    #                       (0, 1, 1),
    #                       (1, 0, 1),
    #                       (1, 1, 0)],
    #                       dtype=[('x', 'f4'), ('y', 'f4'), ('z', 'f4')])
    # face = numpy.array([([0, 1, 2],),
    #                     ([0, 2, 3],),
    #                     ([0, 1, 3],),
    #                     ([1, 2, 3],)],
    #                     dtype=[('vertex_indices', 'i4', (3,))])
    from plyfile import PlyData, PlyElement

    vertices = [(x.x, x.y, x.z) for x in mesh_msg.vertices]
    faces = [(x.vertex_indices, ) for x in mesh_msg.triangles]

    vertices_np = np.array(
        vertices, dtype=[('x', 'f4'), ('y', 'f4'), ('z', 'f4')])
    faces_np = np.array(faces, dtype=[('vertex_indices', 'i4', (3, ))])

    vertex_element = PlyElement.describe(vertices_np, 'vertex')
    face_element = PlyElement.describe(faces_np, 'face')

    PlyData([vertex_element, face_element], text=True).write(ply_filepath)


def complete_scene(object_completion_topic):
    # create an action server client
    # and wait for the server to come up.
    scene_completion_client = actionlib.SimpleActionClient(
        "SceneCompletion",
        pc_pipeline_msgs.msg.CompleteSceneAction)
    rospy.loginfo("waiting for scene_completion server...")
    scene_completion_client.wait_for_server()
    rospy.loginfo("scene_completion server started")

    # send an empty goal requesting a completed planning scene
    rospy.loginfo("about to send scene_completion goal")
    goal = pc_pipeline_msgs.msg.CompleteSceneGoal()
    goal.object_completion_topic = object_completion_topic
    scene_completion_client.send_goal(goal)

    rospy.loginfo("waiting for result")
    scene_completion_client.wait_for_result()

    rospy.loginfo("received result")
    result = scene_completion_client.get_result()

    return result
