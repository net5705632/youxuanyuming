import requests
import re
import chardet

urls = [
    "https://ip.164746.xyz/ipTop10.html",
    "https://zip.baipiao.eu.org/45102-1-443.txt",
    "https://zip.baipiao.eu.org/31898-1-443.txt",
    "https://cf.090227.xyz",
    "https://www.wetest.vip/page/cloudfront/address_v4.html",
    "https://raw.githubusercontent.com/ymyuuu/IPDB/main/BestProxy/proxy.txt"
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

ip_set = set()

# 调整正则，允许IP后跟端口或特殊字符
ip_pattern = re.compile(r'\b(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b')

for url in urls:
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        # 自动检测编码
        if response.encoding == 'ISO-8859-1':
            detected_enc = chardet.detect(response.content)['encoding']
            text = response.content.decode(detected_enc, errors='ignore')
        else:
            text = response.text

        found_ips = ip_pattern.findall(text)
        
        if found_ips:
            ip_set.update(found_ips)
            print(f"从 {url} 找到 {len(found_ips)} 个IP")
        else:
            print(f"警告：{url} 未找到IP地址（样本）: {text[:100]}")  # 打印前100字符辅助排查

    except requests.exceptions.HTTPError as e:
        print(f"HTTP错误 {url}: 状态码 {e.response.status_code}")
    except Exception as e:
        print(f"请求 {url} 时出错：{str(e)}")

if ip_set:
    with open("ip.txt", "w") as f:
        f.write("\n".join(sorted(ip_set)))
    print(f"成功保存 {len(ip_set)} 个唯一IP地址到 ip.txt")
else:
    print("未找到任何IP地址")
