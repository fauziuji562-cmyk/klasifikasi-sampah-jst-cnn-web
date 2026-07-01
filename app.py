import streamlit as st
from PIL import Image

# 1. ENGINE SISTEM PAKAR (RULE-BASED EXPERT SYSTEM AI)
# Memilah kategori sampah berdasarkan karakteristik fisik (Poin 2 & 3 Instruksi Dosen)
def sistem_pakar_pemilah(karakteristik):
    rules = {
        "organik": ["Mudah membusuk", "Berasal dari makhluk hidup", "Basah/Lembab", "Sisa makanan/tumbuhan"],
        "anorganik": ["Sulit terurai", "Buatan manusia/pabrik", "Kering/Keras", "Bahan plastik/logam/kaca"]
    }
    
    skor_organik = sum(1 for k in karakteristik if k in rules["organik"])
    skor_anorganik = sum(1 for k in karakteristik if k in rules["anorganik"])
    
    if skor_organik > skor_anorganik:
        return "Sampah Organik (Organic)", skor_organik / (skor_organik + skor_anorganik) * 100
    elif skor_anorganik > skor_organik:
        return "Sampah Anorganik (Recyclable)", skor_anorganik / (skor_organik + skor_anorganik) * 100
    else:
        return "Perlu Analisis Lebih Lanjut", 50.0

# 2. TAMPILAN INTERMUKA WEB (GUI)
st.set_page_config(page_title="Sistem Pakar AI Pemilah Sampah", page_icon="♻️")

st.title("♻️ Implementasi Sistem Pakar: AI Pemilah Sampah Cerdas")
st.write("**Proyek Akhir Mata Kuliah Kecerdasan Buatan (AI)**")
st.write("---")

st.info("💡 *Yuk, jagalah kebersihan! Buanglah sampah pada tempatnya agar tidak mencemari lingkungan sekitar kita.*")

# Ruang Edukasi & Karakteristik Data (Poin 3)
st.write("### 📚 Pengetahuan Basis (Knowledge Base)")
col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    **🌱 Karakteristik Sampah Organik**
    * Mudah membusuk & terurai alami.
    * Berasal dari sisa makanan/tumbuhan.
    * *Manfaat:* Bagus untuk pupuk kompos!
    """)
with col2:
    st.markdown("""
    **🍾 Karakteristik Sampah Anorganik**
    * Sangat susah terurai secara alami (butuh ratusan tahun).
    * Berasal dari bahan sintetis/plastik/logam.
    """)

st.write("---")

# Fitur Upload Gambar (Poin 4: Data Image)
st.write("### 📸 Langkah 1: Upload Foto Sampah")
uploaded_file = st.file_uploader("Pilih file gambar (JPG, JPEG, PNG)...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Gambar yang dievaluasi oleh sistem.', use_container_width=True)
    
    st.write("---")
    st.write("### 🧠 Langkah 2: Identifikasi Ciri Fisik oleh Pakar")
    st.write("Silakan centang ciri-ciri yang terlihat pada sampah tersebut:")
    
    # Input Gejala / Karakteristik untuk Inference Engine
    c1 = st.checkbox("Mudah membusuk atau berbau dalam beberapa hari")
    c2 = st.checkbox("Berasal dari makhluk hidup (tumbuhan/hewan)")
    c3 = st.checkbox("Kondisinya basah atau lembab")
    c4 = st.checkbox("Berupa sisa makanan, kulit buah, atau daun")
    
    c5 = st.checkbox("Sangat sulit hancur/terurai di tanah")
    c6 = st.checkbox("Merupakan produk buatan pabrik/manusia")
    c7 = st.checkbox("Kondisinya kering atau berstruktur keras")
    c8 = st.checkbox("Terbuat dari plastik, botol, kaleng, atau kaca")
    
    # Proses Analisis Inference Engine (Poin 3)
    karakteristik_terpilih = []
    if c1: karakteristik_terpilih.append("Mudah membusuk")
    if c2: karakteristik_terpilih.append("Berasal dari makhluk hidup")
    if c3: karakteristik_terpilih.append("Basah/Lembab")
    if c4: karakteristik_terpilih.append("Sisa makanan/tumbuhan")
    if c5: karakteristik_terpilih.append("Sulit terurai")
    if c6: karakteristik_terpilih.append("Buatan manusia/pabrik")
    if c7: karakteristik_terpilih.append("Kering/Keras")
    if c8: karakteristik_terpilih.append("Bahan plastik/logam/kaca")
    
    if st.button("🔮 Jalankan Analisis Sistem Pakar AI"):
        if not karakteristik_terpilih:
            st.warning("⚠️ Mohon pilih minimal satu karakteristik fisik di atas untuk dianalisis.")
        else:
            hasil_prediksi, keyakinan = sistem_pakar_pemilah(karakteristik_terpilih)
            
            st.write("---")
            st.success(f"### Kategori Terdeteksi: **{hasil_prediksi}**")
            st.info(f"📊 **Tingkat Keyakinan Sistem Pakar:** {keyakinan:.2f}%")
            
            if "Anorganik" in hasil_prediksi:
                st.warning("⚠️ *Rekomendasi Pakar: Sampah ini sulit terurai. Silakan lakukan daur ulang (Recycle)!*")
            else:
                st.success("✅ *Rekomendasi Pakar: Sampah ini ramah lingkungan, cocok diproses menjadi kompos.*")
        st.info(f"💡 **Tingkat Keyakinan AI:** {persentase:.2f}%")
        st.success("✅ *Sampah ini ramah lingkungan dan bisa membusuk secara alami.*")
