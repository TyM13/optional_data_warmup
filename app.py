from unittest import result
from apihelper import check_endpoint_info
import dbhelper
from flask import Flask, request, make_response
import json
import dbcreds

app = Flask(__name__)




@app.patch('/api/client')
def client_patch():
    invalid = check_endpoint_info(request.json, [request.headers['token'],'email','password','bio','image_url'])
    if(invalid != None):
        return make_response(json.dumps(invalid, default=str), 400)

    results = dbhelper.run_statment('CALL(?,?,?,?,?)', [request.json.get(''), request.json.get(''), request.json.get(''), 
    request.json.get(''), request.json.get(''),])
    if(type(results) == list):
        return make_response(json.dumps(results, default=str), 200)
    else:
        return make_response(json.dumps(results, default=str), 500)






if(dbcreds.production_mode == True):
    print("Running in Production Mode")
    import bjoern # type: ignore
    bjoern.run(app, "0.0.0.0", 5006)
else:
    from flask_cors import CORS
    CORS(app)
    print("Running in Testing Mode!")
    app.run(debug=True)