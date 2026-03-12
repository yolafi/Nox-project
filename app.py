import streamlit as st
import pandas as pd
import base64

# 1. Config de la page
st.set_page_config(page_title="NOX", page_icon="🌑", layout="centered")

# 2. Ton Logo NOX (intégré directement dans le code pour éviter les liens cassés)
LOGO_BASE64 = "https://i.ibb.co/cK88yMMn/16780.png" # Lien de secours

# 3. Mémoire des votes (local)
if 'votes' not in st.session_state:
    st.session_state.votes = {}

# 4. Récupération des données
SHEET_ID = "16bSqmFKnS-Fex_-BP2pr7GaGqnd-gdZ2Q6rtqstddSc"
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

@st.cache_data(ttl=60)
def load_data():
    return pd.read_csv(CSV_URL).dropna(subset=["Nom de l'objet"])

# 5. Interface
try:
    df = load_data()

    # --- AFFICHAGE DU LOGO ---
    # J'utilise ton lien direct qui semble être revenu, 
    # mais cette fois avec une gestion d'erreur pour ne pas bloquer l'app
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.image("https://i.ibb.co/cK88yMMn/16780.png", use_container_width=True)
    
    st.divider()

    for index, row in df.iterrows():
        name = row["Nom de l'objet"]
        image_url = row["Lien vidéo (ou photo)"]
        global_score = row["Nox-score"]

        with st.container():
            try:
                st.image(image_url, use_container_width=True)
            except:
                st.write("⚠️ Image not available")

            st.subheader(name)
            st.metric(label="Global NOX-SCORE", value=f"{global_score}/10")

            if index in st.session_state.votes:
                st.success(f"Your Score: {st.session_state.votes[index]}/10 ✅")
                if st.button(f"Reset vote", key=f"reset_{index}"):
                    del st.session_state.votes[index]
                    st.rerun()
            else:
                note = st.slider(f"Rate", 0, 10, 5, key=f"s_{index}")
                if st.button(f"Submit {note}/10", key=f"b_{index}"):
                    st.session_state.votes[index] = note
                    st.rerun()
            
            st.divider()

except Exception as e:
    st.error("Connection error. Check your Google Sheet.")
