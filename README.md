Liano’s IPA Source

一个面向 iOS 侧载用户的第三方 IPA 软件源，适用于 全能签、Feather、SideStore / AltStore 类客户端。

本仓库主要收录开源项目及第三方 iOS 应用的 IPA 安装包，并通过 GitHub Releases 自动同步应用版本、更新日志、文件大小和下载地址。

⸻

📱 软件源信息

名称： Liano’s ipasource

Identifier：

com.happier1125.ipasource

软件源图标：

https://raw.githubusercontent.com/happier1125/liano-app-store/main/appicon/User.jpeg

软件源地址：

https://raw.githubusercontent.com/happier1125/liano-app-store/main/apps.json

将上面的 apps.json 地址添加到支持自定义软件源的 IPA 签名/侧载工具即可。

⸻

✨ 特性

* 📦 收录多个优秀的 iOS IPA 应用
* 🔄 自动同步 GitHub Releases 最新版本
* 📋 自动获取 Release 更新日志
* 📏 自动获取 IPA 实际文件大小
* 🔗 自动获取 GitHub 官方下载地址
* 🖼️ 支持自定义应用图标
* 🕒 自动记录版本发布时间
* 📚 保留应用版本信息
* 🤖 GitHub Actions 自动执行同步
* 🚫 不在本仓库存储 IPA 文件，降低仓库体积

⸻

📱 当前收录应用

应用	开发者	项目
PiliPlus	bggRGjQaUbCoE	GitHub
Feather	CLARATION	GitHub
PvZ Hybrid	Dey410	GitHub
Kazumi	Predidit	GitHub
Gopeed	GopeedLab	GitHub
TiebaPure	infinityf4p	GitHub
Cilicili	Rone89	GitHub
MeloX	youshen2	GitHub
Open Reading	miloquinn	GitHub
Pixiv-SwiftUI	Eslzzyl	GitHub

应用版本、更新日志、文件大小和 IPA 下载地址会根据对应项目的 GitHub Releases 自动更新。

⸻

🔄 自动更新机制

本软件源使用 GitHub Actions 自动同步应用更新。

工作流文件：

.github/workflows/sync-all.yml

默认每天自动运行一次，同时支持在 GitHub Actions 中手动运行。

同步内容

每次同步会从对应项目的 GitHub Releases 获取最新 Release，并自动更新：

version
versionDate
versionDescription
downloadURL
size
versions

其中：

* version — 最新版本号
* versionDate — Release 发布时间
* versionDescription — Release 更新日志
* downloadURL — IPA 官方下载地址
* size — IPA 实际文件大小（Bytes）
* versions — 应用版本信息

⸻

📦 IPA 文件筛选

为了避免 GitHub Release 中存在多个平台文件导致错误下载，本仓库的自动同步脚本会优先筛选：

.ipa

只有 Release Assets 中的 IPA 文件才会被作为 iOS 安装包写入软件源。

例如一个 Release 同时存在：

Android APK
Windows EXE
macOS DMG
Linux Package
iOS IPA

同步脚本只会选择 IPA。

这样可以避免侧载工具获取到错误的平台安装包。

⸻

🗂️ 仓库结构

liano-app-store/
│
├── .github/
│   └── workflows/
│       └── sync-all.yml
│
├── appicon/
│   ├── User.jpeg
│   ├── Feather.png
│   ├── PVZH.png
│   ├── Kazumi.jpeg
│   ├── Gopeed.png
│   ├── TiebaPure.jpg
│   ├── Cilicili.png
│   ├── Melox.png
│   ├── Open-Reading.png
│   └── Pixiv-SwiftUI.PNG
│
├── apps.json
│
└── README.md

apps.json

软件源核心数据文件。

其中包含软件源基本信息以及所有应用的版本、描述、图标、下载地址和文件大小等信息。

appicon/

存放软件源中应用使用的图标。

.github/workflows/sync-all.yml

GitHub Actions 自动同步脚本。

⸻

➕ 添加新的应用

如果希望向软件源添加新的应用，需要准备：

1. 应用名称
2. GitHub Releases 地址
3. 应用图标
4. 对应的 iOS IPA Release

推荐应用项目具有公开的 GitHub Releases，并且 Release 中提供 .ipa 文件。

添加应用后，在 apps.json 中增加对应的应用信息，并在：

.github/workflows/sync-all.yml

中增加对应的自动同步任务。

之后 GitHub Actions 会负责自动更新版本信息。

⸻

🖼️ 应用图标

应用图标统一存放在：

appicon/

推荐使用：

* PNG
* JPG / JPEG

图标 URL 示例：

https://raw.githubusercontent.com/happier1125/liano-app-store/main/appicon/Gopeed.png

⸻

🛠️ GitHub Actions

自动同步工作流：

.github/workflows/sync-all.yml

自动运行

默认每天执行一次。

手动运行

进入：

GitHub
→ Actions
→ Sync All Apps Updates
→ Run workflow

即可立即执行同步。

如果应用有新版本，工作流会自动修改：

apps.json

并提交新的 Commit。

如果所有应用都没有更新，则不会产生新的 Commit。

⸻

🔗 数据来源

本软件源中的应用版本信息主要来自对应项目的 GitHub Releases。

应用项目：

* PiliPlus
* Feather
* PvZ Hybrid
* Kazumi
* Gopeed
* TiebaPure
* Cilicili
* MeloX
* Open Reading
* Pixiv-SwiftUI

应用的具体版权、许可证及开发者权益均归原项目作者所有。

⸻

⚠️ 免责声明

本仓库只是一个第三方 IPA 软件源，不开发、不修改、不拥有所收录应用的源代码及版权。

本仓库提供的 IPA 下载地址原则上指向对应项目的公开 GitHub Releases。

使用本软件源所产生的任何问题，包括但不限于：

* IPA 安装失败
* 应用闪退
* 证书失效
* 应用无法启动
* 应用版本兼容性问题
* 原项目停止维护
* GitHub Release 被删除
* 开发者撤回 IPA

均需要以对应应用项目及其开发者的说明为准。

请遵守所在地法律法规以及相关软件的许可证协议。

如果某个项目作者希望从本软件源移除其应用，请提交 Issue 或联系仓库维护者。

⸻

⭐ 支持

如果这个软件源对你有帮助，可以：

⭐ Star 本仓库

🐛 提交 Issue

🔧 提交 Pull Request

也欢迎推荐优秀的开源 iOS 项目。

⸻

📄 License

本仓库的软件源配置文件及自动化脚本采用仓库实际声明的许可证。

本仓库收录的软件、图标及相关项目资源，其版权和许可证归各自原作者所有。

⸻

<p align="center">
  Made with ❤️ by Liano
</p>