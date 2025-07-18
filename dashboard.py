import streamlit as st
from gdrive_upload import upload_to_drive
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="Upload Publik", layout="centered")
st.title("📁 Dashboard Data Tanaman 🌾")

hari_dict = {
    "Monday": "Senin", "Tuesday": "Selasa", "Wednesday": "Rabu",
    "Thursday": "Kamis", "Friday": "Jumat", "Saturday": "Sabtu", "Sunday": "Minggu"
}

# === Form Upload ===
with st.form("upload_form"):
    name = st.text_input("Nama Pengunggah")
    uploaded_file = st.file_uploader("Pilih File (.pdf, .docx, .xlsx)", type=["pdf", "docx", "xlsx"])
    submit = st.form_submit_button("Upload")

if submit and name and uploaded_file:
    try:
        file_url = upload_to_drive(uploaded_file, uploaded_file.name)
        st.success(f"✅ Upload sukses: [Lihat File]({file_url})")

        now = datetime.now()
        waktu = f"{hari_dict[now.strftime('%A')]}, {now.strftime('%Y-%m-%d %H:%M:%S')}"

        log = {
            "Nama": name,
            "File": uploaded_file.name,
            "Waktu": waktu,
            "Link": file_url,
            "Status": "Belum Dicek"
        }

        log_path = "upload_log.csv"
        df = pd.read_csv(log_path) if os.path.exists(log_path) else pd.DataFrame()
        df = pd.concat([pd.DataFrame([log]), df], ignore_index=True)
        df.to_csv(log_path, index=False)
    except Exception as e:
        st.error(f"❌ Gagal upload: {e}")

# === Monitoring Tabel ===
st.subheader("📄 Data Upload")
log_path = "upload_log.csv"
if os.path.exists(log_path):
    df = pd.read_csv(log_path)
    for i, row in df.iterrows():
        with st.container():
            col1, col2, col3 = st.columns([4, 1, 1])
            col1.markdown(f"- **{row['File']}** oleh *{row['Nama']}* ({row['Waktu']}) — {row['Status']}")
            if col2.button("✔️ Dicek", key=f"cek{i}"):
                df.at[i, 'Status'] = "Sudah Dicek"
                df.to_csv(log_path, index=False)
                st.experimental_rerun()
            if col3.button("🗑️ Hapus", key=f"hapus{i}"):
                df = df.drop(i).reset_index(drop=True)
                df.to_csv(log_path, index=False)
                st.experimental_rerun()
else:
    st.info("Belum ada data upload.")

# === Style Ringan ===
st.markdown("""
    <style>
    .main {
        background-color: #f9fbff;
        font-size: 14px;
    }
    .stButton>button {
        padding: 0.3em 0.6em;
        font-size: 13px;
    }
    </style>
""", unsafe_allow_html=True)
