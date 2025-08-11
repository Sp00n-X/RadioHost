#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
屏幕工具类 - 提供清屏和格式化输出功能
"""

import os
import sys
import time
from typing import Optional

class ScreenManager:
    """屏幕管理器 - 处理清屏和格式化输出"""
    
    @staticmethod
    def clear():
        """清屏 - 跨平台支持"""
        # Windows
        if os.name == 'nt':
            os.system('cls')
        # macOS 和 Linux
        else:
            os.system('clear')
    
    @staticmethod
    def clear_with_delay(delay: float = 0.5):
        """延迟清屏"""
        time.sleep(delay)
        ScreenManager.clear()
    
    @staticmethod
    def print_separator(char: str = '=', length: int = 50, color: str = None):
        """打印分隔线"""
        separator = char * length
        if color:
            colors = {
                'red': '\033[91m',
                'green': '\033[92m',
                'yellow': '\033[93m',
                'blue': '\033[94m',
                'purple': '\033[95m',
                'cyan': '\033[96m',
                'white': '\033[97m',
                'gray': '\033[90m'
            }
            if color in colors:
                separator = f"{colors[color]}{separator}\033[0m"
        print(separator)
    
    @staticmethod
    def print_header(title: str, subtitle: Optional[str] = None):
        """打印标题头"""
        ScreenManager.clear()
        ScreenManager.print_separator('=', 60, 'cyan')
        print(f"\033[96m{title.center(60)}\033[0m")
        if subtitle:
            print(f"\033[90m{subtitle.center(60)}\033[0m")
        ScreenManager.print_separator('=', 60, 'cyan')
        print()
    
    @staticmethod
    def print_section(title: str, color: str = 'yellow'):
        """打印章节标题"""
        colors = {
            'red': '\033[91m',
            'green': '\033[92m',
            'yellow': '\033[93m',
            'blue': '\033[94m',
            'purple': '\033[95m',
            'cyan': '\033[96m',
            'white': '\033[97m',
            'gray': '\033[90m'
        }
        color_code = colors.get(color, '\033[97m')
        print(f"\n{color_code}=== {title} ===\033[0m\n")
    
    @staticmethod
    def wait_for_continue(message: str = "按回车键继续...", color: str = 'gray'):
        """等待用户继续"""
        colors = {
            'red': '\033[91m',
            'green': '\033[92m',
            'yellow': '\033[93m',
            'blue': '\033[94m',
            'purple': '\033[95m',
            'cyan': '\033[96m',
            'white': '\033[97m',
            'gray': '\033[90m'
        }
        color_code = colors.get(color, '\033[90m')
        input(f"\n{color_code}{message}\033[0m")
    
    @staticmethod
    def print_choice_prompt():
        """打印选择提示"""
        print(f"\n\033[93m请选择：\033[0m")
    
    @staticmethod
    def print_choice_list(choices: list, start_index: int = 1):
        """打印选择列表"""
        for idx, choice in enumerate(choices, start_index):
            print(f"  \033[97m{idx}. {choice}\033[0m")
    
    @staticmethod
    def print_status_line(text: str, color: str = 'white'):
        """打印状态行"""
        colors = {
            'red': '\033[91m',
            'green': '\033[92m',
            'yellow': '\033[93m',
            'blue': '\033[94m',
            'purple': '\033[95m',
            'cyan': '\033[96m',
            'white': '\033[97m',
            'gray': '\033[90m'
        }
        color_code = colors.get(color, '\033[97m')
        print(f"\n{color_code}{text}\033[0m")
    
    @staticmethod
    def format_story_text(text: str, indent: int = 2) -> str:
        """格式化故事文本"""
        lines = text.split('\n')
        formatted_lines = []
        for line in lines:
            if line.strip():
                formatted_lines.append(' ' * indent + line.strip())
            else:
                formatted_lines.append('')
        return '\n'.join(formatted_lines)
