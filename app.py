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


import cloudinary.search


@st.cache_data(ttl=300, show_spinner=False)
def fetch_media(folder: str):
    """Ambil foto & video dari Cloudinary.
    Strategi: pakai Search API (paling andal untuk folder). Kalau folder kosong,
    fallback ke SEMUA aset di akun (kecuali contoh bawaan 'samples')."""
    images, videos = [], []
    diag = {"method": "", "folder_count": 0, "all_count": 0, "error": ""}

    def run_search(expr):
        imgs, vids = [], []
        try:
            cursor = None
            while True:
                s = cloudinary.search.Search().expression(expr).max_results(500).with_field("resource_type")
                if cursor:
                    s = s.next_cursor(cursor)
                res = s.execute()
                for r in res.get("resources", []):
                    url = r.get("secure_url", "")
                    if r.get("resource_type") == "video":
                        vids.append(url)
                    else:
                        imgs.append(url)
                cursor = res.get("next_cursor")
                if not cursor:
                    break
        except Exception as e:
            diag["error"] = str(e)
        return imgs, vids

    # 1) Cari di dalam folder (asset_folder ATAU public_id prefix)
    expr_folder = f'asset_folder="{folder}" OR asset_folder="{folder}/*" OR public_id:{folder}/*'
    images, videos = run_search(expr_folder)
    diag["folder_count"] = len(images) + len(videos)
    diag["method"] = "folder"

    # 2) Fallback: kalau folder kosong, ambil semua kecuali samples bawaan
    if diag["folder_count"] == 0:
        expr_all = '-public_id:samples/* AND -folder:samples'
        images, videos = run_search(expr_all)
        diag["all_count"] = len(images) + len(videos)
        diag["method"] = "all (fallback)"

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
        letter-spacing: .1em;
        text-align: center;
        margin: 2.5rem 0 1.5rem 0;
        font-weight: 400;
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
        "ketemu di folder : %s\n"
        "ketemu semua (fallback) : %s\n"
        "error : %s"
        % (CLOUD_FOLDER, diag.get("folder_count"), diag.get("all_count"),
           diag.get("error") or "(tidak ada)"),
        language="text",
    )
    st.caption("Kalau 'error' berisi pesan, kirim ke chat. Kalau semua 0 tanpa error, "
               "berarti foto belum benar-benar ada di akun ini atau masih diproses.")
    st.stop()


# ------------------------------------------------------------
#  Slideshow otomatis fullscreen (Ken Burns + fade)
# ------------------------------------------------------------
st.markdown('<div class="section-title">✦ Slideshow ✦</div>', unsafe_allow_html=True)

slides_json = json.dumps([optimized(u, 1600) for u in images])

slideshow_html = """
<div id="show">
  <div id="stage"></div>
  <div id="caption"></div>
  <div id="controls">
    <button onclick="prev()">‹</button>
    <button onclick="toggle()" id="pp">❚❚</button>
    <button onclick="next()">›</button>
    <button onclick="fs()">⛶</button>
  </div>
  <div id="progress"><div id="bar"></div></div>
</div>
<style>
  #show {
    position: relative; width: 100%; height: 640px;
    background:#000; border-radius: 14px; overflow: hidden;
    box-shadow: 0 30px 80px rgba(0,0,0,.6);
  }
  #stage { width:100%; height:100%; position:relative; }
  #stage img {
    position:absolute; top:0; left:0; width:100%; height:100%;
    object-fit: cover; opacity:0; transition: opacity 1.6s ease;
  }
  #stage img.active { opacity:1; animation: ken 8s ease-in-out forwards; }
  @keyframes ken {
    0%   { transform: scale(1.0) translate(0,0); }
    100% { transform: scale(1.15) translate(-1.5%, -1.5%); }
  }
  #controls {
    position:absolute; bottom:22px; left:50%; transform:translateX(-50%);
    display:flex; gap:14px; z-index:5;
    background: rgba(10,10,15,.4); backdrop-filter: blur(8px);
    padding: 8px 16px; border-radius: 40px; border:1px solid rgba(184,168,136,.25);
  }
  #controls button {
    background:transparent; border:none; color:#e8ddc5;
    font-size: 20px; cursor:pointer; width:34px; height:34px;
    border-radius:50%; transition: all .25s;
  }
  #controls button:hover { background: rgba(184,168,136,.25); color:#fff; }
  #progress { position:absolute; bottom:0; left:0; width:100%; height:3px; background:rgba(255,255,255,.08); z-index:4;}
  #bar { height:100%; width:0%; background: linear-gradient(90deg,#b8a888,#e8ddc5); }
  #caption {
    position:absolute; top:20px; right:24px; z-index:5;
    font-family:'Inter',sans-serif; font-size:.75rem; letter-spacing:.15em;
    color:#b8a888; background:rgba(10,10,15,.4); padding:4px 12px; border-radius:20px;
  }
</style>
<script>
  const imgs = SLIDES_JSON;
  const stage = document.getElementById('stage');
  const cap = document.getElementById('caption');
  const bar = document.getElementById('bar');
  let i = 0, playing = true, timer=null, DUR=6500, t0=0;

  imgs.forEach((src, idx) => {
    const im = document.createElement('img');
    im.src = src; if(idx===0) im.className='active';
    stage.appendChild(im);
  });
  const els = () => stage.querySelectorAll('img');
  function render(){
    els().forEach((im,idx)=>{ im.classList.remove('active'); if(idx===i) void im.offsetWidth, im.classList.add('active'); });
    cap.textContent = (i+1)+' / '+imgs.length;
  }
  function next(){ i=(i+1)%imgs.length; render(); restart(); }
  function prev(){ i=(i-1+imgs.length)%imgs.length; render(); restart(); }
  function toggle(){ playing=!playing; document.getElementById('pp').textContent = playing?'❚❚':'▶'; if(playing) restart(); else clearInterval(timer); }
  function restart(){ clearInterval(timer); if(!playing) return; t0=Date.now();
    timer=setInterval(()=>{ let p=Math.min(1,(Date.now()-t0)/DUR); bar.style.width=(p*100)+'%'; if(p>=1) next(); }, 40);
  }
  function fs(){ const e=document.getElementById('show'); if(e.requestFullscreen) e.requestFullscreen(); }
  render(); restart();
</script>
""".replace("SLIDES_JSON", slides_json)

components.html(slideshow_html, height=680)


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
  <span id="lbClose">&times;</span>
  <img id="lbImg" onclick="event.stopPropagation()">
</div>
<style>
  #grid {
    columns: 4 240px; column-gap: 14px; padding: 4px;
  }
  #grid .cell {
    break-inside: avoid; margin-bottom: 14px; position:relative;
    border-radius: 10px; overflow:hidden; cursor:pointer;
    opacity:0; transform: translateY(20px);
    animation: rise .7s forwards;
  }
  @keyframes rise { to {opacity:1; transform:translateY(0);} }
  #grid img { width:100%; display:block; transition: transform .7s cubic-bezier(.2,.7,.2,1), filter .5s; filter: grayscale(15%) brightness(.92);}
  #grid .cell:hover img { transform: scale(1.09); filter: grayscale(0) brightness(1.05); }
  #grid .cell::after {
    content:''; position:absolute; inset:0;
    background: linear-gradient(to top, rgba(184,168,136,.25), transparent 55%);
    opacity:0; transition: opacity .5s;
  }
  #grid .cell:hover::after { opacity:1; }
  #lightbox {
    display:none; position:fixed; inset:0; z-index:9999;
    background: rgba(5,5,7,.94); backdrop-filter: blur(6px);
    align-items:center; justify-content:center;
  }
  #lightbox.on { display:flex; }
  #lbImg { max-width:92%; max-height:88%; border-radius:10px; box-shadow:0 20px 80px rgba(0,0,0,.7); animation: pop .4s ease;}
  @keyframes pop { from{opacity:0; transform:scale(.94);} to{opacity:1; transform:scale(1);} }
  #lbClose { position:fixed; top:20px; right:32px; color:#e8ddc5; font-size:44px; cursor:pointer; z-index:10000;}
</style>
<script>
  const data = GRID_DATA;
  const g = document.getElementById('grid');
  data.forEach((d,idx)=>{
    const c=document.createElement('div'); c.className='cell';
    c.style.animationDelay=(idx*45)+'ms';
    const im=document.createElement('img'); im.src=d.t; im.loading='lazy';
    im.onclick=()=>openLb(d.f);
    c.appendChild(im); g.appendChild(c);
  });
  function openLb(src){ document.getElementById('lbImg').src=src; document.getElementById('lightbox').classList.add('on'); }
  function closeLb(){ document.getElementById('lightbox').classList.remove('on'); }
  document.addEventListener('keydown',e=>{ if(e.key==='Escape') closeLb(); });
</script>
""".replace("GRID_DATA", grid_data)

grid_height = max(400, (len(images) // 4 + 1) * 220)
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
