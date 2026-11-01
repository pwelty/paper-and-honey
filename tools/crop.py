"""Crop and enlarge a region of a screenshot (stdlib only).
  python3 tools/crop.py IN.png OUT.png x0 y0 x1 y1 [scale=3]
"""
import sys, zlib, struct

def read_png(p):
    data = open(p, "rb").read(); i = 8; idat = b""
    while i < len(data):
        ln = struct.unpack(">I", data[i:i+4])[0]; t = data[i+4:i+8]; c = data[i+8:i+8+ln]; i += 12 + ln
        if t == b"IHDR": w, h, _, ct = struct.unpack(">IIBB", c[:10])
        elif t == b"IDAT": idat += c
    raw = zlib.decompress(idat); bpp = {2: 3, 6: 4}[ct]; stride = w * bpp; rows = []; prev = bytearray(stride); k = 0
    for _ in range(h):
        f = raw[k]; k += 1; line = bytearray(raw[k:k+stride]); k += stride
        for x in range(stride):
            a = line[x-bpp] if x >= bpp else 0; b = prev[x]; c = prev[x-bpp] if x >= bpp else 0
            if f == 1: line[x] = (line[x] + a) & 255
            elif f == 2: line[x] = (line[x] + b) & 255
            elif f == 3: line[x] = (line[x] + (a + b) // 2) & 255
            elif f == 4:
                p = a + b - c; pa, pb, pc = abs(p-a), abs(p-b), abs(p-c)
                line[x] = (line[x] + (a if pa <= pb and pa <= pc else b if pb <= pc else c)) & 255
        rows.append(bytes(line)); prev = line
    return w, h, bpp, rows

def write_png(p, w, h, bpp, rows):
    raw = b"".join(b"\x00" + r for r in rows)
    chunk = lambda t, c: struct.pack(">I", len(c)) + t + c + struct.pack(">I", zlib.crc32(t + c) & 0xffffffff)
    open(p, "wb").write(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, {3: 2, 4: 6}[bpp], 0, 0, 0))
                        + chunk(b"IDAT", zlib.compress(raw)) + chunk(b"IEND", b""))

if __name__ == "__main__":
    src, dst, x0, y0, x1, y1 = sys.argv[1], sys.argv[2], *map(int, sys.argv[3:7])
    s = int(sys.argv[7]) if len(sys.argv) > 7 else 3
    w, h, bpp, rows = read_png(src); out = []
    for y in range(y0, y1):
        r = rows[y][x0*bpp:x1*bpp]
        out += [b"".join(r[i:i+bpp] * s for i in range(0, len(r), bpp))] * s
    write_png(dst, (x1-x0)*s, (y1-y0)*s, bpp, out)
