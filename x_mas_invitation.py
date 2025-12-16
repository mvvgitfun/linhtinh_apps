import streamlit as st
import time

# --- CẤU HÌNH TRANG WEB ---
st.set_page_config(
    page_title="Thiệp Mời Giáng Sinh",
    page_icon="🎄",
    layout="centered"
)

# --- THÊM HIỆU ỨNG TUYẾT RƠI (phép thuật của Streamlit) ---
st.snow()

# --- NỘI DUNG CHÍNH CỦA THIỆP MỜI ---

# 1. Tiêu đề chính
st.title("🎅 BẠN ĐÃ CÓ MỘT TẤM VÉ ĐẾN XỨ SỞ DIỆU KỲ!")
st.header("✨ **Christmas Party - Phiên bản 'Nhà có gì chơi đó'** ✨", divider='rainbow')

st.write("") # Thêm một dòng trống

# 2. Lời mời chính
st.markdown("""
Chào mừng bạn iu,

Nhân dịp không có gì đặc biệt nhưng vẫn muốn tụ tập, team chúng mình trân trọng (và hơi ép buộc một chút) mời bạn đến tham dự một buổi tiệc Giáng Sinh "cây nhà lá vườn".

Hãy chuẩn bị một tâm hồn đẹp, một chiếc bụng đói và một tinh thần sẵn sàng "quẩy tới bến"!
""")

st.write("") # Thêm một dòng trống

# 3. Thông tin chi tiết - Dùng các cột cho đẹp
col1, col2 = st.columns(2)

with col1:
    st.subheader("🗓️ Thời gian diễn ra:")
    st.markdown("- **17:00 (5 giờ chiều)**, **Thứ 7**")
    st.markdown("- Ngày **27 tháng 12** (Noel muộn một chút cho nó lạ)")

with col2:
    st.subheader("📍 Địa điểm hạ cánh:")
    st.markdown("- **Chung cư Gold View**, Block A3")
    st.markdown("- 346 Bến Vân Đồn, P.1, Q.4")
    # st.link_button("Xem bản đồ Google Maps", "https://maps.app.goo.gl/your-google-maps-link") # Ní có thể thêm link Google Maps ở đây

st.write("") # Thêm một dòng trống

# 4. Các hoạt động "vui là chính"
st.subheader("🎁 Hoạt động không thể bỏ lỡ:")
st.info("Chuẩn bị một món quà **nhỏ xinh (dưới 200k)** để tham gia màn 'SWAP QUÀ' đầy kịch tính và bất ngờ. Món quà càng 'bá đạo', càng dễ đi vào lòng đất... à nhầm, lòng người!", icon="💝")

st.success("Tiệc sẽ bao gồm đồ ăn, thức uống no nê và một dàn **BOARD GAME** huyền thoại để thử thách tình bạn. Kẻ thua sẽ phải rửa bát!", icon="🎲")


# 5. Nút bấm "thần thánh"
st.write("") # Thêm một dòng trống
st.write("") # Thêm một dòng trống

# Căn giữa nút bấm
_, col_button, _ = st.columns([1,2,1])
with col_button:
    if st.button("**XÁC NHẬN THAM GIA NGAY!** 🥳", use_container_width=True, type="primary"):
        # Hiệu ứng chờ đợi hồi hộp
        progress_text = "Đang gửi tín hiệu của bạn lên vũ trụ... Vui lòng chờ!"
        my_bar = st.progress(0, text=progress_text)
        for percent_complete in range(100):
            time.sleep(0.02)
            my_bar.progress(percent_complete + 1, text=progress_text)
        time.sleep(0.5)
        my_bar.empty()

        # Bắn pháo hoa và hiển thị lời cảm ơn
        st.balloons()
        st.success("Tuyệt vời! Vũ trụ đã nhận được tín hiệu! Hẹn gặp bạn tại buổi tiệc nhé. Đừng quên mang theo quà và một chiếc bụng thật rỗng!", icon="🎉")
        st.image("https://media.tenor.com/_np6fV12HqsAAAAM/cute-cat-jumping.gif", caption="Yeahh!")

# --- Chân trang ---
st.write("---")
st.markdown("<p style='text-align: center; color: gray;'>Một sản phẩm được tạo ra bằng tình yêu và một chút Python ❤️</p>", unsafe_allow_html=True)
