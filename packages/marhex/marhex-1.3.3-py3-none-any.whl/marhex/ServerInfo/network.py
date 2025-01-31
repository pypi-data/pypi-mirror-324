import requests
import asyncio


async def display_info():
    all_data = await get_info()
    ip = all_data['ip']
    country = all_data['location']['country']
    city = all_data['location']['city']
    is_proxy = all_data['is_proxy']
    is_vpn = all_data['is_vpn']
    local_time = all_data['location']['local_time']
    local_time_unix = all_data['location']['local_time_unix']

    print(f"""
        ==================================================
        IP                   =>      {ip}
        Country              =>      {country}
        City                 =>      {city}
        ==================================================
        is_Proxy             =>      {is_proxy}
        is_VPN               =>      {is_vpn}
        ==================================================
        Local_Time           =>      {local_time}
        Local_Time_Unix      =>      {local_time_unix}
        ==================================================
    """)


async def get_info():
    all_data = requests.get("https://api.ipapi.is").json()
    return all_data


def display_short_info():
    asyncio.run(display_info())
