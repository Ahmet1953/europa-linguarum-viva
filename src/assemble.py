import base64
t=open('template.html').read()
import json
g=json.load(open('geo.json')); [g['states'][c].__setitem__('peaks', json.load(open(f'peaks_st{c}.json'))) for c in g['states']]
t=t.replace('/*GEO*/null',json.dumps(g,separators=(',',':')))
# fonts are embedded (no request to Google): EB Garamond and IBM Plex Mono, SIL Open Font License, via @fontsource
R={'latin':'U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD',
   'latin-ext':'U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+0304,U+0308,U+0329,U+1D00-1DBF,U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF'}
ff=''
for fam,slug,ws in [('EB Garamond','eb-garamond',(400,500,600)),('IBM Plex Mono','ibm-plex-mono',(400,500))]:
    for w in ws:
        for sub in ('latin-ext','latin'):
            b=base64.b64encode(open(f'fonts/{slug}-{sub}-{w}-normal.woff2','rb').read()).decode()
            ff+=f"@font-face{{font-family:'{fam}';font-style:normal;font-weight:{w};font-display:swap;src:url(data:font/woff2;base64,{b}) format('woff2');unicode-range:{R[sub]}}}"
t=t.replace('/*FONTS*/',ff)
t=t.replace('/*CONTENT*/',open('content.js').read())
for k,f in [('REL_E','art_europe.webp'),('REL_A','art_austria.webp'),('INTRO','intro_map.webp')]:
    t=t.replace('/*'+k+'*/','data:image/webp;base64,'+base64.b64encode(open(f,'rb').read()).decode())
t=t.replace('/*REL_STATES*/', ','.join(f'st{c}:"data:image/webp;base64,'+base64.b64encode(open(f'art_st{c}.webp','rb').read()).decode()+'"' for c in g['states']))
open('europa-linguarum-viva.html','w').write(t)
print(len(t))
