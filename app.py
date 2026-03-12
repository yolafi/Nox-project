import streamlit as st
import pandas as pd

# 1. Configuration de la page (l'icône de l'onglet reste la lune pour le rappel)
st.set_page_config(page_title="NOX", page_icon="🌑", layout="centered")

# 2. Initialisation du stockage des votes en session
if 'votes' not in st.session_state:
    st.session_state.votes = {}

# 3. Connexion au Google Sheet
# Remplace bien par ton ID si tu le changes, mais celui-là semble être le bon
SHEET_ID = "16bSqmFKnS-Fex_-BP2pr7GaGqnd-gdZ2Q6rtqstddSc"
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

@st.cache_data(ttl=60)
def load_data():
    return pd.read_csv(CSV_URL).dropna(subset=["Nom de l'objet"])

# 4. Interface principale
try:
    df = load_data()

    # --- AFFICHAGE DE TON LOGO UNIQUEMENT ---
    # Centrage du logo
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("https://i.ibb.co/cK88yMMn/16780.png", use_container_width=True)
    
    st.divider()

    for index, row in df.iterrows():
        name = row["Nom de l'objet"]
        image_url = row["Lien vidéo (ou photo)"]
        global_score = row["Nox-score"]

        with st.container():
            # Affichage de l'image de l'item
            try:
                st.image(image_url, use_container_width=True)
            except:
                st.write("⚠️ Image not available")

            st.subheader(name)

            # Affichage du score global (issu du Google Sheet)
            st.metric(label="Global NOX-SCORE", value=f"{global_score}/10")

            # Logique de vote personnelle
            if index in st.session_state.votes:
                st.success(f"Your Score: {st.session_state.votes[index]}/10 ✅")
                
                # Bouton pour annuler et revoter
                if st.button(f"Reset my vote", key=f"reset_{index}"):
                    del st.session_state.votes[index]
                    st.rerun()
            else:
                # Curseur de vote
                note = st.slider(f"Rate this item", 0, 10, 5, key=f"s_{index}")
                if st.button(f"Submit {note}/10", key=f"b_{index}"):
                    st.session_state.votes[index] = note
                    st.rerun()
            
            st.divider()

except Exception as e:
    st.error("Connection error. Please check your Google Sheet settings.")
