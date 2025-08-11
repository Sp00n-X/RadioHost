#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
崖边电台主持人 - 集成故事系统的完整版本
基于模块化故事系统设计
"""

import sys
import time
import json
import random
import threading
from datetime import datetime
from typing import Optional, Dict, Any

# 导入故事系统
from story_system import StoryProgress, StoryContent, CharacterManager
from story_system.story_base import StoryState

class TypewriterEffect:
    """打字机效果输出"""
    
    @staticmethod
    def type_out(text: str, delay: float = 0.05, color: str = None):
        """逐字输出文字"""
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
        
        if color and color in colors:
            sys.stdout.write(colors[color])
        
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        
        if color:
            sys.stdout.write('\033[0m')
        
        sys.stdout.write('\n')
        sys.stdout.flush()

class SignalEffect:
    """信号干扰效果"""
    
    @staticmethod
    def add_noise(text: str, strength: float = 0.1) -> str:
        """添加信号干扰"""
        noise_chars = ['▒', '░', '▓', '█', '■', '□', '▪', '▫']
        result = ""
        
        for char in text:
            if random.random() < strength:
                if random.random() < 0.5:
                    result += random.choice(noise_chars)
                else:
                    result += ' '
            else:
                result += char
        
        return result
    
    @staticmethod
    def simulate_static(duration: float = 1.0):
        """模拟静电噪音"""
        static_chars = ['嘶——', '沙沙...', '...滋...', '[信号中断]', '[频道干扰]']
        TypewriterEffect.type_out(random.choice(static_chars), 0.1, 'gray')
        time.sleep(duration)

class RadioGameIntegrated:
    """集成故事系统的主游戏类"""
    
    def __init__(self):
        self.current_frequency = 14250
        self.game_time = 0
        self.game_active = True
        
        # 初始化故事系统
        self.story_progress = StoryProgress()
        self.story_content = StoryContent()
        self.character_manager = self.story_progress.character_manager
        
        # 游戏状态
        self.current_scene = None
        self.in_conversation = False
        self.current_character = None
        
    def intro(self):
        """游戏开场"""
        TypewriterEffect.type_out("=== 崖边电台主持人 ===", 0.1, 'cyan')
        time.sleep(1)
        
        # 使用故事系统的开场
        self.current_scene = self.story_content.get_scene("start")
        self.display_current_scene()
        
        time.sleep(2)
        SignalEffect.simulate_static(1.5)
    
    def display_current_scene(self):
        """显示当前场景内容"""
        if not self.current_scene:
            return
            
        # 显示标题
        if self.current_scene.title:
            TypewriterEffect.type_out(f"\n=== {self.current_scene.title} ===", 0.08, 'cyan')
        
        # 显示内容
        for line in self.current_scene.content:
            if line.strip():  # 跳过空行
                TypewriterEffect.type_out(line, 0.05, 'white')
            else:
                print()  # 空行
        
        # 显示选择
        if self.current_scene.choices:
            TypewriterEffect.type_out("\n请选择：", 0.05, 'yellow')
            for idx, choice in enumerate(self.current_scene.choices, 1):
                TypewriterEffect.type_out(f"  {idx}. {choice.text}", 0.05, 'white')
    
    def show_help(self):
        """显示帮助"""
        TypewriterEffect.type_out("\n=== 操作指南 ===", 0.05, 'cyan')
        TypewriterEffect.type_out("  1. 切换频率 (/tune <频率>)", 0.05, 'white')
        TypewriterEffect.type_out("  2. 查看可联络对象 (/list)", 0.05, 'white')
        TypewriterEffect.type
