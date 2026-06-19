// Render an HTML file -> PDF via Chrome DevTools Protocol.
// A4, 2cm margins, centered "n / total" page numbers in the footer.
//
//   node render_pdf.js <input.html> <output.pdf>
//
// Chrome/Chromium path: override with the CHROME env var, otherwise the first
// candidate found below is used. Needs a Node with a built-in WebSocket (v21+).
const { spawn } = require('child_process');
const http = require('http');
const fs = require('fs');
const path = require('path');

const CHROME_CANDIDATES = [
  process.env.CHROME,
  '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
  '/usr/bin/google-chrome',
  '/usr/bin/chromium',
  '/usr/bin/chromium-browser',
  '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
].filter(Boolean);
const CHROME = CHROME_CANDIDATES.find(p => { try { return fs.existsSync(p); } catch (e) { return false; } });

const PORT = Number(process.env.CDP_PORT || 9333);
const htmlArg = process.argv[2];
const outArg = process.argv[3];

if (!htmlArg || !outArg) {
  console.error('usage: node render_pdf.js <input.html> <output.pdf>');
  process.exit(2);
}
if (!CHROME) {
  console.error('no chrome/chromium found; set CHROME=/path/to/chrome');
  process.exit(2);
}

const htmlPath = path.resolve(htmlArg);
const outPath = path.resolve(outArg);
const fileUrl = 'file://' + htmlPath;

const sleep = (ms) => new Promise(r => setTimeout(r, ms));
function getJSON(url) {
  return new Promise((resolve, reject) => {
    http.get(url, res => { let d = ''; res.on('data', c => d += c); res.on('end', () => resolve(JSON.parse(d))); }).on('error', reject);
  });
}

(async () => {
  const proc = spawn(CHROME, [
    '--headless=new', '--disable-gpu', '--no-sandbox', '--hide-scrollbars',
    `--remote-debugging-port=${PORT}`, 'about:blank'
  ], { stdio: 'ignore' });

  // wait for devtools endpoint
  let ver;
  for (let i = 0; i < 50; i++) {
    try { ver = await getJSON(`http://127.0.0.1:${PORT}/json/version`); break; } catch (e) { await sleep(200); }
  }
  if (!ver) { console.error('no devtools'); proc.kill(); process.exit(1); }

  const ws = new WebSocket(ver.webSocketDebuggerUrl);
  await new Promise(r => ws.addEventListener('open', r));

  let id = 0; const pending = new Map();
  ws.addEventListener('message', ev => {
    const m = JSON.parse(ev.data);
    if (m.id && pending.has(m.id)) { pending.get(m.id)(m); pending.delete(m.id); }
  });
  const send = (method, params = {}, sessionId) => new Promise(res => {
    const mid = ++id; pending.set(mid, res);
    ws.send(JSON.stringify({ id: mid, method, params, sessionId }));
  });

  const { result: { targetId } } = await send('Target.createTarget', { url: 'about:blank' });
  const { result: { sessionId } } = await send('Target.attachToTarget', { targetId, flatten: true });

  await send('Page.enable', {}, sessionId);
  await send('Page.navigate', { url: fileUrl }, sessionId);
  await sleep(2000); // allow webfonts (CDN) + layout

  const inch = 0.7874015748; // 20mm
  const { result } = await send('Page.printToPDF', {
    printBackground: true,
    paperWidth: 8.2677, paperHeight: 11.6929, // A4
    marginTop: inch, marginBottom: inch, marginLeft: inch, marginRight: inch,
    preferCSSPageSize: false,
    displayHeaderFooter: true,
    headerTemplate: '<div></div>',
    footerTemplate: '<div style="width:100%; text-align:center; font-size:9px; color:#9aa3ad; font-family:Pretendard,\'Malgun Gothic\',sans-serif;"><span class="pageNumber"></span> / <span class="totalPages"></span></div>'
  }, sessionId);

  fs.writeFileSync(outPath, Buffer.from(result.data, 'base64'));
  console.log('written', outPath, fs.statSync(outPath).size, 'bytes');
  ws.close(); proc.kill();
  process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });
