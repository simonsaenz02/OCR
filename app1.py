import streamlit as st
import cv2
import numpy as np
import pytesseract
from PIL import Image

# ----------------- CONFIGURACIÓN -----------------
st.set_page_config(
    page_title="🔍 OCR - Lupa Mágica de Texto",
    layout="wide",
    page_icon="🪄"
)

# ----------------- ESTILOS -----------------
st.markdown(
    """
    <style>
    body {
        background: linear-gradient(to right, #fdfbfb, #ebedee);
        font-family: 'Segoe UI', sans-serif;
    }
    .title {
        text-align: center; 
        font-size: 42px; 
        font-weight: bold; 
        color: #1e3d59;
        margin-bottom: 0px;
    }
    .subtitle {
        text-align: center; 
        font-size: 20px; 
        color: #4a6572; 
        margin-top: 0px;
        margin-bottom: 25px;
    }
    .stButton>button {
        background: linear-gradient(to right, #1e3c72, #2a5298);
        color: white;
        border-radius: 10px;
        padding: 0.6em 1.2em;
        font-size: 16px;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        background: linear-gradient(to right, #2a5298, #1e3c72);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ----------------- ENCABEZADO -----------------
st.markdown("<p class='title'>🪄 Lupa Mágica de Texto</p>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Convierte imágenes en palabras y revela mensajes ocultos al instante</p>", unsafe_allow_html=True)


# ----------------- SIDEBAR -----------------
with st.sidebar:
    st.header("⚙️ Opciones de captura")
    fuente = st.radio("📷 Elige la fuente de la imagen", ("Cámara", "Archivo"))
    filtro = st.radio("🎨 Aplicar filtro", ("Con Filtro", "Sin Filtro"))
    st.markdown("---")
    st.info("✨ El filtro invierte los colores, muy útil cuando el texto es oscuro sobre un fondo claro.")


# ----------------- CAPTURA / CARGA -----------------
img_file_buffer = None

if fuente == "Cámara":
    img_file_buffer = st.camera_input("📸 Captura una imagen")
else:
    img_file_buffer = st.file_uploader("📂 Sube una imagen", type=["jpg", "jpeg", "png"])


# ----------------- PROCESO -----------------
if img_file_buffer is not None:
    # Leer imagen con OpenCV
    bytes_data = img_file_buffer.getvalue()
    cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)

    # Aplicar filtro si es necesario
    if filtro == "Con Filtro":
        cv2_img = cv2.bitwise_not(cv2_img)

    # Convertir a RGB para Tesseract
    img_rgb = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)

    # Mostrar imagen procesada
    st.markdown("## 🖼️ Imagen procesada")
    st.image(img_rgb, caption="🔎 Imagen utilizada para OCR", use_container_width=True)

    # Extraer texto
    text = pytesseract.image_to_string(img_rgb)

    # Mostrar resultado
    st.markdown("## 📜 Texto reconocido")
    if text.strip():
        st.success(f"✨ Aquí está el mensaje oculto:\n\n{text}")
    else:
        st.warning("⚠️ No se detectó texto en la imagen. Intenta mejorar la iluminación o usar el filtro.")



    


