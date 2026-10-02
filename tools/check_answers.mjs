// 회로도 정답 검사: 18개 과제마다 정답 배선을 놓고 시뮬레이터로 동작 사항(answer_scenarios.mjs)대로 움직이는지,
// 단자를 다르게 골라도 정답으로 보는지, 틀린 배선은 잡아내는지 확인한다.
// 사용법 (저장소 맨 위 폴더에서, Node 22 이상·Chrome·Python 필요):  node tools/check_answers.mjs
import {spawn} from 'node:child_process';
import {mkdtempSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {join, dirname} from 'node:path';
import {fileURLToPath} from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url)), ROOT = join(HERE, '..'), PORT = 8765, DBG = 9333;
const srv = spawn(process.platform === 'win32' ? 'py' : 'python3', ['-m', 'http.server', String(PORT), '--directory', join(ROOT, 'docs')], {stdio: 'ignore'});
const chrome = spawn('C:/Program Files/Google/Chrome/Application/chrome.exe', ['--headless=new', `--remote-debugging-port=${DBG}`,
  `--user-data-dir=${mkdtempSync(join(tmpdir(), 'cpw-'))}`, '--window-size=1400,900', 'about:blank'], {stdio: 'ignore'});
const sleep = ms => new Promise(r => setTimeout(r, ms));
let ws, seq = 0; const pend = new Map();
try {
  for (let i = 0; ; i++) { try { const l = await (await fetch(`http://127.0.0.1:${DBG}/json`)).json(); const pg = l.find(t => t.type === 'page'); if (pg) { ws = new WebSocket(pg.webSocketDebuggerUrl); break; } } catch (e) { if (i > 50) throw e; } await sleep(200); }
  await new Promise(r => ws.onopen = r);
  ws.onmessage = m => { const d = JSON.parse(m.data); if (d.id && pend.has(d.id)) { pend.get(d.id)(d); pend.delete(d.id); } };
  const send = (method, params) => new Promise(r => { const id = ++seq; pend.set(id, r); ws.send(JSON.stringify({id, method, params})); });
  const ev = async expr => { const r = await send('Runtime.evaluate', {expression: expr, awaitPromise: true, returnByValue: true}); if (r.result.exceptionDetails) throw new Error(JSON.stringify(r.result.exceptionDetails).slice(0, 800)); return r.result.result.value; };
  await send('Page.enable'); await send('Runtime.enable');
  await send('Page.navigate', {url: `http://localhost:${PORT}/?t=${Date.now()}`});
  for (let i = 0; i < 50; i++) { await sleep(200); if (await ev("typeof concreteAnswer==='function'&&!!S.parts.length").catch(() => false)) break; }
  const SC = (await import('./answer_scenarios.mjs')).default;
  const res = await ev(`(${String(runAll)})(${JSON.stringify(SC)})`);
  let bad = 0;
  for (const [n, r] of Object.entries(res)) { const ok = !r.err.length; if (!ok) bad++; console.log(`${n.padStart(2)} ${ok ? 'OK ' : 'BAD'} 전선 ${r.wires}, 비교 빠짐 ${r.miss}/잘못 ${r.extra}, 3가닥 ${r.over}, 경로없음 ${r.noRoute}${ok ? '' : '\n    ' + r.err.join('\n    ')}`); }
  console.log(bad ? `실패 ${bad}개` : '모두 통과');
  process.exitCode = bad ? 1 : 0;
} finally { try { ws && ws.close(); } catch (e) {} chrome.kill(); srv.kill(); }

function runAll(SC) {
  const out = {};
  for (let n = 1; n <= 18; n++) {
    const err = [];
    loadProblem(n); answerWires();
    for (const p of S.parts) { if (p.type === 'timer') p.set = 2; if (p.type === 'flicker') p.set = 4; }
    const cur = elecNets(), c = compare(concreteAnswer(n, cur).map(x => x.pins), cur);
    if (c.miss.length || c.extra.length) err.push('자기 비교 불일치 ' + JSON.stringify(c).slice(0, 300));
    const cnt = wireCounts(), over = Object.values(cnt).filter(v => v > 2).length;
    const A = parseAns(n); for (const e of A.els.values()) if (e.nodes.length !== 2 || !e.kind) err.push('정답 표기 오류 ' + e.id);
    setMode('sim'); sim.power = true;
    const L = l => S.parts.find(p => p.label === l), R = l => rtOf(L(l).id);
    const run = s => { for (let t = 0; t < s - 1e-9; t += .05) simStep(.05); };
    run(.3);
    if (sim.fault) err.push('전원 투입 시 ' + sim.fault.msg);
    if (!R('EOCR').powered) err.push('EOCR 전원 없음');
    const st = l => l === 'M1' ? R('TB2').run !== 0 : l === 'M2' ? R('TB3').run !== 0 : ['RL', 'GL', 'YL', 'WL', 'BZ'].includes(l) ? R(l).lit : R(l).coil;
    let step = 0;
    for (const raw of SC[n].split(';').map(s => s.trim()).filter(Boolean)) {
      step++;
      const [a, b] = raw.split(/\s+/);
      if (a === 'ss') { R('SS').pos = b === 'A' ? 1 : 0; run(.3); }
      else if (a === 'lvl') { R('TB4').level = +b; run(.3); }
      else if (a === 'ls1' || a === 'ls2') { R('TB4')[a] = b === '1'; run(.3); }
      else if (a === 'pb') { R(b).pressed = true; run(.3); R(b).pressed = false; run(.3); }
      else if (a === 'hold') { R(b).pressed = true; run(.3); }
      else if (a === 'release') { R(b).pressed = false; run(.3); }
      else if (a === 'wait') run(+b);
      else if (a === 'trip') { R('EOCR').trip = true; run(.3); }
      else if (a === 'reset') { R('EOCR').trip = false; run(.3); }
      else for (const tok of raw.split(/\s+/)) {
        const off = tok.endsWith('-'), l = off ? tok.slice(0, -1) : tok;
        if (!/^M[12]$/.test(l) && !L(l)) { err.push(`#${step} 기구 없음 ${l}`); continue; }
        if (st(l) === off) err.push(`#${step} [${raw}] ${l}이(가) ${off ? '켜져' : '꺼져'} 있음`);
      }
      if (sim.fault) { err.push(`#${step} ${sim.fault.msg}`); break; }
    }
    setMode('place');
    /* 단자를 다르게 고른 배선: 릴레이 a접점 1-3↔8-6, 코일·램프 방향, 퓨즈 홀더, EOCR 10↔11 등을 바꿔도 정답이어야 한다 */
    const PERM = {relay: {1: 8, 8: 1, 3: 6, 6: 3, 4: 5, 5: 4, 2: 7, 7: 2}, timer: {2: 7, 7: 2}, flicker: {2: 7, 7: 2}, mc: {6: 12, 12: 6},
      eocr: {10: 11, 11: 10, 6: 12, 12: 6}, fuse: {1: 2, 2: 1, 3: 4, 4: 3}, fls: {5: 6, 6: 5}, rl: {1: 2, 2: 1}, gl: {1: 2, 2: 1}, yl: {1: 2, 2: 1}, wl: {1: 2, 2: 1}, bz: {1: 2, 2: 1},
      pbg: {a1: 'a2', a2: 'a1', b1: 'b2', b2: 'b1'}, pbr: {a1: 'a2', a2: 'a1', b1: 'b2', b2: 'b1'}, ss: {a1: 'a2', a2: 'a1'}, tbl: {1: 2, 2: 1}};
    const mv = e => { const t = partById(e.p).type, m = PERM[t]; return m && m[e.k] !== undefined ? {p: e.p, k: '' + m[e.k]} : e; };
    const saved = S.wires;
    S.wires = saved.map(w => ({...w, a: mv(w.a), b: mv(w.b)}));
    { const cur2 = elecNets(), c2 = compare(concreteAnswer(n, cur2).map(x => x.pins), cur2);
      if (c2.miss.length || c2.extra.length) err.push('단자 바꾼 배선이 틀리게 나옴 ' + JSON.stringify(c2).slice(0, 400)); }
    /* 틀린 배선: 전선 하나 빼기, 전선 한쪽을 다른 단자로 옮기기 → 반드시 잡아야 한다 */
    for (let k = 0; k < 6; k++) {
      const i = (k * 37 + n * 11) % saved.length, ws = saved.slice();
      if (k % 2) ws.splice(i, 1); else { const w = ws[i], p = partById(w.b.p), d = DEFS[p.type], other = d.pins.find(q => q.k !== w.b.k && !saved.some(x => (x.a.p === p.id && x.a.k === q.k) || (x.b.p === p.id && x.b.k === q.k))); if (!other || (LINKED[p.type] || []).some(l => l.includes(other.k) && l.includes(w.b.k))) continue; ws[i] = {...w, b: {p: p.id, k: other.k}}; }
      S.wires = ws; const cur3 = elecNets(), c3 = compare(concreteAnswer(n, cur3).map(x => x.pins), cur3);
      if (!c3.miss.length && !c3.extra.length) err.push(`틀린 배선을 못 잡음 (${k % 2 ? '빼기' : '옮기기'} ${pinName(saved[i].a)}-${pinName(saved[i].b)})`);
    }
    S.wires = saved;
    out[n] = {err, wires: S.wires.length, miss: c.miss.length, extra: c.extra.length, over, noRoute: S.wires.filter(w => !w.pts).length};
  }
  return out;
}
