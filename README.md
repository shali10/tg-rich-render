# tg-rich-render 📊✨

> **Zero-dependency, CJK-aware Markdown table & rich format converter for Telegram bots.**  
> 专治 Telegram 机器人表格排版错位、中英混排对不齐、手机端横向溢出变难看代码块的痛点。

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![CI Status](https://github.com/shali10/tg-rich-render/actions/workflows/ci.yml/badge.svg)](https://github.com/shali10/tg-rich-render/actions)

---

## 💡 为什么需要 tg-rich-render？

Telegram 官方的 MarkdownV2 并不支持标准的 GFM Pipe Table（管道表格）。在日常 Telegram 机器人开发（运维巡检播报、资产统计、行情早报）中，直接发送表格通常会遇到以下问题：

1. **直接报错**：Telegram Bot API 无法解析 `| col | col |` 语法；
2. **粗暴丢进代码块**：直接用 ```` 包裹，但在中英汉字、Emoji 混排时由于字符显示宽度（CJK 宽度为 2）导致竖线完全错位，排版歪歪扭扭；
3. **窄屏移动端阅读体验差**：宽表格在手机竖屏下横向拉长折行。

`tg-rich-render` 提供纯 Python 标准库实现的智能 CJK 宽度对齐与多风格自适应渲染，一行代码即可集成到 **aiogram 3**、**python-telegram-bot** 或任何 HTTP 请求中。

---

## ✨ 核心特性

- 🚀 **零外部依赖**：纯 Python 标准库构建（基于 `unicodedata` 模块），即装即用，启动开销 0ms。
- 📐 **精准 CJK / Emoji 宽度补偿**：完美对齐汉字、日韩文、全角符号与 Emoji 表情，拒绝折线与锯齿。
- 🎨 **多风格视觉呈现**：
  - `rounded`：现代优雅圆角框线（`╭───┬───╮`），视觉质感拉满。
  - `classic`：经典 ASCII 风格（`+---+---+`）。
  - `clean`：极简流式无竖框风格。
  - `card`：移动端窄屏优先卡片流（键值对展示，杜绝横向滚动）。
  - `html`：Telegram 兼容 HTML `<table>` 格式。
- 🤖 **主流框架开箱即用**：自带 aiogram 3 与 python-telegram-bot 发送适配器。
- 💻 **CLI 工具支持**：支持管道输入与终端即时预览。

---

## 📦 快速安装

```bash
pip install tg-rich-render
```

或直接克隆使用：

```bash
git clone https://github.com/shali10/tg-rich-render.git
cd tg-rich-render
pip install -e .
```

---

## 🚀 快速上手

### 1. 独立使用（纯 Python）

```python
from tg_rich_render import render_telegram

raw_markdown = """
# 节点健康巡检

| 节点 | 状态 | 延迟 |
|:---|:---:|---:|
| 香港CN2 🚀 | 正常 | 15ms |
| 美国洛杉矶 | 良好 | 135ms |
| 日本东京 ⚡ | 正常 | 48ms |

巡检完成，无异常节点。
"""

# 渲染为 Telegram 优雅圆角等宽表格
message = render_telegram(raw_markdown, style="rounded")
print(message)
```

**输出效果：**

```
# 节点健康巡检

```
╭────────────┬──────┬───────╮
│ 节点       │ 状态 │  延迟 │
├────────────┼──────┼───────┤
│ 香港CN2 🚀 │ 正常 │  15ms │
│ 美国洛杉矶 │ 良好 │ 135ms │
│ 日本东京 ⚡ │ 正常 │  48ms │
╰────────────┴──────┴───────╯
```

巡检完成，无异常节点。
```

---

### 2. 结合 aiogram 3

```python
from aiogram import Bot
from tg_rich_render import send_smart_message

bot = Bot(token="YOUR_BOT_TOKEN")

# 一行代码自适应格式化并发送
await send_smart_message(
    bot=bot,
    chat_id=12345678,
    text=raw_markdown,
    table_style="rounded"
)
```

---

### 3. 结合 python-telegram-bot

```python
from telegram import Bot
from tg_rich_render import send_smart_message

bot = Bot(token="YOUR_BOT_TOKEN")

await send_smart_message(
    bot=bot,
    chat_id=12345678,
    text=raw_markdown,
    table_style="rounded"
)
```

---

### 4. 命令行（CLI）使用

```bash
# 转换 Markdown 文件
tg-rich-render report.md --style rounded

# 从终端管道流式转换
cat summary.md | tg-rich-render --style card
```

---

## 🎨 渲染风格展示

| 风格名称 | 预览示意 | 适用场景 |
|:---|:---|:---|
| **rounded** (默认) | `╭─┬─╮\n│A│B│\n╰─┴─╯` | PC 端与大屏客户端，视觉质感极高 |
| **classic** | `+-+-+\n|A|B|\n+-+-+` | 通用等宽终端、标准日志输出 |
| **clean** | `A  B\n─  ─\n1  2` | 极简通知、紧凑监控通知 |
| **card** | `📌 节点\n  • 延迟: 15ms` | 移动端窄屏、列数较多的宽表格 |
| **html** | `<table>...</table>` | Telegram WebApp 或特定富文本容器 |

---

## 🧪 单元测试

项目自带完整的自动化测试集（覆盖 CJK 宽度、对齐算法、长文本解析与适配器）：

```bash
python3 -m unittest discover -s tests
```

---

## 📄 开源许可

本项目基于 [MIT License](LICENSE) 开源。
