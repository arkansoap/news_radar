import urllib.request
import ssl
from environs import Env

env = Env()
env.read_env()

proxy = env.str("PROXY_URL")
url = "https://geo.brdtest.com/welcome.txt?product=dc&method=native"

opener = urllib.request.build_opener(
    urllib.request.ProxyHandler({"https": proxy, "http": proxy})
)

try:
    print(opener.open(url).read().decode())
except Exception as e:
    print(f"Error: {e}")
