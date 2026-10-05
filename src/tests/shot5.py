import asyncio
from playwright.async_api import async_playwright
SP='/tmp/claude-0/-home-claude/37c37c24-e61e-5f96-a9b1-f0bd18559ae8/scratchpad/'
html=open('europa-linguarum-viva.html').read()
open('test.html','w').write('<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><style>body{margin:0}[hidden]{display:none!important}</style></head><body>'+html+'</body></html>')
async def run(name,w,h,mobile):
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':w,'height':h},is_mobile=mobile,has_touch=mobile)
        errs=[];pg.on('pageerror',lambda e:errs.append(str(e)));pg.on('console',lambda m: m.type=='error' and errs.append(m.text))
        await pg.goto('file:///root/viva/test.html?nointro');await pg.wait_for_timeout(2500)
        await pg.click('#enter-at');await pg.wait_for_timeout(1500)
        await pg.evaluate('goState("5")');await pg.wait_for_timeout(1500)
        if mobile: await pg.click('#sb-cards');await pg.wait_for_timeout(900)
        print(name,'drawer',await pg.evaluate('document.getElementById("drawer").classList.contains("open")'),'cards',await pg.evaluate('document.querySelectorAll("#track .card").length'))
        for i in (0,1,2,4):
            await pg.evaluate(f'goCard({i},false)');await pg.wait_for_timeout(500)
            await pg.screenshot(path=SP+f'c_{name}_{i}.png')
        # gau click: Pinzgau
        await pg.evaluate('closeDrawer()');await pg.wait_for_timeout(700)
        r=await pg.evaluate('''(()=>{const g=GEO.states["5"].gaue.find(g=>g.iso==="506");const svg=document.getElementById("svg-state");const pt=svg.createSVGPoint();pt.x=g.cx;pt.y=g.cy;const q=pt.matrixTransform(svg.getScreenCTM());return [q.x,q.y]})()''')
        if mobile:
            await pg.evaluate(f'document.querySelector(".sb-map").scrollLeft=0')
            r=await pg.evaluate('''(()=>{const g=GEO.states["5"].gaue.find(g=>g.iso==="506");const svg=document.getElementById("svg-state");const pt=svg.createSVGPoint();pt.x=g.cx;pt.y=g.cy;const q=pt.matrixTransform(svg.getScreenCTM());return [q.x,q.y]})()''')
        await pg.mouse.click(r[0],r[1]);await pg.wait_for_timeout(1200)
        print(name,'gau click → card',await pg.evaluate('CONTENT.cards[card].id'),'open',await pg.evaluate('document.getElementById("drawer").classList.contains("open")'))
        await pg.screenshot(path=SP+f'c_{name}_pinz.png')
        await pg.click('#lang-de');await pg.wait_for_timeout(500)
        await pg.screenshot(path=SP+f'c_{name}_pinz_de.png')
        await pg.click('#d-meth');await pg.wait_for_timeout(500)
        await pg.screenshot(path=SP+f'c_{name}_meth.png')
        await pg.keyboard.press('Escape');await pg.wait_for_timeout(300)
        print(name,'meth closed',await pg.evaluate('document.getElementById("meth").hidden'),'hOverflow',await pg.evaluate('document.documentElement.scrollWidth>innerWidth'),'errors',errs)
        await b.close()
async def main(): await run('desk',1440,820,False); await run('phone',390,844,True)
asyncio.run(main())
