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
    """Đọc file Excel, lấy cột đầu tiên thành list tên."""
    df = pd.read_excel(uploaded_file)
    return df.iloc[:, 0].dropna().astype(str).tolist()

def split_predefined_used(list_a, list_b):
    """
    Trả về:
      - used predefined pairs (the ones that exist in both lists),
      - set used_a, set used_b
    """
    pairs = predefined_pairs.copy()
    random.shuffle(pairs)  # shuffle copy để kết quả predefined không quá cố định
    used_pairs = []
    used_a, used_b = set(), set()
    for a, b in pairs:
        if a in list_a and b in list_b and a not in used_a and b not in used_b:
            used_pairs.append((a, b))
            used_a.add(a)
            used_b.add(b)
    return used_pairs, used_a, used_b

def generate_pairs(list_a, list_b):
    """Ghép cặp từ danh sách A, B và cặp predefined."""
    final_pairs = []
    used_pairs, used_a, used_b = split_predefined_used(list_a, list_b)
    final_pairs.extend(used_pairs)

    remaining_a = [x for x in list_a if x not in used_a]
    remaining_b = [x for x in list_b if x not in used_b]
    random.shuffle(remaining_a)
    random.shuffle(remaining_b)

    for a, b in zip_longest(remaining_a, remaining_b, fillvalue="(Chưa có bạn)"):
        final_pairs.append((a, b))

    return final_pairs

def maybe_swap_lists(list_a, list_b):
    """Nếu user upload nhầm A và B thì hoán đổi lại dựa trên đa số cặp predefined."""
    predefined_a = [pair[0] for pair in predefined_pairs]
    predefined_b = [pair[1] for pair in predefined_pairs]

    score_a = sum(name in list_b for name in predefined_a)
    score_b = sum(name in list_a for name in predefined_b)

    # Nếu > nửa predefined nằm sai list thì swap
    if score_a > len(predefined_a) // 2 and score_b > len(predefined_b) // 2:
        return list_b, list_a
    return list_a, list_b

def to_excel_bytes(df: pd.DataFrame) -> bytes:
    """Trả về bytes của DataFrame dưới dạng excel để download."""
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Pairs")
    buffer.seek(0)
    return buffer.read()

# ===== UI =====
st.set_page_config(page_title="Random Badminton Pairs", layout="centered")
st.title("🏸 Random Ghép Cặp Cầu Lông — Phiên bản xịn xò")

st.markdown("Tải 2 file `.xlsx` (mỗi file 1 cột tên). Sau đó bấm **Ghép cặp** để thấy hiệu ứng shuffle 🔥")

# Upload files
uploaded_file_a = st.file_uploader("📂 Tải danh sách A lên", type=["xlsx"])
uploaded_file_b = st.file_uploader("📂 Tải danh sách B lên", type=["xlsx"])

# Animation controls
st.sidebar.header("Tùy chỉnh hiệu ứng shuffle")
shuffle_iters = st.sidebar.slider("Số lần shuffle (ít → nhiều)", min_value=6, max_value=40, value=18, step=1)
shuffle_speed = st.sidebar.slider("Độ nhanh (ms giữa mỗi lần)", min_value=20, max_value=400, value=70, step=10)

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

    # Nút random + animation
    if st.button("🎲 Ghép cặp (có shuffle)"):
        # 1) Tách các predefined đã có
        used_pairs, used_a, used_b = split_predefined_used(list_a, list_b)

        # 2) Remaining lists
        remaining_a = [x for x in list_a if x not in used_a]
        remaining_b = [x for x in list_b if x not in used_b]

        # 3) Tạo final result cho phần remaining (đây là kết quả cuối)
        final_remaining_a = remaining_a.copy()
        final_remaining_b = remaining_b.copy()
        random.shuffle(final_remaining_a)
        random.shuffle(final_remaining_b)
        final_remaining_pairs = list(zip_longest(final_remaining_a, final_remaining_b, fillvalue="(Chưa có bạn)"))
        final_pairs = used_pairs + final_remaining_pairs

        # 4) Hiệu ứng shuffle: hiển thị nhiều lần các ghép tạm thời trước khi show kết quả cuối
        placeholder = st.empty()
        for i in range(shuffle_iters):
            tmp_a = remaining_a.copy()
            tmp_b = remaining_b.copy()
            random.shuffle(tmp_a)
            random.shuffle(tmp_b)
            tmp_pairs = used_pairs + list(zip_longest(tmp_a, tmp_b, fillvalue="(Chưa có bạn)"))
            df_tmp = pd.DataFrame(tmp_pairs, columns=["Người A", "Người B"])
            # Thêm header "Shuffle..." cho cảm giác drama
            with placeholder.container():
                st.markdown(f"**Shuffle đang chạy...** ⏳ ({i+1}/{shuffle_iters})")
                st.dataframe(df_tmp, height=420)
            time.sleep(shuffle_speed / 1000.0)

        # 5) Hiển thị kết quả cuối
        df_final = pd.DataFrame(final_pairs, columns=["Người A", "Người B"])
        with placeholder.container():
            st.success("✅ Kết quả ghép cặp (đã lock!)")
            st.dataframe(df_final, height=420)

        # 6) Tải xuống excel
        excel_bytes = to_excel_bytes(df_final)
        st.download_button(
            label="⬇️ Tải kết quả (.xlsx)",
            data=excel_bytes,
            file_name="ket_qua_ghep_cap.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

else:
    st.info("Chưa có file. Hãy tải lên 2 file .xlsx (mỗi file 1 cột tên) để bắt đầu.")
