import requests
from bs4 import BeautifulSoup
import re
import os

# 配置请求头模拟浏览器
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9'
}

# 目标网址列表
urls = [
    'https://ip.164746.xyz/ipTop10.html',
    'https://cf.090227.xyz',
    'https://www.wetest.vip/page/cloudfront/address_v4.html',
    'https://raw.githubusercontent.com/ymyuuu/IPDB/main/proxy.txt'
]

# 优化的IP地址正则表达式（排除误匹配）
ip_pattern = r'\b(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b'

def fetch_ips():
    # 清理旧文件
    if os.path.exists('ip.txt'):
        os.remove('ip.txt')
    
    with open('ip.txt', 'a') as f:
        for url in urls:
            try:
                # 发送带超时设置的请求
                response = requests.get(url, headers=headers, timeout=15)
                response.raise_for_status()
                
                # 内容类型判断
                content_type = response.headers.get('Content-Type', '')
                
                if 'text/plain' in content_type or url.endswith('.txt'):
                    # 处理纯文本内容
                    ips = re.findall(ip_pattern, response.text)
                    for ip in set(ips):  # 去重
                        f.write(f"{ip}\n")
                    print(f"[{url}] 文本解析完成")
                    continue

                # HTML内容处理
                soup = BeautifulSoup(response.text, 'lxml')
                
                # 针对不同网站定制解析策略
                if 'wetest.vip' in url:
                    # 通过CSS选择器定位目标元素
                    targets = soup.select('pre.code')
                    if not targets:
                        targets = soup.find_all(['pre', 'code'])
                elif any(x in url for x in ['164746.xyz', '090227.xyz']):
                    targets = soup.find_all('tr')
                else:
                    targets = soup.find_all(['li', 'p', 'div.ip-item'])

                # 多重解析策略组合
                found_ips = []
                for element in targets:
                    found_ips.extend(re.findall(ip_pattern, element.get_text()))
                
                # 后备策略：全文本搜索
                if not found_ips:
                    found_ips = re.findall(ip_pattern, soup.get_text())

                # 写入去重后的结果
                for ip in set(found_ips):
                    f.write(f"{ip}\n")
                print(f"[{url}] 解析完成，找到{len(found_ips)}个IP")

            except Exception as e:
                print(f"[{url}] 处理失败: {str(e)}")
                continue

if __name__ == "__main__":
    fetch_ips()
    print('IP地址已更新到ip.txt文件')
