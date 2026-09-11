import os
from micloud import MiCloud
from mcp.server.fastmcp import FastMCP

# Khởi tạo MCP Server
mcp = FastMCP("Xiaozhi Cloud Fan Controller")

# ĐIỀN TÀI KHOẢN XIAOMI HOME CỦA BẠN
XIAOMI_USER = "flykite00@gmail.com"
XIAOMI_PASS = "MAT_KHAU_XIAOMI_CUA_BAN"  # <--- Thay mật khẩu tài khoản Xiaomi vào đây

# Đăng nhập Xiaomi Cloud
mc = MiCloud(XIAOMI_USER, XIAOMI_PASS)
mc.login()

# Danh sách DID của 5 quạt từ bảng trích xuất trước đó
FANS_DID = {
    "le_tan": "2052457320",      # Lumias F08PRO 3Receptiondesk
    "phong_khach": "2052470868", # Lumias F08PRO
    "pkt": "2052476497",         # Lumias F08PRO pkt
    "phong_ngu": "2052486418",   # Lumias F08PRO 2
    "sofa": "2052458288"         # Lumias F08PRO sofa
}

def control_fan_cloud(did: str, power_on: bool):
    """Gửi lệnh Bật/Tắt quạt qua Xiaomi Cloud MIOT API"""
    params = [{
        "did": did,
        "siid": 2,  # SIID 2 thường là dịch vụ Fan trong chuẩn MIOT
        "piid": 1,  # PIID 1 thường là On/Off
        "value": power_on
    }]
    return mc.set_props(params)

@mcp.tool()
def turn_on_fan(location: str = "sofa") -> str:
    """Bật quạt ở vị trí: 'le_tan', 'phong_khach', 'pkt', 'phong_ngu', 'sofa'"""
    did = FANS_DID.get(location)
    if not did:
        return f"Không tìm thấy vị trí {location}"
    res = control_fan_cloud(did, True)
    return f"Đã gửi lệnh BẬT quạt {location}: {res}"

@mcp.tool()
def turn_off_fan(location: str = "sofa") -> str:
    """Tắt quạt ở vị trí: 'le_tan', 'phong_khach', 'pkt', 'phong_ngu', 'sofa'"""
    did = FANS_DID.get(location)
    if not did:
        return f"Không tìm thấy vị trí {location}"
    res = control_fan_cloud(did, False)
    return f"Đã gửi lệnh TẮT quạt {location}: {res}"

@mcp.tool()
def turn_off_all_fans() -> str:
    """Tắt tất cả 5 quạt"""
    for loc, did in FANS_DID.items():
        control_fan_cloud(did, False)
    return "Đã gửi lệnh tắt toàn bộ quạt."

if __name__ == "__main__":
    # Chạy MCP Server cổng 8080 dạng SSE cho Render
    port = int(os.environ.get("PORT", 8080))
    mcp.run(transport="sse", host="0.0.0.0", port=port)