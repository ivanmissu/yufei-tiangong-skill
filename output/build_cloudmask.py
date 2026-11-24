"""Cloud-sea mask v2: smooth analytic falloff, architecture fully protected."""
from PIL import Image, ImageDraw, ImageFilter
import numpy as np

W, H = 2560, 1440
im = Image.open('output/tiangong-2k.jpg').convert('RGB')

mask = Image.new('L', (W, H), 0)
d = ImageDraw.Draw(mask)

# soft cloud masses — kept below the distant mountain band and inside the colons
cloud_polys = [
    [(300, 560), (1130, 600), (1150, 1230), (300, 1250)],      # left cloud sea
    [(1430, 620), (2260, 580), (2270, 1250), (1440, 1230)],    # right cloud sea
    [(300, 430), (860, 470), (870, 700), (300, 690)],          # left bank behind gate
    [(1830, 440), (2270, 430), (2270, 760), (1840, 730)],      # right bank behind gate
    [(980, 1080), (1560, 1070), (1580, 1290), (970, 1290)],    # spill at stair foot
]
for p in cloud_polys:
    d.polygon(p, fill=255)

# architecture / ground: never displace
exclude_polys = [
    [(600, 0), (2020, 0), (2015, 320), (1830, 355), (1820, 760),
     (800, 760), (790, 350), (605, 320)],                       # cinnabar gate
    [(1195, 650), (1365, 650), (1490, 1250), (1070, 1250)],      # stairway
    [(0, 0), (265, 0), (270, 900), (320, 1180), (0, 1220)],      # left column
    [(2295, 0), (2560, 0), (2560, 1200), (2255, 1170), (2285, 900)],
    [(0, 1225), (2560, 1185), (2560, 1440), (0, 1440)],          # platform
]
for p in exclude_polys:
    d.polygon(p, fill=0)

m = np.asarray(mask.filter(ImageFilter.GaussianBlur(70))).astype(np.float32) / 255.0

y = np.arange(H, dtype=np.float32)[:, None]
x = np.arange(W, dtype=np.float32)[None, :]

def smoothstep(e0, e1, v):
    t = np.clip((v - e0) / (e1 - e0), 0, 1)
    return t * t * (3 - 2 * t)

# fade in below the distant mountain band, fade out above the foreground platform
m *= smoothstep(330, 560, y) * (1.0 - smoothstep(1080, 1235, y))
# keep clear of the far floating temples (upper corners)
m *= smoothstep(250, 520, x) * (1.0 - smoothstep(2040, 2310, x))
# slight preference for the lower cloud shelf, where the sea is thickest
m *= 0.55 + 0.45 * smoothstep(430, 900, y)
m = np.clip(m * 1.5, 0, 1) ** 1.1

ov = np.asarray(im).astype(np.float32)
tint = np.zeros_like(ov); tint[..., 0] = 255; tint[..., 1] = 40
ov = ov * (1 - m[..., None] * 0.55) + tint * (m[..., None] * 0.55)
Image.fromarray(ov.astype(np.uint8)).resize((1280, 720), Image.LANCZOS).save(
    'output/_mask_check.jpg', quality=92)

np.save('output/cloudmask.npy', m.astype(np.float16))
print('coverage %.3f  max %.2f' % (m.mean(), m.max()))
