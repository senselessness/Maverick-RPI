from flask import Flask, render_template, request, jsonify
import controls as C
import sys
import os
import webbrowser
import signal
from threading import Timer

app = Flask(__name__)

Shutdown = 26

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
        C.GPIO.cleanup()
        try:
            own_pid=os.getpid()
            os.kill(own_pid, signal.SIGINT)
            #func=request.environ.get('werkzeug.server.shutdown')
            #func()
            print("Exiting by Website\nReady For Power Off")
            #os.system("sudo shutdown -h now")
            
        except:
            sys.exit("Exiting by button\nReady For Power Off")
            #os.system("sudo shutdown -h now")

#Automatically Opens Browser
def open_browser():
    webbrowser.open_new("http://0.0.0.0:5000")


C.GPIO.setup(Shutdown, C.GPIO.IN, pull_up_down=C.GPIO.PUD_DOWN)
C.GPIO.add_event_detect(Shutdown,C.GPIO.FALLING, callback=lambda x: Shutdown_Prep(), bouncetime=300)

Timer(1,open_browser).start()
 
#Disable Debug When Deployed
#if __name__=='__main__':   
    #app.run(debug=True, host='0.0.0.0', port=5000)