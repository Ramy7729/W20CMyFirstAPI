import dbconnect
from flask import Flask, request, Response
import json

app = Flask(__name__)
# This decorater handles the get request.
@app.get("/animals")
def get_animals():
    # Creating a db connection and cursor.
    conn = dbconnect.get_db_connection()
    cursor = dbconnect.get_db_cursor(conn)
    # Initiaize variable to none. Will be used in a conditional check.
    animal_rows = None
    
    try:
        # Executing the select statement to fetch data from the animals table with specified columns.
        cursor.execute("SELECT mammal, id FROM animals")
        animal_rows = cursor.fetchall()

    except:
        # Handling error when having problems connecting to the db.
        print("Error in running db query")
        return Response("Error in running db query", mimetype="plain/text", status=500)
    # Closing the cursor and db connection.
    dbconnect.close_db_cursor(cursor)
    dbconnect.close_db_connection(conn)

    # Conditional statement to ensure that data was fetched without any errors.
    # If error occurs a response is sent back to the user.
    if(animal_rows == None):
        return Response("Failed to get animals from DB", mimetype="test/plain, status=500")
    else:
        # On succession data is converted to json and response is sent back to the user.
        response_body = json.dumps(animal_rows, default=str)
        return Response(response_body, mimetype="application/json", status=200)

# This decorater handles the post request.
@app.post("/animals")
def add_animal():
    try:  
        # Requesting json from user.
        add_mammal = request.json['add_mammal']
        
    except:
        print("Input Error")
        return Response("Too many characters entered, please try again", mimetype="plain/text", status=400)
    # Creating a db connection and cursor.
    conn = dbconnect.get_db_connection()
    cursor = dbconnect.get_db_cursor(conn)
    # Initializing variables for conditional checks.
    row_count = 0
    mammal_rows = None    
    
    try:
        # Execute insert statement to add mammal into table.
        cursor.execute("INSERT INTO animals (mammal) VALUES (?)", [add_mammal,])
        conn.commit()
        # Using the rowcount property to determine the number of rows.
        row_count = cursor.rowcount
        # Execute the select statement.
        cursor.execute("SELECT mammal FROM animals WHERE mammal=?", [add_mammal,])
        mammal_rows = cursor.fetchall()
       
    except:
        print("Error in running db query")
        return Response("Error in running db query", mimetype="plain/text", status=500)
   
    dbconnect.close_db_cursor(cursor)
    dbconnect.close_db_connection(conn)
    # Conditional that checks for the numbers of rows returned and if fetched data is available or not.
    if(row_count == 1 and mammal_rows != None):
        # Converting into json string and sending data back to user.
        response_body = json.dumps(mammal_rows, default=str)
        return Response(response_body, mimetype="application/json", status=200)
    else:   
        return Response("Failed to add a new animal", mimetype="application/json", status=200)

# This decorater handles the patch request.
@app.patch("/animals")
def update_animals():
    try:
        # Requesting data from user.
        update_mammal =request.json["update_mammal"]
        mammal_id = int(request.json["id"])
    # Handling error for user input.  
    except:
        print("Input error")
        return Response("Invalid id or too many characters entered, please try again", mimetype="text/plain", status=400)
    
    conn = dbconnect.get_db_connection()
    cursor = dbconnect.get_db_cursor(conn)
    row_count = 0
    updated_mammal = None
    
    try:
        # Executes update statement to change mammal name based on the id.
        cursor.execute("UPDATE animals SET mammal =? WHERE id=?", [update_mammal, mammal_id])
        conn.commit()
        # Using the rowcount property to determine the number of rows.
        row_count = cursor.rowcount
        cursor.execute("SELECT mammal, id FROM animals WHERE id=?", [mammal_id,])
        updated_mammal = cursor.fetchall()

    except:
        print("Error in running db query")
        return Response("Error in running db query", mimetype="text/plain", status=400)
    
    dbconnect.close_db_cursor(cursor)
    dbconnect.close_db_connection(conn)
    # Conditional that checks for a success in the update request.
    if(row_count ==1 and updated_mammal !=None):
        response_body = json.dumps(updated_mammal, default=str)
        return Response(response_body, mimetype="application/json", status=200)
        
    else:
        return Response("Failed to update animal", mimetype="text/plain", status=400)

# This decorater handles the delete request.
@app.delete("/animals")
def delete_animal():
    try:   
        # Requesting data from user.
        mammal_id = int(request.json['id'])
        
    except:
        print("Input error")
        return Response("Invalid input. Please enter a valid id.", mimetype="plain/text", status=500)
       
    conn = dbconnect.get_db_connection()
    cursor = dbconnect.get_db_cursor(conn)
    row_count = 0
    
    try:
        # Execute delete statment to delete an animal based on their id.
        cursor.execute("DELETE FROM animals WHERE id=?", [mammal_id,])
         # Using the rowcount property to determine the number of rows.
        row_count = cursor.rowcount
        conn.commit()
    
    except:
        print("Error in running db query")
        return Response("Error in running db query", mimetype="text/plain", status=400)
    
    dbconnect.close_db_cursor(cursor)
    dbconnect.close_db_connection(conn)
    # Conditional to check for a failed delete request.
    if(row_count == 0):
        response_body = json.dumps("Failed to delete animal!", default=str)
        return Response(response_body, mimetype="application/json", status=200)
    else:
        return Response("Animal deleted!", mimetype="text/plain", status=400)
    
app.run(debug=True)
