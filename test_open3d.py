import open3d as o3d

mesh = o3d.geometry.TriangleMesh.create_sphere(radius=1.0)

mesh.paint_uniform_color([1, 0, 0])

o3d.visualization.draw_geometries([mesh])