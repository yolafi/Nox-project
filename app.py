import streamlit as st
import pandas as pd
from google_auth_oauthlib.flow import Flow

# 1. CONFIGURATION
st.set_page_config(page_title="NOX Project", layout="wide")

# 2. RÉCUPÉRATION DES SECRETS
CLIENT_ID = st.secrets["google_client_id"]
CLIENT_SECRET = st.secrets["google_client_secret"]
REDIRECT_URI = "https://nox-project-xxwo8gphqmfphkndnksaqn.streamlit.app/"

# 3. CONFIGURATION DU FLUX GOOGLE
client_config = {
    "web": {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
    }
}

# 4. GESTION DE LA SESSION
if 'connected' not in st.session_state:
    st.session_state.connected = False

# --- LOGIQUE DE CONNEXION ---
def get_login_url():
    flow = Flow.from_client_config(
        client_config,
        scopes=["openid", "https://www.googleapis.com/auth/userinfo.email", "https://www.googleapis.com/auth/userinfo.profile"],
        redirect_uri=REDIRECT_URI
    )
    auth_url, _ = flow.authorization_url(prompt='select_account')
    return auth_url

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://raw.githubusercontent.com/yolafi/Nox-project/main/Sans%20titre%203_20260312145229.png", width=80)
    st.title("NOX Account")
    
    if not st.session_state.connected:
        login_url = get_login_url()
        # On utilise un lien stylisé en bouton
        st.markdown(f'''
            <a href="{login_url}" target="_self" style="text-decoration: none;">
                <div style="background-color: #df4b3b; color: white; padding: 10px; text-align: center; border-radius: 5px;">
                    Se connecter avec Google
                </div>
            </a>
        ''', unsafe_allow_html=True)
        
        # Petit hack pour le test : si on revient avec un code dans l'URL
        if "code" in st.query_params:
            st.session_state.connected = True
            st.rerun()
    else:
        st.success("Connecté")
        if st.button("Déconnexion"):
            st.session_state.connected = False
            st.rerun()

# --- RESTE DE L'INTERFACE ---
st.title("NOX Database")
st.divider()

if st.session_state.connected:
    st.write("✅ Accès autorisé aux votes.")
    # Ici tes données Google Sheets...
else:
    st.warning("🔒 Veuillez utiliser le bouton Google dans le menu à gauche.")
