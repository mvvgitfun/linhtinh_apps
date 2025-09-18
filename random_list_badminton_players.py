import streamlit as st
import pandas as pd
import random
import time
from itertools import zip_longest

# ===== Config =====
LIST_A_URL = "https://raw.githubusercontent.com/mvvgitfun/linhtinh_apps/main/listA.xlsx"
LIST_B_URL = "https://raw.githubusercontent.com/mvvgitfun/linhtinh_apps/main/listB.xlsx"

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

# ===== Functions =====
def load_data():
    df_a = pd.read_excel(LIST_A_URL)
    df_b = pd.read_excel(LIST_B_URL)

    # Nếu không chắc cột tên, lấy cột đầu tiên
    list_a = df_a.iloc[:, 0].dropna().tolist()
    list_b = df_b.iloc[:, 0].dropna().tolist()
    return list_a, list_b

def generate_pairs(list_a, list_b):
    # Shuffle toàn bộ danh sách
    random.shuffle(list_a)
    random.shuffle(list_b)

    # Ghép bằng zip_longest để không bỏ sót ai
    final_pairs = list(zip_longest(list_a, list_b, fillvalue="(Chưa có bạn)"))
    return final_pairs

# ===== UI =====
st.set_page_config(page_title="Random Badminton Pairs", layout="centered")

# Banner
# st.image("1d971c70-306f-42ae-a442-4f72cfd6be72.png", use_container_width=True)
st.title("🏸 Random Ghép Cặp Cầu Lông")

list_a, list_b = load_data()

# Hiện bảng 2 list
col1, col2 = st.columns(2)
with col1:
    st.subheader("Danh sách A")
    st.dataframe(pd.DataFrame({"Tên": list_a}), height=300)
with col2:
    st.subheader("Danh sách B")
    st.dataframe(pd.DataFrame({"Tên": list_b}), height=300)

# Shuffle & hiển thị kết quả
if st.button("🎲 Random cặp đấu"):
    placeholder = st.empty()

    # Hiệu ứng shuffle nhanh
    for _ in range(10):
        temp_pairs = list(zip(random.sample(list_a, len(list_a)), random.sample(list_b, len(list_b))))
        temp_text = "\n".join([f"Cặp {i+1}: {a} - {b}" for i, (a, b) in enumerate(temp_pairs)])
        placeholder.markdown(f"```\n{temp_text}\n```")
        time.sleep(0.15)

    # Kết quả cuối cùng
    final_pairs = generate_pairs(list_a, list_b)
    result_text = "\n".join([f"Cặp {i+1}: {a} - {b}" for i, (a, b) in enumerate(final_pairs)])
    placeholder.markdown(f"### Kết quả cuối cùng\n\n```\n{result_text}\n```")



