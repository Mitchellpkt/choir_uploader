# handler_in_str_to_out_str.py
# Strings together a few functions, to get from input filename to output evaluation
#
# mitchellpkt@protonmail.com
# github.com/mitchellpkt/operatoraware
#
##########
# INPUTS:
#
# >> audio_file_name_w_extension - the string showing what file to load in
# >> audio_folder_path - path of audio file. If 'auto', guesses (./INPUT_audio) from running directory
# >> transcription_directory path - where the transcripts are stored, guesses (./CACHE_transcriptions) from running directory
# >> qVerbose - extra feedback in console? default = 0
# >> str_dict_version - specify what version of dictionary to use. 'newest' by default
#
# *** Both of these inputs are provided by load_audio_from_filename.py
#

###########
# OUTPUTS:
# >> eval_str - a single string containing the evaluation

###########
# CHANGELOG:
# >>

########
# TO DO:
#

#############
# EXAMPLE:
#

def handler_in_str_to_out_str(audio_file_name_w_extension,audio_folder_path='auto',transcription_slices_directory_path='auto',transcription_training_directory_path='auto',qVerbose=1,str_dict_version='newest',demo_mode=0):
    # Load in the relevant modules,
    import os
    import hashlib
    import re

    # From OperatorAware
    from .load_audio_from_filename import load_audio_from_filename
    from .evaluate_string import evaluate_string
    from .return_dictionary import return_dictionary
    from .fetch_transcript import fetch_transcript
    from .convert_audio_to_flac import convert_audio_to_flac
    from .chop_up_audio import chop_up_audio

    # Form input filename
    if audio_folder_path == 'auto':
        # guess at file path from the current directory
        full_audio_file_path = os.path.join(
            os.getcwd(),
            'INPUT_audio',
            audio_file_name_w_extension)
    else:
        # Construct from input path
        full_audio_file_path = os.path.join(audio_folder_path,audio_file_name_w_extension)

    # What do we call this project?
    audio_data, audio_config_junk = load_audio_from_filename(full_audio_file_path)
    hash_object = hashlib.sha256(audio_data.SerializePartialToString())
    hex_dig = hash_object.hexdigest()
    base_name = os.path.basename(full_audio_file_path)
    hash_tag = hex_dig[0:4]
    master_name_raw = hash_tag + '_' + base_name
    master_name = master_name_raw.replace('.','_')
    print('*********Master Name**********')
    print(master_name)

    # Make a subdirectory for this task
    if demo_mode == 0:
        new_path = os.path.join(audio_folder_path,master_name)
    else:
        new_path = audio_folder_path
    if not os.path.isdir(new_path):
        os.mkdir(new_path)

    print('New path:' + new_path)

    new_full_audio_file_path = os.path.join(new_path,audio_file_name_w_extension)
    print('New filename/location: ' + new_full_audio_file_path)
    os.rename(full_audio_file_path,new_full_audio_file_path)
    print('(renamed)')
    # Convert the audio to flask
    flac_full_audio_file_path = convert_audio_to_flac(new_full_audio_file_path)
    print('new FLAC file at:' + flac_full_audio_file_path)

    if flac_full_audio_file_path == "ERROR_UNKNOWN_EXTENSION":
        return('Unknown file extension. Please upload mp3, wav, or flac files.')

    # Chop the audio into < 1 min pieces
    num_segments, audio_length_s = chop_up_audio(flac_full_audio_file_path)
    print(audio_length_s)

    # Init for loop
    net_transcription = ''
    net_categories = list()
    net_words = list()
    net_results_printout = ''
    confidence_metric = list()
    net_is_urgent = 0

    # Loop over each audio segment
    for n in list(range(1, num_segments+1)):
        # Load the audio
        segment_filename = flac_full_audio_file_path+'.'+str(n)
        audio_data, audio_config = load_audio_from_filename(segment_filename)
        print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
        print('Loading: ' + segment_filename)

        # Specify transcription directory
        if transcription_slices_directory_path=='auto':
            use_transcript_directory = os.path.join(
                os.getcwd(),
                'CACHE_transcriptions')
        else:
            use_transcript_directory = transcription_slices_directory_path

        # Fetch the transcript
        print('pieces of transcriptions stored in: ')
        print(transcription_slices_directory_path)
        transcription_str, this_confidence_metric = fetch_transcript(audio_data, audio_config, transcript_directory=transcription_slices_directory_path, qVerbose=qVerbose, force_fresh=0, do_not_save=0)
        confidence_metric.append(this_confidence_metric)
        net_transcription += ' /// ' + transcription_str
        print('Transcription for segment:')
        print(transcription_str)

        # Retrieve the dictionary
        danger_words, danger_names = return_dictionary(str_dict_version=str_dict_version)

        # Evaluate the call
        is_urgent, category_list, word_list, results_printout = evaluate_string(transcription_str, danger_words, danger_names)
        print('Danger words:')
        print(danger_words)
        net_is_urgent += is_urgent
        net_categories.append(category_list)
        net_words.append(word_list)
        net_results_printout += results_printout

        os.remove(segment_filename) # cleanup

    print('*'*30)
    print('Net transcription:')
    print(net_transcription)

    new_transcript_filename_pre1 = base_name + "_" + hash_tag + '_transcript'
    new_transcript_filename_pre2 = new_transcript_filename_pre1.replace('.','_')
    new_transcript_filename = new_transcript_filename_pre2+'.txt'

    # Record the net transcription
    transcription_filename = os.path.join(new_path,new_transcript_filename)
    with open(transcription_filename, 'w') as f_open:
        f_open.write(str(confidence_metric)+'\n')
        f_open.write(str(net_transcription))
        f_open.close()

    # Training data path
    print('training directory is:')
    print(transcription_training_directory_path)
    training_data_path = os.path.join(transcription_training_directory_path) # is .. .. dangerous?? probably
    if not os.path.isdir(training_data_path):
        os.mkdir(training_data_path)

    # Store transcription in the training folder
    training_data_filename = os.path.join(training_data_path, new_transcript_filename)
    with open(training_data_filename, 'w') as f_open:
        f_open.write(str(confidence_metric)+'\n')
        f_open.write(str(net_transcription))
        f_open.close()

    # Make categories file
    with open(training_data_filename+'.categories', 'w') as f_open:
        f_open.write('Lorem,')
        f_open.close()

    from itertools import chain

    net_categories = list(set(list(chain.from_iterable(net_categories))))
    net_words = list(set(list(chain.from_iterable(net_words))))

    return net_results_printout, audio_length_s, confidence_metric, net_words, net_categories, net_is_urgent, net_transcription
