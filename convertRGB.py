def RGB_HEX(rgb=(255,255,255)):
    out = hex(int("0x%02x%02x%02x" % rgb,16))
    out = "0x%02x%02x%02x" % rgb
    return out
