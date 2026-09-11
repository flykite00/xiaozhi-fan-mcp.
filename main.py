import os
from micloud import MiCloud
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Xiaozhi Cloud Fan")

# BẠN BẮT BUỘC PHẢI SỬA DÒNG NÀY THÀNH MẬT KHẨU XIAOMI THẬT
XIAOMI_USER = "flykite00@gmail.com"
XIAOMI_PASS = "ĐIỀN_MẬT_KHẨU_XIAOMI_CỦA_BẠN_VÀO_ĐÂY" 

# Mã định danh (DID) của 5 quạt trên Xiaomi Cloud
FANS_DID = {
    "le_tan": "2052457320",
    "phong_khach": "2052470868",
    "pkt": "2052476497",
    "phong_ngu": "2052486418",
    "sofa": "2052458288"
}

def control_fan_cloud(location: str, power_on: bool) -> str:
    did = FANS_DID.get(location)
    if not did:
        return f"Lỗi: Không có quạt nào ở {location}"
    try:
        # Đăng nhập vào Mi Home
        mc = MiCloud(XIAOMI_USER, XIAOMI_PASS)
        mc.login()
        # Gửi lệnh On/Off
        res = mc.set_props([{"did": did, "siid": 2, "piid": 1, "value": power_on}])
        trang_thai = "BẬT" if power_on else "TẮT"
        return f"Thành công: Đã {trang_thai} quạt {location}. (Mã: {res})"
    except Exception as e:
        return f"Lỗi Cloud: Có thể sai mật khẩu hoặc bị chặn ({str(e)})"

@mcp.tool()
def turn_on_fan(location: str = "sofa") -> str:
    """Bật quạt. Vị trí: 'le_tan', 'phong_khach', 'pkt', 'phong_ngu', 'sofa'"""
    return control_fan_cloud(location, True)

@mcp.tool()
def turn_off_fan(location: str = "sofa") -> str:
    """Tắt quạt. Vị trí: 'le_tan', 'phong_khach', 'pkt', 'phong_ngu', 'sofa'"""
    return control_fan_cloud(location, False)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    mcp.run(transport="sse", host="0.0.0.0", port=port)
