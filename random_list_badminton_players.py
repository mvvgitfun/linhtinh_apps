import streamlit as st
import pandas as pd
import random
import time

st.set_page_config(page_title="Random Pair Tool", layout="centered")

st.title("🎲 Random Pair Generator")

# Upload file CSV
file_a = st.file_uploader("Upload list A (CSV, 1 cột)", type=["csv"])
file_b = st.file_uploader("Upload list B (CSV, 1 cột)", type=["csv"])

# Fixed pairs setup (demo)
fixed_pairs = {
    "A1": "B3",   # A1 luôn đi với B3
    "A5": "B4"
}

if file_a and file_b:
    list_a = pd.read_csv(file_a, header=None)[0].tolist()
    list_b = pd.read_csv(file_b, header=None)[0].tolist()

    if st.button("🔀 Shuffle & Pair"):
        # Shuffle effect
        with st.spinner("Shuffling... 🎰"):
            time.sleep(2)

        # Apply fixed pairs
        remaining_a = list_a[:]
        remaining_b = list_b[:]
        pairs = []

        for a, b in fixed_pairs.items():
            if a in remaining_a and b in remaining_b:
                pairs.append((a, b))
                remaining_a.remove(a)
                remaining_b.remove(b)

        random.shuffle(remaining_a)
        random.shuffle(remaining_b)

        for a, b in zip(remaining_a, remaining_b):
            pairs.append((a, b))

        st.success("✨ Done! Here are your pairs:")
        st.write(pd.DataFrame(pairs, columns=["List A", "List B"]))
