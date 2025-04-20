#verify crontab
from flask import Flask,jsonify,render_template,request
import json

with open("morse-code.json") as file:
    c2mDict=json.load(file)

m2cDict={value:key for key,value in c2mDict.items()}


app=Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/c2m",methods=["GET"])
def c2m():
    return jsonify(c2mDict)

@app.route("/api/c2m/alpha",methods=["GET"])
def c2mAlpha():
    alpha={}
    for key in c2mDict.keys():
        if key.isalpha():
            alpha[key]=c2mDict[key]
    return jsonify(alpha)

@app.route("/api/c2m/numeric",methods=["GET"])
def c2mNumeric():
    numeric={}
    for key in c2mDict.keys():
        if key.isnumeric():
            numeric[key]=c2mDict[key]
    return jsonify(numeric)

@app.route("/api/c2m/symbol",methods=["GET"])
def c2mSymbol():
    symbol={}
    for key in c2mDict.keys():
        if not(key.isnumeric() or key.isalpha()):
            symbol[key]=c2mDict[key]
    return jsonify(symbol)

#curl "http://127.0.0.1:5000/api/c2m/char?key="a"
@app.route("/api/c2m/char",methods=["GET"])
def c2mChar():
    char=request.args.get('key')
    if not char:
        return jsonify({"error": "'key' parameter is required"}), 400
    if not char in c2mDict.keys():
        return jsonify({"error": "'key' parameter is invalid: value not found in database"}), 400
    return jsonify(c2mDict[char])




@app.route("/api/m2c",methods=["GET"])
def m2c():
    return jsonify(m2cDict)

@app.route("/api/m2c/alpha",methods=["GET"])
def m2cAlpha():
    alpha={}
    for key in c2mDict.keys():
        if key.isalpha():
            alpha[c2mDict[key]]=key
    return jsonify(alpha)

@app.route("/api/m2c/numeric",methods=["GET"])
def m2cNumeric():
    numeric={}
    for key in c2mDict.keys():
        if key.isnumeric():
            numeric[c2mDict[key]]=key
    return jsonify(numeric)

@app.route("/api/m2c/symbol",methods=["GET"])
def m2cSymbol():
    symbol={}
    for key in c2mDict.keys():
        if not(key.isnumeric() or key.isalpha()):
            symbol[c2mDict[key]]=key
    return jsonify(symbol)

@app.route("/api/m2c/char",methods=["GET"])
def m2cChar():
    char=request.args.get('key')
    if not char:
        return jsonify({"error": "'key' parameter is required"}), 400
    if not char in m2cDict.keys():
        return jsonify({"error": "'key' parameter is invalid: value not found in database"}), 400
    return jsonify(m2cDict[char])

@app.route("/api/c2m",methods=["POST"])
def c2mPost():
    global c2mDict, m2cDict
    errorformating=jsonify({"error":"bad formating, good format example: {char0: morse_code0, char1: morse_cose1, ...}"}),400
    new=request.json
    # encountering errors
    if type(new)!=dict:
        return errorformating
    for key,value in new.items():
        if not (type(key)==str and type(value)==str):
            return errorformating
        if len(key)!=1:
            return errorformating
        if key in c2mDict.keys() or value in c2mDict.values():
            return jsonify({"error": "data conflicting with what is already existing in database"}),400
    # actually adding to database
    c2mDict.update(new)
    m2cDict={value:key for key,value in c2mDict.items()}
    with open("morse-code.json",'w') as file:
        json.dump(c2mDict,file)
    return jsonify({"success": f"""the following data is successfully added to the database: {new}, thank you for helping us"""}),202

#curl -X POST -H "Content-Type: application/json" -d '{"-.-.-.":"*"}' http://127.0.0.1:5000/api/m2c
@app.route("/api/m2c",methods=["POST"])
def m2cPost():
    global c2mDict, m2cDict
    errorformating=jsonify({"error":"bad formating, good format example: {morse_code0: char0, morse_cose1: char1, ...}"}),400
    new=request.json
    # encountering errors
    if type(new)!=dict:
        return errorformating
    for key,value in new.items():
        if not (type(key)==str and type(value)==str):
            return errorformating
        if len(value)!=1:
            return errorformating
        if key in m2cDict.keys() or value in m2cDict.values():
            return jsonify({"error": "data conflicting with what is already existing in database"}),400
    # actually adding to database
    m2cDict.update(new)
    c2mDict={value:key for key,value in m2cDict.items()}
    with open("morse-code.json",'w') as file:
        json.dump(c2mDict,file)
    return jsonify({"success": f"""the following data is successfully added to the database: {new}, thank you for helping us"""}),202

if __name__=="__main__": app.run()
