import os
import struct
import numpy as np
from PIL import Image


def read_codebook(data):
    # data: bytes of codebook.bin -> list of centroids (side x side uint8 arrays)
    count, side = struct.unpack("<HB", data[:3])
    size = side * side
    codebook = []
    pos = 3
    for _ in range(count):
        centroid = np.frombuffer(data[pos:pos + size], dtype=np.uint8).reshape(side, side)
        codebook.append(centroid)
        pos += size
    return codebook


def read_compressed(data):
    # data: bytes of compressed.bin -> header info + list of indices
    header_size = struct.calcsize("<HHHHBB")
    ow, oh, pw, ph, bits_per_index, mode_len = struct.unpack("<HHHHBB", data[:header_size])
    pos = header_size
    old_mode = data[pos:pos + mode_len].decode("ascii")
    pos += mode_len
    stream = data[pos:]
    return (ow, oh), (pw, ph), bits_per_index, old_mode, stream


def decode_indices(stream, bits_per_index, num_blocks):
    # convert bytes back to bit string then cut it into indices (padding zeros at the end are ignored)
    bits = "".join(format(byte, "08b") for byte in stream)
    indices = []
    for i in range(num_blocks):
        chunk = bits[i * bits_per_index:(i + 1) * bits_per_index]
        indices.append(int(chunk, 2))
    return indices


def reconstruct_image(indices, codebook, padded_size):
    pw, ph = padded_size
    side = codebook[0].shape[0]
    image_array = np.zeros((ph, pw), dtype=np.uint8)
    blocks_per_row = pw // side
    for k, index in enumerate(indices):
        row = (k // blocks_per_row) * side  # blocks were stored left->right, top->bottom
        col = (k % blocks_per_row) * side
        image_array[row:row + side, col:col + side] = codebook[index]
    return image_array


def decompress(compressed_bytes, codebook_bytes):
    codebook = read_codebook(codebook_bytes)
    original_size, padded_size, bits_per_index, old_mode, stream = read_compressed(compressed_bytes)
    side = codebook[0].shape[0]
    num_blocks = (padded_size[0] // side) * (padded_size[1] // side)

    indices = decode_indices(stream, bits_per_index, num_blocks)
    image_array = reconstruct_image(indices, codebook, padded_size)

    image = Image.fromarray(image_array)
    image = image.crop((0, 0, original_size[0], original_size[1]))  # remove the padding
    if old_mode != image.mode:  # return to the original mode of the image
        image = image.convert(old_mode)
    return image


def calculate_compression_ratio(original_size, compressed_path, codebook_path):
    # original image is grayscale 8 bit => 1 byte per pixel
    original_bytes = original_size[0] * original_size[1]
    compressed_bytes = os.path.getsize(compressed_path) + os.path.getsize(codebook_path)
    return original_bytes / compressed_bytes
