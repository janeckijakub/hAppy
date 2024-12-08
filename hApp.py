import streamlit as st
import sqlite3
import random
import re
import datetime
import time
from datetime import datetime

# Konfiguracja strony
st.set_page_config(
    page_title="hAppy Apka",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

# Style
st.markdown("""
    <style>
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    
    .video-container, .thumbnail-container {
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
        margin: 1rem 0;
    }
    
    .controls-container {
        display: flex;
        justify-content: center;
        gap: 20px;
        margin-bottom: 2rem;
        align-items: center;
        padding: 1rem;
    }
    
    iframe {
        max-width: 100%;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    
    .thumbnail-img {
        max-width: 800px;
        width: 100%;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    
    .link-container {
        background: rgba(128, 128, 128, 0.1);
        padding: 10px;
        border-radius: 4px;
        margin: 10px 0;
        word-break: break-all;
    }
    
    .settings-section {
        padding: 10px;
        margin: 10px 0;
        border-radius: 4px;
        background: rgba(128, 128, 128, 0.1);
    }
    
    .settings-info {
        font-size: 0.9em;
        margin-top: 5px;
        color: rgba(255, 255, 255, 0.7);
    }
    
    .stButton button {
        min-width: 120px;
        border: none;
        background-color: rgba(255, 255, 255, 0.1);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 4px;
        cursor: pointer;
        transition: background-color 0.3s;
    }
    
    .stButton button:hover {
        background-color: rgba(255, 255, 255, 0.2);
    }
    
    .stCheckbox {
        background: transparent !important;
    }
    
    /* Ukrycie domyślnego hamburger menu */
    .st-emotion-cache-1dp5vir {
        display: none;
    }
    </style>
""", unsafe_allow_html=True)

# Inicjalizacja stanu sesji
if 'links' not in st.session_state:
    st.session_state.links = []
if 'current_video' not in st.session_state:
    st.session_state.current_video = None
if 'last_refresh' not in st.session_state:
    st.session_state.last_refresh = None
if 'auto_play' not in st.session_state:
    st.session_state.auto_play = True  # hAppy continuum domyślnie wyłączone
if 'last_video_time' not in st.session_state:
    st.session_state.last_video_time = time.time()
if 'video_duration' not in st.session_state:
    st.session_state.video_duration = 6
if 'video_active' not in st.session_state:
    st.session_state.video_active = True
if 'first_load' not in st.session_state:
    st.session_state.first_load = True

def refresh_links():
    """Odświeża listę linków z bazy danych"""
    try:
        conn = sqlite3.connect('clips.db')
        cursor = conn.cursor()
        cursor.execute("SELECT clip_url FROM clips")
        st.session_state.links = cursor.fetchall()
        st.session_state.last_refresh = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    except sqlite3.Error as e:
        st.sidebar.error(f"Błąd bazy danych: {e}")
        st.session_state.links = []
    finally:
        if 'conn' in locals():
            conn.close()

def get_video_id(link):
    """Wyciąga ID filmu z linku YouTube"""
    match = re.search(r"v=([a-zA-Z0-9_-]+)", link)
    return match.group(1) if match else None

def get_thumbnail_url(video_id):
    """Pobiera URL miniaturki filmu YouTube"""
    return f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"

def get_random_link():
    """Zwraca losowy link z listy"""
    if not st.session_state.links:
        return None, 0, 0
    index = random.randint(0, len(st.session_state.links) - 1)
    return st.session_state.links[index][0], index + 1, len(st.session_state.links)

def transform_to_embed(link):
    """Przekształca link YouTube na format embed"""
    video_id = get_video_id(link)
    if not video_id:
        return None
    
    start_time_match = re.search(r"[&?]t=(\d+)", link)
    start_time = start_time_match.group(1) if start_time_match else "0"
    
    return f"https://www.youtube.com/embed/{video_id}?start={start_time}&autoplay=1&enablejsapi=1"

def get_new_video():
    """Pobiera nowe losowe wideo i aktualizuje stan"""
    link, current, total = get_random_link()
    if link:
        video_id = get_video_id(link)
        embed_link = transform_to_embed(link)
        thumbnail_url = get_thumbnail_url(video_id)
        
        st.session_state.current_video = {
            'original_link': link,
            'embed_link': embed_link,
            'thumbnail_url': thumbnail_url,
            'current': current,
            'total': total
        }
        st.session_state.last_video_time = time.time()
        st.session_state.video_active = True
        st.session_state.first_load = False
    return link is not None

def check_video_state():
    """Sprawdza stan odtwarzania wideo"""
    if st.session_state.current_video:
        current_time = time.time()
        elapsed_time = current_time - st.session_state.last_video_time
        
        if st.session_state.auto_play and elapsed_time >= st.session_state.video_duration:
            get_new_video()
            st.rerun()
        elif not st.session_state.auto_play and elapsed_time >= st.session_state.video_duration and st.session_state.video_active:
            st.session_state.video_active = False
            st.rerun()

# Automatyczne pierwsze załadowanie linków
if not st.session_state.links:
    refresh_links()
    if st.session_state.first_load:
        get_new_video()

# Główne kontrolki nad filmem
st.markdown('<div class="controls-container">', unsafe_allow_html=True)
col1, col2 = st.columns([1, 1])
with col1:
    if st.button("🎲 hAppy shot", key="random"):
        get_new_video()
with col2:
    auto_play = st.checkbox("🔄 hAppy continuum", value=st.session_state.auto_play)
    if auto_play != st.session_state.auto_play:
        st.session_state.auto_play = auto_play
        st.session_state.last_video_time = time.time()
        st.session_state.video_active = True
st.markdown('</div>', unsafe_allow_html=True)

# Główny obszar z wideo
placeholder = st.empty()
with placeholder.container():
    check_video_state()
    
    if st.session_state.current_video:
        if st.session_state.video_active:
            # Wyświetlanie aktywnego wideo
            st.markdown('<div class="video-container">', unsafe_allow_html=True)
            st.components.v1.iframe(
                src=st.session_state.current_video['embed_link'],
                width=800,
                height=450,
                scrolling=False
            )
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            # Wyświetlanie miniaturki po zakończeniu odtwarzania
            st.markdown(f"""
                <div class="thumbnail-container">
                    <img src="{st.session_state.current_video['thumbnail_url']}" 
                         class="thumbnail-img" 
                         alt="Miniaturka filmu">
                </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Kliknij 'hAppy shot', aby rozpocząć")

# Sidebar z dodatkowymi ustawieniami
with st.sidebar:
    st.title("Menu kontroli")
    
    # Sekcja ustawień czasu
    st.markdown("### Ustawienia")
    selected_duration = st.slider(
        "⏱️ Czas odtwarzania (sekundy)",
        min_value=5,
        max_value=10,
        value=st.session_state.video_duration,
        step=1,
        help="Ustaw czas odtwarzania filmu (od 5 do 10 sekund)"
    )
    
    if selected_duration != st.session_state.video_duration:
        st.session_state.video_duration = selected_duration
        if st.session_state.video_active:
            st.session_state.last_video_time = time.time()

    # Informacje o aktualnym wideo
    if st.session_state.current_video:
        st.markdown("### Informacje")
        st.info(f"Wideo {st.session_state.current_video['current']} z {st.session_state.current_video['total']}")
        
        # Timer i pasek postępu
        if st.session_state.video_active or st.session_state.auto_play:
            current_time = time.time()
            elapsed = current_time - st.session_state.last_video_time
            time_left = max(0, st.session_state.video_duration - elapsed)
            progress = 1 - (time_left / st.session_state.video_duration)
            st.progress(progress)
            st.write(f"Pozostało: {int(time_left)} sekund")
        
        # Link do skopiowania
        st.markdown("### Link do filmu")
        st.markdown(f"""
            <div class="link-container">
                <div style="word-break: break-all;">{st.session_state.current_video['original_link']}</div>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("📋 Kopiuj link", key="copy_link"):
            st.write("Link skopiowany!")
            st.code(st.session_state.current_video['original_link'], language=None)
    
    # Status odświeżania
    if st.session_state.last_refresh:
        st.markdown("### Status")
        st.info(f"🕒 Ostatnie odświeżenie: {st.session_state.last_refresh}")

# Wymuszenie odświeżania dla licznika
if st.session_state.current_video and (st.session_state.auto_play or st.session_state.video_active):
    time.sleep(1)
    st.rerun()