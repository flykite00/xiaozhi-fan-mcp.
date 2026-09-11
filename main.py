import os
from micloud import MiCloud
from mcp.server.fastmcp import FastMCP

# Tạo MCP Server
mcp = FastMCP("Xiaozhi Cloud Fan")

# BẠN ĐIỀN ĐÚNG TÀI KHOẢN VÀ MẬT KHẨU XIAOMI VÀO ĐÂY
XIAOMI_USER = "flykite00@gmail.com"
XIAOMI_PASS = "MẬT_KHẨU_XIAOMI_CỦA_BẠN"  # <--- Thay mật khẩu thật tại đây

FANS_DID = {
    "le_tan": "2052457320",
    "phong_khach": "2052470868",
    "pkt": "2052476497",
    "phong_ngu": "2052486418",
    "sofa": "2052458288"
}

def send_fan_command(did: str, power_on: bool):
    """Đăng nhập và gửi lệnh tới Xiaomi Cloud khi có yêu cầu từ Xiaozhi"""
    try:
        mc = MiCloud(XIAOMI_USER, XIAOMI_PASS)
        mc.login()
        res = mc.set_props([{"did": did, "siid": 2, "piid": 1, "value": power_on}])
        return True, res
    except Exception as e:
        return False, str(e)

@mcp.tool()
def turn_on_fan(location: str = "sofa") -> str:
    """Bật quạt ở vị trí: 'le_tan', 'phong_khach', 'pkt', 'phong_ngu', 'sofa'"""
    did = FANS_DID.get(location)
    if not did:
        return f"Không tìm thấy vị trí {location}"
    
    success, res = send_fan_command(did, True)
    if success:
        return f"Đã BẬT quạt {location} thành công: {res}"
    return f"Lỗi BẬT quạt {location}: {res}"

@mcp.tool()
def turn_off_fan(location: str = "sofa") -> str:
    """Tắt quạt ở vị trí: 'le_tan', 'phong_khach', 'pkt', 'phong_ngu', 'sofa'"""
    did = FANS_DID.get(location)
    if not did:
        return f"Không tìm thấy vị trí {location}"
    
    success, res = send_fan_command(did, False)
    if success:
        return f"Đã TẮT quạt {location} thành công: {res}"
    return f"Lỗi TẮT quạt {location}: {res}"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    mcp.run(transport="sse", host="0.0.0.0", port=port)
