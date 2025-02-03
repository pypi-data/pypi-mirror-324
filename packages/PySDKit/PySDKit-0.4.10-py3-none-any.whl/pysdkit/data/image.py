# -*- coding: utf-8 -*-
"""
Created on 2025/02/02 13:01:46
@author: Whenxuan Wang
@email: wwhenxuan@gmail.com
生成用于测试二维图像数据的样例
"""
import numpy as np
from os import path


def test_grayscale() -> np.ndarray:
    """
    加载用于测试的二维灰度图像样例
    This data comes from https://www.mathworks.com/matlabcentral/fileexchange/45918-two-dimensional-variational-mode-decomposition
    Konstantin, Dragomiretskiy, and Dominique Zosso. "Two-dimensional variational mode decomposition."
    Energy Minimization Methods in Computer Vision and Pattern Recognition. Vol. 8932. 2015.
    """
    # 获取当前数据的路径
    current_file_path = path.dirname(path.abspath(__file__))
    data_path = path.join(current_file_path, "texture.txt")
    # 读取数据并返回文件
    return np.loadtxt(data_path)
