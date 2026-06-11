from Crypto.PublicKey import RSA


# Open PEM certificate
with open("privacy_enhanced_mail.pem", "rb") as f:
    key = RSA.importKey(f.read())

print(key.d)