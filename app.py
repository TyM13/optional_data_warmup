from unittest import result
from apihelper import check_endpoint_info, fill_optional_data
import dbhelper
from flask import Flask, request, make_response
import json
import dbcreds

app = Flask(__name__)




@app.patch('/api/client')
def client_patch():
    invalid = check_endpoint_info(request.headers, ['token'])
    if(invalid != None):
        return make_response(json.dumps(invalid, default=str), 400)

    results = dbhelper.run_statment('CALL get_info(?)', [request.headers.get('token')])
    if(type(results) != list and len(results) != 1):
        return make_response(json.dumps(results), 400)

    results = fill_optional_data(request.json, results[0] ['email','password','image_url','bio'])
    results = dbhelper.run_statment('CALL patch_client(?,?,?,?,?)',
    [request.headers['token'], results['email'], results['password'], results['bio'], results['image_url'] ])
    if(type(results) == list):
        return make_response(json.dumps('success'), 200)
    else:
        return make_response(json.dumps(results), 500)






if(dbcreds.production_mode == True):
    print("Running in Production Mode")
    import bjoern # type: ignore
    bjoern.run(app, "0.0.0.0", 5006)
else:
    from flask_cors import CORS
    CORS(app)
    print("Running in Testing Mode!")
    app.run(debug=True)