import ctypes
import time
import subprocess
import hashlib
import random

libc = ctypes.cdll.LoadLibrary("libc.so.6")

def c_rand(seed):
    libc.srand(seed)
    return libc.rand()

def md5_string(input_string):
    md5 = hashlib.md5()
    md5.update(input_string)
    return md5.hexdigest()

def guess_and_test_hash():
    known_start_time = int(time.time())

    for i in range(-30, 30):
        seed = known_start_time + i
        c_random_number = c_rand(seed)

        key = str(c_random_number)
        generated_md5 = md5_string(key)

        print("Trying MD5: {} for seed {}".format(generated_md5, seed))

        process = subprocess.Popen(['nc', 'cs2107-challs.nusgreyhats.org', '8051'], 
                                   stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            
        stdout, stderr = process.communicate(input="{}\n".format(generated_md5))

        output = stdout
        print(output)

        if "CS2107" in output:
            print("Flag found: {}".format(output))
            return  
            
guess_and_test_hash()