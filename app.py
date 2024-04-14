from flask import Flask, jsonify, request
from flask_marshmallow import Marshmallow
from marshmallow import fields, ValidationError
from connect_db import connect_db, Error

app = Flask(__name__)
app.json.sort_keys = False

ma = Marshmallow(app)


class MemberSchema(ma.Schema):
    member_id = fields.Int(dump_only=True)
    name = fields.String(required=True)
    email = fields.String(required=True)
    phone = fields.String(required=True)
    membership_type = fields.String(required=True)


    class Meta:  
        
        fields = ("member_id", "name", "email", "phone", "membership_type")

member_schema = MemberSchema()
members_schema = MemberSchema(many=True)

@app.route('/')
def home():
    return "Welcome to our super cool Fitness Tracker, time to get swole brah!"

@app.route('/members', methods=['GET'])
def get_members(): 
    print("hello from the get")  
    try:
        conn = connect_db()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        
        cursor = conn.cursor(dictionary=True) 

        query = "SELECT * FROM Members"

        cursor.execute(query)

        members = cursor.fetchall()

        return members_schema.jsonify(members)
    
    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/members', methods = ['POST']) 
def add_member():
    try:
        member_data = member_schema.load(request.json)

    except ValidationError as e:
        print(f"Error: {e}")
        return jsonify(e.messages), 400

    try:
        conn = connect_db()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor()

        new_member = (member_data['name'], member_data['email'], member_data['phone'], member_data['membership_type'])

        query = "INSERT INTO Members (name, email, phone, membership_type) VALUES (%s, %s, %s, %s)"

        cursor.execute(query, new_member)
        conn.commit()

        return jsonify({"message":"New member added succesfully"}), 201

    except Error as e:
        print(f"error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/members/<int:member_id>', methods= ["PUT"])
def update_member(member_id):
    print("hello")
    try:
        member_data = member_schema.load(request.json)
        print(member_data)

    except ValidationError as e:
        print(f"Error: {e}")
        return jsonify(e.messages), 400
    
    try:
        conn = connect_db()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor()

        updated_member = (member_data['name'], member_data['email'], member_data['phone'], member_data['membership_type'], member_id)

        query = "UPDATE Members SET name = %s, email = %s, phone = %s, membership_type = %s WHERE member_id = %s"

        cursor.execute(query, updated_member)
        conn.commit()

        return jsonify({"message":"Member details were succesfully updated!"}), 200
    
    except Error as e:
        print(f"error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/members/<int:id>', methods=["DELETE"])
def delete_member(id):
    try:
        conn = connect_db()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor()
        member_to_remove = (id,)
        

        query = "SELECT * FROM Members WHERE member_id = %s"
        cursor.execute(query, member_to_remove)
        member = cursor.fetchone()
        if not member:
            return jsonify({"error": "User does not exist"}), 404
        
        del_query = "DELETE FROM Member WHERE member_id = %s"
        cursor.execute(del_query, member_to_remove)
        conn.commit()

        return jsonify({"message":"Member Removed succesfully"}), 200

    except Error as e:
        print(f"error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close() 

class WorkoutSchema(ma.Schema):
    sesh_id = fields.Int(dump_only=True)
    date = fields.String(required=True)
    member_id = fields.Int(required=True)
    workout_type = fields.String(required=True)

    class Meta:
        fields = ("sesh_id", "date", "member_id", "workout_type")

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)

@app.route('/workouts', methods=['GET'])
def get_workouts(): 
    print("hello from the get")  
    try:
        conn = connect_db()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM Dank_sesh"
        cursor.execute(query)

        workouts = cursor.fetchall()
      
        return workouts_schema.jsonify(workouts)
    
    except Error as e:
     
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    
    finally:
      
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/workouts', methods = ['POST']) 
def add_workout():
    try:
        workout_data = workout_schema.load(request.json)

    except ValidationError as e:
        print(f"Error: {e}")
        return jsonify(e.messages), 400

    try:
        conn = connect_db()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor()

        new_workout = (workout_data['date'], workout_data['member_id'], workout_data['workout_type'])

        query = "INSERT INTO Dank_sesh (date, member_id, workout_type) VALUES (%s, %s, %s)"

        cursor.execute(query, new_workout)
        conn.commit()

        return jsonify({"message":"New workout added succesfully"}), 201

    except Error as e:
        print(f"error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/workouts/<int:id>', methods= ["PUT"])
def update_workout(id):
    print("hello")
    try:
        workout_data = workout_schema.load(request.json)
        print(workout_data)

    except ValidationError as e:
        print(f"Error: {e}")
        return jsonify(e.messages), 400
    
    try:
        conn = connect_db()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor()

        updated_workout = (workout_data['date'], workout_data['member_id'], workout_data['workout_type'], id)

        query = "UPDATE Dank_sesh SET date = %s, member_id = %s, workout_type = %s WHERE sesh_id = %s"

        cursor.execute(query, updated_workout)
        conn.commit()

        return jsonify({"message":"Workout details were succesfully updated!"}), 200
    
    except Error as e:
        print(f"error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()



if __name__ == "__main__":
    app.run(debug=True)