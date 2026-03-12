import streamlit as st
import pandas as pd

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(
    page_title="NOX Project",
    page_icon="https://raw.githubusercontent.com/yolafi/Nox-project/main/Sans%20titre%203_20260312145229.png",
    layout="wide"
)

# 2. RÉCUPÉRATION DES SECRETS (GOOGLE AUTH)
# Note: Ces variables doivent exister dans Streamlit Cloud > Settings > Secrets
try:
    CLIENT_ID = st.secrets["google_client_id"]
    CLIENT_SECRET = st.secrets["google_client_secret"]
except:
    st.warning("⚠️ Configuration Google Auth manquante dans les Secrets.")

# 3. CHARGEMENT DES DONNÉES GOOGLE SHEETS
SHEET_ID = "16bSqmFKnS-Fex_-BP2pr7GaGqnd-gdZ2Q6rtqstddSc"
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

@st.cache_data(ttl=60)
def load_data():
    try:
        data = pd.read_csv(CSV_URL)
        return data.dropna(subset=["Nom de l'objet"])
    except Exception as e:
        st.error(f"Erreur de connexion au Google Sheet : {e}")
        return pd.DataFrame()

# 4. GESTION DE LA CONNEXION (SESSION STATE)
if 'connected' not in st.session_state:
    st.session_state.connected = False

# --- SIDEBAR (CONNEXION & LOGO) ---
with st.sidebar:
    # Petit logo en haut de la sidebar
    st.image("https://raw.githubusercontent.com/yolafi/Nox-project/main/Sans%20titre%203_20260312145229.png", width=80)
    st.title("NOX Account")
    st.divider()
    
    if not st.session_state.connected:
        st.write("Connectez-vous pour voter.")
        if st.button("🔴 Sign in with Google"):
            # Simulation du succès pour le moment
            st.session_state.connected = True
            st.rerun()
    else:
        st.success("Connecté à NOX")
        if st.button("Se déconnecter"):
            st.session_state.connected = False
            st.rerun()
    
    st.divider()
    st.caption("Version 1.0 - NOX Project")

# --- INTERFACE PRINCIPALE ---
# Affichage du logo et du titre sur la page
col_logo, col_titre = st.columns([1, 6])
with col_logo:
    st.image("https://raw.githubusercontent.com/yolafi/Nox-project/main/Sans%20titre%203_20260312145229.png", width=100)
with col_titre:
    st.title("NOX - Database & Voting")

st.divider()

# Chargement du DataFrame
df = load_data()

if not df.empty:
    # Boucle pour afficher chaque objet du Google Sheet
    for index, row in df.iterrows():
        name = row["Nom de l'objet"]
        img_url = row["Lien vidéo (ou photo)"]
        score = row["Nox-score"]
        
        with st.container(border=True):
            c1, c2 = st.columns([1, 2])
            
            with c1:
                # Affichage de l'image de l'objet
                st.image(img_url, use_container_width=True)
            
            with c2:
                st.subheader(name)
                st.metric("Global NOX-SCORE", f"{score}/10")
                
                # Système de vote (uniquement si connecté)
                if st.session_state.connected:
                    vote = st.slider(f"Votre note pour {name}", 0, 10, 5, key=f"slider_{index}")
                    if st.button(f"Voter {vote}/10", key=f"btn_{index}"):
                        st.balloons()
                        st.success(f"Vote enregistré pour {name} !")
                else:
                    st.info("💡 Connectez-vous dans le menu à gauche pour voter.")

else:
    st.info("Aucune donnée trouvée dans le Google Sheet.")
