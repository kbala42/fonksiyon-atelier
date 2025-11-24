import numpy as np
import matplotlib.pyplot as plt
import streamlit as st


# -----------------------------
# Streamlit temel ayar
# -----------------------------
st.set_page_config(page_title="Fonksiyon Çizim Atölyesi", page_icon="📈")

st.title("📈 Fonksiyon Çizim Atölyesi")
st.write(
    """
Bu atölyede **lineer**, **karesel** ve **karekök** fonksiyonlarının grafikleriyle oynayarak  
fonksiyon–grafik ilişkisini gözlemleyeceksin.

- Fonksiyonu seç
- x aralığını ayarla
- Grafiğin nasıl değiştiğini incele
"""
)

st.markdown("---")


# -----------------------------
# Fonksiyon seçimi ve x aralığı
# -----------------------------
func_name = st.radio(
    "Fonksiyon seç:",
    ["y = x", "y = x²", "y = √x"],
)

x_min, x_max = st.slider(
    "x aralığını seç:",
    min_value=-10.0,
    max_value=10.0,
    value=(-5.0, 5.0),
    step=0.5,
    help="Karekök fonksiyonu için x en az 0'dan başlamalıdır.",
)


# -----------------------------
# x değerlerini hazırlama
# -----------------------------
if func_name == "y = √x":
    # Kareköklü fonksiyon için negatiflerden kaçın
    x_min_effective = max(0.0, x_min)
    if x_min_effective >= x_max:
        st.error("Karekök fonksiyonu için x aralığının üst sınırı 0'dan büyük olmalıdır.")
        st.stop()
    x = np.linspace(x_min_effective, x_max, 400)
else:
    x = np.linspace(x_min, x_max, 400)


# -----------------------------
# Fonksiyon değerlerini hesaplama
# -----------------------------
def compute_y(name: str, x_values: np.ndarray) -> np.ndarray:
    if name == "y = x":
        return x_values
    elif name == "y = x²":
        return x_values ** 2
    elif name == "y = √x":
        return np.sqrt(x_values)
    else:
        return x_values


y = compute_y(func_name, x)


# -----------------------------
# Grafiği çizme
# -----------------------------
fig, ax = plt.subplots()

ax.plot(x, y, label=func_name)

# Eksenleri çiz
ax.axhline(0, linewidth=0.8)
ax.axvline(0, linewidth=0.8)

ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_title("Fonksiyon Grafiği")
ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.5)
ax.legend()

st.pyplot(fig)


# -----------------------------
# Küçük açıklamalar
# -----------------------------
st.markdown("---")

if func_name == "y = x":
    st.info(
        "Bu fonksiyon **doğrusal (lineer)** bir fonksiyondur. "
        "Grafiği orijinden geçen düz bir doğrudur ve x arttıkça y de aynı oranda artar."
    )
elif func_name == "y = x²":
    st.info(
        "Bu fonksiyon **karesel** bir fonksiyondur. "
        "Grafiği yukarı doğru açılan bir **paraboldür**. "
        "Negatif ve pozitif x değerleri için y aynı olur (çünkü x²)."
    )
elif func_name == "y = √x":
    st.info(
        "Bu fonksiyon **karekök** fonksiyonudur. "
        "Sadece x ≥ 0 için tanımlıdır. "
        "x büyüdükçe y artar ama gitgide daha yavaş artar."
    )

st.caption(
    "Bu atölye, fonksiyon–grafik ilişkisini sezgisel olarak keşfetmek isteyen "
    "ortaokul/erken lise öğrencileri için tasarlanmıştır."
)
