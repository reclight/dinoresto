#web-browser based interface for controlling the MIR robot
#version 1.0
#date: 2018-04-10
#Maintainer: Dr.Liang Conghui
#Copyright: ARTC, A*STAR, 2018-2013

import requests
import time
from flask import Flask, request, render_template
import subprocess , time, os
import requests
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)
app = Flask(__name__)
CORS(app)

x  = 123

@app.route('/')
def static_page0():
    return render_template('index.html')      #Host the web-browser based user interface (Warehouse and Assembly Line)


@app.route('/warehouse')
def static_page1():
    return render_template('agv_warehouse.html')      #Host the web-browser based user interface (Warehouse and Assembly Line)


@app.route('/warehouse_micr')
def static_page4():
    return render_template('agv_warehouse_micr.html')


@app.route('/station1')
def static_page2():
    return render_template('agv_station.html')      #Host the web-browser based user interface (Warehouse and Assembly Line)


@app.route('/ntx1000')
def static_page3():
    return render_template('agv_NTX1000.html')      #Host the web-browser based user interface (Warehouse and Assembly Line)




@app.route("/script", methods=['POST'])





def script():

    input_string = request.form['value']
    if (input_string == 'Dispatch_parts_NTX1000') :   #Dispatch Parts to NTX1000

        headers = {'Content-type': 'application/json' 'accept': 'application/json' 'Accept-Language': 'en_US' 'Authorization': 'Basic YWRtaW46OGM2OTc2ZTViNTQxMDQxNWJkZTkwOGJkNGRlZTE1ZGZiMTY3YTljODczZmM0YmI4YTgxZjZmMmFiNDQ4YTkxOA=='}
        r = requests.post('http://mir.com/api/v2.0.0/missions', json ={"mission":"5461f0d2-0567-11e8-b987-f44d306f3f85"}, headers=headers)  #1.start position
        print(r.text)
        return "Call for parts mission has been accomplished!"


    input_string = request.form['value']
    if (input_string == 'Bring_Empty_Trolley_NTX1000') :   #Bring back Empty Trolley from NTX1000 to warehouse

    	headers = {'Content-type': 'application/json'}
        r = requests.post('http://mir.com:8080/v1.0.0/mission_queue', json ={"mission":"97b0f8eb-4855-11e8-a4e3-f44d306f3f85"}, headers=headers)  #1.start position
        print(r.text)

    	headers = {'Content-type': 'application/json'}
        r = requests.post('http://mir.com:8080/v1.0.0/mission_queue', json ={"mission": "5a44e279-3d3c-11e8-99fb-f44d306f3f85"}, headers=headers)  #2.go to NTX1000 waiting position
        print(r.text)


    	headers = {'Content-type': 'application/json'}
        r = requests.post('http://mir.com:8080/v1.0.0/mission_queue', json ={"mission": "9c4b4293-3d3c-11e8-99fb-f44d306f3f85"}, headers=headers)  #2.Pick up trolley from the NTX1000 machine
        print(r.text)

    	headers = {'Content-type': 'application/json'}
        r = requests.post('http://mir.com:8080/v1.0.0/mission_queue', json ={"mission": "5461f0d2-0567-11e8-b987-f44d306f3f85"}, headers=headers)   #6.make a sound
        print(r.text)


        headers = {'Content-type': 'application/json'}
        r = requests.post('http://mir.com:8080/v1.0.0/mission_queue', json ={"mission": "1cd195ef-1d35-11e8-ba33-f44d306f3f85"}, headers=headers)   #5.go to wait position near warehouse
        print(r.text)
        time.sleep(5)

    	headers = {'Content-type': 'application/json'}
        r = requests.post('http://mir.com:8080/v1.0.0/mission_queue', json ={"mission": "22cb488a-6dea-11e8-9f16-f44d306f3f85"}, headers=headers)   #10.release trolley
        print(r.text)


    	headers = {'Content-type': 'application/json'}
        r = requests.post('http://mir.com:8080/v1.0.0/mission_queue', json ={"mission": "5461f0d2-0567-11e8-b987-f44d306f3f85"}, headers=headers)   #6.make a sound
        print(r.text)


    	headers = {'Content-type': 'application/json'}
        r = requests.post('http://mir.com:8080/v1.0.0/mission_queue', json ={"mission":"97b0f8eb-4855-11e8-a4e3-f44d306f3f85"}, headers=headers)  #11.go back to start position
        print(r.text)
        return "Bring back empty trolley from NTX1000 to warehouse mission has been accomplished!"


    input_string = request.form['value']
    if (input_string == 'Dispatch_Parts_Line') :   #Dispatch Parts to Assembly Line

    	headers = {'Content-type': 'application/json'}
        r = requests.post('http://mir.com:8080/v1.0.0/mission_queue', json ={"mission":"97b0f8eb-4855-11e8-a4e3-f44d306f3f85"}, headers=headers)  #1.start position
        print(r.text)

    	headers = {'Content-type': 'application/json'}
        r = requests.post('http://mir.com:8080/v1.0.0/mission_queue', json ={"mission": "fd2fc112-485a-11e8-9812-f44d306f3f85"}, headers=headers)  #2.wait position #2 near warehouse
        print(r.text)

    	headers = {'Content-type': 'application/json'}
        r = requests.post('http://mir.com:8080/v1.0.0/mission_queue', json ={"mission": "eded94e0-6de8-11e8-9f16-f44d306f3f85"}, headers=headers)   #3.pick up trolley
        print(r.text)

    	headers = {'Content-type': 'application/json'}
        r = requests.post('http://mir.com:8080/v1.0.0/mission_queue', json ={"mission": "5461f0d2-0567-11e8-b987-f44d306f3f85"}, headers=headers)   #4.make a sound
        print(r.text)

    	headers = {'Content-type': 'application/json'}
        r = requests.post('http://mir.com:8080/v1.0.0/mission_queue', json ={"mission": "7f107423-e3a3-11e7-896e-f44d306f3f85"}, headers=headers)   #5.go to station 1
        print(r.text)
        time.sleep(5)

    	headers = {'Content-type': 'application/json'}
        r = requests.post('http://mir.com:8080/v1.0.0/mission_queue', json ={"mission": "5461f0d2-0567-11e8-b987-f44d306f3f85"}, headers=headers)   #6.make a sound
        print(r.text)

    	headers = {'Content-type': 'application/json'}
        r = requests.post('http://mir.com:8080/v1.0.0/mission_queue', json ={"mission": "8ead8319-21e6-11e8-bbd3-f44d306f3f85"}, headers=headers)   #5.wait for 5 seconds
        print(r.text)
        time.sleep(5)

    	headers = {'Content-type': 'application/json'}
        r = requests.post('http://mir.com:8080/v1.0.0/mission_queue', json ={"mission": "22cb488a-6dea-11e8-9f16-f44d306f3f85"}, headers=headers)   #10.release trolley
        print(r.text)

    	headers = {'Content-type': 'application/json'}
        r = requests.post('http://mir.com:8080/v1.0.0/mission_queue', json ={"mission":"97b0f8eb-4855-11e8-a4e3-f44d306f3f85"}, headers=headers)  #11.go back to start position
        print(r.text)
        return "Dispacth parts to the assembly line mission has been accomplished!"

    input_string = request.form['value']
    if (input_string == 'Dispatch_Parts_Line_Error') :   #Dispatch Parts to Assembly Line for MICR Error demo
	
	headers = {'Content-type': 'application/json'}
	r = requests.post('http://mir.com:8080/v1.0.0/mission_queue', json ={"mission":"97b0f8eb-4855-11e8-a4e3-f44d306f3f85"}, headers=headers)  #1.start position
	print(r.text)
	
	headers = {'Content-type': 'application/json'}	
	r = requests.post('http://mir.com:8080/v1.0.0/mission_queue', json ={"mission": "fd2fc112-485a-11e8-9812-f44d306f3f85"}, headers=headers)  #2.wait position #2 near warehouse
	print(r.text)
	
	headers = {'Content-type': 'application/json'}
	r = requests.post('http://mir.com:8080/v1.0.0/mission_queue', json ={"mission": "590f1604-5504-11e8-8d66-f44d306f3f85"}, headers=headers)  #2.Error_demo
	print(r.text)
	
	headers = {'Content-type': 'application/json'}
	r = requests.post('http://mir.com:8080/v1.0.0/mission_queue', json ={"mission": "eded94e0-6de8-11e8-9f16-f44d306f3f85"}, headers=headers)   #3.pick up trolley
	print(r.text)
	
	headers = {'Content-type': 'application/json'}
	r = requests.post('http://mir.com:8080/v1.0.0/mission_queue', json ={"mission": "5461f0d2-0567-11e8-b987-f44d306f3f85"}, headers=headers)   #4.make a sound
	print(r.text)
	
	headers = {'Content-type': 'application/json'}
	r = requests.post('http://mir.com:8080/v1.0.0/mission_queue', json ={"mission": "7f107423-e3a3-11e7-896e-f44d306f3f85"}, headers=headers)   #5.go to station 1
	print(r.text)
	time.sleep(5)
	
	headers = {'Content-type': 'application/json'}
	r = requests.post('http://mir.com:8080/v1.0.0/mission_queue', json ={"mission": "5461f0d2-0567-11e8-b987-f44d306f3f85"}, headers=headers)   #6.make a sound
	print(r.text)
	
	headers = {'Content-type': 'application/json'}
	r = requests.post('http://mir.com:8080/v1.0.0/mission_queue', json ={"mission": "8ead8319-21e6-11e8-bbd3-f44d306f3f85"}, headers=headers)   #5.wait for 5 seconds
	print(r.text)
	time.sleep(5)
	
	headers = {'Content-type': 'application/json'}
	r = requests.post('http://mir.com:8080/v1.0.0/mission_queue', json ={"mission": "22cb488a-6dea-11e8-9f16-f44d306f3f85"}, headers=headers)   #10.release trolley
	print(r.text)
	
    	headers = {'Content-type': 'application/json'}
    	r = requests.post('http://mir.com:8080/v1.0.0/mission_queue', json ={"mission":"97b0f8eb-4855-11e8-a4e3-f44d306f3f85"}, headers=headers)  #11.go back to start position
    	print(r.text)
	return "Dispacth parts to the assembly line mission has been accomplished!"


    input_string = request.form['value']
    if (input_string == 'Bring_Empty_Trolley_Line') :   #Bring Empty Trolley from Assembly Line

    	headers = {'Content-type': 'application/json'}
        r = requests.post('http://mir.com:8080/v1.0.0/mission_queue', json ={"mission":"97b0f8eb-4855-11e8-a4e3-f44d306f3f85"}, headers=headers)  #1.start position
        print(r.text)

    	headers = {'Content-type': 'application/json'}
        r = requests.post('http://mir.com:8080/v1.0.0/mission_queue', json ={"mission": "798ad3c2-3d33-11e8-99fb-f44d306f3f85"}, headers=headers)  #2. go to wait position 2 near station one
        print(r.text)

    	headers = {'Content-type': 'application/json'}
        r = requests.post('http://mir.com:8080/v1.0.0/mission_queue', json ={"mission": "3561d489-3d35-11e8-99fb-f44d306f3f85"}, headers=headers)   #3.pick up trolley from station one
        print(r.text)

    	headers = {'Content-type': 'application/json'}
        r = requests.post('http://mir.com:8080/v1.0.0/mission_queue', json ={"mission": "5461f0d2-0567-11e8-b987-f44d306f3f85"}, headers=headers)   #4.make a sound
        print(r.text)

    	headers = {'Content-type': 'application/json'}
        r = requests.post('http://mir.com:8080/v1.0.0/mission_queue', json ={"mission": "fd2fc112-485a-11e8-9812-f44d306f3f85"}, headers=headers)   #5.go to wait position 2 near warehouse
        print(r.text)
        time.sleep(5)

    	headers = {'Content-type': 'application/json'}
        r = requests.post('http://mir.com:8080/v1.0.0/mission_queue', json ={"mission": "22cb488a-6dea-11e8-9f16-f44d306f3f85"}, headers=headers)   #10.release trolley
        print(r.text)


    	headers = {'Content-type': 'application/json'}
        r = requests.post('http://mir.com:8080/v1.0.0/mission_queue', json ={"mission": "5461f0d2-0567-11e8-b987-f44d306f3f85"}, headers=headers)   #6.make a sound
        print(r.text)


    	headers = {'Content-type': 'application/json'}
        r = requests.post('http://mir.com:8080/v1.0.0/mission_queue', json ={"mission":"97b0f8eb-4855-11e8-a4e3-f44d306f3f85"}, headers=headers)  #11.go back to start position
        print(r.text)
        return "Bring back empty trolley from assembly line to warehouse mission has been accomplished!"


    input_string = request.form['value']
    if (input_string == 'Charge_AGV') :   #AGV go to Charging station

    	headers = {'Content-type': 'application/json'}
        r = requests.post('http://mir.com:8080/v1.0.0/mission_queue', json ={"mission":"97b0f8eb-4855-11e8-a4e3-f44d306f3f85"}, headers=headers)  #1.start position
        print(r.text)

    	headers = {'Content-type': 'application/json'}
        r = requests.post('http://mir.com:8080/v1.0.0/mission_queue', json ={"mission":"bdf70234-3d3e-11e8-99fb-f44d306f3f85"}, headers=headers)  #1.go to charging station
        print(r.text)

    	headers = {'Content-type': 'application/json'}
        r = requests.post('http://mir.com:8080/v1.0.0/mission_queue', json ={"mission":"7ffe916c-3d40-11e8-99fb-f44d306f3f85"}, headers=headers)  #1.docking to charging station
        print(r.text)


    	headers = {'Content-type': 'application/json'}
        r = requests.post('http://mir.com:8080/v1.0.0/mission_queue', json ={"mission":"950b1425-2724-11e8-9f01-f44d306f3f85"}, headers=headers)  #1.charginig the robot
        print(r.text)


    input_string = request.form['value']
    if (input_string == 'Pause_AGV') :   #Pause the AGV
    	headers = {'Content-type': 'application/json'}
        #r = requests.put('http://mir.com:8080/v1.0.0/state', json ={'state':3}, headers=headers)
        #r = requests.get('http://mir.com:8080/v1.0.0/state', json ={'state':1}, headers=headers)
        #r = requests.get('http://mir.com:8080/v1.0.0/missions/{9c4b4293-3d3c-11e8-99fb-f44d306f3f85}')
        #r = requests.post('http://mir.com:8080/v1.0.0/actions', json ={"action_type_id": 300, "mission_id" : "a4c19cdc-1d34-11e8-ba33-f44d306f3f85"}, headers=headers)  #1.charginig the robot
        r = requests.get('http://mir.com:8080/v1.0.0/status', json ={"whitelist" : "string"}, headers=headers )
        print(r.text)
        return "Operation status of the MIR robot are obbtained!"

    input_string = request.form['value']
    if (input_string == 'Initialize_AGV') :   #STOP the AGV and clear up all missions in the MIR robot
    	headers = {'Content-type': 'application/json'}
	r = requests.delete('http://mir.com:8080/v1.0.0/mission_queue')
	print(r.text)
        r = requests.post('http://mir.com:8080/v1.0.0/mission_queue', json ={"mission":"97b0f8eb-4855-11e8-a4e3-f44d306f3f85"}, headers=headers)  #1.start position
        print(r.text)

    input_string = request.form['value']
    if (input_string == 'Stop_AGV') :   #STOP the AGV and clear up all missions in the MIR robot
	headers = {'Content-type': 'application/json'}
        r = requests.delete('http://mir.com:8080/v1.0.0/mission_queue')
        print(r.text)
        return "STOPPING the robot and all missions are being cleared up!"

    input_string = request.form['value']
    if (input_string == 'CallforParts') :       #Call for Parts from the warehouse

    	headers = {'Content-type': 'application/json'}
        r = requests.post('http://mir.com:8080/v1.0.0/mission_queue', json ={"mission":"97b0f8eb-4855-11e8-a4e3-f44d306f3f85"}, headers=headers)  #1.start position
        print(r.text)

    	headers = {'Content-type': 'application/json'}
        r = requests.post('http://mir.com:8080/v1.0.0/mission_queue', json ={"mission": "1cd195ef-1d35-11e8-ba33-f44d306f3f85"}, headers=headers)  #2.go to the wait position near warehouse
        print(r.text)

    	headers = {'Content-type': 'application/json'}
        r = requests.post('http://mir.com:8080/v1.0.0/mission_queue', json ={"mission": "eded94e0-6de8-11e8-9f16-f44d306f3f85"}, headers=headers)   #3.pick up trolley
        print(r.text)

    	headers = {'Content-type': 'application/json'}
        r = requests.post('http://mir.com:8080/v1.0.0/mission_queue', json ={"mission": "5461f0d2-0567-11e8-b987-f44d306f3f85"}, headers=headers)   #4.make a sound
        print(r.text)

    	headers = {'Content-type': 'application/json'}
        r = requests.post('http://mir.com:8080/v1.0.0/mission_queue', json ={"mission": "e2f78da8-3d3b-11e8-99fb-f44d306f3f85"}, headers=headers)   #4.go to NTX1000 drop off position
        print(r.text)


    	headers = {'Content-type': 'application/json'}
        r = requests.post('http://mir.com:8080/v1.0.0/mission_queue', json ={"mission": "22cb488a-6dea-11e8-9f16-f44d306f3f85"}, headers=headers)   #10.release trolley
        print(r.text)


    	headers = {'Content-type': 'application/json'}
        r = requests.post('http://mir.com:8080/v1.0.0/mission_queue', json ={"mission": "5461f0d2-0567-11e8-b987-f44d306f3f85"}, headers=headers)   #6.make a sound
        print(r.text)


    	headers = {'Content-type': 'application/json'}
        r = requests.post('http://mir.com:8080/v1.0.0/mission_queue', json ={"mission":"97b0f8eb-4855-11e8-a4e3-f44d306f3f85"}, headers=headers)  #11.go back to start position
        print(r.text)
        return "Call for parts mission has been accomplished!"


    input_string = request.form['value']
    if (input_string == 'DispatchParts') :   #Ready for Dispatch from NTX1000 to warehouse

    	headers = {'Content-type': 'application/json'}
        r = requests.post('http://mir.com:8080/v1.0.0/mission_queue', json ={"mission":"97b0f8eb-4855-11e8-a4e3-f44d306f3f85"}, headers=headers)  #1.start position
        print(r.text)

    	headers = {'Content-type': 'application/json'}
        r = requests.post('http://mir.com:8080/v1.0.0/mission_queue', json ={"mission": "5a44e279-3d3c-11e8-99fb-f44d306f3f85"}, headers=headers)  #2.go to NTX1000 waiting position
        print(r.text)


    	headers = {'Content-type': 'application/json'}
        r = requests.post('http://mir.com:8080/v1.0.0/mission_queue', json ={"mission": "9c4b4293-3d3c-11e8-99fb-f44d306f3f85"}, headers=headers)  #2.Pick up trolley from the NTX1000 machine
        print(r.text)

    	headers = {'Content-type': 'application/json'}
        r = requests.post('http://mir.com:8080/v1.0.0/mission_queue', json ={"mission": "5461f0d2-0567-11e8-b987-f44d306f3f85"}, headers=headers)   #6.make a sound
        print(r.text)

        headers = {'Content-type': 'application/json'}
        r = requests.post('http://mir.com:8080/v1.0.0/mission_queue', json ={"mission": "1cd195ef-1d35-11e8-ba33-f44d306f3f85"}, headers=headers)   #5.go to wait position near warehouse
        print(r.text)
        time.sleep(5)

    	headers = {'Content-type': 'application/json'}
        r = requests.post('http://mir.com:8080/v1.0.0/mission_queue', json ={"mission": "22cb488a-6dea-11e8-9f16-f44d306f3f85"}, headers=headers)   #10.release trolley
        print(r.text)


    	headers = {'Content-type': 'application/json'}
        r = requests.post('http://mir.com:8080/v1.0.0/mission_queue', json ={"mission": "5461f0d2-0567-11e8-b987-f44d306f3f85"}, headers=headers)   #6.make a sound
        print(r.text)


    	headers = {'Content-type': 'application/json'}
        r = requests.post('http://mir.com:8080/v1.0.0/mission_queue', json ={"mission":"97b0f8eb-4855-11e8-a4e3-f44d306f3f85"}, headers=headers)  #11.go back to start position
        print(r.text)
        return "Bring back empty trolley from NTX1000 to warehouse mission has been accomplished!"

    input_string = request.form['value']
    if (input_string == 'CallforPartsStation') :       #Call for Parts from the warehouse

    	headers = {'Content-type': 'application/json'}
        r = requests.post('http://mir.com:8080/v1.0.0/mission_queue', json ={"mission":"97b0f8eb-4855-11e8-a4e3-f44d306f3f85"}, headers=headers)   #1.start position
        print(r.text)

    	headers = {'Content-type': 'application/json'}
        r = requests.post('http://mir.com:8080/v1.0.0/mission_queue', json ={"mission": "fd2fc112-485a-11e8-9812-f44d306f3f85"}, headers=headers)  #2.go to wait position 2  near warehouse
        print(r.text)

    	headers = {'Content-type': 'application/json'}
        r = requests.post('http://mir.com:8080/v1.0.0/mission_queue', json ={"mission": "eded94e0-6de8-11e8-9f16-f44d306f3f85"}, headers=headers)   #3.pick up trolley
        print(r.text)

    	headers = {'Content-type': 'application/json'}
        r = requests.post('http://mir.com:8080/v1.0.0/mission_queue', json ={"mission": "5461f0d2-0567-11e8-b987-f44d306f3f85"}, headers=headers)   #4.make a sound
        print(r.text)

    	headers = {'Content-type': 'application/json'}
        r = requests.post('http://mir.com:8080/v1.0.0/mission_queue', json ={"mission": "7f107423-e3a3-11e7-896e-f44d306f3f85"}, headers=headers)   #5.go to station one near assembly line
        print(r.text)
        time.sleep(5)

    	headers = {'Content-type': 'application/json'}
        r = requests.post('http://mir.com:8080/v1.0.0/mission_queue', json ={"mission": "5461f0d2-0567-11e8-b987-f44d306f3f85"}, headers=headers)   #6.make a sound
        print(r.text)

    	headers = {'Content-type': 'application/json'}
        r = requests.post('http://mir.com:8080/v1.0.0/mission_queue', json ={"mission": "8ead8319-21e6-11e8-bbd3-f44d306f3f85"}, headers=headers)   #5.wait for 5 seconds
        print(r.text)
        time.sleep(5)

    	headers = {'Content-type': 'application/json'}
        r = requests.post('http://mir.com:8080/v1.0.0/mission_queue', json ={"mission": "22cb488a-6dea-11e8-9f16-f44d306f3f85"}, headers=headers)   #10.release trolley
        print(r.text)

    	headers = {'Content-type': 'application/json'}
        r = requests.post('http://mir.com:8080/v1.0.0/mission_queue', json ={"mission":"97b0f8eb-4855-11e8-a4e3-f44d306f3f85"}, headers=headers)  #11.go back to start position
        print(r.text)
        return "Call for parts mission has been accomplished!"


    input_string = request.form['value']
    if (input_string == 'DispatchPartsStation') :   #Ready for Dispatch from assembly line to warehouse

    	headers = {'Content-type': 'application/json'}
        r = requests.post('http://mir.com:8080/v1.0.0/mission_queue', json ={"mission":"97b0f8eb-4855-11e8-a4e3-f44d306f3f85"}, headers=headers)  #1.start position
        print(r.text)

    	headers = {'Content-type': 'application/json'}
        r = requests.post('http://mir.com:8080/v1.0.0/mission_queue', json ={"mission": "798ad3c2-3d33-11e8-99fb-f44d306f3f85"}, headers=headers)  #2.go to wait position 2 near station one
        print(r.text)

    	headers = {'Content-type': 'application/json'}
        r = requests.post('http://mir.com:8080/v1.0.0/mission_queue', json ={"mission": "3561d489-3d35-11e8-99fb-f44d306f3f85"}, headers=headers)   #3.pick up trolley from station one
        print(r.text)

    	headers = {'Content-type': 'application/json'}
        r = requests.post('http://mir.com:8080/v1.0.0/mission_queue', json ={"mission": "5461f0d2-0567-11e8-b987-f44d306f3f85"}, headers=headers)   #4.make a sound
        print(r.text)

    	headers = {'Content-type': 'application/json'}
        r = requests.post('http://mir.com:8080/v1.0.0/mission_queue', json ={"mission": "fd2fc112-485a-11e8-9812-f44d306f3f85"}, headers=headers)   #5.go to wait positio 2n near warehouse
        print(r.text)
        time.sleep(5)

    	headers = {'Content-type': 'application/json'}
        r = requests.post('http://mir.com:8080/v1.0.0/mission_queue', json ={"mission": "22cb488a-6dea-11e8-9f16-f44d306f3f85"}, headers=headers)   #10.release trolley
        print(r.text)


    	headers = {'Content-type': 'application/json'}
        r = requests.post('http://mir.com:8080/v1.0.0/mission_queue', json ={"mission": "5461f0d2-0567-11e8-b987-f44d306f3f85"}, headers=headers)   #6.make a sound
        print(r.text)


    	headers = {'Content-type': 'application/json'}
        r = requests.post('http://mir.com:8080/v1.0.0/mission_queue', json ={"mission":"97b0f8eb-4855-11e8-a4e3-f44d306f3f85"}, headers=headers)  #11.go back to start position
        print(r.text)
        return "Call for parts mission has been accomplished!"





if __name__ == "__main__":
    app.run()
