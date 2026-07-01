import streamlit as st
import tensorflow as tf
from PIL import Image
import numpy as np
import os
import urllib.request

# 1. DOWNLOAD & LOAD MODEL AI DARI GOOGLE DRIVE PERMANEN
@st.cache_resource
def load_my_model():
    model_path = 'model_klasifikasi_sampah.h5'
    
    # Jika file model belum ada di server cloud, download otomatis dari Google Drive kamu
    if not os.path.exists(model_path):
        with st.spinner('Sedang mengunduh otak AI dari server Google Drive... Mohon tunggu sebentar (proses ini hanya sekali di awal).'):
            # ID Google Drive milik Fauzi yang sudah dikonfigurasi publik
            drive_id = "1mo4IusdfPGZpqt9ygjic5d6Lp_m-x5Nm" 
            url = f'https://docs.google.com/uc?export=download&id={drive_id}'
            
            # Mengatasi kendala keamanan user-agent pada server cloud
            opener = urllib.request.build_opener()
            opener.addheaders = [('User-agent', 'Mozilla/5.0')]
            urllib.request.install_opener(opener)
            
            urllib.request.urlretrieve(url, model_path)
            
    return tf.keras.models.load_model(model_path)

try:
    model = load_my_model()
except Exception as e:
    st.error(f"Gagal memuat model AI. Error: {e}")

class_names = ['Sampah Organik (Organic)', 'Sampah Anorganik (Recyclable)']

# 2. TAMPILAN INTERMUKA WEB (GUI) SESUAI INSTRUKSI DOSEN
st.set_page_config(page_title="Sistem Pakar & AI Pemilah Sampah", page_icon="♻️")

# Judul Utama Akademis (Poin 2 & 3 Instruksi Dosen)
st.title("♻️ Sistem Pakar & AI Pemilah Sampah Berbasis Jaringan Saraf Tiruan (JST)")
st.write("**Proyek Akhir Mata Kuliah Kecerdasan Buatan (AI)**")
st.write("---")

# Edukasi & Kata-kata Bijak Lingkungan (Sesuai Permintaan)
st.info("💡 *Yuk, jagalah kebersihan! Buanglah sampah pada tempatnya agar tidak mencemari lingkungan sekitar kita.*")

st.write("### 📚 Tahukah Kamu?")
col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    **🌱 Sampah Organik**
    * Mudah membusuk dan terurai secara alami.
    * *Contoh:* Sisa makanan, daun kering, kulit buah.
    * *Manfaat:* Sangat bagus diolah kembali menjadi pupuk kompos!
    """)
with col2:
    st.markdown("""
    **🍾 Sampah Anorganik**
    * Sangat susah terurai secara alami oleh tanah.
    * Butuh waktu **10 hingga 20 tahun** (bahkan ratusan tahun untuk plastik) untuk hancur.
    * *Contoh:* Plastik, botol kaca, kaleng soda.
    """)

st.write("---")

# Fitur Utama Upload Gambar Evaluasi (Poin 3 & 4)
st.write("### 📸 Silakan Upload Foto Sampah")
uploaded_file = st.file_uploader("Pilih file gambar (JPG, JPEG, PNG)...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Gambar sampah yang di-upload.', use_container_width=True)
    
    st.write("🔄 **AI sedang menganalisis gambar menggunakan arsitektur CNN...**")
    
    # Preprocessing Data Test (Poin 3 Instruksi Dosen)
    img = image.resize((150, 150))
    img_array = np.array(img)
    
    if img_array.shape[-1] == 4:
        img_array = img_array[..., :3]
        
    img_array = img_array / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    
    # Evaluasi & Analisis Hasil Real-time (Poin 3)
    predictions = model.predict(img_array)
    score = predictions[0][0]
    
    if score >= 0.5:
        hasil_prediksi = class_names[1]
        persentase = score * 100
        st.write("---")
        st.success(f"### Kategori Terdeteksi: **{hasil_prediksi}**")
        st.info(f"💡 **Tingkat Keyakinan AI:** {persentase:.2f}%")
        st.warning("⚠️ *Ingat, sampah jenis ini sulit terurai. Mari lakukan daur ulang (recycle)!*")
    else:
        hasil_prediksi = class_names[0]
        persentase = (1 - score) * 100
        st.write("---")
        st.success(f"### Kategori Terdeteksi: **{hasil_prediksi}**")
        st.info(f"💡 **Tingkat Keyakinan AI:** {persentase:.2f}%")
        st.success("✅ *Sampah ini ramah lingkungan dan bisa membusuk secara alami.*")