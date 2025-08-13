#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Radio项目启动脚本
用于验证重构后的项目结构
"""

import sys
import os

def main():
    """主函数"""
    print("=" * 50)
    print("Radio项目重构验证")
    print("=" * 50)
    
    try:
        # 测试故事系统
        from story_system import StoryProgress, StoryContent, CharacterManager
        print("✅ 故事系统模块导入成功")
        
        
        # 测试工具模块
        from utils import demo_screen_refresh
        print("✅ 工具模块导入成功")
        
        print("\n" + "=" * 50)
        print("项目结构验证完成！")
        print("=" * 50)
        
        print("\n📁 当前项目结构：")
        os.system("tree -I '__pycache__|*.pyc'")
        
        print("\n🎮 运行方式：")
        print("  基础版本: python game_engine/radio_game.py")
        print("  集成版本: python game_engine/radio_game_integrated.py")
        
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
