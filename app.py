import streamlit as st
import pandas as pd

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

    for index, row in df.iterrows():
        # On utilise exactement les noms de ta capture d'écran
        nom = row["Nom de l'objet"]
        image_url = row["Lien vidéo (ou photo)"]
        description = row["Description courte"]

        with st.container():
            # Affichage de l'image
            try:
                st.image(image_url, use_container_width=True)
            except:
                st.write("⚠️ Image non disponible")
            
            st.subheader(nom)
            st.write(f"*{description}*")
            
            # Slider de note
            note = st.slider(f"Note pour {nom}", 0, 10, 5, key=f"s_{index}")
            
            if st.button(f"Valider {note}/10", key=f"b_{index}"):
                st.success(f"Voté !")
            st.divider()

except Exception as e:
    st.error("Erreur de lecture. Vérifie que ton Sheet est bien en 'Tous les utilisateurs disposant du lien'.")
    # Pour t'aider à débugger si ça plante encore :
    # st.write(e) 
