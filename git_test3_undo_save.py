import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from functools import partial
from matplotlib.patches import Circle
from matplotlib.widgets import Button
# 如果需要在jupyter notebook中实现交互式作图，可以考虑使用以下命令切换交互式后端
# %matplotlib notebook
# 如果使用的是较新版本的 Jupyter 和 Matplotlib，可以尝试 %matplotlib widget


# 加载数据
spatial1 = np.array(pd.read_csv('data_test/spatial1.csv', header=None))  # ndarray:(46026,2)
spatial2 = np.array(pd.read_csv('data_test/spatial2.csv', header=None))
landmark1 = np.array(pd.read_csv('data_test/landmark1.csv', header=None))  # ndarray:(50,2)
landmark2 = np.array(pd.read_csv('data_test/landmark2.csv', header=None))

# 用于存储高亮对象的列表
highlights = []
highlight_history = []  # 历史记录列表

# 定义pick回调函数
def on_pick(event, lm1, lm2, spatial1, spatial2):
    global highlights, highlight_history
    
    if event.artist in (scatter2, scatter4):
        xdata, ydata = event.artist.get_offsets().T
        indices = event.ind
        print("Selected indices:", indices)

        ax1 = fig.axes[0]
        for index in indices:
            circle = Circle((lm1[index, 0], lm1[index, 1]), 120, color='black', fill=False, lw=3)
            ax1.add_patch(circle)
            highlights.append(circle)
            highlight_history.append(circle)  # 记录高亮对象

        ax2 = fig.axes[1]
        for index in indices:
            circle = Circle((lm2[index, 0], lm2[index, 1]), 120, color='black', fill=False, lw=3)
            ax2.add_patch(circle)
            highlights.append(circle)
            highlight_history.append(circle)

        fig.canvas.draw_idle()

        if event.artist == scatter2:
            for index in indices:
                error = 1e-6
                matches = (np.abs(lm1[:, 0] - xdata[index]) < error) & (np.abs(lm1[:, 1] - ydata[index]) < error)
                target_indices = np.where(matches)[0]
                print(f"找到lm1坐标 ({xdata[index]}, {ydata[index]}) 在索引位置: {target_indices}")
                print(f"对应lm2坐标({lm2[index, 0]}, {lm2[index, 1]})")
        elif event.artist == scatter4:
            for index in indices:
                error = 1e-6
                matches = (np.abs(lm2[:, 0] - xdata[index]) < error) & (np.abs(lm2[:, 1] - ydata[index]) < error)
                target_indices = np.where(matches)[0]
                print(f"找到lm2坐标 ({xdata[index]}, {ydata[index]}) 在索引位置: {target_indices}")
                print(f"对应lm1坐标({lm1[index, 0]}, {lm1[index, 1]})")

# 定义清除高亮的函数
def clear_highlights(event):
    global highlights
    for highlight in highlights:
        highlight.remove()
    highlights.clear()
    fig.canvas.draw_idle()
    print("------------已清除全部高亮------------")

# 定义撤销高亮的函数
def undo_highlight(event):
    global highlights, highlight_history
    if highlight_history:
        last_highlight1 = highlight_history.pop()
        last_highlight1.remove()
        last_highlight2 = highlight_history.pop()
        last_highlight2.remove()
        highlights.remove(last_highlight1)
        highlights.remove(last_highlight2)  # 撤销最后两个高亮
        fig.canvas.draw_idle()
        print("------------已撤销最后两个高亮------------")
    else:
        print("------------无可撤销的高亮------------")

# 定义保存当前高亮图片的函数
def save_figure(event):
    plt.savefig('highlighted_figure.png')
    print("------------已保存当前图片------------")
    print(highlights)

# 构建画布
fig, (ax1, ax2) = plt.subplots(1, 2, dpi=150, figsize=(15, 8))

# 左图
scatter1 = ax1.scatter(spatial1[:, 0], spatial1[:, 1], s=1)
scatter2 = ax1.scatter(landmark1[:, 0], landmark1[:, 1], s=30, c="red", picker=True, pickradius=5)
ax1.invert_yaxis()
ax1.invert_xaxis()
for i in range(landmark1.shape[0]):
    ax1.text(landmark1[i, 0], landmark1[i, 1], f'{i}', c='red')
ax1.set_title('slice1', fontsize=20)

# 右图
scatter3 = ax2.scatter(spatial2[:, 0], spatial2[:, 1], s=1)
scatter4 = ax2.scatter(landmark2[:, 0], landmark2[:, 1], s=30, c="red", picker=True, pickradius=5)
ax2.invert_yaxis()
ax2.invert_xaxis()
for i in range(landmark2.shape[0]):
    ax2.text(landmark2[i, 0], landmark2[i, 1], f'{i}', c='red')
ax2.set_title('slice2', fontsize=20)

# 连接pick事件到回调函数
on_pick_with_lm = partial(on_pick, lm1=landmark1, lm2=landmark2, spatial1=spatial1, spatial2=spatial2)
pick_id = fig.canvas.mpl_connect('pick_event', on_pick_with_lm)

# 添加清除高亮的按钮
clear_button_ax = plt.axes([0.9, 0.15, 0.1, 0.05]) 
clear_button = Button(clear_button_ax, 'Clear Highlights', hovercolor='0.9')
clear_button.label.set_fontsize(7)
clear_button.on_clicked(clear_highlights)

# 添加撤销按钮
undo_button_ax = plt.axes([0.9, 0.2, 0.1, 0.05])
undo_button = Button(undo_button_ax, 'Undo Highlights', hovercolor='0.9')
undo_button.label.set_fontsize(7)
undo_button.on_clicked(undo_highlight)

# 添加保存按钮
save_button_ax = plt.axes([0.9, 0.25, 0.1, 0.05])
save_button = Button(save_button_ax, 'Save Figure', hovercolor='0.9')
save_button.label.set_fontsize(8)
save_button.on_clicked(save_figure)

# 显示图片
plt.show()