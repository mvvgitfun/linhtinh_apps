import streamlit as st
import pandas as pd
import time
import gspread
from google.oauth2.service_account import Credentials

# --- CẤU HÌNH TRANG WEB ---
st.set_page_config(
    page_title="Hế lô bạn ei, toai có lời mời cho bạn nè!",
    page_icon="💌",
    layout="centered"
)

# --- KHỞI TẠO SESSION STATE ---
if 'guest_name' not in st.session_state:
    st.session_state.guest_name = ""

# === KẾT NỐI TỚI GOOGLE SHEETS BẰNG GSPREAD (CÁCH BẤT BẠI) ===
@st.cache_resource
def get_gsheets_client():
    try:
        # Lấy toàn bộ credentials từ secrets
        creds_dict = st.secrets["connections"]["gsheets"]["credentials"]
        
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
        client = gspread.authorize(creds)
        return client
    except Exception as e:
        st.error("Lỗi kết nối tới Google Sheets. Vui lòng kiểm tra lại secrets.")
        st.exception(e)
        return None

def get_worksheet(client):
    try:
        spreadsheet_id = st.secrets["connections"]["gsheets"]["spreadsheetId"]
        worksheet_name = st.secrets["connections"]["gsheets"]["worksheet"]
        spreadsheet = client.open_by_key(spreadsheet_id)
        worksheet = spreadsheet.worksheet(worksheet_name)
        return worksheet
    except Exception as e:
        st.error(f"Không tìm thấy Spreadsheet hoặc Worksheet. Lỗi: {e}")
        return None
# =================================================================

# --- TRANG CHÀO MỪNG ---
def show_welcome_page():
    st.title("💌 Bạn ei, bạn có một thư mời đặc biệt!")
    st.write("Vui lòng cho toai biết tên của bạn để mở thiệp mời nhó hẹ hẹ:")
    name_input = st.text_input("Tên bạn là gì nào?", placeholder="Ví dụ: Ní Đẹp Trai", label_visibility="collapsed")
    if st.button("Xem Thiệp Mời 📬", use_container_width=True, type="primary"):
        if name_input:
            st.session_state.guest_name = name_input
            st.rerun()
        else:
            st.warning("Bạn ei, nhập tên vào đi hay muốn bị ăn đòn nè... :(")

# --- TRANG THIỆP MỜI ---
def show_invite_page():
    # ... (Toàn bộ phần giao diện st.snow, st.title, markdown, thông tin... giữ nguyên) ...

    # --- PHẦN TƯƠNG TÁC LƯU VÀO GOOGLE SHEETS ---
    st.write("---")
    st.subheader("Bạn sẽ tham gia chứ hẻ? 😉")
    
    _, col_button, _ = st.columns([1, 2, 1])
    with col_button:
        if st.button("CHẮC CHẮN RỒI! XÁC NHẬN NGAY! 🥳", use_container_width=True, type="primary"):
            with st.spinner("Đang khắc tên bạn lên Google Sheets..."):
                try:
                    client = get_gsheets_client()
                    if client:
                        worksheet = get_worksheet(client)
                        if worksheet:
                            # Đọc dữ liệu cũ
                            records = worksheet.get_all_records()
                            existing_data = pd.DataFrame.from_records(records)

                            if not existing_data.empty and st.session_state.guest_name in existing_data["Tên Khách Mời"].values:
                                st.warning("Oops! Tên của bạn đã có trong danh sách rồi. Cảm ơn đã xác nhận lại nhé!")
                            else:
                                # Thêm dòng mới
                                new_row = [st.session_state.guest_name, pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')]
                                worksheet.append_row(new_row)
                                
                                st.balloons()
                                st.success("Tuyệt vời! Tên của bạn đã được ghi vào danh sách. Hẹn gặp lại nhé!", icon="🎉")
                except Exception as e:
                    st.error("Ối! Có lỗi xảy ra khi ghi vào Google Sheets.")
                    st.exception(e)
    
    # --- Hiển thị danh sách khách mời ---
    st.write("---")
    with st.expander("Xem ai đã xác nhận tham gia..."):
        try:
            client = get_gsheets_client()
            if client:
                worksheet = get_worksheet(client)
                if worksheet:
                    records = worksheet.get_all_records()
                    guest_list = pd.DataFrame.from_records(records)
                    if not guest_list.empty:
                        st.dataframe(guest_list[["Tên Khách Mời"]], use_container_width=True)
                        st.info(f"Tổng cộng đã có **{len(guest_list)}** người xác nhận tham gia!")
                    else:
                        st.write("Chưa có ai xác nhận cả, buồn hiu...")
        except Exception as e:
            st.warning("Không thể tải danh sách khách mời. Lỗi!")
            st.exception(e)
            
# --- LOGIC CHÍNH ---
if st.session_state.guest_name == "":
    show_welcome_page()
else:
    show_invite_page()
