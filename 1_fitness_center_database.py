from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

db_config = {
    'database' : 'Lesson_2_Assignment_Structured_Query_Language',
    'user' : 'your_username',
    'password': 'your_password',
    'host': 'localhost',
}

def get_db_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except Error as e:
        print(f'Error: {e}')
        return None

@app.route('/members', methods=['POST'])
def add_member():
    data = request.json
    name = data.get('name')
    age = data.get('age')

    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("INSERT INTO Members (name, age) VALUES (%s, %s)", (name, age))
            connection.commit()
            return jsonify({'message': 'Member added successfully!'}), 201
        except Error as e:
            return jsonify({'error': str(e)}), 400
        finally:
            cursor.close()
            connection.close()
    return jsonify({'error': 'Database connection failed'}), 500

@app.route('/members/<int:id>', methods=['GET'])
def get_member(id):
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM Members WHERE id = %s", (id,))
            member = cursor.fetchone()
            if member:
                return jsonify(member), 200
            else:
                return jsonify({'message': 'Member not found'}), 404
        except Error as e:
            return jsonify({'error': str(e)}), 400
        finally:
            cursor.close()
            connection.close()
    return jsonify({'error': 'Database connection failed'}), 500

@app.route('/members/<int:id>', methods=['PUT'])
def update_member(id):
    data = request.json
    name = data.get('name')
    age = data.get('age')

    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("UPDATE Members SET name = %s, age = %s WHERE id = %s", (name, age, id))
            connection.commit()
            if cursor.rowcount > 0:
                return jsonify({'message': 'Member updated successfully!'}), 200
            else:
                return jsonify({'message': 'Member not found'}), 404
        except Error as e:
            return jsonify({'error': str(e)}), 400
        finally:
            cursor.close()
            connection.close()
    return jsonify({'error': 'Database connection failed'}), 500

@app.route('/members/<int:id>', methods=['DELETE'])
def delete_member(id):
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("DELETE FROM Members WHERE id = %s", (id,))
            connection.commit()
            if cursor.rowcount > 0:
                return jsonify({'message': 'Member deleted successfully!'}), 200
            else:
                return jsonify({'message': 'Member not found'}), 404
        except Error as e:
            return jsonify({'error': str(e)}), 400
        finally:
            cursor.close()
            connection.close()
    return jsonify({'error': 'Database connection failed'}), 500

if __name__ == '__main__':
    app.run(debug=True)
