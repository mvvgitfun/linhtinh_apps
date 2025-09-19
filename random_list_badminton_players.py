import streamlit as st
import pandas as pd
import random
import time
from itertools import zip_longest

# ===== Predefined Pairs =====
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
@st.cache_data
def load_data_from_file(uploaded_file):
    # Đọc file Excel từ người dùng tải lên
    df = pd.read_excel(uploaded_file)
    return df.iloc[:, 0].dropna().tolist()

def generate_pairs(list_a, list_b):
    final_pairs = []
    used_a, used_b = set(), set()

    # Thêm predefined pairs sau khi random
    random.shuffle(predefined_pairs)
    for a, b in predefined_pairs:
        if a in list_a and b in list_b:
            final_pairs.append((a, b))
            used_a.add(a)
            used_b.add(b)

    # Phần còn lại random
    remaining_a = [x for x in list_a if x not in used_a]
    remaining_b = [x for x in list_b if x not in used_b]
    random.shuffle(remaining_a)
    random.shuffle(remaining_b)

    for a, b in zip_longest(remaining_a, remaining_b, fillvalue="(Chưa có bạn)"):
        final_pairs.append((a, b))

    return final_pairs

# ===== UI =====
st.set_page_config(page_title="Random Badminton Pairs", layout="centered")
st.title("🏸 Random Ghép Cặp Cầu Lông")

# Upload files
uploaded_file_a = st.file_uploader("Tải danh sách A lên", type=["xlsx"])
uploaded_file_b = st.file_uploader("Tải danh sách B lên", type=["xlsx"])

if uploaded_file_a and uploaded_file_b:
    # Load dữ liệu
    list_a = load_data_from_file(uploaded_file_a)
    list_b = load_data_from_file(uploaded_file_b)

    # Kiểm tra và hoán đổi nếu người dùng tải nhầm danh sách
    predefined_a = [pair[0] for pair in predefined_pairs]
    predefined_b = [pair[1] for pair in predefined_pairs]
    
    if all(name in list_b for name in predefined_a) and all(name in list_a for name in predefined_b):
        # Nếu A và B bị hoán đổi, hoán lại danh sách
        list_a, list_b = list_b, list_a

    # Hiển thị danh sách A và B
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Danh sách A")
        st.dataframe(pd.DataFrame({"Tên": list_a}), height=300)

