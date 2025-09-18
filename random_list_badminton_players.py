import streamlit as st
import random
import pandas as pd
import time

st.set_page_config(page_title="Random Pair Demo", layout="centered")

st.title("🎲 Random Pair Demo")

# Tạo list mẫu
list_a = ["A", "B", "C", "D"]
list_b = ["X", "Y", "E", "Z"]

# Cặp cố định (ví dụ: A luôn đi với X)
fixed_pairs = {
    "A": "X"
}

if st.button("🔀 Shuffle & Pair"):
    with st.spinner("Shuffling... 🎰"):
        time.sleep(2)

    remaining_a = list_a[:]
    remaining_b = list_b[:]
    pairs = []

    # Ghép cặp cố định trước
    for a, b in fixed_pairs.items():
        if a in remaining_a and b in remaining_b:
            pairs.append((a, b))
            remaining_a.remove(a)
            remaining_b.remove(b)

    # Shuffle phần còn lại
    random.shuffle(remaining_a)
    random.shuffle(remaining_b)

    for a, b in zip(remaining_a, remaining_b):
        pairs.append((a, b))

    st.success("✨ Đây là kết quả:")
    st.write(pd.DataFrame(pairs, columns=["List A", "List B"]))
