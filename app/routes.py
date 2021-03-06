from flask import render_template, request
from app import app
#from operator_aware_lib.handler_in_str_to_out_str import handler_in_str_to_out_str
#from operator_aware_lib.check_passphrase import check_passphrase
import time
import os
import re
from shutil import copyfile
from werkzeug.utils import secure_filename

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
ALLOWED_EXTENSIONS = set(['mp4', 'mp3'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    print('route through index alone')
    return render_template('index.html')

@app.route('/', methods=["POST"])
@app.route('/index', methods=["POST"])
def indexpost(confidence_threshold=0.6):
    print('route through index post')

    net_results_printout = ''  # init
    call_list = list()
    filename_list = list()
    print(request.files.getlist("file"))
    for upload in request.files.getlist("file"):
        print(upload)
        # check extension
        if allowed_file(upload.filename)
           # secure the file name to protect against path trasversal injection using the file name
           filename_str = secure_filename(upload.filename)
        
            print("{} is the filename".format(filename_str))

            destination = "./files/" + str(round(time.time())) + "_" + filename_str # ####### "/".join([target, filename_str])
            print("Accepted incoming file: ", filename_str)

            upload.save(destination)
            print("Saved it to: ", destination)

            filename_list.append(destination)
            return render_template('output2.html')
            
    if not filename_list:
        return render_template('outputEMPTY.html')
        print("Empty upload, no files received this time!")
            #new_filename_list = os.listdir(os.path.join(APP_ROOT, 'static/demo_files'))
            #print(new_filename_list)

  #  else:
   # 	return render_template('output2.html')
        #return render_template('output.html', calls=call_list)
