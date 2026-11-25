#!/usr/bin/env python3
"""Sync additional IPA apps from stable GitHub Releases into apps.json."""
import json
import os
import plistlib
import tempfile
import urllib.request
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APPS_FILE = os.path.join(ROOT, "apps.json")
TOKEN = os.environ.get("GITHUB_TOKEN", "")

APPS = [
    {"name":"短剧之家","repo":"jackherex/duanjuzhijia-down-ios","icon":"https://raw.githubusercontent.com/Lianolt/liano-app-store/main/appicon/duanjuzhijia.png","description":"短剧之家 iOS 客户端，提供短剧内容浏览与观看。","bundle":"com.jackherex.duanjuzhijia"},
    {"name":"GuoDuo","repo":"81199000/GuoDuo","icon":"https://raw.githubusercontent.com/Lianolt/liano-app-store/main/appicon/GuoDuo.png","description":"GuoDuo iOS 客户端。","bundle":"me.rrmm.hongguo"},
    {"name":"iBuilder","repo":"Absenti/iBuilder","icon":"https://raw.githubusercontent.com/Lianolt/liano-app-store/main/appicon/ibuilder.png","description":"在 iPhone 上将自己拥有的 Nintendo Switch 游戏构建为原生 iOS 应用；不包含游戏、密钥或固件。","bundle":"dev.ibuilder.app"},
    {"name":"轻哩","repo":"liuliuya2333/LiLite","icon":"https://raw.githubusercontent.com/Lianolt/liano-app-store/main/appicon/LiLite.PNG","description":"轻哩（LiLite）iOS 客户端。","bundle":"com.liuliuya.lilite"},
    {"name":"i 短剧","repo":"my-name-is-alan/iDuanJu","icon":"https://raw.githubusercontent.com/Lianolt/liano-app-store/main/appicon/iDuanju.png","description":"i 短剧 iOS 客户端。","bundle":"com.local.STV"},
    {"name":"DSH Go","repo":"ccch1mneyyy/dsh-Go","icon":"https://raw.githubusercontent.com/Lianolt/liano-app-store/main/appicon/DSH-Go.png","description":"DSH Go iOS 客户端。","bundle":"io.github.ccch1mneyyy.dshgo"},
    {"name":"Erosion","repo":"Kianuni/Erosion-CN","icon":"https://raw.githubusercontent.com/Lianolt/liano-app-store/main/appicon/Erosion.PNG","description":"Erosion 中文版 iOS 客户端。","bundle":"com.jbdotparty.Erosion"},
    {"name":"DuoDuo","repo":"81199000/DouDuo","icon":"https://raw.githubusercontent.com/Lianolt/liano-app-store/main/appicon/DuoDuo.png","description":"第三方抖音客户端，支持视频浏览、搜索、评论、直播及收藏等功能。","bundle":"me.rrmm.douduo"},
    {"name":"酷安 lite","repo":"coolapk-desktop/coolapk-desktop","icon":"https://raw.githubusercontent.com/Lianolt/liano-app-store/main/appicon/coolapk.PNG","description":"酷安桌面版轻量客户端。","bundle":"com.coolapk.desktop"},
    {"name":"HGhubX","repo":"zxsos/HGhubX","icon":"https://raw.githubusercontent.com/Lianolt/liano-app-store/main/appicon/HGhubX.png","description":"HGhubX iOS 客户端。","bundle":"com.hghubx.app"},
    {"name":"itchPocket","repo":"Liano1125/Itch","icon":"https://raw.githubusercontent.com/Lianolt/liano-app-store/main/appicon/itchPocket.PNG","description":"itchPocket：管理 itch.io 游戏库、作者动态与 Ren’Py 游戏的 iOS 应用。","bundle":"com.liano.itchPocket"},
]

def request_json(url):
    headers = {"Accept":"application/vnd.github+json", "User-Agent":"Liano-iPASource-Sync"}
    if TOKEN:
        headers["Authorization"] = "Bearer " + TOKEN
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=60) as response:
        return json.load(response)

def get_bundle_id(asset_url, fallback):
    # Read the actual bundle identifier from the IPA when possible.
    headers = {"User-Agent":"Liano-iPASource-Sync"}
    if TOKEN:
        headers["Authorization"] = "Bearer " + TOKEN
    req = urllib.request.Request(asset_url, headers=headers)
    with tempfile.NamedTemporaryFile(suffix=".ipa") as tmp:
        try:
            with urllib.request.urlopen(req, timeout=180) as response:
                while True:
                    chunk = response.read(1024 * 1024)
                    if not chunk:
                        break
                    tmp.write(chunk)
            tmp.flush()
            with zipfile.ZipFile(tmp.name) as archive:
                candidates = [n for n in archive.namelist() if n.startswith("Payload/") and n.endswith(".app/Info.plist")]
                if candidates:
                    info = plistlib.loads(archive.read(candidates[0]))
                    value = info.get("CFBundleIdentifier")
                    if value:
                        return value
        except Exception as exc:
            print("  WARN: IPA bundle ID inspection failed:", exc)
    return fallback

def main():
    with open(APPS_FILE, "r", encoding="utf-8") as f:
        source = json.load(f)
    existing = {a.get("name"): a for a in source.get("apps", [])}

    for item in APPS:
        releases = request_json("https://api.github.com/repos/" + item["repo"] + "/releases?per_page=100")
        selected = None
        ipa = None
        for release in releases:
            if release.get("draft") or release.get("prerelease"):
                continue
            assets = [a for a in release.get("assets", []) if a.get("name", "").lower().endswith(".ipa")]
            if assets:
                selected, ipa = release, assets[0]
                break
        if not selected:
            print("SKIP", item["name"], "- no stable Release IPA found")
            continue

        tag = selected.get("tag_name") or selected.get("name") or "unknown"
        published = selected.get("published_at") or selected.get("created_at") or ""
        body = selected.get("body") or ""
        bundle_id = get_bundle_id(ipa["browser_download_url"], item["bundle"])
        metadata = {
            "name": item["name"],
            "bundleIdentifier": bundle_id,
            "developerName": item["repo"].split("/")[0],
            "version": tag,
            "versionDate": published,
            "versionDescription": body,
            "localizedDescription": item["description"],
            "downloadURL": ipa["browser_download_url"],
            "iconURL": item["icon"],
            "tintColor": "#000000",
            "size": int(ipa["size"]),
            "versions": [{
                "version": tag,
                "date": published,
                "localizedDescription": body,
                "downloadURL": ipa["browser_download_url"],
                "size": int(ipa["size"])
            }]
        }
        if item["name"] in existing:
            idx = source["apps"].index(existing[item["name"]])
            source["apps"][idx] = metadata
        else:
            source.setdefault("apps", []).append(metadata)
        existing[item["name"]] = metadata
        print("SYNC", item["name"], tag, ipa["name"], ipa["size"], "bytes")

    with open(APPS_FILE, "w", encoding="utf-8") as f:
        json.dump(source, f, ensure_ascii=False, indent=2)
        f.write("\n")

if __name__ == "__main__":
    main()
