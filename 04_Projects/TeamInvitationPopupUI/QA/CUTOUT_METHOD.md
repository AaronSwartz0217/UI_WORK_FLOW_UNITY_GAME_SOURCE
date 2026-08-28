# Cutout Method

- 来源：Review06 实测像素边界与线框层级。
- 清底：父级内部整体采用同源大面积皮革纹理自适应填充，避免重复拼接线。
- Alpha：倒角多边形真透明遮罩，四角 Alpha 0。
- 子件：Header、List、Row 分层，父级不包含子级。
- 四态：Accept / Reject 由同一轮廓生成；Close 精确复用 Cook 标准四态。
- 100%：PASS。
- 400%：PASS。
- 棋盘格：PASS。
- 原位回拼：PASS。
- Result：PASS。
