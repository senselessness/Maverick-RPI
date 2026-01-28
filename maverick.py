from flask import Flask, render_template, request, jsonify
import controls as C
import sys
import os
import time
import signal

app = Flask(__name__)

Shutdown = C.Button(26)
assigned_port=C.assigned_port

#Opens html script on local host.
@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == "POST":
        if request.form["Shutdown"] == "true":
            Shutdown_Prep()
    return render_template('select.html')

@app.route('/acvmix', methods=['GET', 'POST'])
def acvmix():
          
        
    if request.method == "POST":
        
        if request.form["Form"]=="process":
            if request.form["Process"] == "Start":
                C.Start_button(C.ACVDistribution)
                return render_template('mix.html', system=C.ACVDistribution)
            elif request.form["Process"]== "Stop":
                C.Stop_button(C.ACVDistribution)
                return render_template('mix.html', system=C.ACVDistribution)
                
        elif request.form["Form"]=="settings":
            C.ACVDistribution.Target = int(request.form["targetsetting"])
            C.writeControls()
            
    return render_template('mix.html', system=C.ACVDistribution)

@app.route('/acvdata')
def acvdata():
    return jsonify({"count": C.ACVDistribution.Counter, "total":C.ACVDistribution.Total_Product, "started":C.ACVDistribution.StartProcess})
    
#Shutdown Procedure Handles Physical Request and Website Request
def Shutdown_Prep():
        C.writeControls()
        try:
            print("Ready For Power Off")
            own_pid=os.getpid()
            os.kill(own_pid, signal.SIGINT)
            C.peripherialsoff()
            sys.exit("Exiting by button\nReady For Power Off")
            #os.system("sudo shutdown -h now")
            
        except:
           print("Unexpected Fail")

Shutdown.when_pressed = Shutdown_Prep

 
#Disable Debug When Deployed
if __name__=='__main__':
    app.run(debug=False, host='0.0.0.0', port=assigned_port)