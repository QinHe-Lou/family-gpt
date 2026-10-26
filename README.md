# 家庭 GPT 3.0 — iPhone 文件审查、重试与记住登录

这是对已经上线的 Streamlit 家庭 GPT 网站的**原地升级**。无需重新购买 ChatGPT 订阅或新建 OpenAI API Key。

## 新功能

1. **记住这台设备 7 天**：家庭密码登录时勾选即可。Safari Cookie 只保存 HMAC 签名的限时凭证，不写入明文密码；有“退出登录并取消设备记忆”按钮。修改 Streamlit Secrets 中的 `FAMILY_PASSWORD` 或 `OPENAI_API_KEY`，原有 Cookie 会自动失效。此方式是普通家庭网站的轻量登录，不是正式多用户账号系统，也不能防御设备失窃或恶意脚本。Safari 私密浏览 / 禁用 Cookie / 清除网站数据时可能无法记住。
2. **文件上传前预览和检查**：支持 `pdf/docx/xlsx/txt/md/csv/json/png/jpg/jpeg`，最多 2 个文件，每个最大 8 MB，图片最大 4 MB。检查扩展名、文件签名（适用格式）、解析有效性、ZIP 内部展开上限；展示截取内容或图像、哈希指纹，需再次勾选确认后才把审查内容传给 OpenAI。**不是杀毒软件**；不支持提取扫描版 PDF 里的文字，建议转文字或拍照后上传。
3. **失败后手动重试**：请求超时、网络/API 故障时保留本次问题和已确认的附件内容，最多尝试 3 次。**不自动重发**，以降低重复提交风险。即使手动重试，服务端已处理但回复丢失的请求仍可能产生重复费用。
4. 保留 **文字聊天、语音输入、朗读 AI 回复、聊天记录 TXT/JSON 导出与恢复、手机屏幕适配**。

## 在 iPhone 上更新你的原网站

**先备份原来的 `app.py` 和 `requirements.txt`，不要删除仓库、不要修改 Secrets 的真实密钥。**

1. 在 iPhone 的“文件”App 中打开提供的 ZIP，找到 `app.py`、`requirements.txt`。
2. Safari 登录 GitHub，打开你的 `family-gpt` 仓库。
3. 在 `app.py` 右上角点铅笔 **Edit file**，删除旧代码，替换为新 `app.py` 的全部内容，点 **Commit changes** 保存到 `main`。（若 Safari 页面功能不全，选择“请求桌面网站”。）
4. 打开仓库根目录的 `requirements.txt`，同样点编辑，将内容完整替换为：

   ```txt
   streamlit>=1.54,<2
   openai>=2.0,<3
   pypdf>=5,<8
   python-docx>=1.1,<2
   openpyxl>=3.1,<4
   streamlit-cookies-controller>=0.0.3,<1
   ```

5. 打开 [Streamlit 部署管理](https://share.streamlit.io/)；应用通常自动拉取 GitHub 的更新并重新安装依赖。若没更新，在 **Manage app → Reboot** 重启，检查 **Logs**。
6. 打开你原来的网址 `https://family-gpt-01.streamlit.app/` 测试文字问答。**第一次登录先勾选「记住这台设备 7 天」**。关掉 Safari 再打开，检查是否自动登录（需要允许 Cookie）。
7. 测试文件：上传一个简单 `.txt` 文件，查看内容预览，勾选确认，再点「确认并发送审查」。失败时点击「手动重试」，不需要重新选文件。

### Secrets：保持原样

```toml
OPENAI_API_KEY = "你原有的真实 API Key"
FAMILY_PASSWORD = "你的家庭密码"
OPENAI_MODEL = "你当前已验证能用的模型名称"
```

可以选填：

```toml
TRANSCRIBE_MODEL = "gpt-4o-mini-transcribe"
TTS_MODEL = "gpt-4o-mini-tts"
```

**任何 Secrets 都不要放进 GitHub、聊天截图或聊天消息。**

## 隐私、安全、费用说明

- 文件在点击「确认并发送」前，只在 Streamlit 应用的会话中解析和预览；点击后，提取文字或图片会送往 OpenAI API。默认没有数据库长期保存上传的文件。不要上传不必要的身份证、合同、财务资料等敏感内容。
- TXT、Word、PDF、Excel 的提取会有截断上限，只能算内容审查辅助。**不能承诺病毒查杀、法律合规审核或文件绝对安全。**
- 7 天“记住设备”使用**可由浏览器 JavaScript 读取**的签名 Cookie，不保存明文密码、API Key，也不是 HttpOnly 的专业身份认证。只建议在家庭成员自己的受信任设备上勾选；若担心泄露，修改 `FAMILY_PASSWORD` 或使用侧边栏的“退出登录并取消设备记忆”。
- 聊天记录仅暂存于当前浏览器会话，不随记住登录而持久保存。要保存聊天，使用导出功能。
- 每次文字问答、文件审查、语音识别和朗读都可能产生 API 费用。**手动重试也可能重复计费**。会话计数是软限制，不代表整个网站的预算上限。
- 若 Streamlit 社区云组件加载失败，先检查 Logs，尤其是 `ModuleNotFoundError` 与新增的 Cookies Controller 依赖。

## 开发者自检

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

修改后的代码通过 Python 语法检查和本地纯函数测试；由于没有用户 API 密钥或在线 Streamlit 浏览器环境，实际云端部署、Cookie 保留与 API 请求仍需要按上文测试。
