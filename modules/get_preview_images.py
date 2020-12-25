import shutil
import glob
import os
import re
import copy



PIC_NAMES = [
    'alien',
    'alienmonster',
    'avocado',
    'beamingfacewithsmilingeyes',
    'baguettebread',
    'butterfly',
    'banana',
    'babychick',
    'balloon',
    'books',
    'bird',
    'cat',
    'cactus',
    'carrot',
    'dragon',
    'dog',
    'duck',
    'eyes',
    'frog',
    'fire',
    'ghost',
    'growingheart',
    'gemstone',
    'hamburger',
    'octopus',
    'parrot',
    'penguin',
    'pizza',
    'rocket',
    'rainbow',
    'smilingfacewithsmilingeyes',
]

PAL_DIR = os.path.join('backend', 'palette')
DEST_DIR = os.path.join('static', 'emotes')

for family in os.listdir(PAL_DIR):
    path = os.path.join(PAL_DIR, family)
    count = 0
    if os.path.isdir(path):
        "Check if this is directory"
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
        for fil in os.listdir(destination):
            name = os.path.basename(fil)[:-4]
            
            try:
                all_pics.pop(all_pics.index(name))
            except ValueError:
                print(f"This file is not on wanted list!: {family} {fil}")

        print()
        print(f"{path}")
        print(f"missing:\n{all_pics}")
 
    
    else:
        pass

