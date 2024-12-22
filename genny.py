from PIL import Image
import os
import socket
import hashlib
import random_prompt as rp
from PIL import Image
from PIL.PngImagePlugin import PngInfo
import time
import shutil
import subprocess

tmpfldr = 'images'
magicfile = 'nfs/isnfsmounted'
destdir = 'nfs/sdimg'

def isnfsmounted():
    with open(magicfile) as f: s = f.read(); return True if s=='yes\n' else False

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # doesn't even have to be reachable
        s.connect(('10.254.254.254', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def gen_image(prompt, newname):
    starttime = time.time()
    print('Starting generation at',time.ctime())
    result = subprocess.run(['./sd','--prompt',prompt,'--output',os.path.join(tmpfldr,newname), '--rpi'],
						 stdout=subprocess.PIPE).stdout.decode('utf-8')
    f = os.path.join(tmpfldr,newname)
    res = [s.split(':') for s in result.split('\n')]
    totalstepstime=steps=0
    stepmsarray=[]
    for l in res:
        if l[0].startswith('seed'):
            seed = l[1]
        if l[0].startswith('step'):
            if l[0] == 'steps':
                continue
            stepn = int(str(l[1].lstrip()[0]))
            stepms = str(l[1])[2:].lstrip()[:-2]
            try:
                stepms = int(stepms)
            except ValueError:
                stepms = int("{:.0f}".format(float(stepms)))
            totalstepstime+=stepms
            steps+=1
            stepnms = str(stepn) + ":" + str(stepms)
            stepmsarray.append(stepnms)
    endtime = time.time()
    stepmsarray = ','.join(stepmsarray)
    avgstepms = str(round(totalstepstime/steps))
    targetImage = Image.open(f)
    metadata = PngInfo()
    metadata.add_text("prompt", prompt)
    metadata.add_text("seed", seed)
    metadata.add_text("steps", stepmsarray)
    metadata.add_text("avg_step_ms", avgstepms)
    #negative during testing as we're not actually generating anything
    decodetime = str(round(((endtime - starttime)*1000)-totalstepstime))
    metadata.add_text("decode_time", decodetime)
    totaltime = str(round((endtime - starttime)*1000))
    metadata.add_text("totaltime", totaltime)
    metadata.add_text("hostname",socket.gethostname())
    metadata.add_text("generator_ip",get_ip())
    print('Time taken to create image:',totaltime)
    newimg = os.path.join(tmpfldr,newname)
    targetImage.save(newimg, pnginfo=metadata)
    targetImage = Image.open(newimg)
    return targetImage.filename

def movefile(filetoupload):
    if isnfsmounted():
        shutil.move(filetoupload, os.path.join(destdir,os.path.basename(filetoupload)))
        print('Moved image to NFS')
        for image in os.listdir(tmpfldr):
            if (image.endswith(".png")):
                shutil.move(os.path.join(tmpfldr,image),os.path.join(destdir,os.path.basename(image)))
                print('Moved previously forgotten files to NFS')
    else:
        print('NFS not mounted, keeping image locally for now')

while True:
    prompt = rp.random_prompt()
    print('Prompt:',prompt)
    newname = str(hashlib.md5(prompt.encode()).digest().hex()) + ".png"
    print('Filename:',newname)
    if os.path.exists(os.path.join(destdir,newname)):
        print('Wow, it happened, we have a repeated filename')
        continue
    filetoupload = gen_image(prompt, newname)
    movefile(filetoupload)
