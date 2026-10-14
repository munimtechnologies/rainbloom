"""Tests for Rainbloom (Apache-2.0), by MV2 of Munim, Inc., made with AI agents.

Static checks always run. With Node.js installed, the rules block (<script id="logic">) runs and
selfTestLogic() must return no problems, and the whole page runs against a stub browser (a canvas that
rejects NaN and negative radii, pointer and key events, localStorage, a fake clock) in four modes:
#selftest, normal play, #demo and #cover.
"""
import json
import os
import re
import shutil
import subprocess
import tempfile
import unittest

GAME_FILE = "index.html"

HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, GAME_FILE), encoding="utf-8") as f:
    HTML = f.read()
LOGIC = re.search(r'<script id="logic">(.*?)</script>', HTML, re.S).group(1)
PAGE = "\n".join(re.findall(r"<script>(.*?)</script>", HTML, re.S))

HARNESS = """
;(function(){
  const problems=selfTestLogic();
  console.log(JSON.stringify({problems:problems.slice(0,25)}));
  process.exitCode=problems.length?1:0;
})();
"""

# a stub browser: enough of document, window, canvas, events and storage to run the page script
STUB = r"""
"use strict";
const __clock={t:1000};
try{Object.defineProperty(globalThis,"performance",{value:{now:()=>__clock.t},configurable:true,writable:true});}catch(e){performance.now=()=>__clock.t;}
const __raf=[];globalThis.requestAnimationFrame=cb=>{__raf.push(cb);return __raf.length;};
const __handlers={};globalThis.addEventListener=(type,fn)=>{(__handlers[type]=__handlers[type]||[]).push(fn);};
function __fire(type,props){const e=Object.assign({preventDefault(){},button:0,pointerType:"mouse",shiftKey:false},props);for(const fn of (__handlers[type]||[]))fn(e);}
function __click(x,y,button){__fire("pointermove",{clientX:x,clientY:y});__fire("pointerdown",{clientX:x,clientY:y,button:button||0});}
function __clickL(x,y,button){__click(view.ox+x*view.scale,view.oy+y*view.scale,button);}
function __key(key,extra){__fire("keydown",Object.assign({key},extra||{}));}
function __frames(n,dt){for(let k=0;k<n;k++){__clock.t+=dt*1000;const cbs=__raf.splice(0);for(const cb of cbs)cb(__clock.t);}}
function __num(p,a){for(const x of a)if(typeof x==="number"&&!isFinite(x))throw new Error("non-finite number passed to "+String(p));}
const __any=new Proxy(function(){},{get(t,p){if(p===Symbol.toPrimitive)return()=>0;if(p==="then")return undefined;return __any;},apply(){return __any;},construct(){return __any;},set(){return true;}});
function __ctx(){
  const store={};
  return new Proxy({},{
    get(t,p){
      if(p in store)return store[p];
      if(p==="measureText")return s=>({width:String(s).length*11});
      if(p==="createLinearGradient")return(...a)=>{__num(p,a);return {addColorStop(){}};};
      return(...a)=>{
        __num(p,a);
        if(p==="arc"&&a[2]<0)throw new Error("negative arc radius "+a[2]);
        if(p==="ellipse"&&(a[2]<0||a[3]<0))throw new Error("negative ellipse radius");
        if(p==="arcTo"&&a[4]<0)throw new Error("negative arcTo radius");
      };
    },
    set(t,p,v){if(typeof v==="number"&&!isFinite(v))throw new Error("bad "+String(p)+": "+v);store[p]=v;return true;}
  });
}
function __el(tag){
  const e={tag,hidden:true,textContent:"",style:{},children:[],onclick:null,classList:{add(){}},appendChild(c){this.children.push(c);return c;}};
  if(tag==="canvas"){e.width=300;e.height=150;e.getContext=()=>__ctx();e.toDataURL=()=>"data:image/png;base64,AAAA";}
  return e;
}
const __els={c:__el("canvas"),test:__el("div"),covers:__el("div")};
globalThis.document={getElementById:id=>__els[id],createElement:__el,body:__el("body"),hidden:false,addEventListener(){}};
globalThis.window=globalThis;globalThis.innerWidth=1280;globalThis.innerHeight=720;globalThis.devicePixelRatio=1;
globalThis.location={hash:__HASH__};
const __ls=new Map();
Object.defineProperty(globalThis,"localStorage",{value:{getItem:k=>__ls.has(k)?__ls.get(k):null,setItem:(k,v)=>__ls.set(k,String(v))},configurable:true,writable:true});
globalThis.AudioContext=__any;
"""

AFTER = {
    "#selftest": r"""
__frames(3,0.016);
console.log(JSON.stringify({box:__els.test.textContent,hidden:__els.test.hidden}));
""",
    "": r"""
const __out={};
__frames(5,0.016);
__out.lands=cur.mode==="level"&&cur.n===1&&!!L&&overlay===null;
__key("m");__out.muted=save.mute===true;__key("M");__out.unmuted=save.mute===false;
for(let k=0;k<200&&!won;k++){const [x,y]=tileCentre(hintTile(L,P));__clickL(x,y);__frames(1,0.016);}
__out.won1=won;
__frames(120,0.05);
const __nb=winButtons()[0];__clickL(__nb.x+5,__nb.y+5);
__out.after=cur.n;
const __s1=JSON.parse(__ls.get("rainbloom.v1"));
__out.saved=__s1.level;__out.best1=__s1.best["1"];
__key("ArrowRight");__key("ArrowDown");
kb.i=L.cells.findIndex(canTurn);const __m0=L.moves;__key(" ");__out.keyTurn=L.moves===__m0+1;
const __hb=UI.buttons.find(b=>b.id==="hint");const __h0=L.hints;__clickL(__hb.x+5,__hb.y+5);__out.hint=L.hints===__h0+1;
__frames(10,0.05);
const __rb=UI.buttons.find(b=>b.id==="restart");__clickL(__rb.x+5,__rb.y+5);__out.restart=L.moves===0&&L.hints===0;
const __lb=UI.buttons.find(b=>b.id==="levels");__clickL(__lb.x+5,__lb.y+5);__out.levelsOpen=overlay==="levels";
__frames(3,0.016);
const __lv1=overlayButtons().find(b=>b.id==="lv1");__clickL(__lv1.x+5,__lv1.y+5);__out.picked=cur.mode==="level"&&cur.n===1&&overlay===null;
const __ti=L.cells.findIndex(canTurn),__mk=L.cells[__ti].mask;const [__tx,__ty]=tileCentre(__ti);__clickL(__tx,__ty,2);
__out.back=L.cells[__ti].mask===rot(__mk,3);
__frames(10,0.05);
const __db=UI.buttons.find(b=>b.id==="daily");__clickL(__db.x+5,__db.y+5);__out.daily=cur.mode==="daily";
for(let k=0;k<600&&!won;k++){const [x,y]=tileCentre(hintTile(L,P));__clickL(x,y);if(k%5===0)__frames(1,0.016);}
__out.dailyWon=won;
__frames(100,0.05);
__out.streak=JSON.parse(__ls.get("rainbloom.v1")).daily.streak;
globalThis.innerWidth=390;globalThis.innerHeight=844;__fire("resize",{});__frames(3,0.016);
__out.portrait=VW===720&&VH===1280;
const __nb2=winButtons()[0];__clickL(__nb2.x+5,__nb2.y+5);__out.backToGardens=cur.mode==="level"&&cur.n===2;
const __pm=L.moves,__pi=L.cells.findIndex(canTurn);const [__px,__py]=tileCentre(__pi);__clickL(__px,__py);__out.portraitTurn=L.moves===__pm+1;
__frames(30,0.05);
console.log(JSON.stringify(__out));
""",
    "#demo": r"""
for(let k=0;k<1200;k++)__frames(1,0.05);
console.log(JSON.stringify({level:cur.n,saved:__ls.has("rainbloom.v1"),demo}));
""",
    "#cover": r"""
__frames(2,0.016);
console.log(JSON.stringify({children:__els.covers.children.length,hidden:__els.covers.hidden,srcs:__els.covers.children.filter(c=>c.tag==="img").map(c=>c.src.slice(0,22))}));
""",
}


def node(path):
    return subprocess.run(["node", path], capture_output=True, text=True, encoding="utf-8", timeout=300)


def run_page(hash_):
    with tempfile.TemporaryDirectory() as d:
        path = os.path.join(d, "page.js")
        with open(path, "w", encoding="utf-8") as f:
            f.write(STUB.replace("__HASH__", json.dumps(hash_)) + LOGIC + "\n" + PAGE + "\n" + AFTER[hash_])
        out = node(path)
    if out.returncode != 0:
        raise AssertionError("page run %r failed:\n%s\n%s" % (hash_, out.stdout[-3000:], out.stderr[-3000:]))
    lines = [l for l in out.stdout.splitlines() if l.startswith("{")]
    return json.loads(lines[-1])


class Static(unittest.TestCase):
    def test_one_self_contained_file(self):
        # portals and jams want one file that works offline and inside an iframe
        self.assertIsNone(re.search(r'\b(src|href)\s*=\s*["\']?(https?:)?//', HTML))
        self.assertIsNone(re.search(r'\b(fetch|import)\(\s*["\']https?://', HTML))
        self.assertIsNone(re.search(r"<link\b[^>]*stylesheet", HTML))

    def test_no_links_or_external_ads(self):
        # CrazyGames: no cross-promotion links and no external ads in the game
        self.assertNotIn("http://", HTML)
        self.assertNotIn("https://", HTML)

    def test_logic_has_no_browser_code(self):
        for name in ("document", "window", "AudioContext", "requestAnimationFrame", "localStorage"):
            self.assertIsNone(re.search(r"\b" + name + r"\b", LOGIC), name + " in the rules block")
        self.assertIn("function selfTestLogic(", LOGIC)
        self.assertRegex(LOGIC, r"\bconst W=\d+,H=\d+")

    def test_audio_waits_for_a_gesture(self):
        self.assertEqual(len(re.findall(r"new \(window\.AudioContext", PAGE)), 1)
        self.assertRegex(PAGE, r'addEventListener\("pointerdown",[^\n]*audio\.unlock\(\)')
        self.assertRegex(PAGE, r'addEventListener\("keydown",e=>\{\s*audio\.unlock\(\)')
        self.assertIn("audio.started()", PAGE)

    def test_sound_can_be_turned_off_on_screen_and_with_m(self):
        self.assertRegex(PAGE, r'e\.key==="m"\|\|e\.key==="M"\)\{audio\.toggle\(\)')
        self.assertIn('["sound","Sound"]', PAGE)

    def test_portal_rules(self):
        # CrazyGames gives fullscreen itself and forbids in-game fullscreen buttons; Escape leaves fullscreen
        self.assertNotIn("requestFullscreen", HTML)
        self.assertNotRegex(PAGE, r'\bkey===?"Escape"')
        # lands straight in a garden, and progress is kept
        self.assertRegex(PAGE, r'\nstart\("level",Math\.max\(1,save\.level\)\);')
        self.assertIn('SAVE_KEY="rainbloom.v1"', PAGE)
        self.assertRegex(PAGE, r"localStorage\.setItem\(SAVE_KEY")

    def test_selftest_cover_and_demo_hooks(self):
        self.assertIn('location.hash==="#selftest"', PAGE)
        self.assertIn('location.hash==="#cover"', PAGE)
        self.assertIn('location.hash==="#demo"', PAGE)

    def test_disclosure_licence_and_wording(self):
        self.assertIn("Made by MV2 of Munim, Inc. with AI agents", HTML)
        self.assertIn("Apache-2.0", HTML)
        self.assertIsNone(re.search(r"MV2[^.]{0,60}\b(an AI|a bot|AI assistant)\b", HTML))
        self.assertIsNone(re.search(r"(License|Licence)\s*:\s*MIT|MIT License", HTML))


@unittest.skipUnless(shutil.which("node"), "Node.js is not installed")
class Node(unittest.TestCase):
    def test_rules(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "logic.js")
            with open(path, "w", encoding="utf-8") as f:
                f.write(LOGIC + "\n" + HARNESS)
            out = node(path)
        self.assertEqual(out.returncode, 0, out.stdout[-3000:] + out.stderr[-3000:])
        self.assertEqual(json.loads(out.stdout[out.stdout.index("{"):])["problems"], [])

    def test_page_script_parses(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "page.js")
            with open(path, "w", encoding="utf-8") as f:
                f.write(LOGIC + "\n" + PAGE)
            out = subprocess.run(["node", "--check", path], capture_output=True, text=True, encoding="utf-8", timeout=60)
        self.assertEqual(out.returncode, 0, out.stderr[-3000:])

    def test_page_selftest(self):
        r = run_page("#selftest")
        self.assertFalse(r["hidden"])
        self.assertIn("No problems found.", r["box"], r["box"])

    def test_page_play(self):
        r = run_page("")
        for key in ("lands", "muted", "unmuted", "won1", "keyTurn", "hint", "restart", "levelsOpen", "picked",
                    "back", "daily", "dailyWon", "portrait", "backToGardens", "portraitTurn"):
            self.assertTrue(r.get(key), "%s failed: %r" % (key, r))
        self.assertEqual(r["after"], 2, r)
        self.assertEqual(r["saved"], 2, r)
        self.assertIn(r["best1"], (1, 2, 3), r)
        self.assertEqual(r["streak"], 1, r)

    def test_page_demo_plays_itself_and_never_saves(self):
        r = run_page("#demo")
        self.assertTrue(r["demo"])
        self.assertGreaterEqual(r["level"], 17, r)
        self.assertFalse(r["saved"], r)

    def test_page_covers(self):
        r = run_page("#cover")
        self.assertFalse(r["hidden"])
        self.assertEqual(r["children"], 6, r)
        self.assertEqual(r["srcs"], ["data:image/png;base64,"] * 3, r)


if __name__ == "__main__":
    unittest.main()
