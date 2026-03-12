import streamlit as st
import pandas as pd

if 'votes' not in st.session_state:
    st.session_state.votes = {}

st.set_page_config(page_title="NOX", page_icon="🌑")

# --- CONNEXION ---
sheet_id = "16bSqmFKnS-Fex_-BP2pr7GaGqnd-gdZ2Q6rtqstddSc"
csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

def load_data():
    # On lit le CSV et on nettoie les lignes vides
    return pd.read_csv(csv_url).dropna(subset=["Nom de l'objet"])

try:
    df = load_data()

    st.title("🌑 NOX")
    st.write("Le baromètre de la hype.")

    # La ligne ci-dessous doit avoir exactement 4 espaces de décalage par rapport au bord
    for index, row in df.iterrows():
        nom = row["Nom de l'objet"]
        image_url = row["Lien vidéo (ou photo)"]
        description = row["Description courte"]

        with st.container():
            try:
                st.image(image_url, use_container_width=True)
            except:
                st.write("⚠️ Image non disponible")

            st.subheader(nom)
            st.write(f"*{description}*")

            # --- LOGIQUE SANS BALLONS ---
            if index in st.session_state.votes:
                st.success(f"Ton Nox-Score : {st.session_state.votes[index]}/10 ✅")
            else:
                note = st.slider(f"Note pour {nom}", 0, 10, 5, key=f"s_{index}")
                if st.button(f"Valider {note}/10", key=f"b_{index}"):
                    st.session_state.votes[index] = note
                    st.rerun()
            
            st.divider()

except Exception as e:
    st.error("Erreur de lecture.")