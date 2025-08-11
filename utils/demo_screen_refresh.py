#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
屏幕刷新功能演示
展示如何在命令行中实现清晰的界面切换
"""

import time
from game_engine.screen_utils import ScreenManager

def demo_screen_refresh():
    """演示屏幕刷新功能"""
    
    # 演示1: 开场清屏
    ScreenManager.print_header("崖边电台主持人 - 屏幕刷新演示", "命运的频率")
    print("正在加载故事内容...")
    time.sleep(2)
    
    # 演示2: 章节切换
    ScreenManager.print_section("第一章：命运的起点", 'cyan')
    print("  你坐在无线电前，手指轻轻转动着调频旋钮。")
    print("  窗外的雨声与静电噪音交织在一起。")
    print("  突然，一个微弱的声音从扬声器中传来...")
    ScreenManager.wait_for_continue()
    
    # 演示3: 选择界面
    ScreenManager.clear()
    ScreenManager.print_section("选择你的行动", 'yellow')
    choices = [
        "仔细聆听那个微弱的声音",
        "调整频率寻找更清晰的信号",
        "记录下这个奇怪的现象",
        "忽略它，继续日常的工作"
    ]
    ScreenManager.print_choice_list(choices)
    
    # 演示4: 结果展示
    time.sleep(3)
    ScreenManager.clear_with_delay(0.5)
    ScreenManager.print_section("信号分析结果", 'green')
    print("  频率：14250 kHz")
    print("  信号强度：微弱但稳定")
    print("  内容特征：似乎来自另一个时空")
    print("  建议：继续监听，记录所有细节")
    
    ScreenManager.wait_for_continue("演示结束，按回车键退出...")

if __name__ == "__main__":
    demo_screen_refresh()
