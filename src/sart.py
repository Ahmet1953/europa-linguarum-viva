# Salzburg relief from the 20 m DGM (EPSG:31287), rendered in the Salzburg view's LAEA projection
import json, re, numpy as np, tifffile
from PIL import Image, ImageDraw
from scipy.ndimage import gaussian_filter, map_coordinates
from pyproj import Transformer
import sys
CODE = sys.argv[1]; TIF = sys.argv[2]
g = json.load(open('geo.json')); P = g['proj']['st'+CODE]; S = g['states'][CODE]; W, H = P['w'], P['h']; SC = 2
def fwd(lon, lat):
    l0, p0 = np.radians(-P['rotate'][0]), np.radians(-P['rotate'][1]); l, p = np.radians(lon), np.radians(lat)
    cosc = np.sin(p0)*np.sin(p) + np.cos(p0)*np.cos(p)*np.cos(l-l0); k = np.sqrt(2/(1+cosc))
    x = k*np.cos(p)*np.sin(l-l0); y = k*(np.cos(p0)*np.sin(p) - np.sin(p0)*np.cos(p)*np.cos(l-l0))
    return P['translate'][0] + P['scale']*x, P['translate'][1] - P['scale']*y
def inv(xs, ys):
    l0, p0 = np.radians(-P['rotate'][0]), np.radians(-P['rotate'][1])
    x = (xs - P['translate'][0])/P['scale']; y = (P['translate'][1] - ys)/P['scale']
    r = np.hypot(x, y) + 1e-12; c = 2*np.arcsin(np.clip(r/2, 0, 1))
    lat = np.arcsin(np.cos(c)*np.sin(p0) + y*np.sin(c)*np.cos(p0)/r)
    lon = l0 + np.arctan2(x*np.sin(c), r*np.cos(p0)*np.cos(c) - y*np.sin(p0)*np.sin(c))
    return np.degrees(lon), np.degrees(lat)
for ll, xy in P['test']:
    fx, fy = fwd(*ll); assert abs(fx-xy[0]) < .05 and abs(fy-xy[1]) < .05
DEMS = {'1':'bgl/burgenland','2':'ktn/kaernten','3':'noe/niederoesterreich','4':'ooe/oberoesterreich','5':'sbg/salzburg',
        '6':'stm/steiermark','7':'tir/tirol','8':'vbg/vorarlberg','9':'wien/wien'}
tr = Transformer.from_crs('EPSG:4326', 'EPSG:31287', always_xy=True)
ys, xs = np.mgrid[0:H*SC, 0:W*SC].astype(np.float64)
lon, lat = inv((xs+.5)/SC, (ys+.5)/SC)
ex, ey = tr.transform(lon, lat)
mpp = 6371000/(P['scale']*SC)            # metres per output pixel
def sample(path):
    """sample one state's DGM onto the output grid; NaN where it has no data"""
    t = tifffile.TiffFile(path).pages[0]
    X0, Y0 = t.tags['ModelTiepointTag'].value[3:5]; R = float(t.tags['ModelPixelScaleTag'].value[0])
    col = (ex - X0)/R - .5; row = (Y0 - ey)/R - .5
    a = t.asarray(); hh, ww = a.shape
    r0, r1 = int(max(0, np.floor(row.min())-4)), int(min(hh, np.ceil(row.max())+5))
    c0, c1 = int(max(0, np.floor(col.min())-4)), int(min(ww, np.ceil(col.max())+5))
    if r0 >= r1 or c0 >= c1: return None, None
    sub = a[r0:r1, c0:c1].astype(np.float32); nod = sub <= -32000
    if nod.all(): return None, None
    sub[nod] = np.nan
    filled = np.where(nod, np.nanmean(sub), sub)
    pre = gaussian_filter(filled, max(0.5, mpp/R/2.2))
    z = map_coordinates(pre, [row-r0, col-c0], order=1, mode='nearest')
    nv = map_coordinates(nod.astype(np.float32), [row-r0, col-c0], order=1, mode='constant', cval=1.0)
    z[nv > 0.5] = np.nan
    return z, (sub, X0 + c0*R, Y0 - r0*R, R)
Z, own = sample(DEMS[CODE] + '_dhm_20m_int16_2kmpay.tif')
dem, X0, Y0, RES = own
for c, pth in DEMS.items():
    if c == CODE or np.isfinite(Z).all(): continue
    z2, _ = sample(pth + '_dhm_20m_int16_2kmpay.tif')
    if z2 is not None: Z = np.where(np.isfinite(Z), Z, z2)
have = np.isfinite(Z)
Z = np.where(have, Z, np.nanmean(Z))
def poly_mask(d):
    """even-odd fill of an SVG path (holes stay open)"""
    m = np.zeros((H*SC, W*SC), bool)
    for ring in re.findall(r'M([^MZ]+)Z?', d or ''):
        pts = [tuple(float(v)*SC for v in xy.split(',')) for xy in ring.split('L') if ',' in xy]
        if len(pts) > 2:
            im = Image.new('1', (W*SC, H*SC), 0); ImageDraw.Draw(im).polygon(pts, fill=1); m ^= np.asarray(im)
    return m.astype(np.float32)
mask = poly_mask(S['outline'])
mAT = poly_mask(S['atFill'])
mNB = np.clip(mAT - mask, 0, 1) * have
mask = mask * have
def ramp(z, stops):
    zs = np.array([s[0] for s in stops], float); cols = np.array([[int(s[1][i:i+2], 16)/255 for i in (1,3,5)] for s in stops])
    return np.stack([np.interp(z, zs, cols[:, k]) for k in range(3)], -1)
def hillshade(z, az, alt, exag):
    gy, gx = np.gradient(z*exag, mpp); slope = np.arctan(np.hypot(gx, gy)); aspect = np.arctan2(-gx, gy)
    a, b = np.radians(az), np.radians(alt)
    return np.clip(np.sin(b)*np.cos(slope) + np.cos(b)*np.sin(slope)*np.cos(a - aspect), 0, 1)
zmin, zmax = float(np.nanpercentile(dem, 0.5)), float(np.nanmax(dem))
zp = float(np.nanpercentile(dem, 97))
STRETCH = float(np.clip(1500.0/(zp - zmin), 1.0, 2.4))   # low-relief states: spread colours over their own height range
EX = 1.7*STRETCH**0.6
print('stretch', round(STRETCH, 2))
hs = 0.6*hillshade(Z, 315, 33, EX) + 0.25*hillshade(Z, 250, 42, EX) + 0.15*hillshade(Z, 20, 55, EX)
lr = Z - gaussian_filter(Z, 10*SC)
Zc = Z if STRETCH == 1.0 else 400 + (Z - zmin)*STRETCH
base = ramp(Zc, [(400, '#0b4a5e'), (550, '#127c9b'), (800, '#2fb3c3'), (1100, '#e8b04a'), (1500, '#f08a3a'),
                (2000, '#e5573f'), (2500, '#d9a39b'), (3000, '#eef3f6'), (3700, '#ffffff')])
shade = 0.16 + 1.05*hs**1.15
ao = 1 + 0.4*np.tanh(lr*STRETCH/220)
spec = np.clip(hs, 0, 1)**9 * 0.55
NAVY = np.array([.03, .07, .16])
land = np.clip(base*shade[..., None]*ao[..., None] + spec[..., None]*np.array([1, .93, .8]), 0, 1)
land = land*0.9 + NAVY*np.clip(1-shade, 0, 1)[..., None]*0.55
bright = np.clip(land - 0.62, 0, 1)*mask[..., None]
land = np.clip(land + np.stack([gaussian_filter(bright[..., k], 9*SC) for k in range(3)], -1)*0.8, 0, 1)
rim = np.clip(mask - gaussian_filter(mask, 1.6*SC), 0, 1)*0.9
land = np.clip(land + rim[..., None]*np.array([1, .86, .62]), 0, 1)
# neighbours: same terrain, desaturated and dimmed, dissolving toward the frame edge
grey = land.mean(-1, keepdims=True)
nbc = (grey*0.6 + land*0.4)*0.5 + NAVY*0.35
yy, xx = np.mgrid[0:H*SC, 0:W*SC]
edge = np.minimum.reduce([xx, yy, W*SC-1-xx, H*SC-1-yy]).astype(np.float32)
fade = np.clip(edge/(110*SC), 0, 1)**1.6
aNB = mNB*0.0*fade   # neighbours are no longer painted: the state floats, borders are shown as stubs
halo = np.clip(gaussian_filter(mask, 2.5*SC)*0.9 + gaussian_filter(mask, 12*SC)*0.35, 0, 1)*(1-mask)
gc = np.array([1.0, .62, .25])
# layer 1: neighbours; layer 2: amber glow; layer 3: the state itself
rgb = nbc*aNB[..., None]; al = aNB.copy()
ga = halo*0.6
rgb = gc*ga[..., None] + rgb*(1-ga[..., None]); al = ga + al*(1-ga)
rgb = land*mask[..., None] + rgb*(1-mask[..., None]); al = mask + al*(1-mask)
out = rgb/np.maximum(al, 1e-4)[..., None]; a = al
Image.fromarray(np.dstack([np.clip(out, 0, 1)*255, a*255]).astype(np.uint8), 'RGBA').save(f'art_st{CODE}.webp', quality=86, method=6)
# peaks: position of the DGM maximum near the official summit, height read from the DGM
def dgm_peak(lo, la, rad=8):
    x, y = tr.transform(lo, la); c, r = int((x-X0)/RES), int((Y0-y)/RES)
    w = dem[r-rad:r+rad+1, c-rad:c+rad+1]; i = np.nanargmax(w); rr, cc = divmod(i, w.shape[1])
    px, py = X0 + (c-rad+cc+.5)*RES, Y0 - (r-rad+rr+.5)*RES
    lo2, la2 = Transformer.from_crs('EPSG:31287', 'EPSG:4326', always_xy=True).transform(px, py)
    sx, sy = fwd(lo2, la2); return round(float(sx), 1), round(float(sy), 1), int(round(float(np.nanmax(w))))
PEAKS = {'5': [('Großvenediger', 12.3464, 47.1094, 3657), ('Kitzsteinhorn', 12.6875, 47.1883, 3203), ('Hochkönig', 13.0628, 47.4203, 2941),
                ('Hoher Göll', 13.0667, 47.5939, 2522), ('Gaisberg', 13.1125, 47.8047, 1287)],
         '7': [('Großglockner', 12.6942, 47.0745, 3798), ('Wildspitze', 10.8673, 46.8853, 3768), ('Weißkugel', 10.7272, 46.7983, 3738),
                ('Zugspitze', 10.9853, 47.4211, 2962), ('Hafelekarspitze', 11.3842, 47.3125, 2334)],
         '1': [('Geschriebenstein', 16.4339, 47.3539, 884)],
         '6': [('Hoher Dachstein', 13.6058, 47.4753, 2995), ('Hochgolling', 13.7614, 47.2672, 2862), ('Hochschwab', 15.1442, 47.6178, 2277), ('Schöckl', 15.4683, 47.1983, 1445)],
         '8': [('Piz Buin', 10.1189, 46.8442, 3312), ('Schesaplana', 9.7083, 47.0533, 2965)],
         '9': [('Hermannskogel', 16.2939, 48.2706, 542, 8, 'left'), ('Kahlenberg', 16.3333, 48.2747, 484)],
         '4': [('Hoher Dachstein', 13.6058, 47.4753, 2995), ('Großer Priel', 14.0631, 47.7175, 2515), ('Plöckenstein', 13.8606, 48.7706, 1379)],
         '3': [('Schneeberg', 15.8070, 47.7672, 2076, 30), ('Ötscher', 15.2017, 47.8625, 1893), ('Jauerling', 15.3378, 48.3347, 960)],
         '2': [('Großglockner', 12.6942, 47.0745, 3798), ('Hochalmspitze', 13.3203, 47.0156, 3360), ('Dobratsch', 13.6697, 46.6036, 2166)]}[CODE]
peaks = []
for pk in PEAKS:
    n, lo, la, off = pk[:4]
    sx, sy, z = dgm_peak(lo, la, pk[4] if len(pk) > 4 else 8); peaks.append({'name': n, 'x': sx, 'y': sy, 'dgm': z, 'official': off, 'left': len(pk) > 5 and pk[5] == 'left'}); print(n, z, off)
json.dump(peaks, open(f'peaks_st{CODE}.json', 'w'))
print('mpp', round(mpp, 1), 'size', Image.open(f'art_st{CODE}.webp').size)
