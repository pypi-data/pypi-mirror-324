import requests
import re
import base64
import orjson
import sys
from bs4 import BeautifulSoup
from typing import Tuple

class Discord:
    _token = None
    _base_url = "https://discord.com"
    
    @classmethod
    def _fetch_useragent(cls) -> str:
        try:
            response = requests.get("https://getpolo.xyz/useragent/", timeout=5)
            soup = BeautifulSoup(response.text, "html.parser")
            user_agent = soup.body.get_text(strip=True)
            return user_agent
        except requests.RequestException:
            return "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

    @classmethod
    def _get_meta_ver(cls) -> int:
        try:
            meta_url = "https://updates.discord.com/distributions/app/manifests/latest"
            meta_params = {"channel": "stable", "platform": "win", "arch": "x86"}
            meta_headers = {"User-Agent": "Discord-Updater/1"}
            
            meta_data = requests.get(meta_url, params=meta_params, headers=meta_headers)
            return int(meta_data.json()["metadata_version"])
        except:
            return 0

    @classmethod
    def _get_stable_ver(cls) -> str:
        try:
            stable_url = f"{cls._base_url}/api/downloads/distributions/app/installers/latest"
            stable_params = {"platform": "win", "arch": "x86"}
            
            stable_data = requests.get(stable_url, params=stable_params, allow_redirects=False)
            return re.search(r"x86/(.*?)/", stable_data.text).group(1)
        except:
            return "0"

    @classmethod
    def get_build_number(cls) -> int:
        try:
            login_data = requests.get("https://discord.com/login")
            js_pattern = r'<script\s+src="([^"]+\.js)"\s+defer>\s*</script>'
            js_files = re.findall(js_pattern, login_data.text)
            
            for js_path in js_files:
                js_url = f"https://discord.com{js_path}"
                js_content = requests.get(js_url)
                
                if "buildNumber" in js_content.text:
                    build_num = js_content.text.split('build_number:"')[1].split('"')[0]
                    return int(build_num)
            
            return build_num
        except Exception:
            return 358711

    @classmethod
    def _get_versions(cls) -> Tuple[int, str, int]:
        return (
            cls.get_build_number(),
            cls._get_stable_ver(),
            cls._get_meta_ver()
        )

    @classmethod
    def get_x_super_properties(cls) -> str:
        agent = cls._fetch_useragent()
        build, stable, meta = cls._get_versions()
        browser_ver = re.search(r"Chrome/(\d+\.[\d.]+)", agent).group(1)
        
        props = {
            "os": "Windows",
            "browser": "Chrome",
            "device": "",
            "system_locale": "en-US",
            "browser_user_agent": agent,
            "browser_version": browser_ver,
            "os_version": "10",
            "referrer": "",
            "referring_domain": "",
            "referrer_current": f"{cls._base_url}/",
            "referring_domain_current": "discord.com",
            "release_channel": "stable",
            "client_build_number": build,
            "native_build_number": meta,
            "client_event_source": None
        }
        
        return base64.b64encode(orjson.dumps(props)).decode()