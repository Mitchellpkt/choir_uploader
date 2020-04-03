# check_passphrase()
# Input string to be verified (pswd_from_user)
# Optional, specify passphrase_file_path

def check_passphrase(pswd_from_user, passphrase_file_path='supervisor_passphrases.keys'):
    #passphrase_file = open(passphrase_file_path, 'r')
    #pswd_read = passphrase_file.readlines(0)
    #pswd_from_file = pswd_read[0].rstrip()
    #passphrase_file.close()

    wordlistFile = open(passphrase_file_path, 'r')  # open wordlist, e.g. BIP39
    valid_passphrases_raw = wordlistFile.read()


    if pswd_from_user in valid_passphrases_raw:
        print('passphrase accepted')
        return 1
    else:
        print('Wrong supervisor passphrase')
        return 0


