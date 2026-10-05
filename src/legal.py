# Writes the legal pages of the public site: ../impressum.html and ../datenschutz.html (German first, English below)
# and copies the self-hosted fonts to ../fonts/. Run from src/ after build_site.py.
import pathlib, shutil
ROOT = pathlib.Path('..')
(ROOT / 'fonts').mkdir(exist_ok=True)
for f in pathlib.Path('fonts').glob('*.woff2'): shutil.copy(f, ROOT / 'fonts' / f.name)

NAME = 'Ahmet Akan'
ADDR_DE = 'Heiligenstädter Straße 131–135/5/31<br>1190 Wien, Österreich'
ADDR_EN = 'Heiligenstädter Straße 131–135/5/31<br>1190 Vienna, Austria'
MAIL = 'info@europalinguarumviva.eu'
STAND_DE, STAND_EN = 'Stand: Oktober 2026', 'Last updated: October 2026'

FACES = ''.join(
    f"@font-face{{font-family:'{fam}';font-weight:{w};font-display:swap;src:url(fonts/{slug}-{sub}-{w}-normal.woff2) format('woff2');unicode-range:{rng}}}"
    for fam, slug, ws in [('EB Garamond', 'eb-garamond', (400, 500)), ('IBM Plex Mono', 'ibm-plex-mono', (400, 500))]
    for w in ws
    for sub, rng in [('latin-ext', 'U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+1E00-1E9F,U+2020,U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF'),
                     ('latin', 'U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+2000-206F,U+20AC,U+2122,U+2212,U+FEFF,U+FFFD')])

CSS = FACES + '''
:root{--night:#06101f;--ivory:#f3ead8;--mute:#9aa6bf;--gold:#e9b766;--gold-hi:#f5d9a0;--line:rgba(233,183,102,.25)}
html{background:var(--night)}body{margin:0;color:var(--ivory);font:19px/1.6 "EB Garamond",Georgia,serif;background:radial-gradient(120% 90% at 70% 0,#0c1b38 0,var(--night) 70%) fixed}
main{max-width:720px;margin:0 auto;padding:40px 16px 80px}
.top{display:flex;justify-content:space-between;align-items:center;gap:16px;font:500 12px/1 "IBM Plex Mono",monospace;letter-spacing:.18em;text-transform:uppercase}
.top a{color:var(--gold);text-decoration:none}.top a:hover{color:var(--gold-hi)}
.top nav{display:flex;gap:14px}.top nav a{color:var(--mute)}
h1{font-weight:500;font-size:clamp(36px,6vw,56px);line-height:1.05;margin:48px 0 8px}
h2{font:500 13px/1.3 "IBM Plex Mono",monospace;letter-spacing:.18em;text-transform:uppercase;color:var(--gold);margin:36px 0 10px}
p,li{margin:0 0 12px}ul{padding-left:20px}
a{color:var(--gold-hi)}
.lang{border-top:1px solid var(--line);margin-top:56px;padding-top:8px}
.note{color:var(--mute);font-size:16px}
dl{display:grid;grid-template-columns:max-content 1fr;gap:6px 22px;margin:0}dt{color:var(--mute)}dd{margin:0}
@media (max-width:560px){dl{grid-template-columns:1fr}dd{margin-bottom:10px}}
'''

def page(fname, title, de, en, other):
    html = f'''<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex">
<title>{title} · Europa Linguarum Viva</title>
<style>{CSS}</style>
</head>
<body>
<main>
<div class="top"><a href="./">← Europa Linguarum Viva</a><nav>{other}<a href="#en">English</a></nav></div>
<section lang="de" id="de">
{de}
<p class="note">{STAND_DE}</p>
</section>
<section lang="en" id="en" class="lang">
{en}
<p class="note">{STAND_EN}</p>
</section>
</main>
</body>
</html>
'''
    (ROOT / fname).write_text(html)

IMP_DE = f'''<h1>Impressum</h1>
<p>Offenlegung gemäß § 25 Mediengesetz und Angaben gemäß § 5 E-Commerce-Gesetz.</p>
<h2>Medieninhaber und Herausgeber</h2>
<dl><dt>Name</dt><dd>{NAME}</dd><dt>Anschrift</dt><dd>{ADDR_DE}</dd><dt>E-Mail</dt><dd><a href="mailto:{MAIL}">{MAIL}</a></dd></dl>
<h2>Grundlegende Richtung</h2>
<p>Europa Linguarum Viva ist ein nicht-kommerzielles Informationsangebot zu den Sprachen und regionalen Sprachformen Europas. Das Pilotprojekt behandelt Österreich und das Land Salzburg.</p>
<h2>Inhalte und Quellen</h2>
<p>Die Inhalte werden mit Unterstützung künstlicher Intelligenz (Claude, Anthropic) erarbeitet und an den genannten Quellen geprüft. Eine fachliche Prüfung durch Dialektologinnen und Dialektologen steht noch aus. Jede Aussage nennt ihre Quelle; die vollständige Liste steht auf der Seite unter „Methode &amp; Quellen“. Hinweise auf Fehler nehmen wir gerne per E-Mail entgegen.</p>
<p>Kartengrundlagen: DGM Österreich (data.gv.at, CC BY 4.0), Statistik Austria (CC BY 4.0), Natural Earth (gemeinfrei). Tonaufnahmen anderer Projekte werden nur verlinkt, nicht übernommen.</p>
<h2>Haftung für Links</h2>
<p>Für Inhalte externer Websites, auf die verlinkt wird, sind ausschließlich deren Betreiber verantwortlich. Bei Bekanntwerden rechtswidriger Inhalte werden entsprechende Links umgehend entfernt.</p>'''

IMP_EN = f'''<h1>Legal notice</h1>
<p>Disclosure under § 25 of the Austrian Media Act and information under § 5 of the Austrian E-Commerce Act.</p>
<h2>Owner and publisher</h2>
<dl><dt>Name</dt><dd>{NAME}</dd><dt>Address</dt><dd>{ADDR_EN}</dd><dt>Email</dt><dd><a href="mailto:{MAIL}">{MAIL}</a></dd></dl>
<h2>Purpose</h2>
<p>Europa Linguarum Viva is a non-commercial information service on the languages and regional varieties of Europe. The pilot covers Austria and the federal state of Salzburg.</p>
<h2>Content and sources</h2>
<p>Content is researched with AI assistance (Claude, Anthropic) and checked against the sources cited. Review by dialectologists is still pending. Every statement names its source; the full list is on the site under “Method &amp; sources”. Corrections are welcome by email.</p>
<p>Map data: DGM Österreich (data.gv.at, CC BY 4.0), Statistik Austria (CC BY 4.0), Natural Earth (public domain). Recordings of other projects are linked, never copied.</p>
<h2>External links</h2>
<p>The operators of linked external websites are solely responsible for their content. Links to unlawful content will be removed as soon as we become aware of it.</p>'''

DS_DE = f'''<h1>Datenschutz</h1>
<h2>Verantwortlicher</h2>
<p>{NAME}, {ADDR_DE.replace('<br>', ', ')}, <a href="mailto:{MAIL}">{MAIL}</a></p>
<h2>Kurz gesagt</h2>
<ul><li>Keine Cookies, keine Analyse- oder Tracking-Werkzeuge, keine Werbung.</li>
<li>Schriften und Karten sind in die Seite eingebettet; beim Aufruf werden keine Daten an Google oder andere Dritte gesendet.</li>
<li>Es gibt keine Formulare und kein Benutzerkonto.</li></ul>
<h2>Hosting</h2>
<p>Die Website wird über GitHub Pages bereitgestellt (GitHub, Inc., 88 Colin P. Kelly Jr. Street, San Francisco, CA 94107, USA). Beim Aufruf verarbeitet GitHub technisch notwendige Verbindungsdaten, insbesondere die IP-Adresse, um die Seite auszuliefern und die Sicherheit des Dienstes zu gewährleisten. Rechtsgrundlage ist unser berechtigtes Interesse an einer sicheren und verlässlichen Bereitstellung (Art. 6 Abs. 1 lit. f DSGVO). Dabei können Daten in die USA übermittelt werden; GitHub stützt solche Übermittlungen nach eigenen Angaben auf das EU-US Data Privacy Framework und auf Standardvertragsklauseln. Näheres: <a href="https://docs.github.com/site-policy/privacy-policies/github-general-privacy-statement">GitHub-Datenschutzerklärung</a>.</p>
<h2>Kontakt per E-Mail</h2>
<p>Wenn Sie uns schreiben, verwenden wir Ihre Angaben nur zur Beantwortung Ihrer Nachricht (Art. 6 Abs. 1 lit. b und f DSGVO) und löschen sie, sobald sie dafür nicht mehr benötigt werden. Das E-Mail-Postfach wird bei IONOS SE (Elgendorfer Str. 57, 56410 Montabaur, Deutschland) betrieben.</p>
<h2>Externe Links</h2>
<p>Die Seite verlinkt auf Quellen und Tonaufnahmen anderer Anbieter, etwa den Sprachatlas Salzburg. Erst wenn Sie einen solchen Link anklicken, verlassen Sie diese Seite; dort gelten die Datenschutzbestimmungen des jeweiligen Anbieters.</p>
<h2>Ihre Rechte</h2>
<p>Sie haben das Recht auf Auskunft, Berichtigung, Löschung, Einschränkung der Verarbeitung, Datenübertragbarkeit und Widerspruch. Wenden Sie sich dazu an <a href="mailto:{MAIL}">{MAIL}</a>. Sie können sich außerdem bei der Österreichischen Datenschutzbehörde beschweren (Barichgasse 40–42, 1030 Wien, <a href="https://www.dsb.gv.at">www.dsb.gv.at</a>).</p>'''

DS_EN = f'''<h1>Privacy</h1>
<h2>Controller</h2>
<p>{NAME}, {ADDR_EN.replace('<br>', ', ')}, <a href="mailto:{MAIL}">{MAIL}</a></p>
<h2>In short</h2>
<ul><li>No cookies, no analytics or tracking tools, no advertising.</li>
<li>Fonts and maps are built into the page; opening it sends no data to Google or other third parties.</li>
<li>There are no forms and no user accounts.</li></ul>
<h2>Hosting</h2>
<p>The site is served by GitHub Pages (GitHub, Inc., 88 Colin P. Kelly Jr. Street, San Francisco, CA 94107, USA). When you open it, GitHub processes the connection data needed to deliver the page and keep the service secure, in particular your IP address. The legal basis is our legitimate interest in providing the site securely and reliably (Art. 6(1)(f) GDPR). Data may be transferred to the USA; according to GitHub, such transfers rely on the EU-US Data Privacy Framework and standard contractual clauses. Details: <a href="https://docs.github.com/site-policy/privacy-policies/github-general-privacy-statement">GitHub privacy statement</a>.</p>
<h2>Contact by email</h2>
<p>If you write to us, we use your details only to answer your message (Art. 6(1)(b) and (f) GDPR) and delete them once they are no longer needed for that. The mailbox is operated by IONOS SE (Elgendorfer Str. 57, 56410 Montabaur, Germany).</p>
<h2>External links</h2>
<p>The site links to sources and recordings of other providers, such as the Sprachatlas Salzburg. Only when you click such a link do you leave this site; the provider's own privacy policy then applies.</p>
<h2>Your rights</h2>
<p>You have the right of access, rectification, erasure, restriction of processing, data portability and objection. Write to <a href="mailto:{MAIL}">{MAIL}</a>. You may also lodge a complaint with the Austrian Data Protection Authority (Barichgasse 40–42, 1030 Vienna, <a href="https://www.dsb.gv.at">www.dsb.gv.at</a>).</p>'''

page('impressum.html', 'Impressum', IMP_DE, IMP_EN, '<a href="datenschutz.html">Datenschutz</a>')
page('datenschutz.html', 'Datenschutz', DS_DE, DS_EN, '<a href="impressum.html">Impressum</a>')
print('impressum.html, datenschutz.html written')
