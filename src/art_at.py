# Cinematic relief artwork from REAL elevation, rendered in exactly the projection of the SVG/Canvas paths.
import json, math, re, numpy as np, h5py
from PIL import Image, ImageDraw
from scipy.ndimage import gaussian_filter, map_coordinates
Image.MAX_IMAGE_PIXELS = None
g = json.load(open('geo.json'))
SC = 2  # output pixels per map unit

def inv(P, xs, ys):
    l0, p0 = np.radians(-P['rotate'][0]), np.radians(-P['rotate'][1])
    x = (xs - P['translate'][0]) / P['scale']; y = (P['translate'][1] - ys) / P['scale']
    r = np.hypot(x, y) + 1e-12; c = 2*np.arcsin(np.clip(r/2, 0, 1))
    lat = np.arcsin(np.cos(c)*np.sin(p0) + y*np.sin(c)*np.cos(p0)/r)
    lon = l0 + np.arctan2(x*np.sin(c), r*np.cos(p0)*np.cos(c) - y*np.sin(p0)*np.sin(c))
    return np.degrees(lon), np.degrees(lat)

def mask_from_paths(paths, w, h):
    im = Image.new('L', (w*SC, h*SC), 0); d = ImageDraw.Draw(im)
    for p in paths:
        for ring in re.findall(r'M([^MZ]+)Z?', p):
            pts = [tuple(float(v)*SC for v in xy.split(',')) for xy in re.split(r'L', ring) if ',' in xy]
            if len(pts) > 2: d.polygon(pts, fill=255)
    return np.asarray(im).astype(np.float32)/255

def ramp(z, stops):
    zs = np.array([s[0] for s in stops], float)
    cols = np.array([[int(s[1][i:i+2], 16)/255 for i in (1, 3, 5)] for s in stops])
    return np.stack([np.interp(z, zs, cols[:, k]) for k in range(3)], -1)

def hillshade(z, mpp, az, alt, exag):
    gy, gx = np.gradient(z*exag, mpp)
    slope = np.arctan(np.hypot(gx, gy)); aspect = np.arctan2(-gx, gy)
    a, b = np.radians(az), np.radians(alt)
    return np.clip(np.sin(b)*np.cos(slope) + np.cos(b)*np.sin(slope)*np.cos(a - aspect), 0, 1)

def finish(land_rgb, mask, glow_col, name, edge_boost):
    # bloom on bright parts
    bright = np.clip(land_rgb - 0.62, 0, 1) * mask[..., None]
    bloom = np.stack([gaussian_filter(bright[..., k], 10*SC) for k in range(3)], -1)
    rgb = np.clip(land_rgb + bloom*0.9, 0, 1)
    # luminous rim just inside the coast / border
    rim = np.clip(mask - gaussian_filter(mask, 1.6*SC), 0, 1) * edge_boost
    rgb = np.clip(rgb + rim[..., None]*np.array([1.0, .86, .62]), 0, 1)
    # outer glow halo (amber)
    halo = np.clip(gaussian_filter(mask, 2.5*SC)*0.9 + gaussian_filter(mask, 12*SC)*0.35, 0, 1)
    a = np.maximum(mask, halo*0.6)
    gc = np.array(glow_col)
    out = (rgb*mask[..., None] + gc*(1-mask[..., None])*halo[..., None]) / np.maximum(a, 1e-4)[..., None]
    img = Image.fromarray(np.dstack([np.clip(out, 0, 1)*255, a*255]).astype(np.uint8), 'RGBA')
    img.save(f'art_{name}.webp', quality=86, method=6)
    print(name, img.size)

# ---------------- AUSTRIA: DGM Österreich (via terrain-RGB preview), validated against known heights ----------------
P = g['proj']['austria']; W, H = P['w'], P['h']
ys, xs = np.mgrid[0:H*SC, 0:W*SC].astype(np.float64)
lon, lat = inv(P, (xs+.5)/SC, (ys+.5)/SC)
a = np.asarray(Image.open('sp/images/DHM-Austria-RGB.png')).astype(np.int64)
dem = (-10000 + (a[..., 0]*65536 + a[..., 1]*256 + a[..., 2])*0.1).astype(np.float32)
merc = lambda lo, la: (lo*20037508.34/180, np.log(np.tan(np.pi/4 + np.radians(la)/2))*6378137)
x0, _ = merc(9.5307, 0); x1, _ = merc(17.1608, 0); _, yN = merc(0, 49.0205); _, yS = merc(0, 46.3722)
mx, my = merc(lon, lat)
col = 34 + (mx - x0)/(x1 - x0)*(2758 - 34) - .5
row = 42 + (yN - my)/(yN - yS)*(1452 - 42) - .5
Z = map_coordinates(dem, [row, col], order=3, mode='nearest')
Z = gaussian_filter(Z, 0.7)
mask = mask_from_paths([g['austria']['outline']], W, H)
Z = np.where(mask > 0, np.maximum(Z, 110), 110)
mpp = 6371000/(P['scale']*SC)
hs = 0.62*hillshade(Z, mpp, 315, 32, 2.6) + 0.23*hillshade(Z, mpp, 255, 40, 2.6) + 0.15*hillshade(Z, mpp, 15, 50, 2.6)
lr = Z - gaussian_filter(Z, 8*SC)
base = ramp(Z, [(100, '#0b4a5e'), (250, '#11799a'), (450, '#2fb5c4'), (700, '#e8b04a'), (1100, '#f08a3a'),
                (1600, '#e5573f'), (2200, '#d9a39b'), (2900, '#eef3f6'), (3800, '#ffffff')])
shade = 0.18 + 1.05*hs**1.15
ao = 1 + 0.45*np.tanh(lr/260)
spec = np.clip(hs, 0, 1)**9 * 0.55
land = np.clip(base*shade[..., None]*ao[..., None] + spec[..., None]*np.array([1, .93, .8]), 0, 1)
NAVY = np.array([.03, .07, .16])
land = land*0.9 + NAVY*np.clip(1-shade, 0, 1)[..., None]*0.55
finish(land, mask, [1.0, .62, .25], 'austria', 0.9)

