<!-- markdownlint-disable MD033 MD041 -->
<p align="center">
  <a href="https://cli.nonebot.dev/"><img src="https://cli.nonebot.dev/logo.png" width="200" height="200" alt="nonebot"></a>
</p>

<div align="center">

# NB CLI Plugin WebUI

_✨ NoneBot2 命令行工具 前端可视化页面（WebUI） 插件 ✨_

</div>

<p align="center">
  <a href="https://raw.githubusercontent.com/nonebot/nb-cli-plugin-webui/master/LICENSE">
    <img src="https://img.shields.io/github/license/nonebot/cli-plugin-webui" alt="license">
  </a>
  <a href="https://pypi.python.org/pypi/nb-cli-plugin-webui">
    <img src="https://img.shields.io/pypi/v/nb-cli-plugin-webui" alt="pypi">
  </a>
  <img src="https://img.shields.io/badge/python-3.10+-blue" alt="python">
  <a href="https://results.pre-commit.ci/latest/github/nonebot/nb-cli-plugin-webui/master">
    <img src="https://results.pre-commit.ci/badge/github/nonebot/cli-plugin-webui/master.svg" alt="pre-commit" />
  </a>
  <br />
  <a href="https://jq.qq.com/?_wv=1027&k=5OFifDh">
    <img src="https://img.shields.io/badge/QQ%E7%BE%A4-768887710-orange?style=flat-square" alt="QQ Chat Group">
  </a>
  <a href="https://qun.qq.com/qqweb/qunpro/share?_wv=3&_wwv=128&appChannel=share&inviteCode=7b4a3&appChannel=share&businessType=9&from=246610&biz=ka">
    <img src="https://img.shields.io/badge/QQ%E9%A2%91%E9%81%93-NoneBot-5492ff?style=flat-square" alt="QQ Channel">
  </a>
  <a href="https://t.me/botuniverse">
    <img src="https://img.shields.io/badge/telegram-botuniverse-blue?style=flat-square" alt="Telegram Channel">
  </a>
  <a href="https://discord.gg/VKtE6Gdc4h">
    <img src="https://discordapp.com/api/guilds/847819937858584596/widget.png?style=shield" alt="Discord Server">
  </a>
</p>

## 功能

- 可视化的 nb cli 操作
  - 创建新的 NoneBot 实例
  - 添加已有的 NoneBot 实例
  - 拓展（插件、适配器、驱动器）管理（安装、卸载）
- 可同时管理多个 NoneBot 实例
- 为启动的 NoneBot 实例提供状态展示、性能查询
- 可视化的 NoneBot 实例配置

## 使用

### 安装

**需要 [nb-cli](https://github.com/nonebot/nb-cli/)**

使用 nb-cli 安装

```shell
nb self install nb-cli-plugin-webui
```

使用 Docker 运行

```shell
docker pull nonebot/cli-plugin-webui:latest
```

Docker 镜像可以选择以下版本:

- `latest`, `latest-slim`: 最新的稳定版本 (Release)
- `latest-${python 版本}`, `latest-slim-${python 版本}`: 指定 Python 版本的最新版本
- `sha-${commit sha:0:7}-${python 版本}`, `sha-${commit sha:0:7}-${python 版本}-slim`: 指定 commit 的版本
- `${branch}-${python 版本}`, `${branch}-${python 版本}-slim`: 指定分支的最新版本

### 命令行使用

```shell
nb ui --help
```

Docker 镜像使用

```shell
docker run -it --rm -p 8080:8080 -v ./:/app nonebot/cli-plugin-webui:latest --help
```

可选附加 env 参数:

- HOST: 指定监听地址，默认为 `0.0.0.0`
- PORT: 指定监听端口，默认为 `8080`

## 开发

### 环境要求

- Python 3.10+
- Node.js 18+
- pnpm 8+（前端包管理）
- pdm（Python 包管理）
- nb-cli（NoneBot 命令行工具）

### 项目结构

```
cli-plugin-webui/
├── frontend/              # Vue 3 前端应用
│   ├── src/               # 前端源码
│   ├── package.json       # 前端依赖配置
│   └── vite.config.ts     # Vite 配置
├── nb_cli_plugin_webui/   # Python 后端
│   ├── app/               # FastAPI 应用
│   ├── cli/               # CLI 命令
│   ├── dist/              # 构建产物
│   └── server.py          # 服务器入口
├── script/                # 脚本文件
├── testbot/               # 测试机器人
├── pyproject.toml         # Python 项目配置
└── package.json           # pnpm 工作区配置
```

### 开发命令

#### 快速启动（推荐）

```bash
# 安装 pdm 和 pnpm 后，一键启动前后端开发服务器
nb ui dev

# 指定后端服务器主机和端口
nb ui dev -h 127.0.0.1 -p 3000
```

`nb ui dev` 命令会同时启动：

- 前端 Vite 开发服务器（热重载，默认端口 5173）
- 后端 FastAPI 服务器（自动重载，默认端口 8080）
- 自动打开浏览器访问 WebUI

**参数说明：**

- `-h` / `--host`：配置后端服务器监听地址（默认 `0.0.0.0`）
- `-p` / `--port`：配置后端服务器监听端口（默认 `8080`）
- 前端开发服务器端口（默认 5173）由 Vite 自动管理，暂不支持通过命令行配置

**开发模式特性：**

- 后端自动启用调试模式（`debug=1`）
- 自动生成 API 文档（`/docs`）
- 前端自动代理 `/api` 请求到后端服务器

#### 前端开发

```bash
# 进入前端目录
cd frontend

# 安装依赖
pnpm install

# 启动开发服务器
pnpm dev

# 构建生产版本
pnpm build

# 代码格式化
pnpm format

# 代码检查
pnpm lint
```

#### 后端开发

```bash
# 安装开发依赖
pdm install -G dev

# 启动后端开发服务器
pdm run dev-backend

# 启动前端开发服务器
pdm run dev-frontend

# 生成 OpenAPI 客户端
pdm run generate
```

### 代码风格

项目使用以下工具确保代码风格一致：

- **Python**: black (格式化) + isort (导入排序) + flake8 (检查)
- **前端**: prettier (格式化) + eslint (检查)
- **提交信息**: nonemoji (emoji 前缀)

### 预提交钩子

项目配置了 pre-commit 钩子，会在提交时自动运行代码格式化和检查：

```bash
# 安装预提交钩子
pre-commit install

# 手动运行所有钩子
pre-commit run --all-files
```

### 提交规范

提交信息需要使用 emoji 前缀，格式为：

```
:emoji: type(scope): description
```

常用 emoji：

- ✨ `:sparkles:` - 新功能
- 🐛 `:bug:` - Bug 修复
- 📝 `:memo:` - 文档更新
- 🔧 `:wrench:` - 配置变更
- 🚨 `:rotating_light:` - 代码风格修复
- ♻️ `:recycle:` - 代码重构
- ⬆️ `:arrow_up:` - 依赖更新

## 补充

nb-cli WebUI 目前正处于快速迭代中，欢迎各位提交在使用过程中发现的 BUG 和建议。
