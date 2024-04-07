########################################################
# Sample customers blueprint of endpoints
# Remove this file if you are not using it in your project
########################################################
from flask import Blueprint, request, jsonify, make_response, current_app
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
@customers.route('/customer/<userID>', methods=['GET'])
def get_customer(userID):
    #query = 'select * from customers where id = ' + str(userID)
    #cursor.execute(query)
    #row_headers = [x[0] for x in cursor.description]
    #json_data = []
    #theData = cursor.fetchall()
    #for row in theData:
    #    json_data.append(dict(zip(row_headers, row)))
    #the_response = make_response(jsonify(json_data))
    #the_response.status_code = 200
    #the_response.mimetype = 'application/json'
    #return the_response
    query = 'SELECT id, first_name, job_title FROM customers WHERE id = ' + str(userID)
    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    column_headers = [x[0] for x in cursor.description]
    json_data = []
    the_data = cursor.fetchall()
    for row in the_data:
        json_data.append(dict(zip(column_headers, row)))
    return jsonify(json_data)


# Update customer information given their ID number
@customers.route('/customer/<userID>', methods=['PUT'])
def update_customer_information(userID):
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    # extracting the variables
    company = the_data['company']
    lastname = the_data['last_name']
    firstname = the_data['first_name']
    jobtitle = the_data['job_title']
    businessPhone = the_data['business_phone']

    # Constructing the query
    query = 'UPDATE customers SET company = "'
    query += company + '", last_name = "'
    query += lastname + '", first_name = "'
    query += firstname + '", job_title = "'
    query += jobtitle + '", business_phone = "'
    query += businessPhone + '" WHERE id = '
    query += str(userID)
    current_app.logger.info(query)

    # executing and committing the update statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'
