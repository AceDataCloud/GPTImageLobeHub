# LobeHub：GPT Image（Ace Data Cloud 提供）

[English](README.md) · [官方搜索入口（独立条目待发布）](https://lobehub.com/mcp?q=GPT%20Image) · [当前 API/价格](https://platform.acedata.cloud/documents/openai-images-generations?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=gpt-image_lobehub_readme_pricing)

这是 **Ace Data Cloud 提供的 GPT Image 集成**，不是模型原厂官方插件。复用现有 [OpenAIMCP](https://github.com/AceDataCloud/OpenAIMCP) 和 `mcp-openai-pro`，不新建重复后台。这是新的纯 GPT Image STDIO 适配层，2026-10-18 尚未发布 PyPI 或 LobeHub，计划 identifier 为 `acedatacloud-gptimagelobehub`。底层现有 OpenAIMCP 同时含聊天/嵌入，此层只开放图片生成、编辑、同 ID 任务查询和 schema 派生的模型说明，真正提供独立分发价值。

## 正式版本安装与发布

PyPI 项目创建受现有发布者配额限制时，使用不可变的 [GitHub v0.1.1 正式产物](https://github.com/AceDataCloud/GPTImageLobeHub/releases/tag/v0.1.1)。先核对资产和 SHA256SUMS；[install-stdio.json](install-stdio.json) 使用 uvx 和精确版本 wheel URL。PyPI、GitHub Release 与 LobeHub 收录分别验证，当前独立市场条目仍待发布。

维护者：v 版本 tag 触发测试、build、twine 校验并上传 wheel/sdist/SHA256SUMS。Release workflow 的 PyPI 发布单独显式 dispatch，使用既有组织 publisher；配额用尽时不重试或换身份绕过。

## 1. 安装

![LobeHub 官方 MCP 市场真实历史截图](https://lobehub.com/img/hub/blog/assetsb811f2aae8e8346aef16793d6bd10f88.webp)

原图来自 [2026-03-03 的官方文档源码](https://github.com/lobehub/lobehub/blob/43578a9bcc37dbf0ec9beb5f5ab1dcd5ba09daf7/docs/usage/community/mcp-market.mdx)，拍摄时间/产品版本未知；2026-10-18 引用核验。它只说明真实搜索框、分类与卡片位置，不是 Ace 已安装、当前排名或调用成功证据。

正式卡片未发布；上面的市场入口用于检查当前搜索结果，不能当作新卡片已安装。搜索 `GPT Image` 或 `Ace Data Cloud`；不保证排名。同名历史卡片以精确 identifier 区分，不另发重复项。

正式目录项尚未发布。开发者手动路径：安装本仓库 `pip install .`，然后在桌面端设置 → 连接器导入 [单项 STDIO 配置](install-stdio.json)。本适配层没有已部署的公共 HTTP 端点；不要将此路径当作市场普通安装已完成。

## 2. 登录并获取 Token

登录或注册 [Ace → Applications（我的应用）](https://platform.acedata.cloud/console/applications?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=gpt-image_lobehub_readme_api_key)。如果还没有 **General application（通用应用）**，先初始化，再打开应用；确认 GPT Image 服务权限、余额和当前价格。复制已有服务 API Token，或在 **Manage Keys** 创建专用于 LobeHub 的 Key。不要填平台管理 Token 或原厂 Key。

![复制 API Token，Ace 真实历史截图；2026-10-18 引用](https://raw.githubusercontent.com/AceDataCloud/SunoDify/8d3d03570e73324220f111f7fe343da0792a8071/_assets/tutorial/get-api-key-en.png)

![创建专用 Key，真实凭据已隐藏；历史截图](https://raw.githubusercontent.com/AceDataCloud/SunoDify/8d3d03570e73324220f111f7fe343da0792a8071/_assets/tutorial/create-api-key-en.png)

图来自上面固定 commit 的真实 Ace 页面，拍摄日期未断言；不是 LobeHub 安装或调用成功证据。

## 3. 在 LobeHub 填写与启用

在此 STDIO 连接器的环境变量 `ACEDATACLOUD_API_TOKEN` 中填 Token 字符串，不加 `Bearer `、引号或遮挡字符。保存并检查连接，再进入 **助理设置 → 连接器** 启用，生成/修改工具先设 Ask 或 Deny。真实界面步骤见 [LobeHub 官方指南](https://lobehub.com/docs/usage/community/mcp-market)。本生态的实际认证截图仍排队核验，不用假截图替代。

## 4. 首用与异步结果

只调用 `gpt_image_list_models`，参数为空；它返回内置信息，不发生成请求。 如果通过聊天模型要求助理调用，聊天模型仍可能计费；优先使用直接工具测试入口。

生成和编辑都必须显式选择 GPT Image 型号，不沿用底层 DALL-E 编辑默认值，也不自动换价。生成前选 schema 支持的型号并核价，只提交一次。保存任务 ID，用 `gpt_image_get_task` 查询同一个 ID，直到明确终态成功或失败。预览链接/等待状态不是完成，不重复提交生成；终态成功后打开最终媒体，保留任务与用量记录检查唯一账单。本次材料没有发收费生成。

## 常见问题

- 401/403：重新复制服务 Token，检查权限、有效期和余额；不要用平台管理凭据。
- 导入后未认证：填写 STDIO 环境变量 `ACEDATACLOUD_API_TOKEN`，重启连接器进程。
- 有连接没有工具：给当前助理启用，并检查工具权限和聊天模型工具能力。
- 本地启动：当前变量是 `ACEDATACLOUD_API_TOKEN`，不是旧 `ACEDATA_API_TOKEN`；此适配层没有公共 HTTP 部署。
- Pending：继续查同 ID，不因等待重发；429/500 保留真实错误，不自动换模型或价格。

发布者应使用已有身份完成 GitHub 归属核验，确认新的独立 `acedatacloud-gptimagelobehub` 尚未收录后再 publish。本仓提供与通用 OpenAIMCP 不同的图片专用工具面，不需要复制底层服务或创建新身份。当前未登录 publisher，不声称收录完成。归因使用后端认可的 opensource/referral/evergreen 四项标签，以 gpt-image_lobehub_* 区分入口。

**底层包必须用 `mcp-openai-pro`；`mcp-openai` 属于其他作者。适配层只开放 GPT Image 工具，不开放聊天、嵌入或其他图片品牌。**

本启动器直接执行固定共源 `mcp-openai-pro==2026.10.18.4 --profile gpt-image --transport stdio`；五工具为 `gpt_image_generate`、`gpt_image_edit`、`gpt_image_get_task`、`gpt_image_list_tasks`、`gpt_image_list_models`。模型策略、脱敏错误 metadata、任务格式全部来自共源，不复制实现、不加回退。开发：`pip install -e ".[test]"` 后 `python -m pytest`。
