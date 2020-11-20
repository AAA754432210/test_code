# -*- coding: utf-8 -*-
"""
@Project : test_code
@File    : test.py
@Author  : 王白熊
@Data    ： 2020/11/18 16:17
PointDEM()
PointNormal()
PointSurfel()
PointUV()
PointWithRange()
PointWithScale()
PointWithViewpoint()
PointXY()
PointXYZ()
PointXYZHSV()
PointXYZI()
PointXYZINormal()
PointXYZL()
PointXYZLNormal()
PointXYZRGB()
PointXYZRGBA()
PointXYZRGBL()
PointXYZRGBNormal()
"""

import pclpy
from pclpy import pcl

from pyntcloud import PyntCloud
import open3d as o3d

obj=pclpy.pcl.PointCloud.PointXYZI()
pcl.io.loadPCDFile(r'D:\data\biaoding\origin.pcd', obj)
# pcl.io.savePCDFileASCII()

viewer = pcl.visualization.PCLVisualizer('Point Cloud viewer')
viewer.addPointCloud(obj)
while not viewer.wasStopped():
    viewer.spinOnce(100)