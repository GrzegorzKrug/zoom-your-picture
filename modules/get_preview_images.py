import imutils
import shutil
import numpy as np
import copy
import glob
import cv2
import os
import re



PIC_NAMES = [
    #'alien',
    'alienmonster',
    #'avocado',
    'beamingfacewithsmilingeyes',
    #'baguettebread',
    'butterfly',
    'banana',
    'babychick',
    'balloon',
    'books',
    'bird',
    #'cat',
    'cactus',
    'carrot',
    #'clapperboard',
    'dragon',
    #'dog',
    #'duck',
    'eyes',
    'fox',
    'fire',
    'fish',
    'frog',
    #'flagpoland',
    'ghost',
    'growingheart',
    'gemstone',
    #'hamburger',
    'honeybee',
    'lizard',
    'octopus',
    'okhandlightskintone',
    'parrot',
    'panda',
    'penguin',
    'pizza',
    'purpleheart',
    'rainbow',
    #'radioactive',
    #'rabbit',
    #'rabbitface',
    'recyclingsymbol',
    'rooster',
    #'rocket',
    #'smilingfacewithsmilingeyes',
    #'shark',
    'shield',
]

PAL_DIR = os.path.join('backend', 'palette')
DEST_DIR = os.path.join('static', 'emotes')
stack = None
SIZE = 40

for family in os.listdir(PAL_DIR):
    path = os.path.join(PAL_DIR, family)
    count = 0
    if os.path.isdir(path):
        "CHECK FAMILY Loop LEVEL"
        destination = os.path.join(DEST_DIR, family)
        os.makedirs(destination, exist_ok=True)

        for fil in os.listdir(path):
            name = os.path.basename(fil)[:-4]
            src = os.path.join(path, fil)
            dst = os.path.join(destination, fil)

            if name in PIC_NAMES:
                shutil.copyfile(src, dst)
                count += 1

        all_pics = copy.copy(PIC_NAMES)
        preview = None
        for name in PIC_NAMES:
            "Check pictures in order from list"
            fil = f"{name}.png"

            img_array = cv2.imread(os.path.join(destination, fil), cv2.IMREAD_UNCHANGED)
            try:
                img_array = cv2.cvtColor(img_array, cv2.COLOR_BGR2BGRA)
                img_array = cv2.resize(img_array, (SIZE,SIZE))
                all_pics.pop(all_pics.index(name))
            except Exception:
                img_array = np.zeros((SIZE,SIZE,4), dtype=np.uint8)
                #img_array = cv2.cvtColor(img_array, cv2.COLOR_BGR2BGRA)

            if preview is not None:
                #print(preview.shape, img_array.shape)
                preview = np.concatenate([preview, img_array], axis=1)
            else:
                preview = img_array

        "Save preview image is exists"
        if preview is not None:
            cv2.imwrite(os.path.join(DEST_DIR, f"{family}.png"), preview)
            if stack is not None:
                stack = np.concatenate([stack, preview], axis=0)
            else:
                stack = preview
            
        print()
        print(f"{path}")
        print(f"missing:\n{all_pics}")
 
    
if stack is not None:
    cv2.imwrite(os.path.join(DEST_DIR, f"STACK.png"), stack)
