import asyncio, sys
from playwright.async_api import async_playwright
SP='/tmp/claude-0/-home-claude/37c37c24-e61e-5f96-a9b1-f0bd18559ae8/scratchpad/'
CODES=sys.argv[1].split(',')
html=open('europa-linguarum-viva.html').read()
open('test.html','w').write('<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><style>body{margin:0}[hidden]{display:none!important}</style></head><body>'+html+'</body></html>')
CL='''(([sel,iso,key])=>{const S=key==="a"?GEO.austria.states.find(s=>s.iso===iso):GEO.states[cur].gaue.find(g=>g.iso===iso);const p=document.querySelector(sel);const svg=p.ownerSVGElement;const pt=svg.createSVGPoint();pt.x=S.cx;pt.y=S.cy;const q=pt.matrixTransform(svg.getScreenCTM());const e=document.elementFromPoint(q.x,q.y);return [q.x,q.y,e&&e.getAttribute('aria-label')]})'''
async def run(name,w,h,mobile):
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':w,'height':h},is_mobile=mobile,has_touch=mobile)
        errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto('file:///root/viva/test.html?nointro');await pg.wait_for_timeout(3000)
        await pg.click('#enter-at');await pg.wait_for_timeout(1600)
        for c in CODES:
            if mobile: await pg.evaluate('document.querySelector(".at-map").scrollLeft=0')
            t=await pg.evaluate(CL+f'(["#svg-austria .state","{c}","a"])')
            if mobile and not t[2]:
                await pg.evaluate(f'(()=>{{const m=document.querySelector(".at-map");const s=GEO.austria.states.find(s=>s.iso==="{c}");const box=document.querySelector(".at-box");m.scrollLeft=box.offsetLeft+s.cx/1000*box.offsetWidth-m.clientWidth/2}})()')
                t=await pg.evaluate(CL+f'(["#svg-austria .state","{c}","a"])')
            await pg.mouse.click(t[0],t[1]);await pg.wait_for_timeout(1600)
            await pg.screenshot(path=SP+f'{name}_st{c}.png')
            gs=await pg.evaluate('GEO.states[cur].gaue.map(g=>g.iso)')
            hits=[]
            if not mobile:
                for gi in gs:
                    r=await pg.evaluate(CL+f'(["#svg-state .gau","{gi}","s"])'); hits.append(bool(r[2]))
            print(name,c,'click→',t[2],'| title',await pg.evaluate('document.getElementById("st-title").textContent'),'| district hits',sum(hits),'/',len(gs) if not mobile else '-')
            await pg.keyboard.press('Escape');await pg.wait_for_timeout(1200)
            if await pg.evaluate('view')!='austria': await pg.keyboard.press('Escape');await pg.wait_for_timeout(1000)
        print(name,'hOverflow',await pg.evaluate('document.documentElement.scrollWidth>innerWidth'),'errors',errs)
        await b.close()
async def main(): await run('desk',1440,820,False); await run('phone',390,844,True)
asyncio.run(main())
