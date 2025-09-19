import streamlit as st
import pandas as pd
import random
import time
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
    df = pd.read_excel(uploaded_file)
    return df.iloc[:, 0].dropna().astype(str).tolist()

def split_predefined_used(list_a, list_b):
    """Trả về các predefined pairs hợp lệ + used sets."""
    used_pairs = []
    used_a, used_b = set(), set()
    for a, b in predefined_pairs:
        if a in list_a and b in list_b:
            used_pairs.append((a, b))
            used_a.add(a)
            used_b.add(b)
    return used_pairs, used_a, used_b

def generate_final_pairs(list_a, list_b):
    """Sinh kết quả cuối cùng (đúng predefined + random phần còn lại)."""
    used_pairs, used_a, used_b = split_predefined_used(list_a, list_b)
    remaining_a = [x for x in list_a if x not in used_a]
    remaining_b = [x for x in list_b if x not in used_b]
    random.shuffle(remaining_a)
    random.shuffle(remaining_b)
    final_pairs = used_pairs + list(zip_longest(remaining_a, remaining_b, fillvalue="(Chưa có bạn)"))
    return final_pairs

def maybe_swap_lists(list_a, list_b):
    """Hoán đổi list nếu user upload nhầm."""
    predefined_a = [pair[0] for pair in predefined_pairs]
    predefined_b = [pair[1] for pair in predefined_pairs]

    score_a = sum(name in list_b for name in predefined_a)
    score_b = sum(name in list_a for name in predefined_b)

    if score_a > len(predefined_a) // 2 and score_b > len(predefined_b) // 2:
        return list_b, list_a
    return list_a, list_b

def to_excel_bytes(df: pd.DataFrame) -> bytes:
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Pairs")
    buffer.seek(0)
    return buffer.read()

# ===== UI =====
st.set_page_config(page_title="Random Badminton Pairs", layout="centered")
st.title("🏸 Random Ghép Cặp Cầu Lông — Phiên bản xịn xò")

# Upload
uploaded_file_a = st.file_uploader("📂 Tải danh sách A lên", type=["xlsx"])
uploaded_file_b = st.file_uploader("📂 Tải danh sách B lên", type=["xlsx"])

# Sidebar controls
st.sidebar.header("Tùy chỉnh hiệu ứng shuffle")
shuffle_iters = st.sidebar.slider("Số lần shuffle (ít → nhiều)", 6, 60, 25, 1)
shuffle_speed = st.sidebar.slider("Độ nhanh (ms)", 20, 400, 80, 10)

# Thêm thời gian shuffle lâu hơn 3s
extra_iters = max(1, int(3000 / shuffle_speed))
shuffle_iters += extra_iters

if uploaded_file_a and uploaded_file_b:
    list_a = load_data_from_file(uploaded_file_a)
    list_b = load_data_from_file(uploaded_file_b)
    list_a, list_b = maybe_swap_lists(list_a, list_b)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Danh sách A")
        st.dataframe(pd.DataFrame({"Tên": list_a}), height=300)
    with col2:
        st.subheader("Danh sách B")
        st.dataframe(pd.DataFrame({"Tên": list_b}), height=300)

    if st.button("🎲 Ghép cặp (Shuffle xịn xò)"):
        # Kết quả cuối cùng (đúng predefined)
        final_pairs = generate_final_pairs(list_a, list_b)

        # Placeholder để update animation
        placeholder = st.empty()

        # Lấy toàn bộ tên để shuffle giả vờ
        all_a = list_a.copy()
        all_b = list_b.copy()

        for i in range(shuffle_iters):
            tmp_a = all_a.copy()
            tmp_b = all_b.copy()
            random.shuffle(tmp_a)
            random.shuffle(tmp_b)
            tmp_pairs = list(zip_longest(tmp_a, tmp_b, fillvalue="(Chưa có bạn)"))
            df_tmp = pd.DataFrame(tmp_pairs, columns=["Người A", "Người B"])
            with placeholder.container():
                st.markdown(f"**Shuffle đang chạy...** ⏳ ({i+1}/{shuffle_iters})")
                st.dataframe(df_tmp, height=420)
            time.sleep(shuffle_speed / 1000.0)

        # Hiển thị kết quả cuối
        df_final = pd.DataFrame(final_pairs, columns=["Người A", "Người B"])
        with placeholder.container():
            st.success("✅ Kết quả ghép cặp (đã lock!)")
            st.dataframe(df_final, height=420)

        # Nút tải xuống
        st.download_button(
            "⬇️ Tải kết quả (.xlsx)",
            to_excel_bytes(df_final),
            file_name="ket_qua_ghep_cap.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
else:
    st.info("👉 Hãy tải lên 2 file .xlsx (mỗi file 1 cột tên) để bắt đầu.")
