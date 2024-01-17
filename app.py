from flask import Flask, render_template, request
import requests
import logging

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/colour", methods=["POST"])
def colourmind():
    input_rgb = request.args.get("colour")

    # Check if input_rgb is provided and is in correct format
    if input_rgb:
        try:
            # Convert the string to an array of integers
            rgb_values = list(map(int, input_rgb.split(',')))

            # Check if rgb_values contains exactly 3 integers
            if len(rgb_values) == 3:
                input_rgb_list = ["N", "N", rgb_values, "N", "N"]
            else:
                return render_template('error.html', 
error_message="Invalid RGB input. Please provide three comma-separated 
values.")

        except ValueError:
            # Handle case where conversion to integers fails
            return render_template('error.html', error_message="Invalid 
input format. Please use comma-separated integers for RGB values.")
    else:
        # Default to a random palette if no input is provided
        input_rgb_list = ["N"] * 5

    colour_response = requests.post(
        "http://colormind.io/api/",
        json={"input": input_rgb_list, "model": "ui"}
    )

    result = colour_response.json().get("result")
    return render_template('colour.html', palette=result)

if  __name__ == '__main__':
    app.run(debug=True)

