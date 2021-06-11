# Collaborated with Liz for this assignment.

from flask import Flask, Response
import json

# Creating the flask object.
app = Flask(__name__)

# Hardcoded database.
animals = ["dragon", "dog", "Pikachu", "cat", "rabbit"]

# This decorater handles the get request.
@app.get("/animals")
def get_animals():
    # Converting into json string.
    response_body = json.dumps(animals, default=str)
    # Returing json object to the user.
    return Response(response_body, mimetype="application/json", status=200)

# This decorater handles the post request.
@app.post("/animals")
def add_animal():
    # Using the append method to add an animal to the list.
    animals.append("mouse")
    # This returns a response message to the user on succession.
    return Response("Success! Animal added", mimetype="text/plain", status=200)

# This decorater handles the patch request.
@app.patch("/animals")
def edit_animal():
    try:
        # Specifying the animal to be edited by using an index.
        animals[3] = "Battle Cat"
        return Response("Success! Animal modified", mimetype="text/plain", status=200)
    # Handling an error when there are less than four items.
    except IndexError:
        return Response("I don't have the power", mimetype="text/plain", status=500)

# This decorater handles a delete request.       
@app.delete("/animals")
def delete_animal():
    try:
        # Using the pop method to delete an animal from the end of the list.
        animals.pop()
        # This returns a response message to the user on succession.
        return Response("Success! Animal deleted", mimetype="text/plain", status=200)
    # Handling an error when there are no more animals to be deleted.
    except IndexError:
        return Response("I don't have the power", mimetype="text/plain", status=500)

# Starts the application flask server. 
# An argument is passed that enables debugging mode to be turned on.
app.run(debug=True)
