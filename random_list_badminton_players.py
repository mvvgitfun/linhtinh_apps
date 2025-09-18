import streamlit as st
import pandas as pd
import random
import time
from io import BytesIO

# --- Config ---
LIST_A_URL = "https://raw.githubusercontent.com/mvvgitfun/linhtinh_apps/refs/heads/main/listA.xlsx"
LIST_B_URL = "https://raw.githubusercontent.com/mvvgitfun/linhtinh_apps/refs/heads/main/listB.xlsx"

# Định nghĩa cặp cố định (tên phải khớp trong file Excel)
predefined_pairs = [
    ("Lê Huỳnh Minh Trí", "Lan Nguyễn"),
    ("Lê Đình Tiến Đạt", "Ngô Thị Trúc Linh"),
    ("Võ Nhật Minh", "Chu Đăng Khoa"),
    ("Nguyễn Hoàng Việt", "Nguyễn Mạnh Cường"),
    ("Thanh Trường", "Thảo Ngân"),
    ("Nguyễn Lâm Tùng", "Nguyễn Thị Thùy Linh"),
    ("Lê Thị Ngọc Bích", "Vũ Thế Trọng"),
    ("Anh Tuân", "Gia Bảo")
]

# --- Helper ---
def load_data():
    # Đọc file Excel, tự động lấy cột đầu tiên
    list_a = pd.read_excel(LIST_A_URL).iloc[:, 0].dropna().tolist()
    list_b = pd.read_excel(LIST_B_URL).iloc[:, 0].dropna().tolist()
    return list_a, list_b

def make_pairs(list_a, list_b, predefined):
    used_a, used_b = set(), set()
    pairs = []

    # Add predefined
    for a, b in predefined:
        if a in list_a and b in list_b:
            pairs.append((a, b))
            used_a.add(a)
            used_b.add(b)

    # Shuffle and match rest
    remain_a = [x for x in list_a if x not in used_a]
    remain_b = [x for x in list_b if x not in used_b]
    random.shuffle(remain_a)
    random.shuffle(remain_b)

    for a, b in zip(remain_a, remain_b):
        pairs.append((a, b))

    return pairs

def convert_to_excel(pairs):
    df = pd.DataFrame(pairs, columns=["List A", "List B"])
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Pairs")
    processed_data = output.getvalue()
    return processed_data

# --- App ---
st.title("🎉 Welcome to Pairing App")

page = st.sidebar.selectbox("Navigation", ["Welcome", "Shuffle & Pair"])

if page == "Welcome":
    st.header("👋 Welcome")
    st.write("This app pairs people from **List A** and **List B**. Some pairs are predefined and fixed.")

    list_a, list_b = load_data()
    st.subheader("List A")
    st.write(list_a)
    st.subheader("List B")
    st.write(list_b)

elif page == "Shuffle & Pair":
    st.header("🔀 Shuffle and Pair")
    if st.button("Start Pairing!"):
        with st.spinner("Shuffling..."):
            time.sleep(2)  # fake animation delay
        list_a, list_b = load_data()
        pairs = make_pairs(list_a, list_b, predefined_pairs)

        st.success("✅ Pairing complete!")
        df_result = pd.DataFrame(pairs, columns=["List A", "List B"])
        st.table(df_result)

        excel_data = convert_to_excel(pairs)
        st.download_button(
            label="📥 Download Result",
            data=excel_data,
            file_name="pairing_result.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

