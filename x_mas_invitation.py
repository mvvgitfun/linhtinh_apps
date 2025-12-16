import streamlit as st

st.title("🕵️ TRANG DEBUG BÍ MẬT 🕵️")

st.write("Dưới đây là toàn bộ những gì mà `st.secrets` đang đọc được:")

# In ra toàn bộ nội dung của st.secrets
st.write(st.secrets.to_dict())

st.write("---")
st.subheader("Check từng thành phần:")

# Kiểm tra xem có mục connections.gsheets không
if "connections" in st.secrets and "gsheets" in st.secrets["connections"]:
    st.success("✅ Đã tìm thấy mục [connections.gsheets]!")
    
    gsheets_config = st.secrets["connections"]["gsheets"]
    
    # Kiểm tra spreadsheetId
    if "spreadsheetId" in gsheets_config:
        st.success(f"✅ Đã tìm thấy `spreadsheetId`: {gsheets_config['spreadsheetId']}")
    else:
        st.error("❌ KHÔNG TÌM THẤY `spreadsheetId`!")

    # Kiểm tra worksheet
    if "worksheet" in gsheets_config:
        st.success(f"✅ Đã tìm thấy `worksheet`: {gsheets_config['worksheet']}")
    else:
        st.error("❌ KHÔNG TÌM THẤY `worksheet`!")

    # Kiểm tra credentials
    if "credentials" in gsheets_config and "private_key" in gsheets_config["credentials"]:
        st.success("✅ Đã tìm thấy mục `credentials` và `private_key`!")
    else:
        st.error("❌ KHÔNG TÌM THẤY `credentials` hoặc `private_key` bên trong!")

else:
    st.error("❌ LỖI NGHIÊM TRỌNG: KHÔNG TÌM THẤY MỤC `[connections.gsheets]` TRONG SECRETS!")
