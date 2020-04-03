# convert_audio_to_flac.py
# Loads the file and exports as FLAC
# Maybe even more importantly, it sets it to mono channel and a fixed bitrates
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
# >> new_filename - path to the preprocessed file

###########
# CHANGELOG:
#

########
# TO DO:
# >> expand to formats beyond FLAC

#############
# EXAMPLE:
#

def convert_audio_to_flac(str_audio_filename):
    # !pip install pydub
    # !sudo apt-get install ffmpeg

    from pydub import AudioSegment
    import re
    import os

    str_extension = str_audio_filename[-3:]

    print('Converting from ' + str_extension)

    # Read in the audio
    audio_data = AudioSegment.from_file(str_audio_filename)

    # Generate path for output file
    if str_extension == 'LAC':
        new_filename = str_audio_filename[0:-4] + 'flac' # Make sure extension is lower case
        os.rename(str_audio_filename, str_audio_filename+'.orig') # move the old file to avoid name conflict
    else:
        new_filename = re.sub('(?i)' + re.escape('.'+str_extension), lambda m: '.flac', str_audio_filename)

    audio_data.export(new_filename, format="flac")

    return new_filename