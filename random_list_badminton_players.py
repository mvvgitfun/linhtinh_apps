import streamlit as st
import pandas as pd
import random
from itertools import zip_longest
from io import BytesIO

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
@st.cache_data(hash_funcs={BytesIO: lambda _: None})
def load_data_from_file(uploaded_file):
    """Đọc file Excel, lấy cột đầu tiên thành list tên."""
    df = pd.read_excel(uploaded_file)
    return df.iloc[:, 0].dropna().tolist()

def generate_pairs(list_a, list_b):
    """Ghép cặp từ danh sách A, B và cặp predefined."""
    final_pairs = []
    used_a, used_b = set(), set()

    # Shuffle bản copy của predefined để tránh thay đổi global
    pairs = predefined_pairs.copy()
    random.shuffle(pairs)

    # Ghép predefined trước
    for a, b in pairs:
        if a in list_a and b in list_b and a not in used_a and b not in used_b:
            final_pairs.append((a, b))
            used_a.add(a)
            used_b.add(b)

    # Random phần còn lại
    remaining_a = [x for x in list_a if x not in used_a]
    remaining_b = [x for x in list_b if x not in used_b]
    random.shuffle(remaining_a)
    random.shuffle(remaining_b)

    for a, b in zip_longest(remaining_a, remaining_b, fillvalue="(Chưa có bạn)"):
        final_pairs.append((a, b))

    return final_pairs

def maybe_swap_lists(list_a, list_b):
    """Nếu user upload nhầm A và B thì hoán đổi lại."""
    predefined_a = [pair[0] for pair in predefined_pairs]
    predefined_b = [pair[1] for pair in predefined_pairs]

    score_a = sum(name in list_b for name in predefined_a)
    score_b = sum(name in list_a for name in predefined_b)

    # Nếu > nửa predefined nằm sai list thì swap
    if score_a > len(predefined_a) // 2 and score_b > len(predefined_b) // 2:
        return list_b, list_a
    return list_a, list_b

# ===== UI =====
st.set_page_config(page_title="Random Badminton Pairs", layout="centered")
st.title("🏸 Random Ghép Cặp Cầu Lông")

# Upload files
uploaded_file_a = st.file_uploader("📂 Tải danh sách A lên", type=["xlsx"])
uploaded_file_b = st.file_uploader("📂 Tải danh sách B lên", type=["xlsx"])

if uploaded_file_a and uploaded_file_b:
    # Load dữ liệu
    list_a = load_data_from_file(uploaded_file_a)
    list_b = load_data_from_file(uploaded_file_b)

    # Tự động check và hoán đổi nếu cần
    list_a, list_b = maybe_swap_lists(list_a, list_b)

    # Hiển thị danh sách A và B
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Danh sách A")
        st.dataframe(pd.DataFrame({"Tên": list_a}), height=300)
    with col2:
        st.subheader("Danh sách B")
        st.dataframe(pd.DataFrame({"Tên": list_b}), height=300)

    # Nút random
    if st.button("🎲 Ghép cặp ngẫu nhiên"):
        pairs = generate_pairs(list_a, list_b)
        df_pairs = pd.DataFrame(pairs, columns=["Người A", "Người B"])
        st.success("✅ Kết quả ghép cặp:")
        st.dataframe(df_pairs, height=500)
