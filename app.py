from flask import Flask,request,render_template,redirect,url_for
from werkzeug.utils import secure_filename
# from ./library/Network_config import  Net_config
import subprocess
import json

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html');

@app.route('/ipSettingMain')
def ipSetting():
    return render_template('ipSettingMain.html');

@app.route('/ipSettingSecond')
def ipSettingSecond():
    return render_template('ipSettingSecond.html');

@app.route("/iniUpdate")
def iniUpdate():
    data = [{'num':1,'name':'apple','format':'jpg','size':123456,'time':'20180730'},{'num':2,'name':'apple','format':'png','size':123456,'time':'20180731'}];
    return render_template('iniUpdate.html',fileList = data);

@app.route("/upload",methods=['POST'])
def upload():
    f = request.files['file']
    f.save('/home/titan/Titan/github/imac-iot/flask_dds/fileUpload/file/'+ secure_filename(f.filename))
    return redirect(url_for('iniUpdate'));

@app.route('/iniSelect')
def iniSelect():
    return render_template('iniSelect.html');

@app.route('/iniBuild')
def iniBuild():
    return render_template('iniBuild.html');

@app.route('/ping')
def ping():
    return render_template('ping.html');

@app.route('/ping',methods=['POST'])
def pings():
    ip = request.form.get('ip')
    try:
        response = subprocess.check_output(
            ['ping', '-c', '1', ip],
            stderr=subprocess.STDOUT,  # get all output
            universal_newlines=True  # return string not bytes
            )
    except :
        response = "From "+ ip +" Destination Host Unreachable"
    return response

@app.route('/logs')
def logs():
    return render_template('logs.html');

@app.route('/sentTest')
def sentTest():
    return render_template('sentTest.html');

if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host='0.0.0.0', port=5000, debug=True)
