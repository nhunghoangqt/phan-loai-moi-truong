# Ứng dụng xác định thủ tục môi trường cần thực hiện
# Cập nhật theo Luật BVMT 2020, NĐ 08/2022/NĐ-CP và NĐ 05/2025/NĐ-CP

import streamlit as st

st.set_page_config(page_title="Phân loại thủ tục môi trường", layout="wide")

st.title("🛠️ Công cụ hỗ trợ PHÂN LOẠI THỦ TỤC MÔI TRƯỜNG cho dự án đầu tư")
st.markdown("""Ứng dụng này giúp xác định **dự án thuộc nhóm I, II, III, IV** và các **thủ tục môi trường cần thực hiện** theo quy định mới nhất.

📘 **Căn cứ pháp lý:**
- Luật Bảo vệ môi trường 2020
- Nghị định 08/2022/NĐ-CP
- Nghị định 05/2025/NĐ-CP sửa đổi, bổ sung

**Các tiêu chí xác định gồm:**
- Loại hình và công suất hoạt động
- Có/không sử dụng đất nhạy cảm (di sản, đô thị, đất lúa...)
- Có phát sinh nước thải, khí thải, chất thải nguy hại?
""")

# ----------- INPUT SECTION ----------- #
st.header("📥 Thông tin dự án")

loai_hinh = st.selectbox("1️⃣ Loại hình sản xuất, kinh doanh, dịch vụ:", [
    "Công nghiệp (hóa chất, luyện kim, dệt nhuộm...)",
    "Chăn nuôi, giết mổ, chế biến thực phẩm",
    "Dịch vụ, du lịch, thương mại",
    "Hạ tầng kỹ thuật (giao thông, cấp thoát nước...)",
    "Dự án hỗn hợp khác"
])

cong_suat = st.selectbox("2️⃣ Quy mô công suất:", ["Lớn", "Trung bình", "Nhỏ"])

yeu_to_nhay_cam = st.multiselect("3️⃣ Dự án có nằm trong các khu vực nhạy cảm?", [
    "Khu dân cư đô thị đặc biệt/I/II/III/IV",
    "Nguồn nước cấp sinh hoạt",
    "Khu bảo tồn thiên nhiên, rừng đặc dụng, rừng phòng hộ",
    "Khu di sản, danh lam thắng cảnh, khu di tích",
    "Đất trồng lúa từ 2 vụ trở lên",
    "Yêu cầu di dân/tái định cư",
    "Không có yếu tố nhạy cảm"
])

phat_sinh = st.multiselect("4️⃣ Phát sinh chất thải nào?", [
    "Nước thải công nghiệp > 10 m³/ngày",
    "Khí thải > 1.000 m³/giờ",
    "Chất thải nguy hại > 100 kg/tháng",
    "Chỉ có nước thải sinh hoạt < 20 m³/ngày",
    "Không phát sinh chất thải"
])

# ----------- LOGIC PHÂN LOẠI ----------- #
def phan_loai():
    if cong_suat == "Lớn" or (cong_suat == "Trung bình" and any(yt != "Không có yếu tố nhạy cảm" for yt in yeu_to_nhay_cam)):
        nhom = "Nhóm I"
        thu_tuc = "Phải lập ĐTM + Giấy phép môi trường"
    elif cong_suat == "Trung bình" or (cong_suat == "Nhỏ" and any(yt != "Không có yếu tố nhạy cảm" for yt in yeu_to_nhay_cam)):
        nhom = "Nhóm II"
        thu_tuc = "Có thể cần ĐTM nếu sử dụng đất nhạy cảm hoặc phát sinh thải. Phải có GPMT nếu phát sinh thải."
    elif cong_suat == "Nhỏ" and all(yt == "Không có yếu tố nhạy cảm" for yt in yeu_to_nhay_cam):
        nhom = "Nhóm III"
        if any("nước thải" in p or "khí thải" in p or "nguy hại" in p for p in phat_sinh):
            thu_tuc = "Cần đăng ký môi trường hoặc xin GPMT nếu phát sinh thải vượt ngưỡng"
        else:
            thu_tuc = "Có thể miễn thủ tục, nhưng nên đăng ký môi trường"
    else:
        nhom = "Nhóm IV"
        thu_tuc = "Không cần thực hiện thủ tục môi trường"
    return nhom, thu_tuc

# ----------- KẾT QUẢ ----------- #
if st.button("🔎 PHÂN LOẠI THỦ TỤC MÔI TRƯỜNG"):
    nhom, thu_tuc = phan_loai()
    st.success(f"**✅ Dự án được phân loại: {nhom}**")
    st.info(f"📌 Thủ tục môi trường cần thực hiện: **{thu_tuc}**")
