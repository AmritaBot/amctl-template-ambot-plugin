# amctl-template-ambot-plugin

`amctl` 模板：生成一个带 WebUI 页面、前端构建链和发布流程的 AmritaBot 插件工程。

## 安装与使用

```bash
uv tool install amctl --with amctl-template-ambot-plugin

amctl create -t ambot_plugin -n my-plugin
cd my-plugin
uv sync
cd frontend && bun install && bun run build && cd ..
uv run amrita run
```

生成后：WebUI 侧边栏出现「my-plugin」页面，页面数据走 `/api/my-plugin/items`，
前端产物在插件包内，随 wheel 分发——部署机不需要 Node。

## 生成什么

```
my-plugin/
├── pyproject.toml          # 依赖 amrita>=1.18.0，package-data 带上产物
├── amrita_plugin_my_plugin/
│   ├── __init__.py         # PluginMetadata，import 即注册
│   ├── config.py           # page_title / page_category
│   ├── api.py              # /api/my-plugin/items 的 GET 与 POST
│   ├── webui.py            # mount_plugin_assets + register_page(module_dir=...)
│   └── assets/             # 构建产物，构建前不存在
├── frontend/
│   ├── amrita-plugin.json  # 入口、产物目录、静态资源
│   ├── package.json        # 依赖 @amrita-constant/webui-plugin-kit
│   └── src/index.tsx       # 示例页面（Card / Input / Button / Badge）
└── .github/workflows/      # CI 检查
```

项目名会被规整成三种形态：发行名 `amrita-plugin-my-plugin`、导入名
`amrita_plugin_my_plugin`、挂载名 `my_plugin`（同时是 `/plugin-assets/<name>/`
与页面路径 `/my_plugin`）。

## 依赖的两个约定

- **宿主契约版本 3**：插件产物末尾带 `export const amritaHostContract = 3`，
  宿主加载时比对；React 等运行时依赖通过 `window.__AMRITA_HOST__` 注入，
  插件不打包第二份。
- **产物挂载**：`mount_plugin_assets("my_plugin", assets/)` 必须在插件 import 期调用，
  晚于 `driver.on_startup` 的 catch-all 路由就收不到请求；产物缺失时只告警，
  页面显示「产物不可用」而不阻断插件加载。

构建器来自 [`@amrita-constant/webui-plugin-kit`](https://github.com/AmritaBot/AmritaBot-PluginKit)，
UI 组件与类型来自 `@amrita-constant/ambot-ui`。

## 开发这个模板

模板本体是 `amctl.templ` 命名空间包，文件后缀决定处理方式：

| 后缀 | 行为 |
|---|---|
| `.tmpl` | Jinja2 渲染，输出时去掉后缀 |
| `.pre` | 原样复制，输出时去掉后缀（用于含 `${{ }}` 的 GitHub Actions 文件） |
| 其他 | 原样复制 |

目录名 `{{ module }}` 也会被渲染。改完本地验证：

```bash
uv build
uv pip install --force-reinstall dist/*.whl   # 装进有 amctl 的环境
amctl create -t ambot_plugin -n demo-panel --frozen -o /tmp/gen
cd /tmp/gen/demo-panel/frontend && bun install && bun run typecheck && bun run build
```
