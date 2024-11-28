from Crypto.PubliKey import RSA

file_to_encrypt = open('file.txt', 'rb').read()
pub_key = open('pub_key.pem', 'rb').read()
o = RSA.importKey(pub_key)
