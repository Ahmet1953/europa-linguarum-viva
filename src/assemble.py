import base64
t=open('template.html').read()
import json
g=json.load(open('geo.json')); [g['states'][c].__setitem__('peaks', json.load(open(f'peaks_st{c}.json'))) for c in g['states']]
t=t.replace('/*GEO*/null',json.dumps(g,separators=(',',':')))
t=t.replace('/*CONTENT*/',open('content.js').read())
for k,f in [('REL_E','art_europe.webp'),('REL_A','art_austria.webp'),('INTRO','intro_map.webp')]:
    t=t.replace('/*'+k+'*/','data:image/webp;base64,'+base64.b64encode(open(f,'rb').read()).decode())
t=t.replace('/*REL_STATES*/', ','.join(f'st{c}:"data:image/webp;base64,'+base64.b64encode(open(f'art_st{c}.webp','rb').read()).decode()+'"' for c in g['states']))
open('europa-linguarum-viva.html','w').write(t)
print(len(t))
