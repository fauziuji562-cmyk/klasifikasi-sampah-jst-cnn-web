import streamlit as st
import tensorflow as tf
from PIL import Image
import numpy as np

# 1. LOAD MODEL AI
@st.cache_resource
def load_my_model():
    return tf.keras.models.load_model('model_klasifikasi_sampah.h5')

try:
    model = load_my_model()
except Exception as e:
    st.error(f"Gagal memuat model. Error: {e}")

class_names = ['Sampah Organik (Organic)', 'Sampah Anorganik (Recyclable)']

# 2. TAMPILAN INTERMUKA WEB (GUI)
st.set_page_config(page_title="AI Pemilah Sampah", page_icon="♻️")

# Header Aplikasi
st.title("♻️ Aplikasi Sistem Pakar & AI Pemilah Sampah")
st.write("**Proyek Akhir Mata Kuliah Kecerdasan Buatan (AI)**")
st.write("---")

# Kata-kata Bijak Santai (Rekomendasi)
st.info("💡 *Yuk, jagalah kebersihan! Buanglah sampah pada tempatnya agar tidak mencemari lingkungan sekitar kita.*")

import streamlit as st
import tensorflow as tf
from PIL import Image
import numpy as np

# 1. LOAD MODEL AI
@st.cache_resource
def load_my_model():
    return tf.keras.models.load_model('model_klasifikasi_sampah.h5')

try:
    model = load_my_model()
except Exception as e:
    st.error(f"Gagal memuat model. Error: {e}")

class_names = ['Sampah Organik (Organic)', 'Sampah Anorganik (Recyclable)']

# 2. TAMPILAN INTERMUKA WEB (GUI)
st.set_page_config(page_title="Sistem Pakar & AI Pemilah Sampah", page_icon="♻️")

# Judul Utama sesuai Proyek Akhir
st.title("♻️ Sistem Pakar & AI Pemilah Sampah Berbasis Jaringan Saraf Tiruan (JST)")
st.write("**Proyek Akhir Mata Kuliah Kecerdasan Buatan (AI)**")
st.write("---")

# Kata-kata Bijak Santai 
st.info("💡 *Yuk, jagalah kebersihan! Buanglah sampah pada tempatnya agar tidak mencemari lingkungan sekitar kita.*")

# Ruang Edukasi Pendek
st.write("### 📚 Tahukah Kamu?")
col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    **🌱 Sampah Organik**
    * Mudah membusuk dan terurai alami.
    * *Contoh:* Sisa makanan, daun, kulit buah.
    * *Manfaat:* Bisa dijadikan pupuk kompos!
    """)
with col2:
    st.markdown("""
    **🍾 Sampah Anorganik**
    * Sangat susah terurai secara alami.
    * Butuh waktu **10 hingga 20 tahun** (bahkan ratusan tahun) untuk hancur.
    * *Contoh:* Plastik, botol, kaleng.
    """)

st.write("---")

# Fitur Utama Upload Gambar
st.write("### 📸 Silakan Upload Foto Sampah")
uploaded_file = st.file_uploader("Pilih file gambar (JPG, JPEG, PNG)...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Gambar yang di-upload.', use_container_width=True)
    
    st.write("🔄 **AI sedang menganalisis gambar...**")
    
    img = image.resize((150, 150))
    img_array = np.array(img)
    
    if img_array.shape[-1] == 4:
        img_array = img_array[..., :3]
        
    img_array = img_array / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    
    predictions = model.predict(img_array)
    score = predictions[0][0]
    
    if score >= 0.5:
        hasil_prediksi = class_names[1]
        persentase = score * 100
        st.write("---")
        st.success(f"### Kategori Terdeteksi: **{hasil_prediksi}**")
        st.info(f"💡 **Tingkat Keyakinan AI:** {persentase:.2f}%")
        st.warning("⚠️ *Ingat, sampah jenis ini sulit terurai. Mari daur ulang atau batasi penggunaannya!*")
    else:
        hasil_prediksi = class_names[0]
        persentase = (1 - score) * 100
        st.write("---")
        st.success(f"### Kategori Terdeteksi: **{hasil_prediksi}**")
        st.info(f"💡 **Tingkat Keyakinan AI:** {persentase:.2f}%")
        st.success("✅ *Sampah ini ramah lingkungan dan bisa diolah menjadi pupuk organik!*")