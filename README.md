# 家庭 GPT 4.1 · Midnight UI（iPhone 修复版）

这版在 4.0 的功能上修复「打开折叠菜单后背景过亮、文字难辨认」的问题，并尽量隐藏 Streamlit Community Cloud 的外部徽标/图标。

## 本次修复

1. **主题级修复**：新增 `.streamlit/config.toml`，固定深色背景/文字/侧栏配色，避免由 iPhone 系统主题或 Streamlit 自动选择导致的反差问题。
2. **弹层级修复**：`app.py` 增加针对 `st.expander`、`st.popover`、selectbox 的新旧 DOM 结构、独立渲染的下拉选项层的高对比 CSS。
3. **视觉重新整理**：深海军蓝背景、松石绿强调色、清晰的对话卡片与输入栏，手机的附件/录音按钮继续在输入框右边。
4. **平台图标处理**：增加 GitHub 图标、Viewer Badge、社区部署按钮、状态角标等 CSS 选择器，并将工具栏模式设为 `minimal`。**Streamlit Community Cloud 有些图标属于平台宿主页面，应用内 CSS 不保证能移除**，尤其是管理员登录后出现的 `Manage app` 图标。家人以非管理员身份访问时通常看不到该控制。
5. **保留原功能**：家庭密码、7 天记住登录、管理员 API 设置、自选模型、语音与附件审查、人工重试、备份恢复都保持不变。

## 必须更新的文件（共三个）

- `app.py` — 替换旧版
- `requirements.txt` — 保持新版依赖完整
- `.streamlit/config.toml` — **新增**，必须放在这个隐藏文件夹中。没有此文件，可能仍出现颜色冲突。

## 只用 iPhone 更新 GitHub

1. 把正在正常工作的 `main` 分支 Commit 号保存下来，以备回退。
2. Safari 打开你的 GitHub 仓库，修改 `app.py` 为此包的新版本，上传/更新 `requirements.txt`。
3. 在仓库根目录选择 `Add file` → `Create new file`。文件名填 `.streamlit/config.toml`（在 GitHub 中输入斜杠会自动建立目录）。复制本包中 `config.toml` 的全部内容粘贴进去并 `Commit changes` 至 `main`。
4. 等待 Streamlit 根据 GitHub 提交自动更新。主题配置可能需要从 Streamlit 控制台 `Manage app` → `Reboot` 生效；必要时在 iPhone Safari 重新载入页面。
5. 打开你的原网址 `https://family-gpt-01.streamlit.app/`，测试设置侧栏中的“模型选择”展开列表、语音/附件弹窗、聊天输入框右边按钮。

你的 `Secrets` 中原有 `OPENAI_API_KEY`、`FAMILY_PASSWORD`、`OPENAI_MODEL`、`ADMIN_PASSWORD` **都保留，不用改**。

## 关于那两个 Community Cloud 图标

此包隐藏应用内部能定位到的常见图标和徽标，但管理员工具/Community Cloud 平台在应用外层注入的控件可能不受普通 Streamlit 网页样式控制，因此不能承诺 100% 移除。如果你更新后依旧看到两个图标，请截一张**仅显示图标位置**的屏幕图，我会区分可通过样式处理的元素和平台强制显示的元素。

## 注意

- CSS 对部分 Streamlit 内部 `data-testid` 和类名有依赖，平台升级后可能发生改变。
- 上传文件检查是格式和大小检查，非恶意软件扫描。API 调用会产生费用。
- 本包只完成本地语法、配置和结构检测；需要在你的 iPhone + Streamlit Community Cloud 环境最终确认视觉效果。
