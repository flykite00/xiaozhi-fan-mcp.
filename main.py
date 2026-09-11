import os
from miio.fan import Fan
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Xiaozhi Cloud Fan Controller")

# Sử dụng Token và IP/Cloud ID của 5 quạt đã trích xuất thành công
FANS = {
    "le_tan": {"ip": "192.168.31.246", "token": "4b20b41c0e4a4474d9a491d2fbb6aff2"},
    "phong_khach": {"ip": "192.168.31.223", "token": "b02017c1383c88aedca7f6321e0fe885"},
    "pkt": {"ip": "192.168.31.148", "token": "3f7d991c5601c8182f58c1703fb2a5c1"},
    "phong_ngu": {"ip": "192.168.31.103", "token": "4d59a7af471fb2517a64955689a75de9"},
    "sofa": {"ip": "192.168.31.86", "token": "f92edaf77132e0ddf5b4b4a481491049"}
}

@mcp.tool()
def turn_on_fan(location: str = "sofa") -> str:
    """Bật quạt ở vị trí: 'le_tan', 'phong_khach', 'pkt', 'phong_ngu', 'sofa'"""
    fan_info = FANS.get(location)
    if not fan_info:
        return f"Không tìm thấy vị trí {location}"
    try:
        fan = Fan(ip=fan_info["ip"], token=fan_info["token"])
        fan.on()
        return f"Đã bật quạt {location} thành công."
    except Exception as e:
        return f"Lỗi khi bật quạt {location}: {str(e)}"

@mcp.tool()
def turn_off_fan(location: str = "sofa") -> str:
    """Tắt quạt ở vị trí: 'le_tan', 'phong_khach', 'pkt', 'phong_ngu', 'sofa'"""
    fan_info = FANS.get(location)
    if not fan_info:
        return f"Không tìm thấy vị trí {location}"
    try:
        fan = Fan(ip=fan_info["ip"], token=fan_info["token"])
        fan.off()
        return f"Đã tắt quạt {location} thành công."
    except Exception as e:
        return f"Lỗi khi tắt quạt {location}: {str(e)}"

@mcp.tool()
def turn_off_all_fans() -> str:
    """Tắt tất cả 5 quạt"""
    results = []
    for loc, info in FANS.items():
        try:
            f = Fan(ip=info["ip"], token=info["token"])
            f.off()
            results.append(f"{loc}: OK")
        except Exception as e:
            results.append(f"{loc}: Lỗi ({str(e)})")
    return "; ".join(results)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    mcp.run(transport="sse", host="0.0.0.0", port=port)
