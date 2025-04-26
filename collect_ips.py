import requests
import re
import chardet

urls = [
    "https://ip.164746.xyz/ipTop10.html",
    "https://zip.baipiao.eu.org/45102-1-443.txt",  # 问题URL
    "https://zip.baipiao.eu.org/31898-1-443.txt",  # 问题URL
    "https://cf.090227.xyz",
    "https://www.wetest.vip/page/cloudfront/address_v4.html",
    "https://raw.githubusercontent.com/ymyuuu/IPDB/main/BestProxy/proxy.txt"
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Encoding': 'identity'  # 明确要求不压缩
}

ip_set = set()

# 增强版正则：捕获带端口的IP（如 1.2.3.4:443）
ip_pattern = re.compile(r'\b((?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?))(?:[:#]\d+)?\b')

for url in urls:
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()

        # 强制处理编码（针对二进制内容）
        if response.encoding == 'ISO-8859-1':
            enc = chardet.detect(response.content)['encoding'] or 'utf-8'
            text = response.content.decode(enc, errors='replace')
        else:
            text = response.text

        # 专用处理：如果URL是问题TXT文件，按行分割后提取
        if "zip.baipiao.eu.org" in url:
            lines = text.splitlines()
            for line in lines:
                line = line.strip()
                if line and ':' in line:  # 示例格式 1.2.3.4:443
                    ip = line.split(':', 1)[0]
                    if ip_pattern.match(ip):
                        ip_set.add(ip)
        else:  # 其他URL用正则处理
            found_ips = ip_pattern.findall(text)
            if found_ips:
                ip_set.update(found_ips)

        print(f"处理完成：{url}")

    except requests.exceptions.HTTPError as e:
        print(f"HTTP错误 {url}: 状态码 {e.response.status_code}")
    except Exception as e:
        print(f"请求 {url} 时出错：{str(e)}")

# 保存结果（同上）
