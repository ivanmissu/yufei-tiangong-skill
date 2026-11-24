"""
Tiangong i2v renderer v2 — locked architecture, layered churning cloud sea.

Implements references/video-motion.md:
  * source still = fixed first frame and composition contract
  * ONE camera motion only: frame fully locked (0% camera travel)
  * architecture / columns / stairway / platform: pixel-identical, never displaced
  * cloud sea: slow layered currents with fractal churn; cloud spill always downward
  * single right-hand light: gentle ray breathing, no flicker, no colour shift
  * no new characters, birds, particles or architecture
  * displacement is scaled by the cloud mask itself, so nothing bleeds into structure
"""
import argparse, os, subprocess, time
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

W, H = 2560, 1440
SRC = 'output/tiangong-2k.jpg'
MASK = 'output/cloudmask.npy'


def smoothstep(e0, e1, v):
    t = np.clip((v - e0) / (e1 - e0), 0.0, 1.0)
    return t * t * (3 - 2 * t)


def build_protection():
    """Static zone around all architecture, dilated by the maximum displacement."""
    m = Image.new('L', (W, H), 255)
    d = ImageDraw.Draw(m)
    for p in [
        [(600, 0), (2020, 0), (2015, 320), (1830, 355), (1820, 760),
         (800, 760), (790, 350), (605, 320)],
        [(1195, 650), (1365, 650), (1490, 1250), (1070, 1250)],
        [(0, 0), (265, 0), (270, 900), (320, 1180), (0, 1220)],
        [(2295, 0), (2560, 0), (2560, 1200), (2255, 1170), (2285, 900)],
        [(0, 1225), (2560, 1185), (2560, 1440), (0, 1440)],
    ]:
        d.polygon(p, fill=0)
    # architecture = 0, cloud = 255. Dilate the architecture by ~MAX_DISP px so a
    # cloud sample can never reach across into a structural edge and ghost it.
    small = m.resize((W // 8, H // 8), Image.LANCZOS)
    # invert -> dilate the STRUCTURE (0s) -> invert back
    from PIL import ImageOps
    inv = ImageOps.invert(small)
    inv = inv.filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.MaxFilter(9))
    small = ImageOps.invert(inv)
    m = small.resize((W, H), Image.BILINEAR).filter(ImageFilter.GaussianBlur(26))
    return np.asarray(m).astype(np.float32) / 255.0


def bilinear(img, x, y):
    x = np.clip(x, 0, W - 1.001); y = np.clip(y, 0, H - 1.001)
    x0 = x.astype(np.int32); y0 = y.astype(np.int32)
    x1 = np.minimum(x0 + 1, W - 1); y1 = np.minimum(y0 + 1, H - 1)
    fx = (x - x0)[..., None]; fy = (y - y0)[..., None]
    f = img.reshape(-1, 3)
    i00 = y0 * W + x0; i10 = y0 * W + x1; i01 = y1 * W + x0; i11 = y1 * W + x1
    c00 = f[i00]; c10 = f[i10]; c01 = f[i01]; c11 = f[i11]
    top = c00 + (c10 - c00) * fx
    bot = c01 + (c11 - c01) * fx
    return top + (bot - top) * fy


def flow_field(t, xs, ys, dur):
    """Displacement in px on a coarse grid. One slow cycle across the clip."""
    ph = 2 * np.pi * t
    near = smoothstep(430, 1200, ys)                # far cloud slow, near cloud faster
    w = 0.30 + 0.70 * near

    # 1. dominant current: one direction, linear in time, ~5% of frame width
    dx = 58.0 * t * w
    # 2. layered lateral shear (two wavelengths, opposite drift)
    dx = dx + 20.0 * w * np.sin(2 * np.pi * xs / 1750.0 + ph * 1.00)
    dx = dx + 11.0 * w * np.sin(2 * np.pi * (ys / 780.0 + xs / 2600.0) - ph * 0.80)
    # 3. rolling swell: vertical lobes, biased downward, never inverted
    dy = 16.0 * w * (0.70 + 0.30 * np.sin(2 * np.pi * xs / 900.0 + ph * 0.85)) * t
    dy = dy + 9.0 * w * (0.5 - 0.5 * np.cos(2 * np.pi * (xs / 620.0 + ys / 1400.0) + ph * 1.2))
    # 4. fractal churn: small-scale lobe deformation that sums to zero over time
    dx = dx + 8.0 * np.sin(2 * np.pi * (xs / 340.0 + ys / 410.0) + ph * 1.6)
    dy = dy + 6.0 * np.sin(2 * np.pi * (xs / 290.0 - ys / 380.0) - ph * 1.3)
    # 5. cloud spill at the stair foot: strictly downward acceleration
    spill = smoothstep(1090, 1210, ys) * (1.0 - smoothstep(1290, 1400, ys))
    dy = dy + 26.0 * spill * t ** 0.85
    return dx, dy


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--start', type=int, default=0)
    ap.add_argument('--end', type=int, default=720)
    ap.add_argument('--fps', type=int, default=30)
    ap.add_argument('--dur', type=float, default=24.0)
    ap.add_argument('--out', default='output/tiangong-2k.mp4')
    ap.add_argument('--crf', type=int, default=17)
    args = ap.parse_args()

    N = int(round(args.fps * args.dur))
    src = Image.open(SRC).convert('RGB')
    base = np.asarray(src).astype(np.float32)
    soft = np.asarray(src.filter(ImageFilter.GaussianBlur(2.0))).astype(np.float32)

    raw_mask = np.load(MASK).astype(np.float32)
    mask = smoothstep(0.28, 0.80, raw_mask) * build_protection()
    mask3 = mask[..., None]

    Y, X = np.mgrid[0:H, 0:W].astype(np.float32)
    raymask = (smoothstep(1250, 2150, X) * smoothstep(900, 260, Y)
               * (1.0 - smoothstep(0.15, 0.62, raw_mask)))[..., None]
    nxp = (X - W / 2) / (W / 2); nyp = (Y - H / 2) / (H / 2)
    vig = (1.0 - 0.15 * np.clip(nxp ** 2 * 0.75 + nyp ** 2, 0, 1) ** 1.35)[..., None]

    cw, ch = W // 2, H // 2
    cxs = (np.arange(cw, dtype=np.float32) * 2)[None, :].repeat(ch, 0)
    cys = (np.arange(ch, dtype=np.float32) * 2)[:, None].repeat(cw, 1)
    gx = X; gy = Y

    cmd = [os.environ.get('FFMPEG', 'ffmpeg'), '-y', '-hide_banner', '-loglevel', 'error',
           '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(args.fps),
           '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-crf', str(args.crf),
           '-pix_fmt', 'yuv420p', '-profile:v', 'high', '-level', '5.1',
           '-x264-params', 'keyint=48:min-keyint=24:scenecut=0',
           '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709',
           '-movflags', '+faststart', args.out]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)

    rng = np.random.default_rng(20261124)
    grain = rng.normal(0, 0.75, (H, W, 1)).astype(np.float32)
    t0 = time.time()
    for i in range(args.start, args.end):
        t = i / float(max(N - 1, 1))
        cx, cy = flow_field(t, cxs, cys, args.dur)
        env = min(1.0, t / 0.04)          # frame 0 == source still, then ease in
        dx = np.asarray(Image.fromarray(cx).resize((W, H), Image.BILINEAR)) * mask * env
        dy = np.asarray(Image.fromarray(cy).resize((W, H), Image.BILINEAR)) * mask * env

        warped = bilinear(soft, gx + dx, gy + dy)
        frame = warped * mask3 + base * (1.0 - mask3)

        amp = 0.022 * np.sin(2 * np.pi * t)
        frame = frame + raymask * (frame * amp)
        frame = frame + grain
        proc.stdin.write(np.clip(frame, 0, 255).astype(np.uint8).tobytes())

        if (i - args.start) % 30 == 0:
            el = time.time() - t0; done = i - args.start + 1
            print(f'frame {i}/{args.end - 1}  {el/done:.2f}s/frame  eta {(args.end-i)*el/done/60:.1f}min',
                  flush=True)

    proc.stdin.close(); proc.wait()
    print('rendered %d frames in %.1fs' % (args.end - args.start, time.time() - t0))


if __name__ == '__main__':
    main()
