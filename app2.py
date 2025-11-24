# Fraktal Piksel Boyama (Basit Mandelbrot)
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st


# -----------------------------
# Streamlit temel ayar
# -----------------------------
st.set_page_config(page_title="Fraktal Piksel Boyama", page_icon="🌀")

st.title("🌀 Fraktal Piksel Boyama (Basit Mandelbrot)")
st.write(
    """
Her piksel için basit bir iterasyon kuralı çalıştırarak,
Mandelbrot kümesinden esinlenen renkli bir desen oluşturalım.

- Genişlik / yükseklik ile piksel sayısını ayarla  
- İterasyon sayısını değiştir  
- Zoom ile ayrıntıya yaklaş
"""
)

st.markdown("---")


# -----------------------------
# Kullanıcı kontrolleri
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    width = st.slider("Genişlik (piksel)", 50, 400, 200, step=50)
with col2:
    height = st.slider("Yükseklik (piksel)", 50, 400, 200, step=50)

max_iter = st.slider("Maksimum iterasyon sayısı", 10, 100, 30, step=5)

zoom = st.slider(
    "Yakınlaştırma (zoom)",
    min_value=1,
    max_value=10,
    value=1,
    step=1,
    help="Değer arttıkça daha küçük bir bölgeyi, daha detaylı görürsün.",
)

st.markdown("---")


# -----------------------------
# Mandelbrot fonksiyonu
# -----------------------------
def mandelbrot(c: complex, max_iter: int) -> int:
    """
    Verilen c noktası için, |z| > 2 olana kadar
    kaç iterasyon gerektiğini döndürür.
    Eğer max_iter'a kadar taşmazsa, max_iter döner.
    """
    z = 0 + 0j
    for n in range(max_iter):
        z = z * z + c
        if abs(z) > 2:
            return n
    return max_iter


# -----------------------------
# Koordinat aralığı (zoom ile)
# -----------------------------
# Mandelbrot kümesinin "ilginç" kısmının ortası:
re_center = -0.5
im_center = 0.0

# Başlangıç aralığı
base_re_min, base_re_max = -2.0, 1.0
base_im_min, base_im_max = -1.5, 1.5

# Zoom'a göre aralığı daralt
scale = 1 / zoom

re_range = (base_re_max - base_re_min) * scale
im_range = (base_im_max - base_im_min) * scale

re_min = re_center - re_range / 2
re_max = re_center + re_range / 2
im_min = im_center - im_range / 2
im_max = im_center + im_range / 2

re_values = np.linspace(re_min, re_max, width)
im_values = np.linspace(im_min, im_max, height)


# -----------------------------
# Piksel tablosunu hesaplama
# -----------------------------
image = np.zeros((height, width))

for i, im in enumerate(im_values):
    for j, re in enumerate(re_values):
        c = complex(re, im)
        n = mandelbrot(c, max_iter=max_iter)
        image[i, j] = n

# -----------------------------
# Görselleştirme
# -----------------------------
fig, ax = plt.subplots(figsize=(6, 6))
im_plot = ax.imshow(
    image,
    extent=[re_min, re_max, im_min, im_max],
    cmap="magma",
    origin="lower",
)
ax.set_xlabel("Gerçek eksen")
ax.set_ylabel("İmajiner eksen")
ax.set_title("Basitleştirilmiş Mandelbrot Fraktali")

st.pyplot(fig)

st.markdown("---")
st.info(
    "Her piksel için aynı formülü uyguluyoruz: "
    "zₙ₊₁ = zₙ² + c, z₀ = 0.\n\n"
    "Eğer |z| değeri hızlıca büyüyorsa (2'yi geçerse), piksel 'dışarıda' sayılıyor "
    "ve daha düşük iterasyon sayılarıyla boyanıyor.\n"
    "Ne kadar uzun süre taşmazsa, o kadar 'içeride' ve o kadar farklı renkte görünüyor."
)

st.caption(
    "Bu uygulama, iterasyon ve fraktal fikrini sezgisel olarak tanıtmak için "
    "ortaokul/erken lise düzeyi öğrencilerle kullanılabilir."
)
