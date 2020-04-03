# load_audio_from_filename.py
# Loads audio waveform, given inpute filename string
# 
#
# mitchellpkt@protonmail.com
# github.com/mitchellpkt/operatoraware
#
##########
# INPUTS:
#
# >> str_audio_filename - a string pointing to the file to be read
#

###########
# OUTPUTS:
# >> audio_data - the data for the audio file
# >> audio_config - information about encoding

###########
# CHANGELOG:
#

########
# TO DO:
# >> expand to formats beyond FLAC

#############
# EXAMPLE:
#

def load_audio_from_filename(str_audio_filename):
    import io
    # from google.cloud.speech import enums
    # from google.cloud.speech import types

    from google.cloud.speech_v1p1beta1 import enums
    from google.cloud.speech_v1p1beta1 import types

   ### Form filename
    #file_name = os.path.join(
    #    os.getcwd(),
    #    'Real_911Calls',
    #    sound_filename + '.flac')

    # Confirm that this is a FLAC file
    # str_extension = str_audio_filename[-4:]
    # if str_extension.upper() != 'FLAC':
    #   raise ValueError('This version of load_audio_from_filename only works for FLAC files')


    ### Load the audio into memory
    with io.open(str_audio_filename, 'rb') as audio_file:
        content = audio_file.read()

    audio_data = types.RecognitionAudio(content=content) # this was in a loop?
    audio_config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
        #sample_rate_hertz=8000,#16000
        language_code='en-US',
        # Enhanced models are only available to projects that
        # opt in for audio data collection.
        use_enhanced=True,
        # A model must be specified to use enhanced model.
        model='phone_call')

    return audio_data, audio_config
