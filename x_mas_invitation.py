import streamlit as st
import pandas as pd
import time
from streamlit_gsheets import GSheetsConnection

# --- Cấu hình trang web ---
st.set_page_config(...)

# --- Khởi tạo session state ---
if 'guest_name' not in st.session_state:
    st.session_state.guest_name = ""

def show_welcome_page():
    # ... code không đổi ...

def show_invite_page():
    # ... code không đổi ...

    # --- PHẦN TƯƠNG TÁC LƯU VÀO GOOGLE SHEETS ---
    st.write("---")
    st.subheader("Bạn sẽ tham gia chứ hẻ? 😉")
    
    # === ĐIỂM THAY THẾ QUAN TRỌNG NHẤT ===
     spreadsheet_id = st.secrets["connections"]["gsheets"]["spreadsheetId"]
    worksheet_name = st.secrets["connections"]["gsheets"]["worksheet"]
    conn = st.connection(
        "gsheets",
        type=GSheetsConnection,
        spreadsheet=spreadsheet_id,
        worksheet=worksheet_name,
    )
    #======================================

    _, col_button, _ = st.columns([1, 2, 1])
    with col_button:
        if st.button("CHẮC CHẮN RỒI! XÁC NHẬN NGAY! 🥳", use_container_width=True, type="primary"):
            with st.spinner("Đang khắc tên bạn lên Google Sheets..."):
                try:
                    existing_data = conn.read(usecols=[0, 1], ttl=5) # Không cần truyền worksheet nữa
                    # ... code còn lại không đổi ...
                    
                    # ... khi update cũng không cần truyền worksheet
                    conn.update(data=updated_df) 
                    
                except Exception as e:
                    # ...
    
    # --- Hiển thị danh sách khách mời ---
    st.write("---")
    with st.expander("Xem ai đã xác nhận tham gia..."):
        try:
            # Ở đây cũng không cần truyền worksheet
            guest_list = conn.read(usecols=[0], ttl=5).dropna(how="all")
            # ... code còn lại không đổi ...

# --- Logic chính ---
if st.session_state.guest_name == "":
    show_welcome_page()
else:
    show_invite_page()
