import streamlit as st
import cv2
import numpy as np
import pytesseract
from PIL import Image


# ----------------- CONFIGURACIÓN -----------------
st.set_page_config(
    page_title="OCR - Reconocimiento de Texto",
    layout="wide"
)

# ----------------- ESTILOS -----------------
st.markdown(
    """
    <style>
    .title {text-align: center; font-size: 36px; font-weight: bold; color: #2c3e50;}
    .subtitle {text-align: center; font-size: 18px; color: #7f8c8d; margin-bottom: 20px;}
    </style>
    """,
    unsafe_allow_html=True
)

# ----------------- ENCABEZADO -----------------
st.markdown("<p class='title'>Reconocimiento Óptico de Caracteres (OCR)</p>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Toma una foto o carga una imagen para extraer el texto automáticamente</p>", unsafe_allow_html=True)


# ----------------- SIDEBAR -----------------
with st.sidebar:
    st.header("Opciones")
    fuente = st.radio("Selecciona la fuente de imagen", ("Cámara", "Archivo"))
    filtro = st.radio("Aplicar filtro", ("Con Filtro", "Sin Filtro"))
    st.markdown("---")
    st.info("El filtro invierte los colores, útil cuando el texto es oscuro sobre fondo claro.")


# ----------------- CAPTURA / CARGA -----------------
img_file_buffer = None

if fuente == "Cámara":
    img_file_buffer = st.camera_input("Captura una imagen")
else:
    img_file_buffer = st.file_uploader("Sube una imagen", type=["jpg", "jpeg", "png"])


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
    st.markdown("### Imagen procesada")
    st.image(img_rgb, caption="Imagen utilizada para OCR", use_container_width=True)

    # Extraer texto
    text = pytesseract.image_to_string(img_rgb)

    # Mostrar resultado
    st.markdown("### Texto reconocido")
    if text.strip():
        st.success(text)
    else:
        st.warning("No se detectó texto en la imagen.")



    


