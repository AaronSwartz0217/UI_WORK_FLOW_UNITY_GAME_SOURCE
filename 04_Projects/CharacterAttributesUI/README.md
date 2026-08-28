# 属性界面 / CharacterAttributesUI

项目状态：19 个 V03 精切组件已进入正式目录，自动校验通过，等待最终目视确认。

## 输入与风格

- 白膜：`in/CharacterAttributesUI_Wireframe_815x1110.jpeg`
- 主风格：`in/StylePrimary_Cook/`
- 次风格：`in/StyleSecondary_EquipmentIdentification/`
- 风格冲突时以 Cook 为准；参考图不修改。
- 普通文字和动态数字全部移除，仅保留关闭 `X` 等功能符号。

## 采用的完整界面

- `FullUI/CharacterAttributesUI_FullUI_Review02_1024x1536.png`
- 画布：`1024x1536`
- 主面板可见范围：`x=30, y=97, width=964, height=1366`
- 全程保持 `ScaleX == ScaleY`，未进行单轴拉伸。

## 正式产物

- 目录：`Components/out/CharacterAttributesUI/`
- 数量：19 PNG
- 页签：两套独立四状态按钮，共 8 PNG。
- 关闭按钮：Cook 标准四状态原件逐像素复制，仅重命名前缀，共 4 PNG。
- 进度轨道/填充：4 PNG。
- 主面板、短属性条、长属性条：3 PNG。

## 精切说明

V03 使用人工核对的源图边界与超采样倒角 Alpha。每个组件的裁框止于自身最外缘，不再带入父面板纹理。父面板的子元素区域由同一完整界面的空白纹理按原像素密度镜像铺设并羽化衔接。

## QA

- 项目验证器：PASS
- 真透明与低 Alpha 残留检查：PASS
- 四状态画布/Alpha 轮廓一致：PASS
- 100% 回装、棋盘格、400% 边缘检查：PASS
- 最终预览：`into/ReassemblyPreview/CharacterAttributes_PrecisionV03_Reassembled_Checkerboard.png`
