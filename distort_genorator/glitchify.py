import random
import os

output_path = '/mnt/data/VQA/video/distorted/test'
buffer_size = 100
header_size = 200

def glitchify(input_path, intensity, **_):
    with open(input_path, "rb") as fin:
        with open(output_path, "wb") as fout:
            # protect the header
            fout.write(fin.read(header_size))
            while True:
                in_byte = fin.read(buffer_size)
                if not in_byte:
                    break
                if (random.random() < intensity / 100):
                    out_byte = os.urandom(buffer_size)
                else:
                    out_byte = in_byte
                fout.write(out_byte)