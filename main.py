import os
import asyncio
from micloud import MiCloud
from mcp.server.fastmcp import FastMCP

# Tạo MCP Server
mcp = FastMCP("Xiaozhi Cloud Fan Controller")

# ĐIỀN CHÍNH XÁC TÀI KHOẢN VÀ MẬT KHẨU XIAOMI CỦA BẠN
XIAOMI_USER = "flykite00@gmail.com"
XIAOMI_PASS = "Mật_Khẩu_Thật_Của_Bạn"  # <--- Thay mật khẩu tài khoản Xiaomi Home vào đây!

FANS_DID = {
    "le_tan": "2052457320",
    "phong_khach": "2052470868",
    "pkt": "2052476497",
    "phong_ngu": "2052486418",
    "sofa": "2052458288"
}

def get_mc_client():
    mc = MiCloud(XIAOMI_USER, XIAOMI_PASS)
    mc.login()
    return mc

@mcp.tool()
def turn_on_fan(location: str = "sofa") -> str:
    """Bật quạt ở vị trí: 'le_tan', 'phong_khach', 'pkt', 'phong_ngu', 'sofa'"""
    did = FANS_DID.get(location)
    if not did:
        return f"Không tìm thấy vị trí {location}"
    try:
        mc = get_mc_client()
        res = mc.set_props([{"did": did, "siid": 2, "piid": 1, "value": True}])
        return f"Đã BẬT quạt {location}: {res}"
    except Exception as e:
        return f"Lỗi BẬT quạt {location}: {str(e)}"

@mcp.tool()
def turn_off_fan(location: str = "sofa") -> str:
    """Tắt quạt ở vị trí: 'le_tan', 'phong_khach', 'pkt', 'phong_ngu', 'sofa'"""
    did = FANS_DID.get(location)
    if not did:
        return f"Không tìm thấy vị trí {location}"
    try:
        mc = get_mc_client()
        res = mc.set_props([{"did": did, "siid": 2, "piid": 1, "value": False}])
        return f"Đã TẮT quạt {location}: {res}"
    except Exception as e:
        return f"Lỗi TẮT quạt {location}: {str(e)}"

@mcp.tool()
def turn_off_all_fans() -> str:
    """Tắt tất cả 5 quạt"""
    try:
        mc = get_mc_client()
        for loc, did in FANS_DID.items():
            mc.set_props([{"did": did, "siid": 2, "piid": 1, "value": False}])
        return "Đã gửi lệnh tắt toàn bộ quạt."
    except Exception as e:
        return f"Lỗi tắt tất cả: {str(e)}"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    mcp.run(transport="sse", host="0.0.0.0", port=port)
