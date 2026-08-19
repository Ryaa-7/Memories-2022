import streamlit as st
import streamlit.components.v1 as components
import cloudinary
import cloudinary.api
import json

# ============================================================
#  MEMORIES · UMN · Angkatan 2022
#  Dark cinematic memories gallery
# ============================================================

st.set_page_config(
    page_title="Memories · UMN 2022",
    page_icon="🎞️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ------------------------------------------------------------
#  Konfigurasi Cloudinary (dibaca dari Streamlit Secrets)
# ------------------------------------------------------------
CLOUD_FOLDER = st.secrets.get("cloudinary", {}).get("folder", "memories")

def configure_cloudinary():
    try:
        c = st.secrets["cloudinary"]
        cloudinary.config(
            cloud_name=c["cloud_name"],
            api_key=c["api_key"],
            api_secret=c["api_secret"],
            secure=True,
        )
        return True
    except Exception:
        return False


@st.cache_data(ttl=300, show_spinner=False)
def fetch_media(folder: str):
    """Ambil foto & video dari Cloudinary pakai Admin API dasar (paling andal).
    Tarik semua aset, filter yang termasuk folder target; kalau kosong, tampilkan
    semua kecuali contoh bawaan 'samples'."""
    diag = {"total_images": 0, "total_videos": 0, "in_folder": 0, "error": ""}

    def pull(resource_type):
        items = []  # (public_id, asset_folder, secure_url)
        cursor = None
        while True:
            kwargs = dict(type="upload", resource_type=resource_type, max_results=500)
            if cursor:
                kwargs["next_cursor"] = cursor
            res = cloudinary.api.resources(**kwargs)
            for r in res.get("resources", []):
                items.append((
                    r.get("public_id", ""),
                    r.get("asset_folder", "") or r.get("folder", ""),
                    r.get("secure_url", ""),
                ))
            cursor = res.get("next_cursor")
            if not cursor:
                break
        return items

    try:
        all_img = pull("image")
        all_vid = pull("video")
    except Exception as e:
        diag["error"] = str(e)
        st.session_state["_diag"] = diag
        return [], []

    diag["total_images"] = len(all_img)
    diag["total_videos"] = len(all_vid)

    def in_target(pid, af):
        f = (folder or "").strip("/").lower()
        return (af or "").strip("/").lower().startswith(f) or (pid or "").lower().startswith(f + "/")

    def not_sample(pid, af):
        return not ((pid or "").lower().startswith("samples/") or (af or "").lower() == "samples")

    img_folder = [u for (p, a, u) in all_img if in_target(p, a) and u]
    vid_folder = [u for (p, a, u) in all_vid if in_target(p, a) and u]
    diag["in_folder"] = len(img_folder) + len(vid_folder)

    if diag["in_folder"] > 0:
        images, videos = img_folder, vid_folder
    else:
        images = [u for (p, a, u) in all_img if not_sample(p, a) and u]
        videos = [u for (p, a, u) in all_vid if not_sample(p, a) and u]

    st.session_state["_diag"] = diag
    return images, videos


def optimized(url: str, w: int = 1600) -> str:
    """Sisipkan transformasi Cloudinary agar foto tidak berat."""
    if "/upload/" in url:
        return url.replace("/upload/", f"/upload/f_auto,q_auto,w_{w}/")
    return url


def thumb(url: str, w: int = 600) -> str:
    if "/upload/" in url:
        return url.replace("/upload/", f"/upload/f_auto,q_auto,w_{w}/")
    return url


# ------------------------------------------------------------
#  Styling global (soft blue playful)
# ------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Baloo+2:wght@400;500;600;700&family=Quicksand:wght@400;500;600;700&display=swap');

    #MainMenu, footer, header {visibility: hidden;}
    .stApp {
        background:
          radial-gradient(circle at 15% 20%, #d6ecff 0%, transparent 40%),
          radial-gradient(circle at 85% 15%, #e5dbff 0%, transparent 42%),
          radial-gradient(circle at 50% 100%, #cdeffd 0%, transparent 55%),
          linear-gradient(160deg, #eaf6ff 0%, #f3f0ff 50%, #eafaff 100%);
        background-attachment: fixed;
    }
    .block-container {padding-top: 0 !important; max-width: 1400px;}

    /* Bentuk lucu mengambang di latar */
    .stApp::before, .stApp::after {
        content:''; position:fixed; border-radius:50%; z-index:0; pointer-events:none;
        filter: blur(2px); opacity:.5;
    }
    .stApp::before {
        width:180px; height:180px; left:4%; top:30%;
        background: radial-gradient(circle at 30% 30%, #bfe3ff, #93c9ff);
        animation: floatA 9s ease-in-out infinite;
    }
    .stApp::after {
        width:120px; height:120px; right:6%; top:60%;
        background: radial-gradient(circle at 30% 30%, #e3d5ff, #b9a4ff);
        animation: floatB 11s ease-in-out infinite;
    }
    @keyframes floatA { 0%,100%{transform:translateY(0) rotate(0)} 50%{transform:translateY(-30px) rotate(12deg)} }
    @keyframes floatB { 0%,100%{transform:translateY(0) rotate(0)} 50%{transform:translateY(28px) rotate(-14deg)} }

    .hero {
        text-align: center;
        padding: 4.5rem 1rem 1.5rem 1rem;
        position: relative; z-index: 1;
        animation: heroIn 1.1s cubic-bezier(.34,1.56,.64,1) both;
    }
    @keyframes heroIn {
        from {opacity:0; transform: translateY(30px) scale(.9);}
        to   {opacity:1; transform: translateY(0) scale(1);}
    }
    .hero h1 {
        font-family: 'Baloo 2', cursive;
        font-size: clamp(3rem, 9vw, 6rem);
        font-weight: 700;
        letter-spacing: .04em;
        background: linear-gradient(120deg, #5aa9ff, #8f7bff 45%, #57c7ff);
        -webkit-background-clip: text; background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        animation: wobble 4s ease-in-out infinite;
        display: inline-block;
    }
    @keyframes wobble { 0%,100%{transform:rotate(-1.5deg)} 50%{transform:rotate(1.5deg)} }
    .hero .sub {
        font-family: 'Quicksand', sans-serif;
        font-weight: 600;
        letter-spacing: .25em;
        text-transform: uppercase;
        font-size: clamp(.68rem, 2vw, .9rem);
        color: #6c8bd6;
        margin-top: 1rem;
    }
    .hero .line {
        width: 90px; height: 5px; border-radius: 5px;
        background: linear-gradient(90deg, #7fc4ff, #b3a4ff);
        margin: 1.4rem auto 0 auto;
        animation: stretch 3s ease-in-out infinite;
    }
    @keyframes stretch { 0%,100%{width:90px} 50%{width:140px} }

    .section-title {
        font-family: 'Baloo 2', cursive;
        font-size: 2rem;
        color: #5a7fd6;
        letter-spacing: .04em;
        text-align: center;
        margin: 4rem 0 2rem 0;
        font-weight: 700;
        position: relative; z-index: 1;
        animation: bobble 3.5s ease-in-out infinite;
    }
    @keyframes bobble { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-8px)} }

    div[data-testid="stImage"] img {border-radius: 18px;}
    [data-testid="stVideo"] {border-radius: 18px; overflow:hidden; box-shadow: 0 14px 40px rgba(120,150,220,.25);}
</style>
""", unsafe_allow_html=True)


# ------------------------------------------------------------
#  Hero
# ------------------------------------------------------------
st.markdown("""
<div class="hero">
    <h1>MEMORIES</h1>
    <div class="sub">Universitas Multimedia Nusantara &middot; Angkatan 2022</div>
    <div class="line"></div>
</div>
""", unsafe_allow_html=True)


# ------------------------------------------------------------
#  Ambil media
# ------------------------------------------------------------
if not configure_cloudinary():
    st.warning("⚠️ Kredensial Cloudinary belum diatur. Isi `.streamlit/secrets.toml` "
               "atau Streamlit Secrets. Lihat README.md untuk panduan.")
    st.stop()

with st.spinner("Memuat kenangan..."):
    images, videos = fetch_media(CLOUD_FOLDER)

if not images and not videos:
    st.info("Belum ada media ditemukan. Diagnostik di bawah membantu cari tahu penyebabnya.")
    diag = st.session_state.get("_diag", {})
    st.code(
        "folder dicari : %s\n"
        "total foto di akun : %s\n"
        "total video di akun : %s\n"
        "cocok dgn folder : %s\n"
        "error : %s"
        % (CLOUD_FOLDER, diag.get("total_images"), diag.get("total_videos"),
           diag.get("in_folder"), diag.get("error") or "(tidak ada)"),
        language="text",
    )
    st.caption("Kalau 'total foto di akun' = 0 dan tidak ada error, API key benar tapi "
               "akun terbaca kosong (cek: kredensial milik cloud yang sama dengan tempat upload). "
               "Kalau ada 'error', kirim ke chat.")
    st.stop()


# ------------------------------------------------------------
#  Slideshow otomatis fullscreen (Ken Burns + fade)
# ------------------------------------------------------------
st.markdown('<div class="section-title">✦ Slideshow ✦</div>', unsafe_allow_html=True)

slides_json = json.dumps([optimized(u, 1600) for u in images])

slideshow_html = """
<div id="show">
  <div id="stage"></div>
  <div id="vignette"></div>
  <div id="caption"></div>
  <div id="controls">
    <button onclick="prev()">&#8249;</button>
    <button onclick="toggle()" id="pp">&#10074;&#10074;</button>
    <button onclick="next()">&#8250;</button>
    <button onclick="fs()">&#9974;</button>
  </div>
  <div id="dots"></div>
  <div id="progress"><div id="bar"></div></div>
</div>
<style>
  #show {
    position: relative; width: 100%; height: 660px;
    background:#dbeeff; border-radius: 28px; overflow: hidden;
    box-shadow: 0 30px 70px rgba(120,160,230,.35), 0 0 0 4px #fff, 0 0 0 6px rgba(150,190,255,.4);
  }
  #stage { width:100%; height:100%; position:relative; }
  #stage img {
    position:absolute; top:0; left:0; width:100%; height:100%;
    object-fit: cover; opacity:0;
    transition: opacity 1.3s cubic-bezier(.34,1.2,.64,1);
    will-change: opacity, transform;
  }
  #stage img.active { opacity:1; animation: ken 8s ease-out forwards; }
  @keyframes ken {
    0%   { transform: scale(1.05) translate(1%, 1%); }
    100% { transform: scale(1.16) translate(-2%, -2%); }
  }
  #vignette {
    position:absolute; inset:0; pointer-events:none; z-index:2;
    background: linear-gradient(to top, rgba(70,110,180,.35), transparent 42%);
  }
  #controls {
    position:absolute; bottom:26px; left:50%; transform:translateX(-50%);
    display:flex; gap:10px; z-index:6; opacity:0; transition:opacity .4s;
    background: rgba(255,255,255,.75); backdrop-filter: blur(14px);
    padding: 9px 14px; border-radius: 50px; border:2px solid rgba(150,190,255,.6);
    box-shadow: 0 8px 24px rgba(120,160,230,.3);
  }
  #show:hover #controls { opacity:1; }
  #controls button {
    background:transparent; border:none; color:#4a7ad0;
    font-size: 20px; cursor:pointer; width:40px; height:40px;
    border-radius:50%; transition: all .25s; display:flex; align-items:center; justify-content:center;
  }
  #controls button:hover { background: #7fc4ff; color:#fff; transform: scale(1.18) rotate(-6deg); }
  #dots {
    position:absolute; bottom:14px; left:50%; transform:translateX(-50%);
    display:flex; gap:6px; z-index:5;
  }
  #dots span { width:7px; height:7px; border-radius:50%; background:rgba(255,255,255,.6); transition:all .3s; }
  #dots span.on { background:#7fc4ff; width:24px; border-radius:4px; }
  #progress { position:absolute; top:0; left:0; width:100%; height:5px; background:rgba(255,255,255,.35); z-index:4;}
  #bar { height:100%; width:0%; background: linear-gradient(90deg,#7fc4ff,#b3a4ff); box-shadow:0 0 12px rgba(130,180,255,.7); }
  #caption {
    position:absolute; top:22px; left:24px; z-index:5;
    font-family:'Quicksand',sans-serif; font-weight:700; font-size:.78rem; letter-spacing:.15em;
    color:#4a7ad0;
    background:rgba(255,255,255,.8); backdrop-filter:blur(8px);
    padding:7px 16px; border-radius:30px; border:2px solid rgba(150,190,255,.5);
  }
</style>
<script>
  const imgs = SLIDES_JSON;
  const stage = document.getElementById('stage');
  const cap = document.getElementById('caption');
  const bar = document.getElementById('bar');
  const dotsBox = document.getElementById('dots');
  let i = 0, playing = true, timer=null, DUR=6000, t0=0;

  imgs.forEach((src, idx) => {
    const im = document.createElement('img');
    im.src = src; if(idx===0) im.className='active';
    stage.appendChild(im);
  });
  // dots: tampilkan maksimal ~18 titik biar tidak penuh
  const maxDots = Math.min(imgs.length, 18);
  for(let d=0; d<maxDots; d++){ const s=document.createElement('span'); dotsBox.appendChild(s); }
  const dots = dotsBox.querySelectorAll('span');

  const els = () => stage.querySelectorAll('img');
  function render(){
    els().forEach((im,idx)=>{ im.classList.remove('active'); if(idx===i){ void im.offsetWidth; im.classList.add('active'); } });
    cap.textContent = String(i+1).padStart(2,'0')+'  /  '+String(imgs.length).padStart(2,'0');
    const active = Math.round((i/Math.max(1,imgs.length-1))*(maxDots-1));
    dots.forEach((s,idx)=> s.classList.toggle('on', idx===active));
  }
  function next(){ i=(i+1)%imgs.length; render(); restart(); }
  function prev(){ i=(i-1+imgs.length)%imgs.length; render(); restart(); }
  function toggle(){ playing=!playing; document.getElementById('pp').innerHTML = playing?'&#10074;&#10074;':'&#9658;'; if(playing) restart(); else clearInterval(timer); }
  function restart(){ clearInterval(timer); if(!playing) return; t0=Date.now();
    timer=setInterval(()=>{ let p=Math.min(1,(Date.now()-t0)/DUR); bar.style.width=(p*100)+'%'; if(p>=1) next(); }, 30);
  }
  function fs(){ const e=document.getElementById('show'); if(e.requestFullscreen) e.requestFullscreen(); }
  document.addEventListener('keydown',e=>{ if(e.key==='ArrowRight') next(); if(e.key==='ArrowLeft') prev(); });
  render(); restart();
</script>
""".replace("SLIDES_JSON", slides_json)

components.html(slideshow_html, height=700)


# ------------------------------------------------------------
#  Grid galeri (hover zoom)
# ------------------------------------------------------------
st.markdown('<div class="section-title">✦ Galeri ✦</div>', unsafe_allow_html=True)

thumbs = [thumb(u, 600) for u in images]
full = [optimized(u, 1600) for u in images]
grid_data = json.dumps([{"t": t, "f": f} for t, f in zip(thumbs, full)])

grid_html = """
<div id="grid"></div>
<div id="lightbox" onclick="closeLb()">
  <span id="lbClose" onclick="event.stopPropagation();closeLb()">&times;</span>
  <span id="lbPrev" onclick="event.stopPropagation();lbMove(-1)">&#8249;</span>
  <div id="lbWrap" onclick="event.stopPropagation()">
    <img id="lbImg">
    <div id="lbCount"></div>
  </div>
  <span id="lbNext" onclick="event.stopPropagation();lbMove(1)">&#8250;</span>
</div>
<style>
  #grid {
    columns: 4 250px; column-gap: 16px; padding: 6px 2px;
  }
  @media (max-width: 900px){ #grid { columns: 3 180px; } }
  @media (max-width: 640px){ #grid { columns: 2 150px; column-gap: 12px; } }
  #grid .cell {
    break-inside: avoid; margin-bottom: 16px; position:relative;
    border-radius: 18px; overflow:hidden; cursor:pointer;
    opacity:0; transform: translateY(24px) scale(.96);
    animation: rise .7s cubic-bezier(.22,1,.36,1) forwards;
    box-shadow: 0 10px 28px rgba(120,160,230,.18);
    border: 3px solid #fff;
    transition: transform .45s cubic-bezier(.22,1,.36,1), box-shadow .45s;
  }
  @keyframes rise { to {opacity:1; transform:translateY(0) scale(1);} }
  #grid .cell:hover {
    transform: translateY(-8px) scale(1.015);
    box-shadow: 0 22px 48px rgba(120,160,230,.35);
  }
  #grid img {
    width:100%; display:block;
    transition: transform .7s cubic-bezier(.22,1,.36,1);
  }
  #grid .cell:hover img { transform: scale(1.07); }
  #grid .cell::after {
    content:'\\2661'; position:absolute; top:10px; right:14px;
    color:#fff; font-size:22px; opacity:0; transform:scale(.4) translateY(-4px);
    transition: all .4s cubic-bezier(.22,1,.36,1); z-index:2; text-shadow:0 2px 10px rgba(80,120,200,.6);
  }
  #grid .cell::before {
    content:''; position:absolute; inset:0; z-index:1;
    background: linear-gradient(to top, rgba(120,170,255,.35), transparent 55%);
    opacity:0; transition: opacity .5s;
  }
  #grid .cell:hover::after { opacity:1; transform:scale(1) translateY(0); }
  #grid .cell:hover::before { opacity:1; }

  #lightbox {
    display:none; position:fixed; inset:0; z-index:9999;
    background: rgba(210,232,255,.85); backdrop-filter: blur(14px);
    align-items:center; justify-content:center;
    opacity:0; transition: opacity .35s;
  }
  #lightbox.on { display:flex; opacity:1; }
  #lbWrap { position:relative; max-width:90%; max-height:90%; display:flex; flex-direction:column; align-items:center; }
  #lbImg { max-width:100%; max-height:82vh; border-radius:22px; border:5px solid #fff; box-shadow:0 30px 80px rgba(90,130,210,.5); }
  #lbImg.anim { animation: pop .5s cubic-bezier(.34,1.56,.64,1); }
  @keyframes pop { from{opacity:0; transform:scale(.8) rotate(-3deg);} to{opacity:1; transform:scale(1) rotate(0);} }
  #lbCount { margin-top:16px; font-family:'Quicksand',sans-serif; font-weight:700; color:#4a7ad0; letter-spacing:.2em; font-size:.8rem;
    background:#fff; padding:6px 18px; border-radius:30px; box-shadow:0 6px 18px rgba(120,160,230,.3); }
  #lbClose { position:fixed; top:24px; right:36px; color:#fff; background:#7fc4ff; font-size:26px; cursor:pointer; z-index:10001;
    width:48px; height:48px; border-radius:50%; display:flex; align-items:center; justify-content:center;
    transition:transform .3s; box-shadow:0 6px 18px rgba(120,160,230,.4);}
  #lbClose:hover { transform:rotate(180deg) scale(1.1); }
  #lbPrev, #lbNext {
    position:fixed; top:50%; transform:translateY(-50%); z-index:10001;
    color:#fff; background:#7fc4ff; font-size:34px; cursor:pointer; user-select:none;
    width:64px; height:64px; display:flex; align-items:center; justify-content:center;
    border-radius:50%; transition: all .25s; box-shadow:0 8px 20px rgba(120,160,230,.4);
  }
  #lbPrev { left:24px; } #lbNext { right:24px; }
  #lbPrev:hover { background:#b3a4ff; transform:translateY(-50%) scale(1.15) translateX(-4px); }
  #lbNext:hover { background:#b3a4ff; transform:translateY(-50%) scale(1.15) translateX(4px); }
  @media (max-width:640px){ #lbPrev{left:6px;} #lbNext{right:6px;} #lbClose{right:16px;} }
</style>
<script>
  const data = GRID_DATA;
  const g = document.getElementById('grid');
  let cur = 0;
  data.forEach((d,idx)=>{
    const c=document.createElement('div'); c.className='cell';
    c.style.animationDelay=Math.min(idx*40, 1200)+'ms';
    const im=document.createElement('img'); im.src=d.t; im.loading='lazy';
    im.onclick=()=>openLb(idx);
    c.appendChild(im); g.appendChild(c);
  });
  const lb = document.getElementById('lightbox');
  const lbImg = document.getElementById('lbImg');
  const lbCount = document.getElementById('lbCount');
  function show(){
    lbImg.classList.remove('anim'); void lbImg.offsetWidth; lbImg.classList.add('anim');
    lbImg.src = data[cur].f;
    lbCount.textContent = String(cur+1).padStart(2,'0')+' / '+String(data.length).padStart(2,'0');
  }
  function openLb(idx){ cur=idx; lb.classList.add('on'); show(); }
  function closeLb(){ lb.classList.remove('on'); }
  function lbMove(dir){ cur=(cur+dir+data.length)%data.length; show(); }
  document.addEventListener('keydown',e=>{
    if(!lb.classList.contains('on')) return;
    if(e.key==='Escape') closeLb();
    if(e.key==='ArrowRight') lbMove(1);
    if(e.key==='ArrowLeft') lbMove(-1);
  });

  // Auto-resize: lapor tinggi asli grid ke Streamlit agar tidak ada scroll dalam
  function reportHeight(){
    const h = document.body.scrollHeight;
    if (window.Streamlit) { window.Streamlit.setFrameHeight(h + 20); }
    if (window.parent) {
      window.parent.postMessage({type:'streamlit:setFrameHeight', height: h + 20}, '*');
    }
  }
  window.addEventListener('load', reportHeight);
  window.addEventListener('resize', reportHeight);
  // foto lazy-load selesai memuat -> tinggi berubah -> lapor ulang
  g.querySelectorAll('img').forEach(im => im.addEventListener('load', reportHeight));
  setInterval(reportHeight, 1500);
</script>
""".replace("GRID_DATA", grid_data)

# Estimasi tinggi awal untuk masonry (foto tinggi bervariasi, ~4 kolom).
# Auto-resize di atas akan menyesuaikan setelah foto termuat.
est_rows = (len(images) + 3) // 4
grid_height = max(600, est_rows * 300)
components.html(grid_html, height=grid_height, scrolling=False)


# ------------------------------------------------------------
#  Video
# ------------------------------------------------------------
if videos:
    st.markdown('<div class="section-title">✦ Video ✦</div>', unsafe_allow_html=True)
    cols = st.columns(2)
    for idx, v in enumerate(videos):
        with cols[idx % 2]:
            st.video(v)


# ------------------------------------------------------------
#  Footer
# ------------------------------------------------------------
st.markdown("""
<div style="text-align:center; padding:3.5rem 0 2.5rem 0; font-family:'Quicksand',sans-serif;
     color:#7a9bd6; letter-spacing:.2em; font-size:.8rem; font-weight:600; position:relative; z-index:1;">
    ♡ Made with love &middot; UMN 2022 ♡
</div>
""", unsafe_allow_html=True)
