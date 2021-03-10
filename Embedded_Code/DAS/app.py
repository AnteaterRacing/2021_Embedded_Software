# DAS Web App
# Written by Michael Felizardo
# Maintained by Michael Felizardo and William Sun
# Last Revision: 3/7/2021 


import os
import pathlib
import datetime
from flask import Flask, render_template, url_for, request, redirect, flash
from werkzeug.utils import secure_filename
import io

import daslib as das

UPLOAD_FOLDER = './uploads/'
ALLOWED_EXTENSIONS = {'csv'}

app = Flask(__name__)
app.secret_key = "racecar"
app.config["CSV_UPLOADS"] = UPLOAD_FOLDER




@app.route('/', methods=['GET'])
def index():
	return render_template('index.html')

@app.route('/file-list', methods=['GET'])
def render_file_list():
	return render_template('file_list.html', file_list=get_file_list())

def get_file_list() -> [(str, str)]:
	# Returns a list of tuples. Each tuple represents one file
	# The tuple contains filename, date modified, 
	files = [f for f in os.listdir(UPLOAD_FOLDER) if os.path.isfile(os.path.join(UPLOAD_FOLDER, f))]
	return [get_file_tuple(f) for f in files]

def get_file_tuple(filename: str) -> (str, str):
	filepath: pathlib.Path = pathlib.Path(os.path.join(UPLOAD_FOLDER, filename))
	modified_time = datetime.datetime.fromtimestamp(filepath.stat().st_ctime)		
	#	st_ctime is Platform dependent: 	see https://docs.python.org/3/library/os.html#os.stat_result
	#		the time of most recent metadata change on Unix,
	#		the time of creation on Windows, expressed in seconds.
	return (filename, modified_time)

@app.route('/file-upload', methods=['POST'])
def upload_file():
	# check if the post request has the file part
	if 'file' not in request.files:
		flash('No file part')
		return redirect(url_for('index'))
	file = request.files['file']

	# handle not uploading file 
	if file.filename == '':
		flash('No selected file')
		return redirect(url_for('index'))

	# get values from uploaded fields
	filename = secure_filename(file.filename)
	file.save(os.path.join(app.config["CSV_UPLOADS"], file.filename))
	sensor = request.form["sensor"]
	func = request.form["function"]

	return redirect(url_for('view_uploaded_files', filename=filename, sensor=sensor, function=func))


@app.route('/file-error', methods=['GET'])
def file_error():
	return render_template('file_error.html')


@app.route('/file/<filename>/<sensor>/<function>', methods=['GET'])
def view_uploaded_files(filename: str, sensor: str, function: str):
	try:
		(averages, absmins, absmaxes) = handle_data(filename, sensor, function)
	except Exception:
		return redirect('/file-error')

	return render_template('data.html', filename=filename, sensor=sensor, function=function,
		averages=averages, absmins=absmins, absmaxes=absmaxes, data=True)


def handle_data(filename,sensor,function):
    headernames = ["Accel_X", "Accel_Y", "Accel_Z", "Gyro_X", "Gyro_Y", "Gyro_Z", "IR_1", "IR_2", "IR_3", "Wheelspeed", "Lat", "Long"]

    #read csv file, append headers
    df = das.getdf(UPLOAD_FOLDER + filename, headernames) #gets dataframe from csv file

    #filter for desired sensor
    df = das.filterSensor(df, sensor)

    f_data = df #assignment in the event that the user chose raw data
    if(function == 'avg'):
        f_data = das.avg(df)
        print(f_data)
    elif(function == 'relmax'):     #relative maximum
        f_data = das.relmax(df)  
    elif(function == 'relmin'):
        f_data = das.relmin(df)  
    elif(function == 'absmax'):
        f_data = das.absExtremum(df, "max")
    elif(function == 'absmin'):
        f_data = das.absExtremum(df, "min")


    #a bunch of if elses to satisfy the sensor argument
    #broken up becasue the raw data option doesn't need the optional arguments 

    if((function == "raw") or (function == "relmin") or (function == "relmax")): #plot these
        if(function == "raw"):             #plots raw graphs without optional arguments
            if(sensor == "accel"):
                fig = das.plotGraph(f_data, "Gs")         #g force
            elif(sensor == 'gyro'):    
                fig = das.plotGraph(f_data, "Dps")        #degrees per second
            elif(sensor == "temp"):    
                fig = das.plotGraph(f_data, "Fahrenheit") #fahrenheit
            elif(sensor == "wheelspeed"):
                fig = das.plotGraph(f_data, "mph")        #miles per hour
        else:
            if(sensor == "accel"):
                fig = das.plotGraph(df, "Gs", f_data)         #g force
            elif(sensor == 'gyro'):    
                fig = das.plotGraph(df, "Dps", f_data)        #degrees per second
            elif(sensor == "temp"):    
                fig = das.plotGraph(df, "Fahrenheit", f_data) #fahrenheit
            elif(sensor == "wheelspeed"):
                fig = das.plotGraph(df, "mph", f_data)        #miles per hour

        
        averages = das.get_avg(df)
        absmins = das.get_absmin(df)
        absmaxes = das.get_absmax(df)

        return (averages, absmins, absmaxes)


    

if __name__ == "__main__":
    app.run(debug=True)
    