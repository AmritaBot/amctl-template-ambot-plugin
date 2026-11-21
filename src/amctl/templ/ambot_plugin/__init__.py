"""AmritaBot 插件模板（含 WebUI 页面与前端构建链）。"""

from __future__ import annotations

import re
from typing import Any, ClassVar

from amctl.templating import BaseTemplate, TmplField, field

__template_ignore__ = False


def _slug(name: str) -> str:
    """把项目名规整成可用的包名后缀：只留字母数字，其余折成下划线。"""
    cleaned = re.sub(r"[^0-9A-Za-z]+", "_", name).strip("_").lower()
    return cleaned or "demo"


class ambotPluginTemplate(BaseTemplate):
    """生成可直接 `uv sync` 的 AmritaBot 插件工程。

    Python 侧提供带 WebUI 页面的插件骨架（路由 + 侧边栏页面 + 产物挂载），
    frontend/ 提供 React 页面与构建脚本，产物落在插件包内随包分发。
    """

    __template_name__: str = "ambot_plugin"
    __template_description__ = "AmritaBot 插件工程：WebUI 页面 + 前端构建 + 打包发布"
    # 依赖的 AmritaBot 需要自带插件产物挂载能力（mount_plugin_assets / module_dir）
    __versions__: tuple[str, ...] = ("1.18.0",)
    __tmpl_fields__: ClassVar[dict[str, TmplField]] = {
        "description": field(
            default="我的第一个 AmritaBot 插件",
            description="插件简介，写入 pyproject 与 README",
        ),
    }

    def _build_context(
        self, name: str, version: str | None, **fields: Any
    ) -> dict[str, Any]:
        ctx = super()._build_context(name, version, **fields)
        slug = _slug(name)
        ctx.update(
            {
                # 发行名用连字符，导入名用下划线，两者都由项目名派生
                "dist": f"amrita-plugin-{slug.replace('_', '-')}",
                "module": f"amrita_plugin_{slug}",
                # 同时是 /plugin-assets/<name>/ 的挂载名与页面路径
                "asset": slug,
                "page_title": name,
            }
        )
        return ctx


__template_export__ = ambotPluginTemplate
