# Cutout Method

- Target Region source：Review02 的实测像素边界与线框层级。
- Isolation method：按父子层级裁切；父板用同源无缝金属/皮革纹理清除子件区域。
- Alpha method：倒角多边形遮罩，画布外为真实 Alpha 0。
- Low-alpha cleanup：生成组件清理 1–5 的杂散 Alpha；复用问号按钮保留其已确认的标准抗锯齿轮廓。
- State Union Bounds：每套按钮四态使用统一画布、尺寸和 Alpha 遮罩。
- 100% check：PASS。
- 400% check：属性行、装备槽、材料卡、附魔按钮均 PASS。
- Checkerboard check：PASS。
- Reassembly check：PASS。
- Result：PASS。
