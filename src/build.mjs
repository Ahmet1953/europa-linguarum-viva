// Preprocess real geodata into SVG path strings.
// The same path string is used for drawing AND for click/tap hit-testing.
import fs from 'fs';
import * as topo from 'topojson-client';
import * as d3 from 'd3-geo';
import polylabel from 'polylabel';
function labelPt(proj, f){
  // pole of inaccessibility of the largest polygon, in projected coordinates
  const polys = f.geometry.type === 'Polygon' ? [f.geometry.coordinates] : f.geometry.coordinates;
  let best = null, bestA = -1;
  for (const poly of polys) { const pr = poly.map(r => r.map(c => proj(c)));
    const a = Math.abs(d3.geoArea({type:'Polygon', coordinates: poly}));
    if (a > bestA) { bestA = a; best = pr; } }
  const p = polylabel(best, 0.5); return [p[0], p[1]];
}

const world = JSON.parse(fs.readFileSync('node_modules/world-atlas/countries-50m.json'));
const atTopo = JSON.parse(fs.readFileSync('GeoJSON-TopoJSON-Austria/2021/simplified-99.5/laender_995_topo.json'));
const atKey = Object.keys(atTopo.objects)[0];
const states = topo.feature(atTopo, atTopo.objects[atKey]);
// Austria outline = dissolve of the official Statistik Austria states (identical geometry in both views)
const austriaOutline = topo.merge(atTopo, atTopo.objects[atKey].geometries);

const countries = topo.feature(world, world.objects.countries).features;

// ---------- Europe view ----------
const EW = 1000, EH = 860;
const eProj = d3.geoAzimuthalEqualArea().rotate([-10, -52]); // ETRS89-LAEA-like centre
const frame = { type: 'MultiPoint', coordinates: [[-11, 35], [31, 35], [-24, 64], [42, 66], [10, 71.5], [10, 34]] };
eProj.fitExtent([[10, 10], [EW - 10, EH - 10]], frame);
// Fit Europe into the gold ring: the smallest circle around the coasts that must stay fully visible
{
  const KEY = [[-24.5,65.5],[-22,63.4],[-16,66.6],[-13.5,65.1],[-9.5,38.7],[-9.0,37.0],[-5.6,36.0],[-9.3,43.0],[-10.5,51.6],[-8.2,58.3],
               [25.8,71.2],[31,70.3],[24,34.9],[26.3,35.2],[29,41],[37.6,55.7],[14.4,35.9]];
  const pts = KEY.map(c => eProj(c));
  // minimal enclosing circle (brute force over pairs and triples; small n)
  const inside = (c, r) => pts.every(p => Math.hypot(p[0]-c[0], p[1]-c[1]) <= r + 1e-6);
  let best = null;
  const tryC = (c, r) => { if ((!best || r < best.r) && inside(c, r)) best = {c, r}; };
  for (let i = 0; i < pts.length; i++) for (let j = i+1; j < pts.length; j++) {
    const a = pts[i], b = pts[j]; tryC([(a[0]+b[0])/2, (a[1]+b[1])/2], Math.hypot(a[0]-b[0], a[1]-b[1])/2);
    for (let k = j+1; k < pts.length; k++) { const c = pts[k];
      const d = 2*(a[0]*(b[1]-c[1]) + b[0]*(c[1]-a[1]) + c[0]*(a[1]-b[1])); if (Math.abs(d) < 1e-9) continue;
      const ux = ((a[0]**2+a[1]**2)*(b[1]-c[1]) + (b[0]**2+b[1]**2)*(c[1]-a[1]) + (c[0]**2+c[1]**2)*(a[1]-b[1]))/d;
      const uy = ((a[0]**2+a[1]**2)*(c[0]-b[0]) + (b[0]**2+b[1]**2)*(a[0]-c[0]) + (c[0]**2+c[1]**2)*(b[0]-a[0]))/d;
      tryC([ux, uy], Math.hypot(a[0]-ux, a[1]-uy)); } }
  const RING = {cx: 500, cy: 430, r: 405}, CLEAR = 0.85;   // key coasts stay inside 85 % of the ring radius
  const k = RING.r*CLEAR/best.r, t = eProj.translate();
  eProj.scale(eProj.scale()*k).translate([RING.cx + (t[0]-best.c[0])*k, RING.cy + (t[1]-best.c[1])*k]);
  globalThis.__RING = RING;
}
const ePath = d3.geoPath(eProj).digits(1);

const box = [[-30, 30], [60, 75]];
const inBox = f => { const [[x0, y0], [x1, y1]] = d3.geoBounds(f); return x1 > box[0][0] && x0 < box[1][0] && y1 > box[0][1] && y0 < box[1][1]; };
const eCountries = [];
for (const f of countries) {
  if (f.id === '040') continue; // replaced by Statistik Austria outline
  if (!inBox(f) && !['643'].includes(f.id)) continue;
  const d = ePath(f);
  if (d) eCountries.push({ id: f.id, name: f.properties.name, d });
}
const eAustria = ePath(austriaOutline);
const eGrat = ePath(d3.geoGraticule().step([5,5]).extent([[-40,25],[70,80]])());
const aB = ePath.bounds(austriaOutline);

// ---------- Austria view ----------
const AW = 1000, AH = 540;
const aProj = d3.geoAzimuthalEqualArea().rotate([-13.33, -47.6]).fitExtent([[82, 58], [AW - 82, AH - 58]], austriaOutline);
const aPath = d3.geoPath(aProj).digits(1);
const aGrat = aPath(d3.geoGraticule().step([1,1]).extent([[8,45],[19,50]])());
const NAMES = {
  '1': ['Burgenland', 'Burgenland'], '2': ['Carinthia', 'Kärnten'], '3': ['Lower Austria', 'Niederösterreich'],
  '4': ['Upper Austria', 'Oberösterreich'], '5': ['Salzburg', 'Salzburg'], '6': ['Styria', 'Steiermark'],
  '7': ['Tyrol', 'Tirol'], '8': ['Vorarlberg', 'Vorarlberg'], '9': ['Vienna', 'Wien']
};
const CAPS = {
  '1': ['Eisenstadt', 16.518, 47.846], '2': ['Klagenfurt', 14.305, 46.624], '3': ['St. Pölten', 15.626, 48.204],
  '4': ['Linz', 14.286, 48.306], '5': ['Salzburg', 13.055, 47.800], '6': ['Graz', 15.439, 47.071],
  '7': ['Innsbruck', 11.404, 47.269], '8': ['Bregenz', 9.747, 47.503], '9': ['Wien', 16.373, 48.208]
};
const aStates = states.features.map(f => {
  const iso = String(f.properties.iso);
  const c = aPath.centroid(f);
  const cap = CAPS[iso];
  return {
    iso, srcName: f.properties.name, en: NAMES[iso][0], de: NAMES[iso][1], d: aPath(f),
    cx: +c[0].toFixed(1), cy: +c[1].toFixed(1),
    cap: cap[0], capXY: aProj([cap[1], cap[2]]).map(v => +v.toFixed(1)),
    bounds: aPath.bounds(f).flat().map(v => +v.toFixed(1))
  };
}).sort((a, b) => a.iso.localeCompare(b.iso));

const out = {ring: globalThis.__RING, 
  europe: { w: EW, h: EH, countries: eCountries, grat: eGrat, austria: eAustria, austriaBounds: aB.flat().map(v => +v.toFixed(1)),
    vienna: eProj([16.373, 48.208]).map(v => +v.toFixed(1)) },
  austria: { w: AW, h: AH, outline: aPath(austriaOutline), grat: aGrat, states: aStates }
};

// ---------- overlays: real cities, rivers, lakes, arcs ----------
const rd = f => JSON.parse(fs.readFileSync('ne/geojson/'+f));
const places = rd('ne_10m_populated_places_simple.geojson').features;
const riversA = rd('ne_10m_rivers_lake_centerlines.geojson').features;
const riversE = rd('ne_10m_rivers_europe.geojson').features;
const lakesA = rd('ne_10m_lakes.geojson').features;
const lakesE = rd('ne_10m_lakes_europe.geojson').features;
const inExt = (p, w, h, m=0) => p && p[0] >= -m && p[0] <= w+m && p[1] >= -m && p[1] <= h+m;
const r1 = v => +v.toFixed(1);

// Europe city lights (pop_max > 120k), size by population
out.europe.cities = places.filter(f => f.properties.pop_max > 120000).map(f => {
  const p = eProj(f.geometry.coordinates); if (!inExt(p, EW, EH)) return null;
  return [r1(p[0]), r1(p[1]), +Math.log10(f.properties.pop_max).toFixed(2), f.properties.adm0cap ? 1 : 0];
}).filter(Boolean);
// Europe rivers: scalerank <= 6 (major only)
const riverPathE = riversA.filter(f => f.properties.scalerank <= 5 && inBox(f)).map(f => ePath(f)).filter(Boolean).join('');
out.europe.rivers = riverPathE;
out.europe.lakes = lakesA.filter(f => f.properties.scalerank <= 2 && inBox(f)).map(f => ePath(f)).filter(Boolean).join('');
// arcs: Vienna to a ring of capitals (great circles)
const caps = {Vienna:[16.373,48.208],Paris:[2.352,48.857],Madrid:[-3.704,40.417],Lisbon:[-9.139,38.722],London:[-0.128,51.507],Dublin:[-6.26,53.35],Oslo:[10.752,59.914],Stockholm:[18.069,59.329],Helsinki:[24.938,60.170],Warsaw:[21.012,52.230],Kyiv:[30.523,50.450],Athens:[23.728,37.984],Rome:[12.496,41.903],Bucharest:[26.103,44.427]};
const arc = (a,b) => ({type:'LineString', coordinates: Array.from({length:41},(_,i)=>d3.geoInterpolate(a,b)(i/40))});
out.europe.arcs = Object.entries(caps).filter(([k])=>k!=='Vienna').map(([k,c]) => ePath(arc(caps.Vienna, c))).join('');

// Austria overlays
const atBox = [[9.3,46.2],[17.3,49.1]];
const inAtBox = f => { const [[x0,y0],[x1,y1]] = d3.geoBounds(f); return x1 > atBox[0][0] && x0 < atBox[1][0] && y1 > atBox[0][1] && y0 < atBox[1][1]; };
out.austria.rivers = [...riversA, ...riversE].filter(inAtBox).map(f => aPath(f)).filter(Boolean).join('');
out.austria.lakes = [...lakesA, ...lakesE].filter(inAtBox).map(f => aPath(f)).filter(Boolean).join('');
out.austria.cities = places.filter(f => f.properties.adm0name === 'Austria').map(f => {
  const p = aProj(f.geometry.coordinates);
  return [r1(p[0]), r1(p[1]), +Math.log10(Math.max(5000,f.properties.pop_max)).toFixed(2), f.properties.name];
});

const gTopo = JSON.parse(fs.readFileSync('GeoJSON-TopoJSON-Austria/2021/simplified-99.5/gemeinden_995_topo.json'));
const gKey = Object.keys(gTopo.objects)[0];
// drop the 23 Vienna districts duplicate layer: keep features whose iso is 5 digits and not the single-Vienna feature '90001'? keep all; mesh of interior arcs only
out.austria.gemeinden = aPath(topo.mesh(gTopo, gTopo.objects[gKey], (a,b) => a !== b));
const bTopo = JSON.parse(fs.readFileSync('GeoJSON-TopoJSON-Austria/2021/simplified-99.5/bezirke_995_topo.json'));
const bKey = Object.keys(bTopo.objects)[0];
out.austria.bezirke = aPath(topo.mesh(bTopo, bTopo.objects[bKey], (a,b) => a !== b));

out.proj = {
  europe: {rotate: eProj.rotate(), scale: eProj.scale(), translate: eProj.translate(), w: EW, h: EH,
    test: [[16.373,48.208],[-9.139,38.722],[24.938,60.17]].map(c => [c, eProj(c)])},
  austria: {rotate: aProj.rotate(), scale: aProj.scale(), translate: aProj.translate(), w: AW, h: AH,
    test: [[16.373,48.208],[9.747,47.503],[13.055,47.8]].map(c => [c, aProj(c)])}
};

// ---------- State views (Salzburg, Tirol, ...) ----------
out.states = {};
const bTopo95 = JSON.parse(fs.readFileSync('GeoJSON-TopoJSON-Austria/2021/simplified-95/bezirke_95_topo.json'));
const bKey95 = Object.keys(bTopo95.objects)[0];
// ---- border stubs: the first ~2 cm of every border that leaves the state, plus a label per neighbour ----
const STUB = 80, TOL = 2.5;       // stub length and endpoint tolerance, in map units (map is 1000 units wide)
function lineLen(pts){ let L = 0; for (let i = 1; i < pts.length; i++) L += Math.hypot(pts[i][0]-pts[i-1][0], pts[i][1]-pts[i-1][1]); return L; }
function cut(pts, len){ const out = [pts[0]]; let acc = 0;
  for (let i = 1; i < pts.length; i++) { const [x0,y0] = pts[i-1], [x1,y1] = pts[i]; const d = Math.hypot(x1-x0, y1-y0);
    if (acc + d >= len) { const t = (len - acc)/d; out.push([x0 + (x1-x0)*t, y0 + (y1-y0)*t]); return out; } out.push(pts[i]); acc += d; }
  return out; }
function segDist(p, a, b){ const dx = b[0]-a[0], dy = b[1]-a[1]; const L2 = dx*dx + dy*dy; let t = L2 ? ((p[0]-a[0])*dx + (p[1]-a[1])*dy)/L2 : 0; t = Math.max(0, Math.min(1, t));
  return Math.hypot(p[0]-a[0]-t*dx, p[1]-a[1]-t*dy); }
const NOE_N = {'301':'Krems an der Donau','302':'St. Pölten','303':'Waidhofen an der Ybbs','304':'Wiener Neustadt','305':'Amstetten','306':'Baden','307':'Bruck an der Leitha','308':'Gänserndorf','309':'Gmünd','310':'Hollabrunn','311':'Horn','312':'Korneuburg','313':'Krems-Land','314':'Lilienfeld','315':'Melk','316':'Mistelbach','317':'Mödling','318':'Neunkirchen','319':'St. Pölten-Land','320':'Scheibbs','321':'Tulln','322':'Waidhofen an der Thaya','323':'Wiener Neustadt-Land','325':'Zwettl'};
// Vienna lies wholly inside Lower Austria: there, the context is the ring of Lower Austrian districts around the city
function viennaContext(proj, W_, H_){
  const obj = bTopo95.objects[bKey95], iso = g => String(g.properties.iso);
  const VF = topo.feature(bTopo95, obj).features.find(f => iso(f) === '900');
  const rings = (VF.geometry.type === 'Polygon' ? [VF.geometry.coordinates] : VF.geometry.coordinates).flat().map(r => r.map(c => proj(c)));
  const segs = rings.flatMap(r => r.map((q, i) => i ? [r[i-1], q] : null).filter(Boolean));
  const inside = p => { let c = false; for (const r of rings) for (let i = 0, j = r.length - 1; i < r.length; j = i++) {
    const [xi, yi] = r[i], [xj, yj] = r[j]; if ((yi > p[1]) !== (yj > p[1]) && p[0] < (xj - xi)*(p[1] - yi)/(yj - yi) + xi) c = !c; } return c; };
  const near = p => segs.some(([a, b]) => segDist(p, a, b) < TOL);
  const stubs = [];
  for (const l of topo.mesh(bTopo95, obj, (a, b) => a !== b && iso(a)[0] === '3' && iso(b)[0] === '3').coordinates) { const pts = l.map(c => proj(c));
    for (const end of [0, 1]) { const seq = end ? [...pts].reverse() : pts; if (!near(seq[0]) || lineLen(seq) < 4) continue;
      stubs.push({k: 'at', d: 'M' + cut(seq, STUB).map(p => p.map(v => v.toFixed(1)).join(',')).join('L')}); } }
  // keep clear of the two Wienerwald summit labels (Hermannskogel to the left of its marker, Kahlenberg to the right)
  const hk = proj([16.2939, 48.2706]), kb = proj([16.3333, 48.2747]);
  const blocks = [[hk[0]-130, hk[1]-22, hk[0]+4, hk[1]+18], [kb[0]-4, kb[1]-22, kb[0]+110, kb[1]+18]];
  const clear = (cx, cy, hw, hh) => { if (blocks.some(([x0, y0, x1, y1]) => cx + hw > x0 && cx - hw < x1 && cy + hh > y0 && cy - hh < y1)) return false;
    for (let i = 0; i <= 6; i++) for (let j = 0; j <= 2; j++) {
      const p = [cx - hw + 2*hw*i/6, cy - hh + 2*hh*j/2]; if (inside(p) || segs.some(([a, b]) => segDist(p, a, b) < 7)) return false; } return true; };
  // each surrounding district: the stretch of the city border it shares, labelled just outside its middle
  const dl = [];
  for (const f of topo.feature(bTopo95, obj).features.filter(f => iso(f)[0] === '3')) {
    const dr = (f.geometry.type === 'Polygon' ? [f.geometry.coordinates] : f.geometry.coordinates).flat().map(r => r.map(c => proj(c)));
    const dsegs = dr.flatMap(r => r.map((q, i) => i ? [r[i-1], q] : null).filter(Boolean));
    const shared = []; for (const r of rings) for (let i = 1; i < r.length; i++) { const m = [(r[i-1][0]+r[i][0])/2, (r[i-1][1]+r[i][1])/2];
      if (dsegs.some(([a, b]) => segDist(m, a, b) < 1.2)) shared.push([m, r[i-1], r[i]]); }
    if (shared.length < 3) continue;
    const nm = NOE_N[iso(f)], hw = nm.length*5.6 + 6, hh = 10;
    let pos = null;
    for (const fr of [0.5, 0.4, 0.6, 0.3, 0.7, 0.2, 0.8, 0.1, 0.9]) { const [m, a, b] = shared[Math.floor(fr*(shared.length-1))]; const d = Math.hypot(b[0]-a[0], b[1]-a[1]) || 1;
      let n = [-(b[1]-a[1])/d, (b[0]-a[0])/d]; if (inside([m[0]+n[0]*5, m[1]+n[1]*5])) n = [-n[0], -n[1]];
      for (let off = 16; off < 160 && !pos; off += 4) { const x = m[0]+n[0]*off, y = m[1]+n[1]*off;
        if (x - hw < 4 || x + hw > W_ - 4 || y - hh < 4 || y + hh > H_ - 4) break; if (clear(x, y, hw, hh)) pos = [r1(x), r1(y)]; }
      if (pos) break; }
    if (pos) dl.push({iso: iso(f), name: nm, x: pos[0], y: pos[1]});
  }
  return {stubs, nbl: [{iso: '3', x: r1(W_/2), y: 26, L: 0}], cl: [], dl};
}
function borderStubs(code, proj, W_, H_){
  if (code === '9') return viennaContext(proj, W_, H_);
  const obj = atTopo.objects[atKey], isCur = g => String(g.properties.iso) === code;
  const curLines = topo.mesh(atTopo, obj, (a, b) => isCur(a) || isCur(b)).coordinates.map(l => l.map(c => proj(c)));
  const onState = p => curLines.some(l => l.some((q, i) => i && segDist(p, l[i-1], q) < TOL));
  const stubs = [];
  const take = (lines, kind) => { for (const l of lines) { const pts = l.map(c => proj(c));
    for (const end of [0, 1]) { const seq = end ? [...pts].reverse() : pts; if (!onState(seq[0])) continue;
      if (lineLen(seq) < 4) continue; stubs.push({k: kind, d: 'M' + cut(seq, STUB).map(p => p.map(v => v.toFixed(1)).join(',')).join('L')}); } } };
  // borders between other Austrian states and Austria's border along other states
  take(topo.mesh(atTopo, obj, (a, b) => !isCur(a) && !isCur(b)).coordinates, 'at');
  // borders between foreign countries that start at this state (coarser source, so a wider tolerance)
  const foreignMesh = topo.mesh(world, world.objects.countries, (a, b) => a !== b && a.id !== '040' && b.id !== '040').coordinates;
  for (const l of foreignMesh) { const pts = l.map(c => proj(c));
    for (const end of [0, 1]) { const seq = end ? [...pts].reverse() : pts;
      if (!curLines.some(cl => cl.some((q, i) => i && segDist(seq[0], cl[i-1], q) < 9))) continue;
      stubs.push({k: 'fx', d: 'M' + cut(seq, STUB).map(p => p.map(v => v.toFixed(1)).join(',')).join('L')}); } }
  // labels: next to the middle of each shared border, pushed outwards
  const SBf = states.features.find(f => String(f.properties.iso) === code);
  // planar even-odd test on the projected outline (independent of ring winding)
  const rings = (SBf.geometry.type === 'Polygon' ? [SBf.geometry.coordinates] : SBf.geometry.coordinates).flat().map(r => r.map(c => proj(c)));
  const inside = p => { let c = false; for (const r of rings) for (let i = 0, j = r.length - 1; i < r.length; j = i++) {
    const [xi, yi] = r[i], [xj, yj] = r[j]; if ((yi > p[1]) !== (yj > p[1]) && p[0] < (xj - xi)*(p[1] - yi)/(yj - yi) + xi) c = !c; } return c; };
  const segs = rings.flatMap(r => r.map((q, i) => i ? [r[i-1], q] : null).filter(Boolean));
  const clear = (cx, cy, hw, hh) => { for (let i = 0; i <= 6; i++) for (let j = 0; j <= 2; j++) {
      const p = [cx - hw + 2*hw*i/6, cy - hh + 2*hh*j/2]; if (inside(p)) return false;
      if (segs.some(([a, b]) => segDist(p, a, b) < 7)) return false; } return true; };
  const push = (m, n, hw, hh) => { for (let off = 18; off < 260; off += 4) { const x = m[0] + n[0]*off, y = m[1] + n[1]*off;
      if (clear(x, y, hw, hh)) return [r1(x), r1(y)]; } return [r1(m[0] + n[0]*40), r1(m[1] + n[1]*40)]; };
  const pointAt = (line, f) => { const L = lineLen(line); let acc = 0;
    for (let i = 1; i < line.length; i++) { const d = Math.hypot(line[i][0]-line[i-1][0], line[i][1]-line[i-1][1]);
      if (acc + d >= L*f) { const t = (L*f - acc)/(d || 1); return [[line[i-1][0] + (line[i][0]-line[i-1][0])*t, line[i-1][1] + (line[i][1]-line[i-1][1])*t],
        [(line[i][0]-line[i-1][0])/(d || 1), (line[i][1]-line[i-1][1])/(d || 1)]]; } acc += d; }
    return [line[line.length-1], [1, 0]]; };
  const tryPush = (m, n, hw, hh) => { for (let off = 18; off < 220; off += 4) { const x = m[0] + n[0]*off, y = m[1] + n[1]*off;
      if (x - hw < 4 || x + hw > W_ - 4 || y - hh < 4 || y + hh > H_ - 4) return null; if (clear(x, y, hw, hh)) return [r1(x), r1(y)]; } return null; };
  const place = (line, hw, hh) => { const L = lineLen(line);
    for (const f of [0.5, 0.35, 0.65, 0.2, 0.8, 0.1, 0.9]) { const [m, dir] = pointAt(line, f);
      let n = [-dir[1], dir[0]]; if (inside([m[0] + n[0]*6, m[1] + n[1]*6])) n = [-n[0], -n[1]];
      const r = tryPush(m, n, hw, hh); if (r) return [r[0], r[1], Math.round(L)]; }
    const [m, dir] = pointAt(line, 0.5); let n = [-dir[1], dir[0]]; if (inside([m[0] + n[0]*6, m[1] + n[1]*6])) n = [-n[0], -n[1]];
    return [r1(m[0] + n[0]*40), r1(m[1] + n[1]*40), Math.round(L)]; };
  const nbl = [];
  for (const f of states.features) { const iso = String(f.properties.iso); if (iso === code) continue;
    const sh = topo.mesh(atTopo, obj, (a, b) => (isCur(a) && String(b.properties.iso) === iso) || (isCur(b) && String(a.properties.iso) === iso)).coordinates;
    if (!sh.length) continue; const longest = sh.map(l => l.map(c => proj(c))).sort((a, b) => lineLen(b) - lineLen(a))[0];
    const nm = NAMES[iso]; const chars = Math.max(nm[0].length, nm[1].length);
    const [x, y, L] = place(longest, chars*6.6 + 6, 11); nbl.push({iso, x, y, L}); }
  // foreign neighbours: walk the state's national border and ask which country lies just outside each stretch
  const ext = topo.mesh(atTopo, obj, (a, b) => a === b && isCur(a)).coordinates.map(l => l.map(c => proj(c)));
  const runs = {};
  for (const l of ext) for (let i = 1; i < l.length; i++) { const a = l[i-1], b = l[i], d = Math.hypot(b[0]-a[0], b[1]-a[1]); if (!d) continue;
    const m = [(a[0]+b[0])/2, (a[1]+b[1])/2]; let n = [-(b[1]-a[1])/d, (b[0]-a[0])/d]; if (inside([m[0]+n[0]*4, m[1]+n[1]*4])) n = [-n[0], -n[1]];
    const ll = proj.invert([m[0]+n[0]*12, m[1]+n[1]*12]); const c = countries.find(c => NEIGH[c.id] && d3.geoContains(c, ll));
    if (c) (runs[c.id] = runs[c.id] || []).push({m, n, d}); }
  const cl = Object.entries(runs).map(([id, segs]) => { const tot = segs.reduce((s, x) => s + x.d, 0); let acc = 0, pick = segs[0];
    for (const x of segs) { acc += x.d; if (acc >= tot/2) { pick = x; break; } }
    const chars = Math.max(NEIGH[id][0].length, NEIGH[id][1].length); const [x, y] = push(pick.m, pick.n, chars*6 + 6, 14);
    return {id, en: NEIGH[id][0], de: NEIGH[id][1], x, y, L: Math.round(tot)}; }).filter(c => c.L > 8);
  return {stubs, nbl, cl};
}
const NEIGH = {'276':['Germany','Deutschland'],'203':['Czechia','Tschechien'],'703':['Slovakia','Slowakei'],'348':['Hungary','Ungarn'],
  '705':['Slovenia','Slowenien'],'380':['Italy','Italien'],'756':['Switzerland','Schweiz'],'438':['Liechtenstein','Liechtenstein']};
function stateView(code, rot, GAU, cityLL){
  // Vienna is shown at city scale: use the finer (95 %) boundary version
  const BT = code === '9' ? bTopo95 : bTopo, BK = code === '9' ? bKey95 : bKey;
  const SB = states.features.find(f => String(f.properties.iso) === code);
  const keep = iso => iso.startsWith(code) && iso !== '900';
  const bk = topo.feature(BT, BT.objects[BK]).features.filter(f => keep(String(f.properties.iso)));
  const SW = 1000;
  const PAD = code === '9' ? 140 : 80;   // room around the state for neighbours (Vienna needs space for district names)
  const p0 = d3.geoAzimuthalEqualArea().rotate(rot).fitWidth(SW - 2*PAD, SB);
  const b0 = d3.geoPath(p0).bounds(SB); const SH = Math.min(900, Math.ceil(b0[1][1] - b0[0][1] + 2*PAD));
  const sProj = d3.geoAzimuthalEqualArea().rotate(rot).fitExtent([[PAD, PAD], [SW - PAD, SH - PAD]], SB);
  const cProj = d3.geoAzimuthalEqualArea().rotate(sProj.rotate()).scale(sProj.scale()).translate(sProj.translate()).clipExtent([[0, 0], [SW, SH]]);
  const cPath = d3.geoPath(cProj).digits(1);
  const visLabel = d => { if (!d) return null; let best = null, bestA = 0;
    for (const ring of d.split('M').filter(Boolean)) { const pts = ring.replace(/Z/g,'').split('L').map(q => q.split(',').map(Number));
      if (pts.length < 3) continue; let a = 0; for (let i = 0; i < pts.length; i++) { const [x1,y1] = pts[i], [x2,y2] = pts[(i+1)%pts.length]; a += x1*y2 - x2*y1; }
      a = Math.abs(a/2); if (a > bestA) { bestA = a; best = pts; } }
    if (!best || bestA < 2500) return null; const p = polylabel([best], 0.5); return [r1(p[0]), r1(p[1]), Math.round(bestA)]; };
  const sPath = d3.geoPath(sProj).digits(1);
  const [[bx0,by0],[bx1,by1]] = d3.geoBounds(SB);
  const inSb = f => { const [[x0,y0],[x1,y1]] = d3.geoBounds(f); return x1 > bx0-.15 && x0 < bx1+.15 && y1 > by0-.15 && y0 < by1+.15; };
  const gem = code === '9' ? null : topo.mesh(gTopo, gTopo.objects[gKey], (a,b) => a !== b && String(a.properties.iso).startsWith(code) && String(b.properties.iso).startsWith(code));
  out.states[code] = {
    w: SW, h: SH,
    outline: sPath(topo.merge(BT, BT.objects[BK].geometries.filter(g => keep(String(g.properties.iso))))),
    numbered: code === '9',
    gaue: bk.map(f => { const iso = String(f.properties.iso); const c = sPath.centroid(f);
      const L = labelPt(sProj, f);
      return {iso, src: f.properties.name, en: GAU[iso][0], de: GAU[iso][1], n: code === '9' ? +iso - 900 : null, d: sPath(f), cx: r1(L[0]), cy: r1(L[1]), a: Math.round(sPath.area(f))}; }),
    gemeinden: gem ? sPath(gem) : '',
    // Natural Earth rivers are too coarse at city scale; in Vienna the Danube is read from the district borders instead
    rivers: code === '9' ? '' : [...riversA, ...riversE].filter(inSb).map(f => sPath(f)).filter(Boolean).join(''),
    lakes: [...lakesA, ...lakesE].filter(inSb).map(f => sPath(f)).filter(Boolean).join(''),
    city: sProj(cityLL).map(r1),
    // neighbouring federal states (dimmed relief, clickable) and neighbouring countries (border + name only)
    nb: states.features.filter(f => String(f.properties.iso) !== code).map(f => { const d = cPath(f); const L = visLabel(d);
      return d && L ? {iso: String(f.properties.iso), d, lx: L[0], ly: L[1], a: L[2]} : null; }).filter(Boolean),
    atFill: cPath(austriaOutline),                       // polygon, clipped to the frame: used to mask the relief
    // borders as clipped lines (meshes), so no artificial edges appear along the frame
    atBorder: cPath(topo.mesh(atTopo, atTopo.objects[atKey], (a, b) => a === b)),
    stBorders: cPath(topo.mesh(atTopo, atTopo.objects[atKey], (a, b) => a !== b)),
    foreign: cPath(topo.mesh(world, world.objects.countries, (a, b) => a !== b && a.id !== '040' && b.id !== '040')),
    countries: Object.entries(NEIGH).map(([id, nm]) => { const f = countries.find(c => c.id === id); const d = f && cPath(f); const L = visLabel(d);
      return L ? {id, en: nm[0], de: nm[1], lx: L[0], ly: L[1], a: L[2]} : null; }).filter(Boolean),
    ...borderStubs(code, sProj, SW, SH),
    // recording places cited in the content (Bülow 2019, p. 30: DiÖ Ortspunkte); vowel of 2.Pl. 'seid'
    // recording places: Sprachatlas Salzburg (32) and the DiÖ places cited by Bülow 2019; see places_sbg.json for coordinate sources
    places: code !== '5' ? [] : JSON.parse(fs.readFileSync('places_sbg.json')).places.map(p => {
      let xy;
      if (p.muni) { const f = topo.feature(gTopo, gTopo.objects[gKey]).features.find(g => String(g.properties.iso) === p.muni); xy = labelPt(sProj, f); }
      else xy = sProj([p.lon, p.lat]);
      return {n: p.n, g: p.g, atlas: p.atlas, v: p.dioe || null, src: p.src, x: r1(xy[0]), y: r1(xy[1])}; })
  };
  out.proj['st'+code] = {rotate: sProj.rotate(), scale: sProj.scale(), translate: sProj.translate(), w: SW, h: SH,
    test: [cityLL].map(c => [c, sProj(c)])};
}
stateView('5', [-12.95, -47.42], {'501':['City of Salzburg','Stadt Salzburg'],'502':['Tennengau','Tennengau'],'503':['Flachgau','Flachgau'],
  '504':['Pongau','Pongau'],'505':['Lungau','Lungau'],'506':['Pinzgau','Pinzgau']}, [13.047, 47.798]);
stateView('7', [-11.45, -47.15], {'701':['City of Innsbruck','Innsbruck-Stadt'],'702':['Imst','Imst'],'703':['Innsbruck-Land','Innsbruck-Land'],
  '704':['Kitzbühel','Kitzbühel'],'705':['Kufstein','Kufstein'],'706':['Landeck','Landeck'],'707':['Lienz (East Tyrol)','Lienz (Osttirol)'],
  '708':['Reutte','Reutte'],'709':['Schwaz','Schwaz']}, [11.3943, 47.2654]);
stateView('1', [-16.45, -47.6], {'101':['Eisenstadt','Eisenstadt'],'102':['Rust','Rust'],'103':['Eisenstadt-Umgebung','Eisenstadt-Umgebung'],
  '104':['Güssing','Güssing'],'105':['Jennersdorf','Jennersdorf'],'106':['Mattersburg','Mattersburg'],'107':['Neusiedl am See','Neusiedl am See'],
  '108':['Oberpullendorf','Oberpullendorf'],'109':['Oberwart','Oberwart']}, [16.524, 47.846]);
stateView('2', [-13.85, -46.75], {'201':['Klagenfurt','Klagenfurt'],'202':['Villach','Villach'],'203':['Hermagor','Hermagor'],
  '204':['Klagenfurt-Land','Klagenfurt-Land'],'205':['St. Veit an der Glan','St. Veit an der Glan'],'206':['Spittal an der Drau','Spittal an der Drau'],
  '207':['Villach-Land','Villach-Land'],'208':['Völkermarkt','Völkermarkt'],'209':['Wolfsberg','Wolfsberg'],'210':['Feldkirchen','Feldkirchen']}, [14.3076, 46.624]);
stateView('4', [-13.9, -48.0], {'401':['Linz','Linz'],'402':['Steyr','Steyr'],'403':['Wels','Wels'],'404':['Braunau','Braunau'],'405':['Eferding','Eferding'],'406':['Freistadt','Freistadt'],'407':['Gmunden','Gmunden'],'408':['Grieskirchen','Grieskirchen'],'409':['Kirchdorf','Kirchdorf'],'410':['Linz-Land','Linz-Land'],'411':['Perg','Perg'],'412':['Ried','Ried'],'413':['Rohrbach','Rohrbach'],'414':['Schärding','Schärding'],'415':['Steyr-Land','Steyr-Land'],'416':['Urfahr-Umgebung','Urfahr-Umgebung'],'417':['Vöcklabruck','Vöcklabruck'],'418':['Wels-Land','Wels-Land']}, [14.2858, 48.3069]);
stateView('3', [-15.8, -48.2], {'301':['Krems an der Donau','Krems an der Donau'],'302':['St. Pölten','St. Pölten'],'303':['Waidhofen an der Ybbs','Waidhofen an der Ybbs'],'304':['Wiener Neustadt','Wiener Neustadt'],'305':['Amstetten','Amstetten'],'306':['Baden','Baden'],'307':['Bruck an der Leitha','Bruck an der Leitha'],'308':['Gänserndorf','Gänserndorf'],'309':['Gmünd','Gmünd'],'310':['Hollabrunn','Hollabrunn'],'311':['Horn','Horn'],'312':['Korneuburg','Korneuburg'],'313':['Krems-Land','Krems-Land'],'314':['Lilienfeld','Lilienfeld'],'315':['Melk','Melk'],'316':['Mistelbach','Mistelbach'],'317':['Mödling','Mödling'],'318':['Neunkirchen','Neunkirchen'],'319':['St. Pölten-Land','St. Pölten-Land'],'320':['Scheibbs','Scheibbs'],'321':['Tulln','Tulln'],'322':['Waidhofen an der Thaya','Waidhofen an der Thaya'],'323':['Wiener Neustadt-Land','Wiener Neustadt-Land'],'325':['Zwettl','Zwettl']}, [15.6243, 48.204]);
stateView('6', [-14.95, -47.25], {'601':['Graz','Graz'],'603':['Deutschlandsberg','Deutschlandsberg'],'606':['Graz-Umgebung','Graz-Umgebung'],'610':['Leibnitz','Leibnitz'],'611':['Leoben','Leoben'],'612':['Liezen','Liezen'],'614':['Murau','Murau'],'616':['Voitsberg','Voitsberg'],'617':['Weiz','Weiz'],'620':['Murtal','Murtal'],'621':['Bruck-Mürzzuschlag','Bruck-Mürzzuschlag'],'622':['Hartberg-Fürstenfeld','Hartberg-Fürstenfeld'],'623':['Südoststeiermark','Südoststeiermark']}, [15.4385, 47.071]);
stateView('8', [-9.9, -47.25], {'801':['Bludenz','Bludenz'],'802':['Bregenz','Bregenz'],'803':['Dornbirn','Dornbirn'],'804':['Feldkirch','Feldkirch']}, [9.7471, 47.5031]);
stateView('9', [-16.37, -48.21], {'901':['Innere Stadt','Innere Stadt'],'902':['Leopoldstadt','Leopoldstadt'],'903':['Landstraße','Landstraße'],'904':['Wieden','Wieden'],'905':['Margareten','Margareten'],'906':['Mariahilf','Mariahilf'],'907':['Neubau','Neubau'],'908':['Josefstadt','Josefstadt'],'909':['Alsergrund','Alsergrund'],'910':['Favoriten','Favoriten'],'911':['Simmering','Simmering'],'912':['Meidling','Meidling'],'913':['Hietzing','Hietzing'],'914':['Penzing','Penzing'],'915':['Rudolfsheim-Fünfhaus','Rudolfsheim-Fünfhaus'],'916':['Ottakring','Ottakring'],'917':['Hernals','Hernals'],'918':['Währing','Währing'],'919':['Döbling','Döbling'],'920':['Brigittenau','Brigittenau'],'921':['Floridsdorf','Floridsdorf'],'922':['Donaustadt','Donaustadt'],'923':['Liesing','Liesing']}, [16.3725, 48.2085]);

// ---- Austria view: where the neighbouring countries' borders meet Austria, plus the country names ----
{
  const ASTUB = 55, proj = aProj;
  const rings = (austriaOutline.type === 'Polygon' ? [austriaOutline.coordinates] : austriaOutline.coordinates).flat().map(r => r.map(c => proj(c)));
  const inside = p => { let c = false; for (const r of rings) for (let i = 0, j = r.length - 1; i < r.length; j = i++) {
    const [xi, yi] = r[i], [xj, yj] = r[j]; if ((yi > p[1]) !== (yj > p[1]) && p[0] < (xj - xi)*(p[1] - yi)/(yj - yi) + xi) c = !c; } return c; };
  const segs = rings.flatMap(r => r.map((q, i) => i ? [r[i-1], q] : null).filter(Boolean));
  const near = (p, tol) => segs.some(([a, b]) => segDist(p, a, b) < tol);
  const stubs = [], ends = [];
  const foreignMesh = topo.mesh(world, world.objects.countries, (a, b) => a !== b && a.id !== '040' && b.id !== '040').coordinates;
  for (const l of foreignMesh) { const pts = l.map(c => proj(c));
    for (const end of [0, 1]) { const seq = end ? [...pts].reverse() : pts;
      if (!near(seq[0], 5)) continue;
      // start the stub at the closest point of Austria's own outline, so it touches the drawn border
      let best = null, bd = 1e9; for (const [a, b] of segs) { const dx = b[0]-a[0], dy = b[1]-a[1], L2 = dx*dx + dy*dy;
        let t = L2 ? ((seq[0][0]-a[0])*dx + (seq[0][1]-a[1])*dy)/L2 : 0; t = Math.max(0, Math.min(1, t));
        const q = [a[0]+t*dx, a[1]+t*dy], d = Math.hypot(q[0]-seq[0][0], q[1]-seq[0][1]); if (d < bd) { bd = d; best = q; } }
      if (ends.some(e => Math.hypot(e[0]-best[0], e[1]-best[1]) < 6)) continue;
      const s = cut([best, ...seq.filter((p, i) => i > 0 || bd > 0.5)], ASTUB);
      if (lineLen(s) < 10) continue; ends.push(best);
      stubs.push({k: 'fx', d: 'M' + s.map(p => p.map(v => v.toFixed(1)).join(',')).join('L')}); } }
  // state name positions as drawn on the page (same nudges as in the template), so country names never sit on them
  const OFF = {'9': s => [s.capXY[0]+34, s.capXY[1]-12], '5': s => [s.cx+4, s.cy+30], '1': s => [s.cx+2, s.cy+26], '3': s => [s.capXY[0]-14, s.capXY[1]-52]};
  const avoid = aStates.map(s => { const [x, y] = OFF[s.iso] ? OFF[s.iso](s) : [s.cx, s.cy]; const n = Math.max(NAMES[s.iso][0].length, NAMES[s.iso][1].length);
    return [x, y, n*6 + 10, 12]; });
  const clear = (cx, cy, hw, hh) => { if (cx - hw < 4 || cx + hw > AW - 4 || cy - hh < 4 || cy + hh > AH - 4) return false;
    if (avoid.some(([x, y, w, h]) => Math.abs(x - cx) < w + hw && Math.abs(y - cy) < h + hh)) return false;
    for (let i = 0; i <= 6; i++) for (let j = 0; j <= 2; j++) { const p = [cx - hw + 2*hw*i/6, cy - hh + 2*hh*j/2];
      if (inside(p) || near(p, 6)) return false; } return true; };
  const runs = {};
  for (const r of rings) for (let i = 1; i < r.length; i++) { const a = r[i-1], b = r[i], d = Math.hypot(b[0]-a[0], b[1]-a[1]); if (!d) continue;
    const m = [(a[0]+b[0])/2, (a[1]+b[1])/2]; let n = [-(b[1]-a[1])/d, (b[0]-a[0])/d]; if (inside([m[0]+n[0]*3, m[1]+n[1]*3])) n = [-n[0], -n[1]];
    const ll = proj.invert([m[0]+n[0]*8, m[1]+n[1]*8]); const c = countries.find(c => NEIGH[c.id] && d3.geoContains(c, ll));
    if (c) (runs[c.id] = runs[c.id] || []).push({m, n, d}); }
  const cl = [];
  for (const [id, sg] of Object.entries(runs)) { const tot = sg.reduce((s, x) => s + x.d, 0); if (tot < 4) continue;
    const chars = Math.max(NEIGH[id][0].length, NEIGH[id][1].length), hw = chars*5.6 + 6, hh = 13;
    let acc = 0, at = null;
    // try points from the middle of the shared border outwards until the label fits outside Austria and inside the frame
    const order = [0.5, 0.4, 0.6, 0.3, 0.7, 0.2, 0.8, 0.1, 0.9];
    const cum = []; for (const x of sg) { acc += x.d; cum.push(acc); }
    for (const f of order) { const k = cum.findIndex(v => v >= tot*f); const x = sg[Math.max(0, k)];
      for (let off = 16; off < 140 && !at; off += 3) { const cx = x.m[0] + x.n[0]*off, cy = x.m[1] + x.n[1]*off;
        if (clear(cx, cy, hw, hh) && !cl.some(o => Math.abs(o.x - cx) < (hw + o.hw) && Math.abs(o.y - cy) < 2*hh)) at = [r1(cx), r1(cy), hw]; }
      if (at) break; }
    if (at) cl.push({id, en: NEIGH[id][0], de: NEIGH[id][1], x: at[0], y: at[1], hw: at[2], L: Math.round(tot)}); }
  out.austria.stubs = stubs; out.austria.cl = cl.map(({hw, ...c}) => c);
  console.log('austria stubs', stubs.length, 'labels', cl.map(c => c.en + '@' + c.x + ',' + c.y + ' L' + c.L).join(' | '));
}
fs.writeFileSync('geo.json', JSON.stringify(out));
console.log('countries', eCountries.length, 'states', aStates.map(s => s.iso + ':' + s.srcName).join(', '));
console.log('bytes', fs.statSync('geo.json').size);
