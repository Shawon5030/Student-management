import ipinfo

access_token = "5cf61de6dfa3ed"  # token না থাকলেও basic lookup চেষ্টা করতে পারেন

handler = ipinfo.getHandler(access_token)

ip = "8.8.8.8"

details = handler.getDetails(ip)

print("IP:", details.ip)
print("Country:", details.country)
print("Region:", details.region)
print("City:", details.city)
print("Postal Code:", details.postal)
print("Latitude:", details.latitude)
print("Longitude:", details.longitude)
print("Timezone:", details.timezone)
print("Organization:", details.org)