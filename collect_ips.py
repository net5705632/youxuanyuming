import requests
import re

# 定义要采集的URL列表
urls = [
    "https://ip.164746.xyz/ipTop10.html",
    "https://zip.baipiao.eu.org/45102-1-443.txt",
    "https://zip.baipiao.eu.org/31898-1-443.txt",
    "https://cf.090227.xyz",
    "https://www.wetest.vip/page/cloudfront/address_v4.html",
    "https://raw.githubusercontent.com/ymyuuu/IPDB/main/BestProxy/proxy.txt"
]

# 设置请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

# 用于存储IP地址的集合（自动去重）
ip_set = set()

# 匹配IPv4地址的正则表达式
ip_pattern = re.compile(r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b')

for url in urls:
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # 检查请求是否成功
        
        # 查找所有匹配的IP地址
        found_ips = ip_pattern.findall(response.text)
        
        if found_ips:
            ip_set.update(found_ips)
            print(f"从 {url} 找到 {len(found_ips)} 个IP")
        else:
            print(f"警告：{url} 未找到IP地址")
            
    except Exception as e:
        print(f"请求 {url} 时出错：{str(e)}")
        continue

# 将结果写入文件
if ip_set:
    with open("ip.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(sorted(ip_set)))
    print(f"成功保存 {len(ip_set)} 个唯一IP地址到 ip.txt")
else:
    print("未找到任何IP地址")
