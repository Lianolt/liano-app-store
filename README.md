# Liano's iPA Source

面向 iOS 侧载用户的第三方 IPA 软件源，收录开源项目及第三方应用。

## 添加软件源

- **名称：** Liano's ipasource
- **Identifier：** `com.Lianolt.ipasource`
- **软件源地址：**  
  `https://raw.githubusercontent.com/Lianolt/liano-app-store/main/apps.json`
- **总图标：**  
  `https://raw.githubusercontent.com/Lianolt/liano-app-store/main/appicon/AppStore.jpg`

将软件源地址添加到支持自定义源的侧载客户端即可。

## 自动更新

GitHub Actions 每天自动同步两次，也支持手动运行。

同步范围包括正式版和预发行版；跳过 Draft，并选择最新的、包含 IPA 文件的 Release。自动更新版本号、更新日志、下载地址及 IPA 文件大小。

## 仓库结构

- `apps.json`：软件源数据。
- `appicon/`：软件源及应用图标。
- `scripts/sync_additional_apps.py`：Release 同步脚本。
- `.github/workflows/sync-all.yml`：自动同步工作流。

## 免责声明

本仓库仅整理并提供公开项目的 IPA 下载信息，不拥有所收录应用的代码、商标或版权。相关权利归原作者所有，请遵守项目许可证及所在地法律法规。

如需移除相关项目，请提交 Issue。
