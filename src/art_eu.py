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

# ---------------- EUROPE: ETOPO1 (10') for colour bands + Natural Earth shaded relief (2') for texture ----------------
NAVY = np.array([.03, .07, .16])
P = g['proj']['europe']; W, H = P['w'], P['h']
ys, xs = np.mgrid[0:H*SC, 0:W*SC].astype(np.float64)
lon, lat = inv(P, (xs+.5)/SC, (ys+.5)/SC)
f = h5py.File('earth-topography-10arcmin.nc'); T = f['topography'][:].astype(np.float32)
Z = map_coordinates(T, [(lat + 90)*6, (lon + 180)*6], order=3, mode='wrap')
sr = np.asarray(Image.open('dl/mpl_toolkits/basemap_data/shadedrelief.jpg').convert('L')).astype(np.float32)/255
SH, SW = sr.shape
R = map_coordinates(sr, [(90 - lat)/180*SH - .5, (lon + 180)/360*SW - .5], order=1, mode='wrap')
Rd = np.clip(0.5 + (R - gaussian_filter(R, 14*SC))*3.2, 0, 1)   # relief detail (true terrain shading)
EU = set('276 040 756 528 056 442 208 578 752 352 826 372 438 234 833 831 832 250 724 620 380 642 498 020 492 674 336 616 203 703 705 191 070 688 499 807 100 804 112 643 440 428 246 233 348 248 300 196 008 470 792 268 051 031'.split())
mask = mask_from_paths([c['d'] for c in g['europe']['countries'] if c.get('id') in EU or c['name'] in ('Kosovo','N. Cyprus')] + [g['europe']['austria']], W, H)
Zl = np.maximum(Z, 0)
mppE = 6371000/(P['scale']*SC)
hsZ = hillshade(gaussian_filter(Zl, 1.5), mppE, 315, 35, 14)
base = ramp(Zl, [(0, '#0d4c66'), (120, '#137e9c'), (300, '#33b4c4'), (550, '#e7ac48'), (900, '#ef8538'),
                 (1400, '#e3563e'), (2000, '#dba59c'), (2800, '#f4f6f7')])
shade = 0.16 + 1.0*(0.55*Rd + 0.45*hsZ)**1.1
spec = np.clip(Rd, 0, 1)**7 * 0.5
land = np.clip(base*shade[..., None] + spec[..., None]*np.array([1, .92, .78]), 0, 1)
land = land*0.9 + NAVY*np.clip(1-shade, 0, 1)[..., None]*0.55
finish(land, mask, [1.0, .64, .28], 'europe', 0.75)
