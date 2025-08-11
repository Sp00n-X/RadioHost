#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试input_manager集成效果
"""

import sys
import os
import time
import threading

# 添加路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'game_engine'))

from game_engine.input_manager import InputBlocker, input_manager
from game_engine.radio_game import TypewriterEffect, SignalEffect

def test_typewriter_with_input_blocking():
    """测试打字机效果时的输入阻止"""
    print("=== 测试打字机效果时的输入阻止 ===")
    print("在下面的测试中，尝试在文字输出时按键盘")
    print("你应该无法输入任何字符，直到输出完成")
    print()
    
    # 测试打字机效果
    TypewriterEffect.type_out("这是一个测试消息，打字机效果会逐字输出...", 0.1, 'green')
    
    print("\n✅ 打字机效果测试完成")
    
def test_signal_effect_with_input_blocking():
    """测试信号效果时的输入阻止"""
    print("\n=== 测试信号效果时的输入阻止 ===")
    print("在下面的测试中，尝试在信号效果时按键盘")
    print("你应该无法输入任何字符，直到效果完成")
    print()
    
    # 测试信号效果
    SignalEffect.simulate_static(2.0)
    
    print("✅ 信号效果测试完成")

def test_normal_input():
    """测试正常输入功能"""
    print("\n=== 测试正常输入功能 ===")
    print("现在应该可以正常输入了")
    
    try:
        user_input = input("请输入一些文字测试：")
        print(f"你输入了：{user_input}")
    except KeyboardInterrupt:
        print("\n用户中断输入")
    
    print("✅ 正常输入测试完成")

def test_context_manager():
    """测试上下文管理器"""
    print("\n=== 测试上下文管理器 ===")
    print("使用with语句测试输入阻止")
    
    with InputBlocker(flush=True):
        print("输入已被阻止，3秒内按键盘不会有反应...")
        time.sleep(3)
        print("上下文结束，输入恢复")
    
    print("✅ 上下文管理器测试完成")

def main():
    """主测试函数"""
    print("🎮 开始测试input_manager集成效果")
    print("=" * 50)
    
    try:
        test_typewriter_with_input_blocking()
        test_signal_effect_with_input_blocking()
        test_context_manager()
        test_normal_input()
        
        print("\n" + "=" * 50)
        print("🎉 所有测试完成！")
        print("input_manager已成功集成到游戏中")
        
    except KeyboardInterrupt:
        print("\n\n测试被用户中断")
    except Exception as e:
        print(f"\n\n测试出错：{e}")

if __name__ == "__main__":
    main()
