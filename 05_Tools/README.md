# Tools

`Common/` 存放可跨项目复用的验证、棋盘格、回拼、命名和清单工具。

`ProjectScripts/ProjectId/` 只存放项目特有坐标、目标范围、层级和组件清单。

禁止在项目脚本中重复复制整套通用 QA 逻辑。

## Crop repair tools

- `inspect_crop_repairs.py` creates enlarged source-bound diagnostics without changing formal assets.
- `repair_reported_component_crops_v01.py` rebuilds the reported slot/button crops, validates RGBA/alpha/state parity, and only replaces formal plus desktop delivery files when run with `--promote`.
- `crop_repair_v01_report.json` records the source bounds, replacement mapping, validation result, and promoted hashes for the latest repair.
