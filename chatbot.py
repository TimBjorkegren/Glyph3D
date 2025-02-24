import open3d as o3d
from openai import OpenAI
from flask import Flask, request, jsonify
import numpy as np
import os

app = Flask(__name__)

client = OpenAI(api_key="#")

def generate_3d_model(shape, color):
    if (shape == "sphere"):
        mesh = o3d.geometry.TriangleMesh.create_sphere(radius=1.0)
    elif shape == "cube":
        mesh = o3d.geometry.TriangleMesh.create_box(width=1.0, height=1.0, depth=1.0)
    elif shape == "cylinder":
        mesh = o3d.geometry.TriangleMesh.create_cylinder(radius=0.5, height=1.5)
    else: return None

    color_dict ={
        "red": [1, 0, 0],
        "green": [0,1,0],
        "blue": [0,0,1],
        "yellow": [1,1,0]
    }

    mesh.paint_uniform_color(color_dict.get(color, [1, 1, 1]))

    if not os.path.exists("static"):
        os.makedirs("static")

    file_path = f"static/{shape}.ply"
    o3d.io.write_triangle_mesh(file_path, mesh)

    return file_path


@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")


    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo", 
            messages=[
                {"role": "user", "content": f"Extract shape and color from this request: {user_input}"}
            ],
            max_tokens=100
        )

        ai_response = response.choices[0].message.content.strip().lower()

        shape = None
        color = None

        if "sphere" in ai_response:
            shape = "sphere"
        elif "cube" in ai_response:
            shape = "cube"
        elif "cylinder" in ai_response:
            shape = "cylinder"

        if "red" in ai_response:
            color = "red"
        elif "green" in ai_response:
            color = "green"
        elif "blue" in ai_response:
            color = "blue"
        elif "yellow" in ai_response:
            color = "yellow"

        if shape and color:
            model_path = generate_3d_model(shape, color)
            if model_path:
                return jsonify({"reply": f"Here is your {color} {shape}!", "model_url": model_path})

    except Exception as e:
        print(f"Error: {e}")

    return jsonify({"reply": "Please specify a valid shape (sphere, cube, cylinder) and color"})

if __name__ == "__main__":
    app.run(debug=True)