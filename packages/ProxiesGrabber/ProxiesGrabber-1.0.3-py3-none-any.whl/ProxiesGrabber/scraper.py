import base64
import re
import requests
import threading


class ProxiesGrabber:

    def __init__(self):
        self.list = []
        self.session = requests.Session()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        self.sites = [self.site1, self.site2, self.site3,
                      self.site4, self.site5, self.site6]
        self.fetch_proxies()

    def fetch_proxies(self):
        threads = []
        for site in self.sites:
            thread = threading.Thread(target=site)
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        self.list = [f"{ip}:{port}" for ip, port in self.list]

    def site1(self):
        try:
            response = self.session.get(
                "https://free-proxy-list.net/", headers=self.headers, timeout=5)
            self.list.extend(re.findall(
                r"(\d+\.\d+\.\d+\.\d+):(\d+)", response.text))
        except requests.RequestException:
            pass

    def site2(self):
        try:
            for page in range(1, 5):
                response = self.session.get(
                    f"http://free-proxy.cz/en/proxylist/main/{page}", headers=self.headers)
                data = re.findall(
                    r'Base64.decode\("(.+?)"\).+?>(\d+)<', response.text)
                self.list.extend(
                    [(base64.b64decode(ip).decode('utf-8'), port) for ip, port in data])
        except requests.RequestException:
            pass

    def site3(self):
        try:
            response = self.session.get(
                "https://proxy-list.org/english/index.php", headers=self.headers)
            self.list.extend([(base64.b64decode(ip).decode("utf-8"), port)
                             for ip, port in re.findall(r"Proxy\('(.+?)'\)", response.text)])
        except requests.RequestException:
            pass

    def site4(self):
        try:
            response = self.session.get(
                "https://www.sslproxies.org/", headers=self.headers)
            self.list.extend(re.findall(
                r"(\d+\.\d+\.\d+\.\d+):(\d+)", response.text))
        except requests.RequestException:
            pass

    def site5(self):
        try:
            response = self.session.get(
                "https://hide.mn/en/proxy-list/", headers=self.headers)
            self.list.extend(re.findall(
                r"(\d+\.\d+\.\d+\.\d+):(\d+)", response.text))
        except requests.RequestException:
            pass

    def site6(self):
        try:
            response = self.session.get(
                "https://api.proxyscrape.com/v4/free-proxy-list/get?request=display_proxies&proxy_format=protocolipport&format=json", timeout=5)
            if response.status_code == 200:
                self.list.extend([(proxy['ip'], proxy['port'])
                                 for proxy in response.json().get('proxies', [])])
        except requests.RequestException:
            pass
