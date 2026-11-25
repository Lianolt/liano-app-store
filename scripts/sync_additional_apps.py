#!/usr/bin/env python3
"""Sync every app in apps.json from GitHub Releases, including prereleases.

Selection rules:
- Ignore draft releases only.
- Accept both stable and prerelease releases.
- Select the newest release that actually contains an IPA asset.
- Paginate the Releases API so repositories with more than 100 releases are covered.
- Keep existing app metadata (bundle ID, icon, localized description) intact.
"""
import json
import os
import time
import urllib.error
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APPS_FILE = os.path.join(ROOT, "apps.json")
TOKEN = os.environ.get("GITHUB_TOKEN", "")

# Existing source apps and their canonical GitHub repositories.
REPOSITORIES = {
    "PiliPlus": "bggRGjQaUbCoE/PiliPlus",
    "Feather": "CLARATION/Feather",
    "PvZ Hybrid": "Dey410/PvZ-Hybrid-For-iOS",
    "Kazumi": "Predidit/Kazumi",
    "Gopeed": "GopeedLab/gopeed",
    "TiebaPure": "infinityf4p/TiebaPure-iOS",
    "Cilicili": "Rone89/cilicili",
    "Melox": "youshen2/MeloX",
    "Open Reading": "miloquinn/origo-x",
    "Pixiv-SwiftUI": "Eslzzyl/Pixiv-SwiftUI",
}

# Apps added to the source in November 2026.
ADDITIONAL_APPS = [
    {"name":"短剧之家","repo":"jackherex/duanjuzhijia-down-ios","icon":"https://raw.githubusercontent.com/Lianolt/liano-app-store/main/appicon/duanjuzhijia.png","description":"短剧之家 iOS 客户端，提供短剧内容浏览与观看。","bundle":"com.duanju.duanjuapp.v2"},
    {"name":"GuoDuo","repo":"81199000/GuoDuo","icon":"https://raw.githubusercontent.com/Lianolt/liano-app-store/main/appicon/GuoDuo.png","description":"GuoDuo iOS 客户端。","bundle":"me.rrmm.hongguo"},
    {"name":"iBuilder","repo":"Absenti/iBuilder","icon":"https://raw.githubusercontent.com/Lianolt/liano-app-store/main/appicon/ibuilder.png","description":"在 iPhone 上将自己拥有的 Nintendo Switch 游戏构建为原生 iOS 应用；不包含游戏、密钥或固件。","bundle":"dev.ibuilder.app"},
    {"name":"轻哩","repo":"liuliuya2333/LiLite","icon":"https://raw.githubusercontent.com/Lianolt/liano-app-store/main/appicon/LiLite.PNG","description":"轻哩（LiLite）iOS 客户端。","bundle":"com.liuliuya.PiliNative"},
    {"name":"i 短剧","repo":"my-name-is-alan/iDuanJu","icon":"https://raw.githubusercontent.com/Lianolt/liano-app-store/main/appicon/iDuanju.png","description":"i 短剧 iOS 客户端。","bundle":"com.local.STV"},
    {"name":"DSH Go","repo":"ccch1mneyyy/dsh-Go","icon":"https://raw.githubusercontent.com/Lianolt/liano-app-store/main/appicon/DSH-Go.png","description":"DSH Go iOS 客户端。","bundle":"io.github.ccch1mneyyy.dshgo"},
    {"name":"Erosion","repo":"Kianuni/Erosion-CN","icon":"https://raw.githubusercontent.com/Lianolt/liano-app-store/main/appicon/Erosion.PNG","description":"Erosion 中文版 iOS 客户端。","bundle":"com.jbdotparty.Erosion"},
    {"name":"DuoDuo","repo":"81199000/DouDuo","icon":"https://raw.githubusercontent.com/Lianolt/liano-app-store/main/appicon/DuoDuo.png","description":"第三方抖音客户端，支持视频浏览、搜索、评论、直播及收藏等功能。","bundle":"me.rrmm.douduo"},
    {"name":"酷安 lite","repo":"coolapk-desktop/coolapk-desktop","icon":"https://raw.githubusercontent.com/Lianolt/liano-app-store/main/appicon/coolapk.PNG","description":"酷安桌面版轻量客户端。","bundle":"com.coolapk.desktop"},
    {"name":"HGhubX","repo":"zxsos/HGhubX","icon":"https://raw.githubusercontent.com/Lianolt/liano-app-store/main/appicon/HGhubX.png","description":"HGhubX iOS 客户端。","bundle":"com.hghubx.app"},
    {"name":"itchPocket","repo":"Liano1125/Itch","icon":"https://raw.githubusercontent.com/Lianolt/liano-app-store/main/appicon/itchPocket.PNG","description":"itchPocket：管理 itch.io 游戏库、作者动态与 Ren’Py 游戏的 iOS 应用。","bundle":"com.liano.itchPocket"},
]

def request_json(url, attempts=4):
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "Liano-iPASource-Sync",
    }
    if TOKEN:
        headers["Authorization"] = "Bearer " + TOKEN
    for attempt in range(attempts):
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=60) as response:
                return json.load(response)
        except urllib.error.HTTPError as exc:
            if exc.code not in (403, 429, 500, 502, 503, 504) or attempt == attempts - 1:
                raise
            retry_after = int(exc.headers.get("Retry-After", "0") or "0")
            time.sleep(max(retry_after, 2 ** attempt))
        except (urllib.error.URLError, TimeoutError):
            if attempt == attempts - 1:
                raise
            time.sleep(2 ** attempt)
    raise RuntimeError("GitHub API request failed after retries: " + url)

def newest_release_with_ipa(repo):
    page = 1
    while True:
        url = f"https://api.github.com/repos/{repo}/releases?per_page=100&page={page}"
        releases = request_json(url)
        if not isinstance(releases, list):
            raise RuntimeError(f"Unexpected Releases API response for {repo}: {releases}")
        for release in releases:
            if release.get("draft"):
                continue
            ipa_assets = [
                asset for asset in release.get("assets", [])
                if asset.get("name", "").lower().endswith(".ipa")
                and asset.get("browser_download_url")
                and int(asset.get("size") or 0) > 0
            ]
            if ipa_assets:
                return release, ipa_assets[0]
        if len(releases) < 100:
            return None, None
        page += 1

def main():
    with open(APPS_FILE, "r", encoding="utf-8") as f:
        source = json.load(f)

    apps = source.get("apps", [])
    by_name = {app.get("name"): app for app in apps}
    missing = [name for name in REPOSITORIES if name not in by_name]
    if missing:
        raise RuntimeError("Repository mapping refers to missing apps.json entries: " + ", ".join(missing))

    manifests = []
    for name, repo in REPOSITORIES.items():
        manifests.append({"name": name, "repo": repo, "bundle": None, "icon": None, "description": None})
    manifests.extend(ADDITIONAL_APPS)

    synced = 0
    skipped = []
    for item in manifests:
        name, repo = item["name"], item["repo"]
        current = by_name.get(name)
        if current is None:
            current = {
                "name": name,
                "bundleIdentifier": item.get("bundle") or "",
                "developerName": repo.split("/")[0],
                "localizedDescription": item.get("description") or "",
                "iconURL": item.get("icon") or "",
                "tintColor": "#000000",
            }
            apps.append(current)
            by_name[name] = current

        release, ipa = newest_release_with_ipa(repo)
        if release is None:
            print(f"SKIP {name}: no non-draft Release with an IPA asset; preserving current metadata")
            skipped.append(name)
            continue

        tag = release.get("tag_name") or release.get("name") or "unknown"
        published = release.get("published_at") or release.get("created_at") or ""
        notes = release.get("body") or ""
        if release.get("prerelease"):
            notes = "⚠️ GitHub 预发行版本（非正式稳定版）\n\n" + notes

        # Preserve stable app identity and presentation metadata from apps.json.
        current.update({
            "name": name,
            "bundleIdentifier": current.get("bundleIdentifier") or item.get("bundle") or "",
            "developerName": current.get("developerName") or repo.split("/")[0],
            "version": tag,
            "versionDate": published,
            "versionDescription": notes,
            "localizedDescription": current.get("localizedDescription") or item.get("description") or "",
            "downloadURL": ipa["browser_download_url"],
            "iconURL": current.get("iconURL") or item.get("icon") or "",
            "tintColor": current.get("tintColor") or "#000000",
            "size": int(ipa["size"]),
            "versions": [{
                "version": tag,
                "date": published,
                "localizedDescription": notes,
                "downloadURL": ipa["browser_download_url"],
                "size": int(ipa["size"]),
            }],
        })
        channel = "预发行" if release.get("prerelease") else "正式版"
        print(f"SYNC {name}: {tag} [{channel}] {ipa['name']} {ipa['size']} bytes")
        synced += 1

    with open(APPS_FILE, "w", encoding="utf-8") as f:
        json.dump(source, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(f"Release IPA sync complete: {synced}/{len(manifests)} apps updated")
    if skipped:
        print("Apps without an eligible IPA Release: " + ", ".join(skipped))

if __name__ == "__main__":
    main()
