########################################################
# Sample customers blueprint of endpoints
# Remove this file if you are not using it in your project
########################################################
from flask import Blueprint, request, jsonify, make_response
import json
from src import db


customers = Blueprint('customers', __name__)

# Get all customers from the DB
@customers.route('/customers', methods=['GET'])
def get_customers():
    cursor = db.get_db().cursor()
    cursor.execute('select id, company, last_name,\
        first_name, job_title, business_phone from customers')
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Get customer detail for customer with particular userID
@customers.route('/customers/<userID>', methods=['GET'])
def get_customer(userID):
    cursor = db.get_db().cursor()
    cursor.execute('select * from customers where id = {0}'.format(userID))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

#update customer information given their ID number
@customers.route('/customers/<userId>', methods=['PUT'])
def update_customer_information(userId):
    if userId not in customers:
        return jsonify({'error': 'customer not found'}), 404
    
    data = request.json
    customers[userId].update(data)

    #customers[userId]['company'] = data.get('company', customers[userId]['company'])
    #customers[userId]['last_name'] = data.get('last_name', customers[userId]['last_name'])
    #customers[userId]['first_name'] = data.get('first_name', customers[userId]['first_name'])
    #customers[userId]['job_title'] = data.get('job_title', customers[userId]['job_title'])
    #customers[userId]['business_phone'] = data.get('business_phone', customers[userId]['business_phone'])
    
    return jsonify(customers[userId])