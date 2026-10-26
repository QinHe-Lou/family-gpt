# 家庭 GPT 4.0 — iPhone Safari 美化版

这是可直接更新旧版 `family-gpt` Streamlit 网站的项目。继续使用原来的网址和家庭密码，不需要创建新的 Streamlit App。

## 新增功能

- **美化界面：** 渐变欢迎区域、卡片聊天、专为 iPhone 优化的控件与触屏尺寸，默认不显示底部的外部推广、部署工具图标（这些 CSS 选择器在 Streamlit 未来更新时可能变化）。
- **输入栏右侧：** `📎` 选择附件、`🎙️` 录音、`➤` 发送；在文本框内按回车也能发送。
- **切换模型：** 侧栏可选 GPT-6 Luna、GPT-6.1 Sol、GPT-6 Astra；更高阶模型可能显著增加费用。
- **管理员 API 设置：** 可临时输入自己的 API Key、完整 HTTPS 接口地址（Base URL），以及选择 Responses API / Chat Completions API 协议或输入自定义模型 ID。
- **保留 v3 功能：** 文件格式和大小审查、预览后确认发送、人工失败重试、聊天记录导出和恢复、语音朗读，以及「记住登录 7 天」。

> UI 代码通过静态 Python 语法检查，文件解析、Cookie 签名和 URL 校验通过本地单元测试。由于无法接入你的线上 Streamlit 和 API 凭证，尚未做在线端到端验证。

## iPhone 更新步骤（原仓库，无需建新站）

1. 先去 GitHub 仓库 `family-gpt`，保存/记下目前正常运行的 Commit 号，以便回退。
2. 将这个压缩包解压，在 iPhone Safari 打开 GitHub 仓库，`Add file` → `Upload files`，将 **新版 `app.py` 与 `requirements.txt` 同时上传到根目录** 覆盖同名旧文件；如果上传界面不支持同名覆盖，可打开每个旧文件编辑/替换内容。
3. 在 GitHub 提交到 `main`。Streamlit 一般自动重新部署。若没更新，进入 Streamlit `Manage app` → `Reboot`，并看 `Logs`。
4. **这次新增一步：** 在 Streamlit 应用设置 `Secrets` 增加独立的管理员密码（注意不要把 Secrets 上传 GitHub）：

   ```toml
   OPENAI_API_KEY = "你的原有API密钥"
   FAMILY_PASSWORD = "你的原有家庭登录密码"
   OPENAI_MODEL = "gpt-6-luna"
   ADMIN_PASSWORD = "你单独设置的管理员强密码"
   # 可选：默认接口地址。不写则使用 OpenAI 官方地址
   # OPENAI_BASE_URL = "https://api.openai.com/v1"
   ```

5. 打开旧网址 `https://family-gpt-01.streamlit.app/`，输入家庭密码（已经登录的设备可继续使用此前的 7 天记住登录）。左上角侧边栏选择模型。
6. 进入侧边栏 **管理员 · 模型与 API**，输入 `ADMIN_PASSWORD` 解锁，才可以修改密钥、Base URL、API 协议和自定义模型 ID。
7. 测试输入一条文本、点击输入框右侧 `📎` 上传 TXT 后预览确认、点击 `🎙️` 录音、尝试保存和恢复对话。

## 安全和计费说明

- **管理员密码不等于家庭密码。** 不填写 `ADMIN_PASSWORD` 时仍可聊天、切换预设模型，但不能在网页里修改连接信息。
- 网页输入的 API Key 和接口地址只存放在当前浏览器对应的 Streamlit 服务端会话中，不会提交到 GitHub、写入聊天记录、Cookie 或上传文件。若网站重启、登出、会话失效会回退为 Secrets 中的设置。若要永久修改，请在 Streamlit Secrets 中更新。
- 不能把你的 ChatGPT 订阅当成 API 余额；调用 API 单独计费。模型、文件图片、语音和人工重试都可能产生费用。
- 自定义 API URL 只能填写 HTTPS 形式的公网地址；请**仅填写你信任的服务商**，因为聊天内容、文件内容及临时输入的 API Key 都会发送给它。应用未保证所有第三方 API 与 OpenAI SDK 兼容；若服务商不支持 Responses API，可在设置中切换 Chat Completions API。
- 文件解析/审查是格式、大小和可提取内容检查，**不是恶意软件扫描或专业安全审计**。文件内容直到你勾选同意并点击确认后才提交 AI。
- 失败时不会自动无限重发，最多人工尝试 3 次；即使请求看似失败也可能实际扣费。
- 7 天记住登录使用签名 Cookie，不含明文家庭密码；应只在私人手机上开启。
- 不建议上传身份证、财务账号、健康资料或其他不必要的敏感文件。

## 依赖环境

推荐 Python 3.11/3.12，Streamlit Community Cloud 上可选择对应运行环境。保留仓库根目录内的 `requirements.txt`；这是此前出现 `ModuleNotFoundError: No module named openai` 的关键。

## 如果升级失败

- GitHub 确认 `app.py` 和 `requirements.txt` 与本包一致，并且都在根目录。
- Streamlit `Manage app` → `Logs` 查看最后 20 行错误。
- 如果新版本影响使用，GitHub 通过旧提交的 `Revert`/恢复旧文件，再提交到 `main` 即可回到上一版。
