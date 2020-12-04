from multiprocessing import Process, Queue, Pool
from itertools import product
from PIL import Image
from io import BytesIO

from .logger_shared import logger

import traceback
import imutils
import pickle
import random
import numpy as np
import glob
import math
import time
import cv2
import sys
import os
import re


def time_it_dec(func):
    def wrapper(*args, **kwargs):
        time0 = time.time()
        result = func(*args, **kwargs)
        time_end = time.time()
        duration = time_end - time0
        if duration < 60:
            print(f"{func.__name__} was executed in {duration:>6.2f}s")
        else:
            print(f"{func.__name__} was executed in {duration / 60:>6.2f}m")
        return result

    return wrapper


class DistanceGraph:
    def __init__(self, array, keys, dimension=3, name=None):
        array = np.array(array)
        if array.shape[1] == dimension:
            self.array = array
        else:
            assert array.shape[0] == dimension, "Dimension does not match!"
            self.array = array.T
        print(self.array.shape)
        self.graph = {}
        self.dimension = dimension
        self.keys = keys
        self.pivots = {0}
        self.name = name

    @time_it_dec
    def create_map(self):
        graph = {}
        keys = [''.join(arr) for arr in product("pm", repeat=self.dimension)]
        template_budds = dict.fromkeys(keys, None).copy()

        for current_key, cur_point in enumerate(self.array):
            budds = template_budds.copy()

            for bud_key, vec in enumerate(self.array):
                if current_key == bud_key:
                    continue

                direction = ['p' if val > cval else 'm' for cval, val in zip(cur_point, vec)]
                direction = ''.join(direction)
                distance = self.calculate_distance(cur_point, vec)

                current_buddy = {"dist": distance, 'key': bud_key}
                is_someone = budds[direction]
                if is_someone:
                    some_dist = is_someone['dist']
                    if distance < some_dist:
                        budds[direction] = current_buddy
                else:
                    budds[direction] = current_buddy
            budds = {b['key'] for b in budds.values() if b}
            graph[current_key] = budds

        for key, budds in graph.items():
            for buddy in budds:
                graph[buddy].add(key)

        self.graph = graph
        self.get_pivots()
        print(f"Created graph of {self.name}")

    @time_it_dec
    def get_pivots(self):
        # points = list(product([40, 127, 210], repeat=self.dimension))
        points = list(product([30, 127, 220], repeat=self.dimension))
        # points = list(product([30, 80, 127, 170, 220], repeat=self.dimension))
        # points = list(product([20, 90, 160, 230], repeat=self.dimension))

        pivots = set()
        pivots = {self.find_closest(vec)[0] for vec in points}
        print(f"Pivots of {self.name}: {pivots}")
        self.pivots = pivots

    #     @time_it_dec
    def find_closest(self, vec):
        roots = [[piv, self.calculate_distance(vec, self.array[piv, :])]
                 for piv in self.pivots
                 ]
        #         print(roots)
        choosen = min(roots, key=lambda x: x[1])[0]
        #         print(f"Choosen: {choosen}")
        steps = len(roots)
        while True:
            choosen, stp1 = self.walk_further(choosen, vec)
            better, stp2, best_distance = self.ask_friends(choosen, vec)
            steps += stp1 + stp2
            if better == choosen:
                break
            else:
                choosen = better
        # print(f"Steps taken: {steps}")
        #         key = self.keys[choosen]
        return choosen, steps, best_distance

    def walk_further(self, choosen, vec):
        steps = 0
        while True:
            steps += len(self.graph[choosen])
            is_better = self.better_neightbour(choosen, vec)
            if is_better:
                choosen = is_better
            else:
                break
        return choosen, steps

    def ask_friends(self, choosen, vec, deep=3):
        """

        Args:
            choosen:
            vec:
            deep:

        Returns:
            bestindex
            steps number
            best distance
        """
        if deep == 3:
            last_buddies = {even_more_buddies
                            for buddy in self.graph[choosen]
                            for more_buddies in self.graph[buddy]
                            for even_more_buddies in self.graph[more_buddies]
                            }
        else:
            n = 0
            last_buddies = {bud for bud in self.graph[choosen]}
            while n < deep - 1:
                n += 1
                budds = {buddy for bud in last_buddies for buddy in self.graph[bud]}
                last_buddies = {*last_buddies, *budds}

        last_buddies.add(choosen)
        dist = [[budy, self.calculate_distance(vec, self.array[budy])] for budy in last_buddies]
        ultimate = min(dist, key=lambda x: x[1])
        steps = len(dist)
        return ultimate[0], steps, ultimate[1]

    @staticmethod
    def calculate_distance(vec1, vec2):
        error = (vec1 - vec2)
        error = (error * error).sum()
        #         error = np.absolute(error).sum()
        return error

    def better_neightbour(self, cur_node_key: int, vec):
        budds = self.graph[cur_node_key]
        better = None
        better_dist = self.calculate_distance(self.array[cur_node_key, :], vec)
        #         print(f"Checking: {cur_node_key}")
        for new_buddy_key in budds:
            if new_buddy_key:
                buddy_node = self.array[new_buddy_key]
                distance = self.calculate_distance(vec, buddy_node)

                if better_dist > distance:
                    better_dist = distance
                    better = new_buddy_key

        out = better if better != cur_node_key else None
        return out


def find_closes_image(arguments):
    (
            targ_blue, targ_green, targ_red,
            palette_list
    ) = arguments
    results = []
    all_steps = 0
    for dg in palette_list:
        best, steps, best_distance = dg.find_closest([targ_blue, targ_green, targ_red])
        path = dg.keys[best]
        results.append([path, best_distance])
        all_steps += steps
    choosen = min(results, key=lambda x: x[1])[0]
    return choosen, all_steps


def image_array_to_pillow(matrix):
    success, img_bytes = cv2.imencode(".png", matrix)
    bytes_like = BytesIO(img_bytes)
    image = Image.open(bytes_like)
    return image


def image_pillow_to_array(image):
    buffer = BytesIO()
    image.save(buffer, format='PNG')
    buffer.seek(0)
    matrix = np.frombuffer(buffer.read(), dtype=np.uint8)
    matrix = cv2.imdecode(matrix, cv2.IMREAD_COLOR)
    return matrix


@time_it_dec
def make_gif(image, config, cx=None, cy=None, ):
    OUTPUT_GIF_MAX_SIZE = config['outputsize']
    PROC_POWER = config['power']

    FRAMES = 500
    height, width, _ = image.shape
    origin_x = width // 2
    origin_y = height // 2
    temp_frame = scale_image_to_max_dim(image, OUTPUT_GIF_MAX_SIZE)
    out_height, out_width, _ = temp_frame.shape  # Keep aspect ratio

    origin_width = out_width
    origin_height = out_height

    origin_x = origin_x - origin_width // 2
    origin_x = 0 if origin_x < 0 else origin_x
    origin_y = origin_y - origin_height // 2
    origin_y = 0 if origin_y < 0 else origin_y
    # print(f"Y: {origin_height}, X:{origin_width}")
    # print(f"Ending height: {height}, width: {width}")

    arr_x = np.linspace(origin_x, 0, FRAMES)
    arr_y = np.linspace(origin_y, 0, FRAMES)
    arr_height = np.linspace(out_height, height, FRAMES)
    arr_width = np.linspace(out_width, width, FRAMES)
    roi_slice = slice(origin_y, origin_y + out_height), \
                slice(origin_x, origin_x + out_width), \
                slice(None)

    frame = image[roi_slice]
    frame = scale_image_to_max_dim(frame, OUTPUT_GIF_MAX_SIZE)
    pil_image = image_array_to_pillow(frame)

    framerate = 1 / 120
    duration = 1 / framerate
    frames_list = [pil_image, pil_image, pil_image]

    for fr, x, y, w, h in zip(range(FRAMES), arr_x, arr_y, arr_width, arr_height):
        if 490 > fr > 10 and (fr % 2 or fr % 3 or fr % 7):
            continue
        x = int(round(x))
        y = int(round(y))
        w = int(round(w))
        h = int(round(h))

        # print(f"Frame: {fr}: xy {x} - {y}, w:{w}, h:{h}")
        roi_slice = slice(y, y + h), slice(x, x + w), slice(None)
        roi = image[roi_slice]
        frame = imutils.resize(roi, width=out_width, height=out_height)
        frame = cv2.resize(frame, (out_width, out_height), interpolation=cv2.INTER_CUBIC)
        pil_image = image_array_to_pillow(frame)
        frames_list.append(pil_image)

    frames_list.append(pil_image)
    frames_list.append(pil_image)
    frames_list[0].save(config['outputpath'], format="GIF",
                        append_images=frames_list[1:],
                        save_all=True, optimize=False, duration=duration, loop=0)
    # print(f"Saved GIF.")


@time_it_dec
def get_mozaic(target, palette_list, config, ignore_image_size=True, fill_border_at_error=False):
    # target_hsv = cv2.cvtColor(target, cv2.COLOR_BGR2HSV)
    h, w, c = target.shape
    PIXEL_RATIO = config['pixelratio']

    if (h % PIXEL_RATIO or w % PIXEL_RATIO) and not ignore_image_size:
        print(f"Invalid size, H:{h}%->{h % PIXEL_RATIO}, W:{w}->{w % PIXEL_RATIO}")
        sys.exit(0)

    output = np.zeros(
            (h * AVATAR_SIZE // PIXEL_RATIO, w * AVATAR_SIZE // PIXEL_RATIO, 3),
            dtype=np.uint8
    )
    # target_hls = cv2.cvtColor(target, cv2.COLOR_BGR2HLS)

    pool = Pool(2)
    steps = []
    loop_range = len(range(0, h, PIXEL_RATIO))
    pixel_count = 0
    for row_num, cur_row in enumerate(range(0, h, PIXEL_RATIO)):
        time0 = time.time()

        "Make Queue"
        iter_like_orders = []
        for col_num, cur_col in enumerate(range(0, w, PIXEL_RATIO)):
            target_slice = slice(cur_row, cur_row + PIXEL_RATIO), slice(cur_col, cur_col + PIXEL_RATIO)
            pixel_count += 1
            curr_target_bgr = target[target_slice]
            # curr_target_hls = target_hls[target_slice]

            blue, green, red = np.mean(curr_target_bgr, axis=0).mean(axis=0)
            # hue, light, sat = np.mean(curr_target_hls, axis=0).mean(axis=0)
            args = blue, green, red, palette_list
            iter_like_orders.append(args)

        results = pool.map(find_closes_image, iter_like_orders)

        "Replace ROI"
        for col_num, cur_col in enumerate(range(0, w, PIXEL_RATIO)):
            output_slice = (
                    slice(row_num * AVATAR_SIZE, row_num * AVATAR_SIZE + AVATAR_SIZE),
                    slice(col_num * AVATAR_SIZE, col_num * AVATAR_SIZE + AVATAR_SIZE)
            )

            roi = output[output_slice]
            relative_path, stp = results.pop(0)
            steps.append(stp)
            if relative_path:
                # print(relative_path)
                abs_path = os.path.join(config['paldir'], relative_path)
                replacer = cv2.imread(abs_path, cv2.IMREAD_COLOR)
                replacer = imutils.resize(replacer, height=AVATAR_SIZE)
                try:
                    roi[:, :, :] = replacer
                except ValueError as err:
                    if ignore_image_size and fill_border_at_error:
                        last_h, last_w, _ = roi.shape
                        replacer = replacer[0:last_h, 0:last_w, :]
                        roi[:, :, :] = replacer
                    elif ignore_image_size:
                        pass
                    else:
                        print(f"{err}")
        timeend = time.time()
        duration = timeend - time0
        # print(f"{row_num:>3} of {loop_range} was executed in: {duration:>4.1f}s")
    logger.info(f"avg steps: {np.average(steps):>3.1f}, all: {np.sum(steps) / 1e6:>3.2f}M, pixels: {pixel_count/1000:>4.1f}k")
    return output


def scale_image_to_max_dim(image, max_val):
    height, width, _ = image.shape

    if height > max_val or width > max_val:
        if height > width:
            image = imutils.resize(image, height=max_val)
        else:
            image = imutils.resize(image, width=max_val)
    return image


def load_palette(config=None):
    if config:
        pal_path = config['palpath']
    else:
        pal_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "palette"))
        pal_path = os.path.join(pal_dir, "palettes.pickle")
    if os.path.isfile(pal_path):
        with open(pal_path, "rb") as fp:
            palette = pickle.load(fp)
    else:
        raise FileNotFoundError("Palette does not exists")
    # print(f"Palette loaded, size: {len(palette)}")  # size 1
    return palette


def make_mozaic_and_gif(target_path, config, selection=None):
    MAX_PIC_SIZE = config['maxpicsize']
    try:
        image = cv2.imread(target_path, cv2.IMREAD_COLOR)
        image = scale_image_to_max_dim(image, MAX_PIC_SIZE)
        height, width, _ = image.shape

        all_pallettes = load_palette(config)
        palette_list = get_palette_list(all_pallettes, selection)
        mozaic = get_mozaic(image, palette_list, config, fill_border_at_error=FILL_BORDER_WHEN_CROP)
        # print(f"Mozaic size: {mozaic.shape}")
        make_gif(mozaic, config)

    except Exception as err:
        tb_text = traceback.format_exception(type(err), err, err.__traceback__)
        tb_text = ''.join(tb_text)
        print(f"Error during making mozaic and gif: {tb_text}")


def make_stamp_square(img_path):
    image = cv2.imread(img_path, cv2.IMREAD_COLOR)
    h, w, c = image.shape
    if h < w:
        w = h
    elif w < h:
        h = w
    else:
        print(f"Images shape is the same, not editing: {img_path}")
        return None
    new_img = image[0:h, 0:w, :]
    cv2.imwrite(img_path, new_img)
    return new_img


def recreate_all_palettes():
    """
    Palettes are grouped by folder name, then by path:
    example:
    {"emotes":
        [
        {"path1": {"r":int, "g":int, "b":int}},
        {"path2": {"r":int, "g":int, "b":int}},
        ...
        ]
    }
    Returns:

    """
    pal_dirs = {}
    PAL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "palette"))
    PAL_PATH = os.path.join(PAL_DIR, "palettes.pickle")

    jobs = []
    for directory in os.listdir(PAL_DIR):
        cur_path = os.path.join(PAL_DIR, directory)

        if os.path.isdir(cur_path):
            jobs.append((directory, cur_path))
            # pal_dirs.update({directory: arr})

    results = Pool(10).map(create_async_graph, jobs)
    for directory, res in results:
        pal_dirs.update({directory: res})
    with open(PAL_PATH, "wb") as fp:
        pickle.dump(pal_dirs, fp)


def create_async_graph(args):
    directory, cur_path = args
    arr = create_palette(cur_path)
    keys, arr = [*zip(*arr.items())]
    good_ar = []
    for dct in arr:
        good_ar.append((dct['b'], dct['g'], dct['r']))
    # print(keys)
    dg = DistanceGraph(good_ar, keys, name=os.path.basename(cur_path))
    dg.create_map()
    return directory, dg


@time_it_dec
def create_palette(dir_path):
    palette = {}
    all_images = glob.glob(f"{dir_path}/**/*.png", recursive=True)
    all_images += glob.glob(f"{dir_path}/**/*.jpg", recursive=True)

    for image_path in all_images:
        image = cv2.imread(image_path, cv2.IMREAD_COLOR)

        height, width, channels = image.shape
        image = imutils.resize(image, width=AVATAR_SIZE)

        if height < AVATAR_SIZE or width < AVATAR_SIZE:
            print(f"This image is too small: {height:>4}, {width:>4} - {image_path}")
            continue
        elif height != width:
            print(f"This image is not squared: {height:>4}, {width:>4} - {image_path}")
            image = make_stamp_square(image_path)
        # hls_img = cv2.cvtColor(image, cv2.COLOR_BGR2HLS)

        blue, green, red = np.mean(image, axis=0).mean(axis=0)
        # hue, light, sat = np.mean(hls_img, axis=0).mean(axis=0)
        rel_dir = re.sub(r"^.*palette" + f"{os.path.sep}", "", image_path)
        # print(rel_dir)

        palette[rel_dir] = {
                "r": red, "g": green, "b": blue,
                # "hue": hue, "sat": sat, "light": light,
        }
    print(f"Palette size: {len(palette.keys())}")
    return palette


def get_palette_list(all_palettes, selection=None):
    if selection:
        assert isinstance(selection, (list, tuple))
        selection = {key: dg for key, dg in all_palettes.items() for text in selection if text in key}

    if selection:
        return list(selection.values())
    else:
        # print(f"KEYS: {all_palettes.keys()}")
        # rnd_key = random.choice(list(all_palettes.keys()))
        # print(f"Random key: {rnd_key}")
        return [random.choice(list(all_palettes.values()))]


def start_job(src_path, output_path, power, output_size=None, palette=None):
    """"""
    t0 = time.time()

    OUTPUT_GIF_MAX_SIZE = output_size
    image = cv2.imread(src_path)
    height, width, ch = image.shape
    if not output_size or height < OUTPUT_GIF_MAX_SIZE and width < OUTPUT_GIF_MAX_SIZE:
        OUTPUT_GIF_MAX_SIZE = max(height, width)

    PROC_POWER = power
    PIXEL_RATIO = round(OUTPUT_GIF_MAX_SIZE / PROC_POWER)
    PIXEL_RATIO = 1 if PIXEL_RATIO < 1 else PIXEL_RATIO
    MAX_PIC_SIZE = PROC_POWER * PIXEL_RATIO
    MAX_PIC_SIZE = OUTPUT_GIF_MAX_SIZE if MAX_PIC_SIZE > OUTPUT_GIF_MAX_SIZE else MAX_PIC_SIZE

    PAL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "palette"))
    PAL_PATH = os.path.join(PAL_DIR, "palettes.pickle")
    pixels = (height // PIXEL_RATIO) * (width // PIXEL_RATIO)

    config = {"pixelratio": PIXEL_RATIO, "power": PROC_POWER,
              "outputsize": OUTPUT_GIF_MAX_SIZE, "maxpicsize": MAX_PIC_SIZE,
              "outputpath": output_path,
              "paldir": PAL_DIR, "palpath": PAL_PATH}
    print(f"Input height: {height}, width: {width}")
    print(f"Processing power: {PROC_POWER}")
    print(f"Pixel ratio: {PIXEL_RATIO}")
    print(f"Pixels to find: {pixels:,}")
    print(f"Processing image size: {MAX_PIC_SIZE}")
    print(f"Output max size: {OUTPUT_GIF_MAX_SIZE}")
    # print(f"paldir: {PAL_DIR}")
    # print(f"palpat: {PAL_PATH}")

    make_mozaic_and_gif(src_path, selection=palette, config=config)
    duration = int(time.time() - t0)

    logger.info(f"Task completed: {os.path.basename(src_path)} in {duration:>1.0f}s")


"Consts"
SAVE_EXT = "jpg"
AVATAR_SIZE = 50
FILL_BORDER_WHEN_CROP = True

if __name__ == "__main__":
    srcpath = os.path.join("..", "incoming", "1606699002-d57e8f63456428ef1e8e5576bc3fe79d88a59f9c.png")
    outpath = os.path.join("..", 'static', "outputgifs", "1606699002-d57e8f63456428ef1e8e5576bc3fe79d88a59f9c.gif")
    # DistanceGraph.__module__ = "backend.create_gif"
    # recreate_all_palettes()
    start_job(srcpath, outpath, 300, 600)
    # pal = load_palette()
    # print(pal)
