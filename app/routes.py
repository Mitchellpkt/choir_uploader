from flask import render_template, request
from app import app
#from operator_aware_lib.handler_in_str_to_out_str import handler_in_str_to_out_str
#from operator_aware_lib.check_passphrase import check_passphrase
import time
import os
import re
from shutil import copyfile


APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def index():
    print('route through index alone')
    return render_template('index.html')

@app.route('/', methods=["POST"])
@app.route('/index', methods=["POST"])
def indexpost(confidence_threshold=0.6):
    print('route through index post')

    # Generate and create target path for audio file (uploads)
    # target = os.path.join(APP_ROOT, 'static/uploads')
    # if not os.path.isdir(target):
    #     os.mkdir(target)
    # else:
    #     print("Couldn't create upload directory: {}".format(target))

    # Check the password
    #pswd_from_user = request.form['password']
    #authenticated = check_passphrase(pswd_from_user, passphrase_file_path='supervisor_passphrases.keys')

    #if pswd_from_user=="naive":
    #    not_naive = 0
    #else:
    #    not_naive = 1

    #if authenticated == 0:
    #    return render_template('wrong_passphrase.html')

    #else:
        # Continue ahead
    net_results_printout = ''  # init
    call_list = list()

    filename_list = list()
        # LOOP OVER UPLOADED FILES
    print(request.files.getlist("file"))
    for upload in request.files.getlist("file"):
        print(upload)

        filename_str = upload.filename
        print("{} is the filename".format(filename_str))

        destination = "./files/upload_at_"+ str(round(time.time())) # ####### "/".join([target, filename_str])
        print("Accepted incoming file: ", filename_str)

        upload.save(destination)
        print("Saved it to: ", destination)

        filename_list.append(destination)
            ######

        # is_not_demo = 1
        # IF NO FILES UPLOADED, USE DEMO
        #if (pswd_from_user=="") or (not filename_list):
        #    is_not_demo = 0
        #    print("DEMO!!!!!")
        #    new_filename_list = os.listdir(os.path.join(APP_ROOT, 'static/demo_files'))
        #    print('new_filename_list:')
        #    print(new_filename_list)
        #    filename_list_all = [os.path.join(APP_ROOT, 'static', 'demo_files', f) for f in new_filename_list]
        #    filename_list = list()
        #    for f in filename_list_all:
        #        print('Looping over:')
        #        print(str(f))
        #        print(str(f[-4:]))
        #        if f[-4:].upper() != 'FLAC':
        #            filename_list.append(f)
        #            print('adding: ' + str(f))
        #    for f in filename_list:
        #        print('from: ')
        #        print(f)
        #        print('to: ')
        #        uploads_dest = os.path.join(APP_ROOT, 'static', 'uploads', os.path.basename(f))
        #        print(uploads_dest)
        #        copyfile(f, uploads_dest)
        #        print('copied: ' + str(f))

        #    filename_list.sort()
        #    print(filename_list)

        # for filename in filename_list:

        #    results_printout, audio_length_s, confidence_metric, words_list, categories_list, is_urgent, net_transcription = handler_in_str_to_out_str(
        #        audio_file_name_w_extension=filename,
        #        audio_folder_path=os.path.join(target),
        #        transcription_slices_directory_path=os.path.join(APP_ROOT,'../CACHE_transcriptions'),
        #        transcription_training_directory_path=os.path.join(APP_ROOT,'../text_training_data'),
        #        qVerbose=1,
        #        str_dict_version='newest', demo_mode=1)

        #    min_conf = float(min(confidence_metric))
        #    min_conf_prct_str = str(round(min_conf * 100))
        #    print('min_conf is type: ' + str(type(min_conf)))
        #    print('confidence_threshold is type: ' + str(type(confidence_threshold)))
        #    if min_conf < confidence_threshold:
        #        confidence_warning = ' [Warning: low transcription confidence: ' + min_conf_prct_str + '%]'
        #    else:
        #        confidence_warning = ''  # Acceptable audio quality, transcription minimum confidence = ' + min_conf_prct_str + '%'

        #    filename_only = os.path.basename(filename)
        #    print('is_not_demo')
        #    print(is_not_demo)

        #    words_list_string = str(words_list)
        #    words_list_string = re.sub("[] []", '', words_list_string) # indecisive about tics around keywords

        #   categories_list_string = str(categories_list)
        #    categories_list_string = re.sub("[]'[]", '', categories_list_string)

        #    if pswd_from_user=="debug":
        #        is_not_demo = 1
        #        is_debug = 1
        #    else:
        #        is_debug = 0

        #    call_list.append({
        #        'base_filename': str(filename_only),
        #        'net_results': results_printout,
        #        'call_duration': time.strftime('%H:%M:%S', time.gmtime(audio_length_s)),
        #        'confidence_warning': confidence_warning,
        #        'audio_file_path': filename,
        #        'words_list': words_list_string,
        #        'categories_list': categories_list_string,
        #        'is_urgent': is_urgent,
        #        'is_not_demo': is_not_demo,
        #        'not_naive': not_naive,
        #        'is_debug': is_debug,
        #        'net_transcription': net_transcription
        #    })

        if not filename_list:
            print("Empty upload, no files received this time!")
            #new_filename_list = os.listdir(os.path.join(APP_ROOT, 'static/demo_files'))
            #print(new_filename_list)

        # Return the result
        return render_template('output2.html')
        #return render_template('output.html', calls=call_list)
