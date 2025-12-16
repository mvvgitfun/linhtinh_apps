import streamlit as st
import pandas as pd
import time
from streamlit_gsheets import GSheetsConnection

# --- CẤU HÌNH TRANG WEB ---
st.set_page_config(
    page_title="Hế lô bạn ei, toai có lời mời cho bạn nè!",
    page_icon="💌",
    layout="centered"
)

# --- KHỞI TẠO SESSION STATE ĐỂ LƯU TÊN KHÁCH MỜI ---
if 'guest_name' not in st.session_state:
    st.session_state.guest_name = ""

# ==============================================================================
# HÀM HIỂN THỊ TRANG CHÀO MỪNG (CỔNG SOÁT VÉ)
# ==============================================================================
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

# ==============================================================================
# HÀM HIỂN THỊ NỘI DUNG THIỆP MỜI
# ==============================================================================
def show_invite_page():
    # --- HIỆU ỨNG VÀ TIÊU ĐỀ ---
    st.snow()
    st.title(f"🎅 Chào {st.session_state.guest_name}, đây là một tấm vé tới buổi tiệc dành cho hội chơi game zà cầu lông!")
    st.header("✨ **Christmas Party - Phiên bản 'Nhà có gì chơi đó'** ✨", divider='rainbow')
    st.markdown("""
    Nhân dịp không có gì đặc biệt nhưng vẫn muốn tụ tập, chúng toai trân trọng (và hơi ép buộc một chút) mời bạn đến tham dự một buổi tiệc Giáng Sinh "cây nhà lá vườn".
    Hãy chuẩn bị một tâm hồn đẹp, một chiếc bụng đói và một tinh thần sẵn sàng "quẩy tới bến"!
    """)
    # --- THÔNG TIN CHI TIẾT ---
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🗓️ Thời gian có thể có mặt:")
        st.markdown("- **17:00 (5 giờ chiều)**, **Thứ 7**\n- Ngày **27 tháng 12**")
    with col2:
        st.subheader("📍 Địa điểm hạ cánh:")
        st.markdown("- **Chung cư Gold View**, Block A3\n- 346 Bến Vân Đồn, P.1, Q.4")
    # --- HOẠT ĐỘNG ---
    st.subheader("🎁 Hoạt động không thể bỏ lỡ:")
    st.info("Chuẩn bị một món quà **nhỏ xinh (dưới 200k)** để tham gia màn 'SWAP QUÀ' đầy kịch tính và bất ngờ!", icon="💝")
    st.success("Tiệc sẽ bao gồm đồ ăn, thức uống no nê và một dàn **BOARD GAME** huyền thoại để thử thách sức mạnh tình bạn (hay là hủy hoại tình bạn)!", icon="🎲")
    # --- PHẦN TƯƠNG TÁC LƯU VÀO GOOGLE SHEETS ---
    st.write("---")
    st.subheader("Bạn sẽ tham gia chứ hẻ? 😉")
    
    # === KHỞI TẠO KẾT NỐI THEO CÁCH "THỦ CÔNG" AN TOÀN ===
    conn = st.connection("gsheets", type=GSheetsConnection)

    _, col_button, _ = st.columns([1, 2, 1])
    with col_button:
        if st.button("CHẮC CHẮN RỒI! XÁC NHẬN NGAY! 🥳", use_container_width=True, type="primary"):
            with st.spinner("Đang khắc tên bạn lên Google Sheets..."):
                try:
                    # Đọc dữ liệu cũ
                    # "Mớm" worksheet và spreadsheetId một cách tường minh
                    existing_data = conn.read(
                        worksheet=st.secrets["connections"]["gsheets"]["worksheet"],
                        spreadsheet=st.secrets["connections"]["gsheets"]["spreadsheetId"],
                        usecols=[0, 1],
                        ttl=5
                    )
                    existing_data = existing_data.dropna(how="all")

                    if not existing_data.empty and st.session_state.guest_name in existing_data["Tên Khách Mời"].values:
                        st.warning("Oops! Tên của bạn đã có trong danh sách rồi. Cảm ơn đã xác nhận lại nhé!")
                        time.sleep(2)
                    else:
                        new_guest = pd.DataFrame([
                            {"Tên Khách Mời": st.session_state.guest_name, "Thời Gian Xác Nhận": pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}
                        ])
                        updated_df = pd.concat([existing_data, new_guest], ignore_index=True)
                        # Cập nhật cũng phải "mớm" spreadsheetId
                        conn.update(
                            spreadsheet=st.secrets["connections"]["gsheets"]["spreadsheetId"],
                            data=updated_df
                        )
                        st.balloons()
                        st.success("Tuyệt vời! Tên của bạn đã được ghi vào danh sách. Hẹn gặp lại nhé!", icon="🎉")
                        st.image("https://media.tenor.com/_np6fV12HqsAAAAM/cute-cat-jumping.gif")
                except Exception as e:
                    st.error("Ối! Có lỗi xảy ra khi kết nối tới Google Sheets. Chắc là do con chế AI nào đó tư vấn sai. Báo cho chủ tiệc biết nhé!")
                    st.exception(e)
    
    # --- Hiển thị danh sách khách mời ---
    st.write("---")
    with st.expander("Xem ai đã xác nhận tham gia..."):
        try:
            # Đọc lại cũng phải "mớm" spreadsheetId
            guest_list = conn.read(
                spreadsheet=st.secrets["connections"]["gsheets"]["spreadsheetId"],
                usecols=[0, 1],
                ttl=5
            ).dropna(how="all")
            if not guest_list.empty:
                st.dataframe(guest_list, use_container_width=True)
                st.info(f"Tổng cộng đã có **{len(guest_list)}** người xác nhận tham gia!")
            else:
                st.write("Chưa có ai xác nhận cả, buồn hiu...")
        except Exception as e:
            st.warning("Không thể tải danh sách khách mời. Có thể có lỗi kết nối.")
            
# ==============================================================================
# LOGIC CHÍNH: KIỂM TRA XEM ĐÃ CÓ TÊN CHƯA ĐỂ HIỂN THỊ ĐÚNG TRANG
# ==============================================================================
if st.session_state.guest_name == "":
    show_welcome_page()
else:
    show_invite_page()
