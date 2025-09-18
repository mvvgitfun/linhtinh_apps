import streamlit as st
import pandas as pd
import random
import time

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
    list_a = pd.read_excel(LIST_A_URL)["Name"].dropna().tolist()
    list_b = pd.read_excel(LIST_B_URL)["Name"].dropna().tolist()
    return list_a, list_b

# ===== UI =====
st.set_page_config(page_title="Random Badminton Pairs", layout="centered")

# Banner (auto resize full width)
st.image("https://raw.githubusercontent.com/mvvgitfun/linhtinh_apps/blob/main/phuocnguyenthanh.jpg", use_container_width=True)

st.title("🏸 Random Ghép Cặp Cầu Lông")

list_a, list_b = load_data()

# Hiện bảng 2 list
col1, col2 = st.columns(2)
with col1:
    st.subheader("Danh sách A")
    st.table(pd.DataFrame({"Tên": list_a}))
with col2:
    st.subheader("Danh sách B")
    st.table(pd.DataFrame({"Tên": list_b}))

# Shuffle & hiển thị kết quả
if st.button("🎲 Random cặp đấu"):
    placeholder = st.empty()

    # Shuffle effect
    for _ in range(10):
        temp_pairs = list(zip(random.sample(list_a, len(list_a)), random.sample(list_b, len(list_b))))
        temp_text = "\n".join([f"Cặp {i+1}: {a} - {b}" for i, (a, b) in enumerate(temp_pairs)])
        placeholder.markdown(f"```\n{temp_text}\n```")
        time.sleep(0.2)

    # Kết quả cuối cùng
    final_pairs = []
    used_a, used_b = set(), set()

    for a, b in predefined_pairs:
        if a in list_a and b in list_b:
            final_pairs.append((a, b))
            used_a.add(a)
            used_b.add(b)

    remaining_a = [x for x in list_a if x not in used_a]
    remaining_b = [x for x in list_b if x not in used_b]
    random.shuffle(remaining_a)
    random.shuffle(remaining_b)

    for a, b in zip(remaining_a, remaining_b):
        final_pairs.append((a, b))

    # Hiển thị kết quả cuối cùng
    result_text = "\n".join([f"Cặp {i+1}: {a} - {b}" for i, (a, b) in enumerate(final_pairs)])
    placeholder.markdown(f"### ✅ Kết quả cuối cùng\n\n```\n{result_text}\n```")
