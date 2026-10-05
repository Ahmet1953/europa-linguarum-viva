# Authoring source for content/salzburg.json and content/sources.json.
# Rule: every statement below is tied to a source id + locator. Dialect forms appear only as spelled in the source.
import json, os
os.makedirs('content', exist_ok=True)
CHECKED = "2026-10-03"

SOURCES = {
 "statistik-2026": {"tier":"A","kind":"official",
   "cite":"Statistik Austria (2026): Bevölkerung zu Jahresbeginn 2026. Pressemitteilung, 9.2.2026.",
   "url":"https://www.statistik.at/fileadmin/announcement/2026/02/20260209Bevoelkerung1.1.2026.pdf"},
 "zahlenspiegel-2025": {"tier":"A","kind":"official",
   "cite":"Land Salzburg, Landesstatistik (2025): Statistik Zahlenspiegel 2025. Stand 1.1.2025.",
   "url":"https://www.salzburg.gv.at/fileadmin/Dateien/Statistik/Zahlenspiegel/statistik-zahlenspiegel-2025.pdf"},
 "buelow-2019": {"tier":"A","kind":"academic",
   "cite":"Bülow, Lars (2019): Variation und Wandel der Pluralformen von sein in den Dialekten Salzburgs. JournaLIPP 7, 18–38.",
   "url":"https://lipp.ub.uni-muenchen.de/lipp/article/download/4879/2760/7842"},
 "sprachatlas-sbg": {"tier":"A","kind":"academic",
   "cite":"Scheutz, Hannes (2016/17): Sprachatlas Salzburg. Universität Salzburg, im Rahmen von Salzburg 20.16.",
   "url":"https://www.sprachatlas.at/salzburg/"},
 "duden": {"tier":"A","kind":"dictionary",
   "cite":"Duden online. Bibliographisches Institut, Berlin. Einträge mit regionaler Kennzeichnung.",
   "url":"https://www.duden.de/"},
 "orf-2017": {"tier":"B","kind":"press",
   "cite":"ORF Salzburg (10.2.2017): Alte Grenzen Salzburgs in Dialekten zu hören.",
   "url":"http://html.orf.at/oeka_1_3/sbg/news/stories/2825028/"},
 "meinbezirk-2017": {"tier":"B","kind":"press",
   "cite":"meinbezirk.at (13.2.2017): Salzburgs Dialekte im „Sprachatlas“ vereint.",
   "url":"https://www.meinbezirk.at/salzburg-stadt/c-lokales/salzburgs-dialekte-im-sprachatlas-vereint_a2021148"},
 "unesco-784": {"tier":"A","kind":"official",
   "cite":"UNESCO World Heritage Centre: Historic Centre of the City of Salzburg (Nr. 784), eingetragen 1996.",
   "url":"https://whc.unesco.org/en/list/784"},
 "tsg-mozart": {"tier":"B","kind":"institution",
   "cite":"Tourismus Salzburg GmbH, salzburg.info: Mozarts Geburtshaus.",
   "url":"https://salzburg.info/de/sehenswertes/top10/mozarts-geburtshaus"},
 "tsg-festspiele": {"tier":"B","kind":"institution",
   "cite":"Tourismus Salzburg GmbH, salzburg.info: Salzburger Festspiele – Chronik.",
   "url":"https://salzburg.info/de/salzburg/salzburger-festspiele/chronik"},
}

def S(i, loc): return {"id":i, "locator":loc, "checked":CHECKED}
D = lambda w: f"https://www.duden.de/rechtschreibung/{w}"

CARDS = [
# ---------------------------------------------------------------- state level
{"id":"sbg-overview","level":"state","type":"overview","cefr":None,
 "h":{"en":"Land Salzburg","de":"Land Salzburg"},
 "body":{
  "en":"""<dl class="kv"><dt>Capital</dt><dd>Salzburg</dd>
<dt>Population</dt><dd>573,748 <small>(1 Jan 2026)</small></dd>
<dt>Area</dt><dd>7,154.5 km²</dd>
<dt>Municipalities</dt><dd>119</dd>
<dt>Regions</dt><dd>Six political districts, known locally as the <i>Gaue</i>: City of Salzburg, Flachgau, Tennengau, Pongau, Pinzgau, Lungau</dd>
<dt>Neighbours</dt><dd>Bavaria (DE), Upper Austria, Styria, Carinthia, Tyrol; South Tyrol (IT) along the main Alpine ridge</dd></dl>
<p class="note">Tap a region on the map to open its card.</p>""",
  "de":"""<dl class="kv"><dt>Hauptstadt</dt><dd>Salzburg</dd>
<dt>Bevölkerung</dt><dd>573.748 <small>(1.1.2026)</small></dd>
<dt>Fläche</dt><dd>7.154,5 km²</dd>
<dt>Gemeinden</dt><dd>119</dd>
<dt>Regionen</dt><dd>Sechs politische Bezirke, im Land <i>Gaue</i> genannt: Stadt Salzburg, Flachgau, Tennengau, Pongau, Pinzgau, Lungau</dd>
<dt>Nachbarn</dt><dd>Bayern (DE), Oberösterreich, Steiermark, Kärnten, Tirol; Südtirol (IT) am Alpenhauptkamm</dd></dl>
<p class="note">Eine Region auf der Karte antippen, um ihre Karte zu öffnen.</p>"""},
 "sources":[S("statistik-2026","Tabelle Bundesländer, 1.1.2026"),S("zahlenspiegel-2025","Fläche 7.154,5 km²; 119 Ortsgemeinden; 6 politische Bezirke; Stand 1.1.2025")],
 "status":"source-verified"},

{"id":"sbg-layers","level":"state","type":"language-layers","cefr":"B1",
 "h":{"en":"A transition zone","de":"Ein Übergangsgebiet"},
 "body":{
  "en":"""<p>Salzburg lies between two large Bavarian dialect areas: <b>Central Bavarian</b> in the north and <b>Southern Bavarian</b> in the south. Above the dialects sits Austrian Standard German, used in school, media and offices.</p>
<p>Lars Bülow (University of Salzburg) describes it this way: the Flachgau is West Central Bavarian, the Lungau is dominated by Southern Bavarian features, and the regions in between form a South-Central Bavarian transition zone.</p>
<div class="views"><h4>Open question: where does the Pinzgau belong?</h4>
<div class="view-a"><b>View 1 · Bülow 2019</b><span>Transition zone, together with Tennengau and Pongau.</span></div>
<div class="view-b"><b>View 2 · Scheutz, reported by ORF 2017</b><span>Southern Bavarian, together with the Lungau.</span></div>
<p class="note">Both views are shown until a dialectologist settles it. Scheutz also notes that very old forms survive in the <i>Oberpinzgau</i>, which may explain the difference.</p></div>""",
  "de":"""<p>Salzburg liegt zwischen zwei großen bairischen Dialekträumen: dem <b>Mittelbairischen</b> im Norden und dem <b>Südbairischen</b> im Süden. Darüber liegt das österreichische Standarddeutsch in Schule, Medien und Ämtern.</p>
<p>Lars Bülow (Universität Salzburg) schreibt: „Im Norden Salzburgs (im Flachgau) finden sich westmittelbairische Dialekte, ganz im Südosten (im Lungau) dominieren südbairische Dialektmerkmale, und die Gebiete dazwischen (Tennengau, Pongau und Pinzgau) zählen zum südmittelbairischen Übergangsgebiet.“</p>
<div class="views"><h4>Offene Frage: Wohin gehört der Pinzgau?</h4>
<div class="view-a"><b>Sicht 1 · Bülow 2019</b><span>Übergangsgebiet, mit Tennengau und Pongau.</span></div>
<div class="view-b"><b>Sicht 2 · Scheutz, laut ORF 2017</b><span>Südbairisch, mit dem Lungau.</span></div>
<p class="note">Beide Sichten bleiben stehen, bis eine Dialektologin oder ein Dialektologe entscheidet. Scheutz verweist zudem auf sehr alte Formen im <i>Oberpinzgau</i>, was den Unterschied erklären könnte.</p></div>"""},
 "sources":[S("buelow-2019","S. 19"),S("orf-2017","Absatz „Einflüsse aus unterschiedlichen Richtungen“"),S("meinbezirk-2017","Zitat Scheutz zu Lungau und Oberpinzgau")],
 "status":"source-verified","open_question":"pinzgau-classification"},

{"id":"sbg-words","level":"state","type":"standard-vocabulary","cefr":"A2",
 "h":{"en":"Austrian words, carefully labelled","de":"Österreichische Wörter, genau gekennzeichnet"},
 "body":{
  "en":"""<p>Standard German has national varieties. These words are standard in Austria. The right-hand column shows exactly how the Duden labels each one.</p>
<table class="pairs"><thead><tr><th>Word</th><th>In Germany</th><th>Duden label</th></tr></thead><tbody>
<tr><td>der Jänner</td><td>Januar</td><td>Austrian, more rarely South German</td></tr>
<tr><td>die Marille</td><td>Aprikose</td><td>Austrian, otherwise regional</td></tr>
<tr><td>der Topfen</td><td>Quark</td><td>Bavarian, Austrian</td></tr>
<tr><td>das Sackerl</td><td>Beutel, Tüte</td><td>Bavarian, Austrian</td></tr>
<tr><td>der Verlängerte</td><td>—</td><td>Austrian: coffee made with double the water</td></tr>
<tr><td>der Paradeiser</td><td>Tomate</td><td><b>South and East Austrian</b></td></tr></tbody></table>
<p class="note">The last row is a reminder that “Austrian” is not one block: the Duden marks <i>Paradeiser</i> as south and east Austrian, so it is not presented here as a Salzburg word.</p>""",
  "de":"""<p>Das Standarddeutsche hat nationale Varietäten. Diese Wörter sind in Österreich standardsprachlich. Die rechte Spalte zeigt genau, wie der Duden sie kennzeichnet.</p>
<table class="pairs"><thead><tr><th>Wort</th><th>In Deutschland</th><th>Duden-Kennzeichnung</th></tr></thead><tbody>
<tr><td>der Jänner</td><td>Januar</td><td>österreichisch, seltener süddeutsch</td></tr>
<tr><td>die Marille</td><td>Aprikose</td><td>österreichisch, sonst landschaftlich</td></tr>
<tr><td>der Topfen</td><td>Quark</td><td>bayrisch, österreichisch</td></tr>
<tr><td>das Sackerl</td><td>Beutel, Tüte</td><td>bayrisch, österreichisch</td></tr>
<tr><td>der Verlängerte</td><td>—</td><td>österreichisch: mit der doppelten Menge Wasser zubereiteter Kaffee</td></tr>
<tr><td>der Paradeiser</td><td>Tomate</td><td><b>süd- und ostösterreichisch</b></td></tr></tbody></table>
<p class="note">Die letzte Zeile erinnert daran, dass „österreichisch“ kein Block ist: Der Duden kennzeichnet <i>Paradeiser</i> als süd- und ostösterreichisch; es wird hier daher nicht als Salzburger Wort ausgegeben.</p>"""},
 "sources":[S("duden","Jänner, Marille, Topfen, Sackerl, Verlängerter, Paradeiser")],
 "links":[D("Jaenner"),D("Marille"),D("Topfen"),D("Sackerl"),D("Verlaengerter"),D("Paradeiser")],
 "status":"source-verified"},

{"id":"sbg-phrases","level":"state","type":"first-phrases","cefr":"A1",
 "h":{"en":"First phrases","de":"Erste Sätze"},
 "body":{
  "en":"""<p>A1 learners learn Austrian Standard German. The dialect is something to recognise, not to imitate.</p>
<div class="phrase"><b>Grüß Gott!</b><span>Hello. Duden: Austrian, otherwise regional greeting</span></div>
<div class="phrase"><b>Servus!</b><span>Hi / bye among friends. Duden: especially Bavarian, Austrian</span></div>
<div class="phrase"><b>Einen Verlängerten, bitte.</b><span>A coffee lengthened with hot water, please.</span></div>
<div class="phrase"><b>Wo ist die Getreidegasse, bitte?</b><span>Where is Getreidegasse, please?</span></div>
<div class="phrase"><b>Danke, auf Wiedersehen!</b><span>Thank you, goodbye!</span></div>""",
  "de":"""<p>Auf A1 wird österreichisches Standarddeutsch gelernt. Den Dialekt soll man erkennen, nicht nachahmen.</p>
<div class="phrase"><b>Grüß Gott!</b><span>Duden: österreichische, sonst landschaftliche Grußformel</span></div>
<div class="phrase"><b>Servus!</b><span>Freundschaftlicher Gruß. Duden: besonders bayrisch, österreichisch</span></div>
<div class="phrase"><b>Einen Verlängerten, bitte.</b><span>Kaffee mit der doppelten Menge Wasser</span></div>
<div class="phrase"><b>Wo ist die Getreidegasse, bitte?</b><span>Nach dem Weg fragen</span></div>
<div class="phrase"><b>Danke, auf Wiedersehen!</b><span>Sich verabschieden</span></div>"""},
 "sources":[S("duden","Gott (Wendung „grüß Gott“), servus, Verlängerter")],
 "links":[D("Gott"),D("servus"),D("Verlaengerter")],
 "status":"source-verified"},

{"id":"sbg-seid","level":"state","type":"dialect-window","cefr":"B2",
 "h":{"en":"One vowel, five villages","de":"Ein Vokal, fünf Orte"},
 "body":{
  "en":"""<p>How do Salzburg dialects say <i>ihr seid</i> (“you are”, plural)? Bülow studies whether the stem vowel is a simple <b>a</b> or the diphthong <b>ai</b>, for example <i>(es) hadds</i> vs. <i>haidds</i>.</p>
<table class="pairs"><thead><tr><th>Place</th><th>Region</th><th>Vowel</th></tr></thead><tbody>
<tr><td>Berndorf</td><td>Flachgau</td><td><i class="vdot a"></i>a only</td></tr>
<tr><td>Maria Alm</td><td>Pinzgau</td><td><i class="vdot a"></i>a only</td></tr>
<tr><td>Rußbach</td><td>Tennengau</td><td><i class="vdot ai"></i>ai preferred</td></tr>
<tr><td>Hüttschlag</td><td>Pongau</td><td><i class="vdot ai"></i>ai preferred</td></tr>
<tr><td>Lessach</td><td>Lungau</td><td><i class="vdot ai"></i>ai preferred</td></tr></tbody></table>
<p>Data: speakers recorded by the project <i>Deutsch in Österreich</i> (DiÖ), as analysed by Bülow.</p>
<p>Change over time: among older rural speakers interviewed for the Sprachatlas in 2016/17, the simple <b>a</b> makes up only 62.5% of the Flachgau examples, while in the Lungau the diphthong now appears in 100% of cases.</p>
<p class="note">For recognition (B2 and above), not for production.</p>""",
  "de":"""<p>Wie heißt <i>ihr seid</i> in Salzburger Dialekten? Bülow untersucht, ob der Stammvokal ein einfaches <b>a</b> oder der Diphthong <b>ai</b> ist, z. B. <i>(es) hadds</i> vs. <i>haidds</i>.</p>
<table class="pairs"><thead><tr><th>Ort</th><th>Gau</th><th>Vokal</th></tr></thead><tbody>
<tr><td>Berndorf</td><td>Flachgau</td><td><i class="vdot a"></i>nur a</td></tr>
<tr><td>Maria Alm</td><td>Pinzgau</td><td><i class="vdot a"></i>nur a</td></tr>
<tr><td>Rußbach</td><td>Tennengau</td><td><i class="vdot ai"></i>ai bevorzugt</td></tr>
<tr><td>Hüttschlag</td><td>Pongau</td><td><i class="vdot ai"></i>ai bevorzugt</td></tr>
<tr><td>Lessach</td><td>Lungau</td><td><i class="vdot ai"></i>ai bevorzugt</td></tr></tbody></table>
<p>Daten: Gewährspersonen des Projekts <i>Deutsch in Österreich</i> (DiÖ), ausgewertet von Bülow.</p>
<p>Wandel: „Im Flachgau macht der Monophthong bei den NORM/Fs, die 2016/17 für den Sprachatlas Salzburg befragt wurden, nur noch 62,5% der Belege aus, während im Lungau nun in 100% der Fälle der Diphthong erscheint.“</p>
<p class="note">Zum Erkennen (ab B2), nicht zum Nachsprechen.</p>"""},
 "sources":[S("buelow-2019","S. 18 (Variable), S. 29 (62,5 %), S. 30 (Ortspunkte DiÖ)")],
 "status":"source-verified"},

{"id":"sbg-border","level":"state","type":"border-story","cefr":"B2",
 "h":{"en":"A border the dialect remembers","de":"Eine Grenze, die der Dialekt erinnert"},
 "body":{
  "en":"""<p>Until the Napoleonic Wars, the towns between Piding and Tittmoning, now in Bavaria, belonged to the Archbishopric of Salzburg.</p>
<p>When Hannes Scheutz recorded speakers for the Sprachatlas, he found a surprise: in the Bavarian towns of <b>Teisendorf</b>, <b>Surheim</b> and <b>Schönau</b>, the old Salzburg base dialect had survived <i>better</i> than on Salzburg’s own territory.</p>
<p>A state border is not a language border, and a language can keep a border that no longer exists.</p>""",
  "de":"""<p>Bis zu den napoleonischen Kriegen gehörten die heute bayerischen Orte zwischen Piding und Tittmoning zum Erzstift Salzburg.</p>
<p>Bei den Aufnahmen für den Sprachatlas fand Hannes Scheutz eine Überraschung: In den bayerischen Orten <b>Teisendorf</b>, <b>Surheim</b> und <b>Schönau</b> hatte sich die Salzburger Grundmundart <i>besser</i> erhalten als auf Salzburger Gebiet.</p>
<p>Eine Staatsgrenze ist keine Sprachgrenze, und eine Sprache kann eine Grenze bewahren, die es nicht mehr gibt.</p>"""},
 "sources":[S("orf-2017","Absatz „Mundart in bayrischen Orten am ursprünglichsten“")],
 "status":"source-verified","note":"Press report (tier B); the primary source is the Sprachatlas itself."},

{"id":"sbg-atlas","level":"state","type":"source-spotlight","cefr":"B1",
 "h":{"en":"Listen: the Salzburg language atlas","de":"Hören: der Sprachatlas Salzburg"},
 "body":{
  "en":"""<p>In 2016/17 Hannes Scheutz recorded the dialects of 32 places, including some in neighbouring Bavaria. At each place he interviewed one older and one younger speaker and worked through a questionnaire of about 500 questions.</p>
<p>The atlas lets you compare places and generations by ear. We link to it rather than copy it: the recordings belong to the atlas.</p>
<blockquote>“For documenting original dialect landscapes it is high time, sometimes already five minutes past twelve.”<cite>Hannes Scheutz, 2017 (translated)</cite></blockquote>
<a class="gmap" href="https://www.sprachatlas.at/salzburg/" target="_blank" rel="noopener">Open the Sprachatlas Salzburg <span aria-hidden="true">↗</span></a>""",
  "de":"""<p>2016/17 nahm Hannes Scheutz die Dialekte von 32 Orten auf, einige davon im benachbarten Bayern. An jedem Ort befragte er eine ältere und eine jüngere Person mit einem Fragebogen von rund 500 Fragen.</p>
<p>Im Atlas lassen sich Orte und Generationen hörend vergleichen. Wir verlinken, statt zu kopieren: Die Aufnahmen gehören dem Atlas.</p>
<blockquote>„Für eine Dokumentation ursprünglicher Dialektlandschaften ist es höchste Zeit, manchmal auch bereits fünf Minuten nach Zwölf.“<cite>Hannes Scheutz, 2017</cite></blockquote>
<a class="gmap" href="https://www.sprachatlas.at/salzburg/" target="_blank" rel="noopener">Sprachatlas Salzburg öffnen <span aria-hidden="true">↗</span></a>"""},
 "sources":[S("sprachatlas-sbg","Einführung: 32 Aufnahmeorte"),S("orf-2017","ältere und jüngere Generation; rund 500 Fragen"),S("meinbezirk-2017","Zitat Scheutz")],
 "status":"source-verified"},

{"id":"sbg-culture","level":"state","type":"culture","cefr":"A2",
 "h":{"en":"A city of music","de":"Eine Stadt der Musik"},
 "body":{
  "en":"""<p>Wolfgang Amadeus Mozart was born on 27 January 1756 in the Hagenauer House at Getreidegasse 9. The Mozarteum Foundation first opened a museum there in 1880.</p>
<p>The Salzburg Festival began on 22 August 1920 with <i>Jedermann</i> on the Cathedral Square, championed by Max Reinhardt, Hugo von Hofmannsthal and Richard Strauss.</p>
<p>The historic centre has been a UNESCO World Heritage Site since 1996.</p>
<a class="gmap" href="https://www.google.com/maps/search/?api=1&query=Mozarts+Geburtshaus,+Getreidegasse+9,+Salzburg" target="_blank" rel="noopener">Mozart’s birthplace in Google Maps <span aria-hidden="true">↗</span></a>""",
  "de":"""<p>Wolfgang Amadeus Mozart wurde am 27. Jänner 1756 im Hagenauer Haus in der Getreidegasse 9 geboren. 1880 eröffnete die Internationale Stiftung Mozarteum dort erstmals ein Museum.</p>
<p>Die Salzburger Festspiele begannen am 22. August 1920 mit dem <i>Jedermann</i> auf dem Domplatz, getragen von Max Reinhardt, Hugo von Hofmannsthal und Richard Strauss.</p>
<p>Die Altstadt ist seit 1996 UNESCO-Welterbe.</p>
<a class="gmap" href="https://www.google.com/maps/search/?api=1&query=Mozarts+Geburtshaus,+Getreidegasse+9,+Salzburg" target="_blank" rel="noopener">Mozarts Geburtshaus in Google Maps <span aria-hidden="true">↗</span></a>"""},
 "sources":[S("tsg-mozart","Geburtsdatum, Adresse, Museum 1880"),S("tsg-festspiele","Eintrag 1920"),S("unesco-784","Inscription 1996")],
 "status":"source-verified"},

# ---------------------------------------------------------------- Gau level
{"id":"gau-501","level":"gau","gau":"501","type":"gau","cefr":None,
 "h":{"en":"City of Salzburg","de":"Stadt Salzburg"},
 "body":{
  "en":"""<p>The state capital is its own district, surrounded by the Flachgau.</p>
<p>The sources used here give the city no separate dialect classification. It lies in the north, the area Bülow calls West Central Bavarian.</p>
<p class="gap">Content gap: a source on present-day urban speech in Salzburg is still missing. Suggestions welcome.</p>""",
  "de":"""<p>Die Landeshauptstadt ist ein eigener Bezirk, umgeben vom Flachgau.</p>
<p>Die hier verwendeten Quellen ordnen die Stadt dialektal nicht gesondert ein. Sie liegt im Norden, den Bülow als westmittelbairisch beschreibt.</p>
<p class="gap">Inhaltslücke: Eine Quelle zur heutigen Stadtsprache Salzburgs fehlt noch. Hinweise willkommen.</p>"""},
 "sources":[S("buelow-2019","S. 19")],"status":"source-verified"},

{"id":"gau-503","level":"gau","gau":"503","type":"gau","cefr":None,
 "h":{"en":"Flachgau","de":"Flachgau"},
 "body":{
  "en":"""<dl class="kv"><dt>Dialect area</dt><dd>West Central Bavarian (Bülow); Central Bavarian (Scheutz)</dd><dt>Recorded place</dt><dd>Berndorf (DiÖ)</dd></dl>
<p>Scheutz: in the north, influences from eastern Austria are clearly audible, and the old Salzburg forms have been overlaid on a large scale.</p>
<p>In Berndorf, <i>ihr seid</i> is heard only with a simple <b>a</b>. Among older speakers in 2016/17, that form makes up 62.5% of Flachgau examples.</p>""",
  "de":"""<dl class="kv"><dt>Dialektraum</dt><dd>westmittelbairisch (Bülow); mittelbairisch (Scheutz)</dd><dt>Aufnahmeort</dt><dd>Berndorf (DiÖ)</dd></dl>
<p>Scheutz: „Im Norden sehen wir eine großflächige Überformung der Altsalzburger Formen durch ostösterreichische Einflüsse.“</p>
<p>In Berndorf erscheint bei <i>ihr seid</i> ausschließlich der Monophthong <b>a</b>; bei den älteren Befragten 2016/17 macht er im Flachgau 62,5 % der Belege aus.</p>"""},
 "sources":[S("buelow-2019","S. 19, 29, 30"),S("orf-2017","Flachgau mittelbairisch"),S("meinbezirk-2017","Zitat Scheutz")],"status":"source-verified"},

{"id":"gau-502","level":"gau","gau":"502","type":"gau","cefr":None,
 "h":{"en":"Tennengau","de":"Tennengau"},
 "body":{
  "en":"""<dl class="kv"><dt>Dialect area</dt><dd>South-Central Bavarian transition zone (Bülow)</dd><dt>Recorded place</dt><dd>Rußbach (DiÖ)</dd></dl>
<p>In Rußbach, speakers prefer the diphthong <b>ai</b> in <i>ihr seid</i>.</p>""",
  "de":"""<dl class="kv"><dt>Dialektraum</dt><dd>südmittelbairisches Übergangsgebiet (Bülow)</dd><dt>Aufnahmeort</dt><dd>Rußbach (DiÖ)</dd></dl>
<p>In Rußbach bevorzugen die Gewährspersonen bei <i>ihr seid</i> den Diphthong <b>ai</b>.</p>"""},
 "sources":[S("buelow-2019","S. 19, 30")],"status":"source-verified"},

{"id":"gau-504","level":"gau","gau":"504","type":"gau","cefr":None,
 "h":{"en":"Pongau","de":"Pongau"},
 "body":{
  "en":"""<dl class="kv"><dt>Dialect area</dt><dd>South-Central Bavarian transition zone (Bülow)</dd><dt>Recorded place</dt><dd>Hüttschlag (DiÖ)</dd></dl>
<p>In Hüttschlag, speakers prefer the diphthong <b>ai</b> in <i>ihr seid</i>.</p>""",
  "de":"""<dl class="kv"><dt>Dialektraum</dt><dd>südmittelbairisches Übergangsgebiet (Bülow)</dd><dt>Aufnahmeort</dt><dd>Hüttschlag (DiÖ)</dd></dl>
<p>In Hüttschlag bevorzugen die Gewährspersonen bei <i>ihr seid</i> den Diphthong <b>ai</b>.</p>"""},
 "sources":[S("buelow-2019","S. 19, 30")],"status":"source-verified"},

{"id":"gau-506","level":"gau","gau":"506","type":"gau","cefr":None,
 "h":{"en":"Pinzgau","de":"Pinzgau"},
 "body":{
  "en":"""<dl class="kv"><dt>Dialect area</dt><dd><b>Sources differ:</b> transition zone (Bülow) · Southern Bavarian (Scheutz, ORF)</dd><dt>Recorded place</dt><dd>Maria Alm (DiÖ)</dd></dl>
<p>Scheutz: in the Lungau and the <b>Oberpinzgau</b>, remnants of very old dialect forms survive, often strikingly similar to the southernmost inner-Alpine Bavarian dialects, such as those of South Tyrol.</p>
<p>In Maria Alm, <i>ihr seid</i> is heard only with a simple <b>a</b>, as in the Flachgau.</p>""",
  "de":"""<dl class="kv"><dt>Dialektraum</dt><dd><b>Quellen uneinig:</b> Übergangsgebiet (Bülow) · südbairisch (Scheutz, ORF)</dd><dt>Aufnahmeort</dt><dd>Maria Alm (DiÖ)</dd></dl>
<p>Scheutz: „Im Lungau und Oberpinzgau finden wir noch Reste ganz alter Dialektformen, die vielfach frappierende Ähnlichkeiten mit den südlichsten inneralpinen bairischen Dialekten, zum Beispiel Südtirol, aufweisen.“</p>
<p>In Maria Alm erscheint bei <i>ihr seid</i> ausschließlich der Monophthong <b>a</b>, wie im Flachgau.</p>"""},
 "sources":[S("buelow-2019","S. 19, 30"),S("orf-2017","Pinzgau südbairisch"),S("meinbezirk-2017","Zitat Scheutz")],
 "status":"source-verified","open_question":"pinzgau-classification"},

{"id":"gau-505","level":"gau","gau":"505","type":"gau","cefr":None,
 "h":{"en":"Lungau","de":"Lungau"},
 "body":{
  "en":"""<dl class="kv"><dt>Dialect area</dt><dd>Southern Bavarian (Bülow and Scheutz agree)</dd><dt>Recorded place</dt><dd>Lessach (DiÖ)</dd></dl>
<p>Scheutz hears a strong linguistic link to Tyrol and South Tyrol here, with remnants of very old dialect forms.</p>
<p>In Lessach, speakers prefer the diphthong <b>ai</b> in <i>ihr seid</i>. Among older speakers in 2016/17, the diphthong appears in 100% of Lungau examples.</p>""",
  "de":"""<dl class="kv"><dt>Dialektraum</dt><dd>südbairisch (Bülow und Scheutz übereinstimmend)</dd><dt>Aufnahmeort</dt><dd>Lessach (DiÖ)</dd></dl>
<p>Scheutz hört hier eine starke sprachliche Verbindung zu Tirol und Südtirol, mit Resten ganz alter Dialektformen.</p>
<p>In Lessach bevorzugen die Gewährspersonen bei <i>ihr seid</i> den Diphthong <b>ai</b>; bei den älteren Befragten 2016/17 erscheint er im Lungau in 100 % der Fälle.</p>"""},
 "sources":[S("buelow-2019","S. 19, 29, 30"),S("orf-2017","Lungau südbairisch"),S("meinbezirk-2017","Zitat Scheutz")],"status":"source-verified"},
]

# ---------------------------------------------------------------- Sprachatlas recording places (read 2026-10-05)
ATLAS_PLACES = {"503":["Dorfbeuern","St. Georgen","Seekirchen","Anthering","Elsbethen","Faistenau","Fuschl","Strobl"],
 "502":["Dürrnberg/Hallein","St. Koloman","Abtenau","Rußbach"],"504":["Mühlbach","Forstau","Hüttschlag"],
 "506":["Unken","St. Martin","Maria Alm","Maishofen","Taxenbach","Fusch","Rauris","Stuhlfelden","Wald"],
 "505":["Zederhaus","Muhr","Mariapfarr","Lasaberg/Tamsweg"],"BY":["Petting","Teisendorf","Surheim","Schönau am Königssee"]}
assert sum(len(v) for v in ATLAS_PLACES.values()) == 32
SA = "https://www.sprachatlas.at/salzburg/data/atlas.html"
SG = "https://www.sprachatlas.at/salzburg/data/generationen.html"
LOC = "Dialektvergleich-Karte: Ortsnamen der 32 Aufnahmeorte (per Mouseover gelesen, 5.10.2026)"
def link(en, de): return {"en": f'<a class="gmap" href="{SA}" target="_blank" rel="noopener">{en} <span aria-hidden="true">↗</span></a>',
                          "de": f'<a class="gmap" href="{SA}" target="_blank" rel="noopener">{de} <span aria-hidden="true">↗</span></a>'}
byid = {c["id"]: c for c in CARDS}
for g, names in ATLAS_PLACES.items():
    if g == "BY": continue
    c = byid[f"gau-{g}"]; L = link("Listen in the Sprachatlas", "Im Sprachatlas anhören")
    c["body"]["en"] += f'<p><b>Sprachatlas recording places ({len(names)}):</b> {", ".join(names)}. Shown as squares on the map; each place has an older and a younger speaker.</p>' + L["en"]
    c["body"]["de"] += f'<p><b>Aufnahmeorte des Sprachatlas ({len(names)}):</b> {", ".join(names)}. Auf der Karte als Quadrate; je Ort eine ältere und eine jüngere Gewährsperson.</p>' + L["de"]
    c["sources"].append(S("sprachatlas-sbg", LOC))
c = byid["gau-501"]
c["body"]["en"] = c["body"]["en"].replace('<p class="gap">', '<p>The Sprachatlas has no recording place inside the city; the nearest are Anthering and Elsbethen in the Flachgau.</p><p class="gap">')
c["body"]["de"] = c["body"]["de"].replace('<p class="gap">', '<p>Der Sprachatlas hat keinen Aufnahmeort in der Stadt selbst; am nächsten liegen Anthering und Elsbethen im Flachgau.</p><p class="gap">')
c["sources"].append(S("sprachatlas-sbg", LOC))
c = byid["sbg-atlas"]
dist_en = "Flachgau 8, Tennengau 4, Pongau 3, Pinzgau 9, Lungau 4, Bavaria 4"
dist_de = "Flachgau 8, Tennengau 4, Pongau 3, Pinzgau 9, Lungau 4, Bayern 4"
c["body"]["en"] = c["body"]["en"].replace("<blockquote>", f'<p><b>The 32 places on our map</b> (squares): {dist_en}. Not one lies inside the city of Salzburg.</p><blockquote>')
c["body"]["de"] = c["body"]["de"].replace("<blockquote>", f'<p><b>Die 32 Orte auf unserer Karte</b> (Quadrate): {dist_de}. Keiner liegt in der Stadt Salzburg selbst.</p><blockquote>')
c["body"]["en"] += f'<a class="gmap" href="{SG}" target="_blank" rel="noopener">Compare the generations <span aria-hidden="true">↗</span></a>'
c["body"]["de"] += f'<a class="gmap" href="{SG}" target="_blank" rel="noopener">Generationen vergleichen <span aria-hidden="true">↗</span></a>'
c["sources"].append(S("sprachatlas-sbg", LOC))
c = byid["sbg-border"]
c["body"]["en"] += '<p>All three towns are recording places of the Sprachatlas, together with Petting. The map shows the four Bavarian places as squares.</p>' + link("Listen in the Sprachatlas","Im Sprachatlas anhören")["en"]
c["body"]["de"] += '<p>Alle drei Orte sind Aufnahmeorte des Sprachatlas, dazu Petting. Die Karte zeigt die vier bayerischen Orte als Quadrate.</p>' + link("Listen in the Sprachatlas","Im Sprachatlas anhören")["de"]
c["sources"].append(S("sprachatlas-sbg", LOC))
c = byid["sbg-seid"]
c["body"]["en"] = c["body"]["en"].replace('<p class="note">For recognition', '<p>Three of these five places, Maria Alm, Rußbach and Hüttschlag, are also recording places of the Sprachatlas: two independent studies meet in the same villages.</p><p class="note">For recognition')
c["body"]["de"] = c["body"]["de"].replace('<p class="note">Zum Erkennen', '<p>Drei dieser fünf Orte, Maria Alm, Rußbach und Hüttschlag, sind auch Aufnahmeorte des Sprachatlas: Zwei unabhängige Studien treffen sich in denselben Dörfern.</p><p class="note">Zum Erkennen')
c["sources"].append(S("sprachatlas-sbg", LOC))


for c in CARDS:
    c.setdefault("expert_review", None)
    c.setdefault("produced_by", "claude-opus-5-5")
    c.setdefault("verified_by", [])
    c["text_tr"] = None
    assert c["sources"], c["id"]
    for s in c["sources"]: assert s["id"] in SOURCES, s

OPEN = [{"id":"pinzgau-classification",
  "en":"Is the Pinzgau Southern Bavarian (Scheutz, reported by ORF 2017) or part of the South-Central Bavarian transition zone (Bülow 2019)?",
  "de":"Ist der Pinzgau südbairisch (Scheutz, laut ORF 2017) oder Teil des südmittelbairischen Übergangsgebiets (Bülow 2019)?"}]

json.dump({"state":"5","updated":CHECKED,"cards":CARDS,"open_questions":OPEN}, open('content/salzburg.json','w'), ensure_ascii=False, indent=1)
json.dump(SOURCES, open('content/sources.json','w'), ensure_ascii=False, indent=1)
print(len(CARDS), "cards,", len(SOURCES), "sources")
open('content.js','w').write("const CONTENT = " + json.dumps({"cards":CARDS,"open_questions":OPEN}, ensure_ascii=False) + ";\nconst SOURCES = " + json.dumps(SOURCES, ensure_ascii=False) + ";\n")
