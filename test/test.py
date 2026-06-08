import os
import getpass

c : dict = {3601183: {'NAME': "NGUYỄN KHẮC MINH PHƯƠNG", 'GENDER': "MALE", 'ROLE': "VERIFY", 'SHIFT': "VN80",' LOC': "TBS", 'STATUS': "ON DUTY", 'FLAG': 0}}
k,v = list(c.items())[0]
print(k)
print(v['FLAG'])