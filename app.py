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
        return url.replace("/upload/", f"/upload/f_auto,q_auto,w_{w},c_fill,g_auto,ar_1:1/")
    return url


# ------------------------------------------------------------
#  Styling global (dark cinematic)
# ------------------------------------------------------------
st.markdown("""
<style>
    #MainMenu, footer, header {visibility: hidden;}
    .stApp {
        background: radial-gradient(ellipse at top, #14141c 0%, #0a0a0f 55%, #050507 100%);
    }
    .block-container {padding-top: 0 !important; max-width: 1400px;}

    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;600&family=Inter:wght@300;400;500&display=swap');

    .hero {
        text-align: center;
        padding: 5.5rem 1rem 2.5rem 1rem;
        animation: heroIn 1.6s cubic-bezier(.2,.7,.2,1) both;
    }
    @keyframes heroIn {
        from {opacity:0; transform: translateY(24px);}
        to   {opacity:1; transform: translateY(0);}
    }
    .hero h1 {
        font-family: 'Cormorant Garamond', serif;
        font-size: clamp(3.2rem, 9vw, 6.5rem);
        font-weight: 600;
        letter-spacing: .18em;
        color: #f4f1ea;
        margin: 0;
        text-shadow: 0 0 40px rgba(200,180,150,.25);
    }
    .hero .sub {
        font-family: 'Inter', sans-serif;
        font-weight: 300;
        letter-spacing: .42em;
        text-transform: uppercase;
        font-size: clamp(.7rem, 2vw, .95rem);
        color: #b8a888;
        margin-top: 1.2rem;
    }
    .hero .line {
        width: 60px; height: 1px;
        background: linear-gradient(90deg, transparent, #b8a888, transparent);
        margin: 1.8rem auto 0 auto;
    }

    .section-title {
        font-family: 'Cormorant Garamond', serif;
        font-size: 1.9rem;
        color: #e8e2d5;
        letter-spacing: .18em;
        text-align: center;
        margin: 4.5rem 0 2.2rem 0;
        font-weight: 400;
        position: relative;
    }

    .stButton>button, .stDownloadButton>button {
        background: rgba(184,168,136,.08);
        border: 1px solid rgba(184,168,136,.3);
        color: #d8cdb5;
        border-radius: 40px;
        padding: .5rem 1.6rem;
        font-family: 'Inter', sans-serif;
        letter-spacing: .12em;
        text-transform: uppercase;
        font-size: .72rem;
        transition: all .3s ease;
    }
    .stButton>button:hover {
        background: rgba(184,168,136,.18);
        border-color: #b8a888;
        color: #fff;
    }
    div[data-testid="stImage"] img {border-radius: 8px;}
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
    background:#000; border-radius: 18px; overflow: hidden;
    box-shadow: 0 40px 100px rgba(0,0,0,.7), 0 0 0 1px rgba(184,168,136,.12);
  }
  #stage { width:100%; height:100%; position:relative; }
  #stage img {
    position:absolute; top:0; left:0; width:100%; height:100%;
    object-fit: cover; opacity:0;
    transition: opacity 1.8s cubic-bezier(.4,0,.2,1);
    will-change: opacity, transform;
  }
  #stage img.active { opacity:1; animation: ken 9s ease-out forwards; }
  @keyframes ken {
    0%   { transform: scale(1.05) translate(1%, 1%); }
    100% { transform: scale(1.18) translate(-2%, -2%); }
  }
  #vignette {
    position:absolute; inset:0; pointer-events:none; z-index:2;
    background:
      radial-gradient(ellipse at center, transparent 55%, rgba(0,0,0,.5) 100%),
      linear-gradient(to top, rgba(0,0,0,.55), transparent 45%);
  }
  #controls {
    position:absolute; bottom:30px; left:50%; transform:translateX(-50%);
    display:flex; gap:10px; z-index:6; opacity:0; transition:opacity .4s;
    background: rgba(12,12,18,.45); backdrop-filter: blur(14px);
    padding: 9px 14px; border-radius: 50px; border:1px solid rgba(184,168,136,.28);
  }
  #show:hover #controls { opacity:1; }
  #controls button {
    background:transparent; border:none; color:#e8ddc5;
    font-size: 20px; cursor:pointer; width:40px; height:40px;
    border-radius:50%; transition: all .25s; display:flex; align-items:center; justify-content:center;
  }
  #controls button:hover { background: rgba(184,168,136,.28); color:#fff; transform: scale(1.12); }
  #dots {
    position:absolute; bottom:14px; left:50%; transform:translateX(-50%);
    display:flex; gap:6px; z-index:5;
  }
  #dots span { width:6px; height:6px; border-radius:50%; background:rgba(255,255,255,.3); transition:all .3s; }
  #dots span.on { background:#e8ddc5; width:22px; border-radius:3px; }
  #progress { position:absolute; top:0; left:0; width:100%; height:3px; background:rgba(255,255,255,.06); z-index:4;}
  #bar { height:100%; width:0%; background: linear-gradient(90deg,#b8a888,#f0e6cf); box-shadow:0 0 12px rgba(184,168,136,.6); }
  #caption {
    position:absolute; top:24px; left:28px; z-index:5;
    font-family:'Inter',sans-serif; font-size:.72rem; letter-spacing:.28em;
    color:#e8ddc5; font-weight:300;
    background:rgba(12,12,18,.4); backdrop-filter:blur(8px);
    padding:6px 16px; border-radius:30px; border:1px solid rgba(184,168,136,.2);
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
    columns: 4 260px; column-gap: 18px; padding: 6px 2px;
  }
  @media (max-width: 640px){ #grid { columns: 2 150px; column-gap: 12px; } }
  #grid .cell {
    break-inside: avoid; margin-bottom: 18px; position:relative;
    border-radius: 14px; overflow:hidden; cursor:pointer;
    opacity:0; transform: translateY(30px) scale(.97);
    animation: rise .8s cubic-bezier(.2,.7,.2,1) forwards;
    box-shadow: 0 10px 30px rgba(0,0,0,.3);
  }
  @keyframes rise { to {opacity:1; transform:translateY(0) scale(1);} }
  #grid img {
    width:100%; display:block;
    transition: transform .8s cubic-bezier(.2,.7,.2,1), filter .6s;
    filter: grayscale(20%) brightness(.9) contrast(1.02);
  }
  #grid .cell:hover img { transform: scale(1.12); filter: grayscale(0) brightness(1.08) contrast(1.05); }
  #grid .cell::after {
    content:'\\2197'; position:absolute; top:12px; right:14px;
    color:#fff; font-size:18px; opacity:0; transform:translateY(-6px);
    transition: all .4s; z-index:2; text-shadow:0 2px 8px rgba(0,0,0,.5);
  }
  #grid .cell::before {
    content:''; position:absolute; inset:0; z-index:1;
    background: linear-gradient(to top, rgba(184,168,136,.3), transparent 50%);
    opacity:0; transition: opacity .5s;
  }
  #grid .cell:hover::after { opacity:1; transform:translateY(0); }
  #grid .cell:hover::before { opacity:1; }

  #lightbox {
    display:none; position:fixed; inset:0; z-index:9999;
    background: rgba(5,5,7,.96); backdrop-filter: blur(10px);
    align-items:center; justify-content:center;
    opacity:0; transition: opacity .35s;
  }
  #lightbox.on { display:flex; opacity:1; }
  #lbWrap { position:relative; max-width:90%; max-height:90%; display:flex; flex-direction:column; align-items:center; }
  #lbImg { max-width:100%; max-height:84vh; border-radius:12px; box-shadow:0 30px 100px rgba(0,0,0,.8); }
  #lbImg.anim { animation: pop .45s cubic-bezier(.2,.7,.2,1); }
  @keyframes pop { from{opacity:0; transform:scale(.92);} to{opacity:1; transform:scale(1);} }
  #lbCount { margin-top:16px; font-family:'Inter',sans-serif; color:#b8a888; letter-spacing:.25em; font-size:.72rem; }
  #lbClose { position:fixed; top:24px; right:36px; color:#e8ddc5; font-size:40px; cursor:pointer; z-index:10001; transition:transform .25s;}
  #lbClose:hover { transform:rotate(90deg); }
  #lbPrev, #lbNext {
    position:fixed; top:50%; transform:translateY(-50%); z-index:10001;
    color:#e8ddc5; font-size:56px; cursor:pointer; user-select:none;
    width:70px; height:70px; display:flex; align-items:center; justify-content:center;
    border-radius:50%; transition: all .25s;
  }
  #lbPrev { left:24px; } #lbNext { right:24px; }
  #lbPrev:hover, #lbNext:hover { background:rgba(184,168,136,.2); transform:translateY(-50%) scale(1.1); }
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
</script>
""".replace("GRID_DATA", grid_data)

grid_height = max(400, (len(images) // 4 + 1) * 240)
components.html(grid_html, height=grid_height, scrolling=True)


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
<div style="text-align:center; padding:3rem 0 2rem 0; font-family:'Inter',sans-serif;
     color:#5a5548; letter-spacing:.25em; font-size:.7rem; text-transform:uppercase;">
    Made with love &middot; UMN 2022
</div>
""", unsafe_allow_html=True)
