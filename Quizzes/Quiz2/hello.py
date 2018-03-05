from flask import Flask
from flask import request
from flask import jsonify

app = Flask(__name__)

list_of_dict = []


@app.route("/")
def hello():
    return "Hello World!"


@app.route('/users', methods=['POST'])  # curl -i -X POST http://127.0.0.1:5000/users -d "name=foo"
def add_users():
    """ Add a user and returns the list"""
    if request.method == 'POST':
        global list_of_dict
        dict_user = {}
        if not list_of_dict:
            dict_user["id"] = 1
            dict_user["name"] = request.form["name"]
            list_of_dict.append(dict_user)
        else:
            dict_user["id"] = list_of_dict[len(list_of_dict) - 1]["id"] + 1
            dict_user["name"] = request.form["name"]
            list_of_dict.append(dict_user)
        return jsonify(201,*list_of_dict)


@app.route('/users/<id>', methods=['GET', 'DELETE'])  # curl -i -X GET http://127.0.0.1:5000/users/1
def get_user_id(id):
    """Get or delete particular id"""
    global list_of_dict
    if request.method == 'GET':
        if list_of_dict:
            for item in list_of_dict:
                if item["id"] == int(id):
                    return jsonify(200,item)
            else:
                return "ID not matched\n"
        else:
            return "404 not found \n"
    if request.method == 'DELETE':  # curl -i -X DELETE  http://127.0.0.1:5000/users/1
        if list_of_dict:
            for index, item in enumerate(list_of_dict):
                print(item["id"])
                if item["id"] == int(id):
                    list_of_dict.pop(index)
                    return jsonify(204,*list_of_dict)
            else:
                return "item not found"



@app.route('/users', methods=['GET'])
def get_users():
    """ Get all users """
    if list_of_dict:
        return jsonify(*list_of_dict)
    else:
        return "404 not found"
