"""v12.0.0 constants, private keys and such"""

ik8 = "3167cc23323fbf00"
ik9 = "e3de0101442c8227"
e7 = "hcdHyOYXb22DrEpMJ8IRsw=="
e8 = "0qMd7mZEW0yuVtmvbxSv1Q=="
e33 = "MxS1XkWu3tR2KEZOogk0hQ=="
e44 = "7cTLMFTZfRHcuaEWcUaY1Q=="

ha_iv = "ov7xs32456bnl0l1"

hh_iv = "lvcas56410c97lpb"

e8_decrypted_by_ik8 = "f1de00116"
e7_decrypted_by_ik9 = "ebafc4b"

e33_decrypted_by_ik9 = "74c2b32"
e44_decrypted_by_ik8 = "ddcbf7815"

request_key = e7_decrypted_by_ik9 + e8_decrypted_by_ik8
response_key = e33_decrypted_by_ik9 + e44_decrypted_by_ik8
