# -*- coding: utf-8 -*-
"""
Created on Sun Apr 01 11:14:15 2018

@author: Prodipta
"""

import hashlib  

def verify_checksum(order_id, time_stamp,checksum, secret_key):
    h = hashlib.sha256(order_id.encode("utf-8") + time_stamp.encode("utf-8") + secret_key.encode("utf-8"))
    if h.hexdigest() == checksum:
        return True
    with open("checksum.txt","a") as outfile:
        outfile.write("mismatched checksum, order id {}, {} vs expected {}".format(order_id,checksum,h))
    return False
