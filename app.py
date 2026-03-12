import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import hashlib
import random
import smtplib
from email.message import EmailMessage

# --- CONFIGURATION DE LA PAGE ---
st.set_page_content(page_title="NOX Project", layout="wide")

# Connexion à Google Sheets (utilise le JSON des secrets)
conn = st.connection("gsheets", type=GSheetsConnection)

# --- FONCTIONS DE SÉCURITÉ ---
def hash_password(password):
    """Crypte le mot de passe pour ne pas le lire en clair dans le Sheet"""
    return hashlib.sha256(str.encode(password)).hexdigest()

def send_otp(target_email, code):
    """Envoie le code de vérification par mail"""
    msg = EmailMessage()
    msg.set_content(f"Ton code de validation NOX est : {code}")
    msg['Subject'] = f"{code} est ton code NOX"
    msg['From'] = st.secrets["EMAIL_SENDER"]
    msg['To'] = target_email
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(st.secrets["EMAIL_SENDER"], st.secrets["EMAIL_PASSWORD"])
            smtp.send_message(msg)
        return True
    except Exception as e:
        st.error(f"Erreur d'envoi de mail : {e}")
        return False

# --- GESTION DE LA SESSION ---
if 'user' not in st.session_state:
    st.session_state.user = None

# --- BARRE LATÉRALE ---
with st.sidebar:
    # Ton logo GitHub
    st.image("https://raw.githubusercontent.com/yolafi/Nox-project/main/Sans%20titre%203_20260312145229.png")
    st.title("Espace Membre")

    if st.session_state.user is None:
        mode = st.radio("Menu", ["Se connecter", "S'inscrire"])
        
        email_input = st.text_input("Email")
        
        if mode == "S'inscrire":
            if st.button("Envoyer le code de validation"):
                otp = str(random.randint(100000, 999999))
                if send_otp(email_input, otp):
                    st.session_state.otp = otp
                    st.session_state.temp_email = email_input
                    st.success("Code envoyé ! Vérifie tes mails.")
            
            code_verif = st.text_input("Entre le code reçu")
            if code_verif and code_verif == st.session_state.get('otp'):
                new_user = st.text_input("Choisis un Pseudo")
                new_pass = st.text_input("Choisis un Mot de passe", type="password")
                
                if st.button("Créer mon compte"):
                    # Lecture du fichier USERS via son URL
                    df_u = conn.read(spreadsheet=st.secrets["connections"]["gsheets"]["url_users"])
                    if new_user in df_u['username'].values:
                        st.error("Ce pseudo est déjà utilisé !")
                    else:
                        # Ajout de l'utilisateur
                        new_data = pd.DataFrame([{
                            "email": st.session_state.temp_email,
                            "username": new_user,
                            "password": hash_password(new_pass)
                        }])
                        conn.create(spreadsheet=st.secrets["connections"]["gsheets"]["url_users"], data=new_data)
                        st.success("Compte créé avec succès !")
        
        else: # Connexion
            u_login = st.text_input("Pseudo")
            p_login = st.text_input("Mot de passe", type="password")
            if st.button("Se connecter"):
                df_u = conn.read(spreadsheet=st.secrets["connections"]["gsheets"]["url_users"])
                if u_login in df_u['username'].values:
                    hashed_input = hash_password(p_login)
                    # On récupère le mot de passe stocké
                    stored_pwd = df_u[df_u['username'] == u_login]['password'].values[0]
                    if hashed_input == stored_pwd:
                        st.session_state.user = u_login
                        st.rerun()
                st.error("Pseudo ou mot de passe incorrect.")
    else:
        st.write(f"Utilisateur : **{st.session_state.user}**")
        if st.button("Déconnexion"):
            st.session_state.user = None
            st.rerun()

# --- CORPS DE LA PAGE (LES ITEMS) ---
st.header("🏆 Classement NOX")

try:
    # Lecture du fichier ITEM NOX via son URL
    df_items = conn.read(spreadsheet=st.secrets["connections"]["gsheets"]["url_items"])
    
    # On trie par score décroissant
    df_sorted = df_items.sort_values(by="nox-score", ascending=False)

    for index, row in df_sorted.iterrows():
        with st.container(border=True):
            c1, c2, c3 = st.columns([1, 3, 1])
            with c1:
                st.image(row['photo'], width=100)
            with c2:
                st.subheader(row['name'])
                st.caption(f"Catégorie : {row['category']}")
            with c3:
                st.metric("Score", f"{row['nox-score']}")
                if st.button("Voter", key=f"btn_{index}"):
                    if st.session_state.user:
                        st.balloons()
                        st.success("Vote enregistré !")
                    else:
                        st.warning("Connecte-toi pour voter !")
except Exception as e:
    st.error("Erreur de chargement des items. Vérifie les liens URL dans tes secrets.")
