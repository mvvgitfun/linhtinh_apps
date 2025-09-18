import streamlit as st
import pandas as pd
import random
import time

# Link excel raw (cột đầu tiên chứa tên)
LIST_A_URL = "https://raw.githubusercontent.com/mvvgitfun/linhtinh_apps/main/listA.xlsx"
LIST_B_URL = "https://raw.githubusercontent.com/mvvgitfun/linhtinh_apps/main/listB.xlsx"

# ====== Config predefined pairs ======
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

# Load data
@st.cache_data
def load_data():
    list_a = pd.read_excel(LIST_A_URL).iloc[:, 0].dropna().tolist()
    list_b = pd.read_excel(LIST_B_URL).iloc[:, 0].dropna().tolist()
    return list_a, list_b


def random_pairs(list_a, list_b, fixed_pairs):
    a = list_a.copy()
    b = list_b.copy()
    result = []

    # Apply predefined pairs trước
    for fa, fb in fixed_pairs:
        if fa in a and fb in b:
            result.append((fa, fb))
            a.remove(fa)
            b.remove(fb)

    # Shuffle phần còn lại
    random.shuffle(a)
    random.shuffle(b)

    for i in range(min(len(a), len(b))):
        result.append((a[i], b[i]))

    return result


# ===== Streamlit App =====
st.title("🏸 Welcome to PUB BADMINTON OPEN!!! 🏸")
st.write("Welcome! Mình sẽ random cặp đánh dựa trên 2 list lông thủ sau nha mọi người ơi.")

list_a, list_b = load_data()

# Hiển thị list ban đầu
st.subheader("📋 Danh sách gốc")
col1, col2 = st.columns(2)
with col1:
    st.write("**List A**")
    st.dataframe(pd.DataFrame(list_a, columns=["Name A"]))
with col2:
    st.write("**List B**")
    st.dataframe(pd.DataFrame(list_b, columns=["Name B"]))

# Nút bắt đầu shuffle
if st.button("🎰 Shuffle & Generate Pairs"):
    placeholder = st.empty()
    for i in range(10):  # giả vờ shuffle
        temp = list(zip(random.sample(list_a, len(list_a)), random.sample(list_b, len(list_b))))
        df_temp = pd.DataFrame(temp, columns=["A", "B"])
        placeholder.dataframe(df_temp)
        time.sleep(0.2)

    # Kết quả cuối
    pairs = random_pairs(list_a, list_b, predefined_pairs)
    df_result = pd.DataFrame(pairs, columns=["A", "B"])

    st.subheader("✅ Kết quả random")
    st.dataframe(df_result)

    # Download button
    csv = df_result.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Tải kết quả về (CSV)", csv, "pairs.csv", "text/csv")

