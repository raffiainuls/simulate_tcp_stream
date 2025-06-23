import streamlit as st
from kafka import KafkaConsumer
import json
import pandas as pd
import altair as alt
import time


# Sidebar konfigurasi
st.sidebar.title("⚙️ Kafka Streaming Setup")


# Pilihan simbol dan topik Kafka
symbol_options = {
    "CAD/USD": "cad_usd_data",
    "CHF/AED": "chf_aed_data",
    "EUR/RSD": "eur_rsd_data",
    "EUR/USD": "eur_usd_data",
    "GBP/MUR": "gbp_mur_data",
    "ILS/VEF": "ils_vef_data",
    "KRW/CNY": "krw_cny_data",
    "TRY/EUR": "try_eur_data",
    "USD/CNY": "usd_cny_data",
    "ZAR/KES": "zar_kes_data"
}

selected_symbol = st.sidebar.selectbox("Pilih Symbol", options=list(symbol_options.keys()))
KAFKA_TOPIC = symbol_options[selected_symbol]
KAFKA_SERVER = "localhost:9093"

max_points = st.sidebar.slider("Jumlah Maksimum Data ditampilkan", min_value=30, max_value=500, value=100)
show_stats = st.sidebar.checkbox("Tampilkan Statistik", value=True)


# UI layout
st.title(f"📈 Real-Time Chart dari Kafka: {selected_symbol}")
chart_placeholder = st.empty()
stats_placeholder = st.empty()

# Inisialisasi Kafka Consumer
consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=[KAFKA_SERVER],
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='latest',
    enable_auto_commit=True,
    group_id=f'streamlit-group-{KAFKA_TOPIC}'
)



# Simpan data streaming
data_df = pd.DataFrame(columns=["DATETIME", "CLOSE"])

print(data_df)

# Loop streaming Kafka
for msg in consumer:
    val = msg.value

    # Filter berdasarkan symbol jika field SYMBOL ada
    if "SYMBOL" in val and val["SYMBOL"] != selected_symbol:
        continue
    # Tambah data
    new_row = pd.DataFrame([[val["DATETIME"], val["CLOSE"]]], columns=["DATETIME", "CLOSE"])
    print(new_row)
    data_df = pd.concat([data_df, new_row], ignore_index=True)

    # Sliding window
    if len(data_df) > max_points:
        data_df = data_df.iloc[-max_points:]

    # Proses data untuk chart
    data_df["CLOSE"] = pd.to_numeric(data_df["CLOSE"])
    data_df["DATETIME"] = pd.to_datetime(data_df["DATETIME"])
    df_plot = data_df.copy()

    # Y-axis dinamis
    y_min = df_plot["CLOSE"].min() * 0.999
    y_max = df_plot["CLOSE"].max() * 1.001

    chart = (
        alt.Chart(df_plot)
        .mark_line()
        .encode(
            x=alt.X("DATETIME:T", title="Waktu", axis=alt.Axis(labelAngle=-45),  timeUnit="hoursminutesseconds",),
            y=alt.Y("CLOSE:Q", title="Harga", scale=alt.Scale(domain=[y_min, y_max])),
        )
        .properties(height=400, width=800)
    )

    chart_placeholder.altair_chart(chart, use_container_width=True)

    if show_stats:
        stats_placeholder.markdown(f"""
        ### 📊 Statistik Harga
        - Jumlah: `{len(data_df)}`
        - Rata-rata: `{df_plot['CLOSE'].mean():.6f}`
        - Maksimum: `{df_plot['CLOSE'].max():.6f}`
        - Minimum: `{df_plot['CLOSE'].min():.6f}`
        - Terakhir: `{df_plot['CLOSE'].iloc[-1]:.6f}` pada `{df_plot['DATETIME'].iloc[-1]}`
        """)
