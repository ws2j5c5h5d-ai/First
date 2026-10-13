"""Ersetzt die Roboterfigur in Digital-PDF (RGB) und Druck-PDF (FOGRA39 CMYK).
Nur der Bildinhalt (und seine SMask) wird ausgetauscht; Platzierung, Text,
Callouts und Layout bleiben byte-identisch im Content-Stream.
"""
import io
import sys
import zlib
import pikepdf
from PIL import Image, ImageCms

robot_png, digital_in, digital_out, print_in, print_out = sys.argv[1:6]
rgba = Image.open(robot_png).convert('RGBA')


def set_jpeg(stream, img, mode):
    buf = io.BytesIO()
    img.save(buf, 'JPEG', quality=95, subsampling=0, dpi=(300, 300))
    data = buf.getvalue()
    if mode == 'CMYK':
        # Adobe-JPEGs aus PIL sind invertiert gespeichert -> Decode-Array setzen
        stream.write(data, filter=pikepdf.Name.DCTDecode)
        stream.Decode = pikepdf.Array([1, 0, 1, 0, 1, 0, 1, 0])
    else:
        stream.write(data, filter=pikepdf.Name.DCTDecode)
        if '/Decode' in stream:
            del stream['/Decode']
    stream.Width, stream.Height = img.size
    stream.BitsPerComponent = 8


def set_mask(stream, alpha):
    stream.write(zlib.compress(alpha.tobytes(), 9), filter=pikepdf.Name.FlateDecode)
    for k in ('/Decode', '/DecodeParms'):
        if k in stream:
            del stream[k]
    stream.Width, stream.Height = alpha.size
    stream.ColorSpace = pikepdf.Name.DeviceGray
    stream.BitsPerComponent = 8


def find_robot(pdf):
    best = None
    for name, xo in pdf.pages[0].Resources.XObject.items():
        if xo.get('/Subtype') == '/Image' and '/SMask' in xo:
            if best is None or int(xo.Width) * int(xo.Height) > int(best.Width) * int(best.Height):
                best = xo
    return best

# --- Digital (RGB) ---------------------------------------------------------
pdf = pikepdf.open(digital_in)
im = find_robot(pdf)
img = rgba.resize((int(im.Width), int(im.Height)), Image.LANCZOS)
set_jpeg(im, img.convert('RGB'), 'RGB')
im.ColorSpace = pikepdf.Name.DeviceRGB
set_mask(im.SMask, img.getchannel('A'))
pdf.save(digital_out)
print('digital ok', im.Width, im.Height)

# --- Druck (FOGRA39 aus dem OutputIntent) --------------------------------
pdf = pikepdf.open(print_in)
icc = bytes(pdf.Root.OutputIntents[0].DestOutputProfile.read_bytes())
fogra = ImageCms.ImageCmsProfile(io.BytesIO(icc))
srgb = ImageCms.createProfile('sRGB')
xf = ImageCms.buildTransform(srgb, fogra, 'RGB', 'CMYK',
                             renderingIntent=ImageCms.Intent.RELATIVE_COLORIMETRIC,
                             flags=ImageCms.Flags.BLACKPOINTCOMPENSATION)
im = find_robot(pdf)
img = rgba.resize((int(im.Width), int(im.Height)), Image.LANCZOS)
cmyk = ImageCms.applyTransform(img.convert('RGB'), xf)
set_jpeg(im, cmyk, 'CMYK')
im.ColorSpace = pikepdf.Name.DeviceCMYK
set_mask(im.SMask, img.getchannel('A'))
pdf.save(print_out)
print('print ok', im.Width, im.Height)
