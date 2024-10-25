import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from functools import partial
from matplotlib.patches import Circle
from matplotlib.widgets import Button
# 如果需要在jupyter notebook中实现交互式作图，可以考虑使用以下命令切换交互式后端
# %matplotlib notebook
# 如果使用的是较新版本的 Jupyter 和 Matplotlib，可以尝试 %matplotlib widget

# 数据导入
spatial1 = np.array(pd.read_csv('data_test\spatial1.csv', header=None))  # ndarray:(46026,2)
spatial2 = np.array(pd.read_csv('data_test\spatial2.csv', header=None))
landmark1 = np.array(pd.read_csv('data_test\landmark1.csv', header=None))  # ndarray:(50,2)
landmark2 = np.array(pd.read_csv('data_test\landmark2.csv', header=None))


# 用于存储高亮对象的列表
highlights = []

# 定义pick回调函数
def on_pick(event, lm1, lm2, spatial1, spatial2):
    global highlights  # 使用全局变量来存储高亮对象

    # 获取被选中的artist对象，检查是否是第二组散点图
    if event.artist in (scatter2, scatter4):
        # 获取坐标原始数据
        xdata, ydata = event.artist.get_offsets().T  # ndarray(50,)
        # 获取被选中的所有点的索引
        indices = event.ind
        print("Selected indices:", indices)

        # 在左侧图像中高亮选中的点或对应的点
        ax1 = fig.axes[0]
        for index in indices:
            circle = Circle((lm1[index, 0], lm1[index, 1]), 120, color='black', fill=False, lw=3)
            ax1.add_patch(circle)
            highlights.append(circle)  # 保存高亮对象

        # 在右侧图像中高亮选中的点或对应的点
        ax2 = fig.axes[1]
        for index in indices:
            circle = Circle((lm2[index, 0], lm2[index, 1]), 120, color='black', fill=False, lw=3)
            ax2.add_patch(circle)
            highlights.append(circle)  # 保存高亮对象

        # 更新图表以显示高亮
        fig.canvas.draw_idle()

        # 打印出所有被选中的点及其对应点坐标，便于查找
        if event.artist == scatter2:
            for index in indices:
                # 设置容差
                error = 1e-6
                # 查找匹配的坐标，获取索引
                matches = (np.abs(lm1[:, 0] - xdata[index]) < error) & (np.abs(lm1[:, 1] - ydata[index]) < error)
                target_indices = np.where(matches)[0]
                # 打印结果
                print(f"找到lm1坐标 ({xdata[index]}, {ydata[index]}) 在索引位置: {target_indices}")
                print(f"对应lm2坐标({lm2[index, 0]}, {lm2[index, 1]})")

        elif event.artist == scatter4:
            for index in indices:
                # 设置容差
                error = 1e-6
                # 查找匹配的坐标，获取索引
                matches = (np.abs(lm2[:, 0] - xdata[index]) < error) & (np.abs(lm2[:, 1] - ydata[index]) < error)
                target_indices = np.where(matches)[0]
                # 打印结果
                print(f"找到lm2坐标 ({xdata[index]}, {ydata[index]}) 在索引位置: {target_indices}")
                print(f"对应lm1坐标({lm1[index, 0]}, {lm1[index, 1]})")


# 定义清除高亮的函数
def clear_highlights(event):
    global highlights
    for highlight in highlights:
        highlight.remove()
    highlights.clear()
    fig.canvas.draw_idle()
    print("------------已清除高亮landmark------------")


# 构建画布
fig, (ax1, ax2) = plt.subplots(1, 2, dpi=150, figsize=(15, 8))  # 图片总像素：2250*1200
# 左图
scatter1 = ax1.scatter(spatial1[:, 0], spatial1[:, 1], s=1)
scatter2 = ax1.scatter(landmark1[:, 0], landmark1[:, 1], s=30, c="red", picker=True, pickradius=10)  # 阈值可调整
ax1.invert_yaxis()
ax1.invert_xaxis()
for i in range(landmark1.shape[0]):
    ax1.text(landmark1[i, 0], landmark1[i, 1], f'{i}', c='red')
ax1.set_title('slice1', fontsize=20)
# 右图
scatter3 = ax2.scatter(spatial2[:, 0], spatial2[:, 1], s=1)
scatter4 = ax2.scatter(landmark2[:, 0], landmark2[:, 1], s=30, c="red", picker=True, pickradius=10)
ax2.invert_yaxis()
ax2.invert_xaxis()
for i in range(landmark2.shape[0]):
    ax2.text(landmark2[i, 0], landmark2[i, 1], f'{i}', c='red')
ax2.set_title('slice2', fontsize=20)

# 连接pick事件到回调函数
on_pick_with_lm = partial(on_pick, lm1=landmark1, lm2=landmark2, spatial1=spatial1, spatial2=spatial2)
pick_id = fig.canvas.mpl_connect('pick_event', on_pick_with_lm)

# 添加清除高亮的按钮
clear_button_ax = plt.axes((0.9, 0.05, 0.1, 0.06))  # proportion of [left, bottom, width, height]
clear_button = Button(clear_button_ax, 'Clear Highlights', hovercolor='0.9')  # 浅灰色：1白0黑
clear_button.on_clicked(clear_highlights)

# 显示图片
plt.show()