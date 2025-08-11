#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
崖边电台主持人 - 增强版
集成屏幕刷新和更好的用户体验
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
from game_engine import ScreenManager

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

class RadioGameEnhanced:
    """增强版游戏主类"""
    
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
        self.in_story_mode = False
        self.current_character = None
        
    def intro(self):
        """游戏开场 - 使用屏幕刷新"""
        ScreenManager.print_header("崖边电台主持人", "命运的频率")
        
        TypewriterEffect.type_out("欢迎来到崖边电台主持人...", 0.08, 'cyan')
        time.sleep(1)
        
        # 使用故事系统的开场
        self.current_scene = self.story_content.get_scene("start")
        self.display_current_scene()
        
        time.sleep(2)
        SignalEffect.simulate_static(1.5)
        
        ScreenManager.wait_for_continue()
    
    def display_current_scene(self):
        """显示当前场景内容 - 带屏幕刷新"""
        if not self.current_scene:
            return
            
        # 清屏并显示新场景
        ScreenManager.clear()
        
        # 显示标题
        if self.current_scene.title:
            ScreenManager.print_section(self.current_scene.title, 'cyan')
        
        # 显示内容
        for line in self.current_scene.content:
            if line.strip():  # 跳过空行
                TypewriterEffect.type_out(line, 0.05, 'white')
            else:
                print()  # 空行
        
        # 显示选择
        if self.current_scene.choices:
            ScreenManager.print_choice_prompt()
            ScreenManager.print_choice_list([choice.text for choice in self.current_scene.choices])
    
    def show_help(self):
        """显示帮助 - 使用屏幕刷新"""
        ScreenManager.print_header("操作指南", "崖边电台主持人")
        
        TypewriterEffect.type_out("基础操作：", 0.05, 'yellow')
        TypewriterEffect.type_out("  1. 切换频率", 0.05, 'white')
        TypewriterEffect.type_out("  2. 查看可联络对象", 0.05, 'white')
        TypewriterEffect.type_out("  3. 开始故事模式", 0.05, 'white')
        TypewriterEffect.type_out("  4. 保存并退出游戏", 0.05, 'white')
        
        TypewriterEffect.type_out("\n故事指令：", 0.05, 'cyan')
        TypewriterEffect.type_out("  /story - 进入故事模式", 0.05, 'white')
        TypewriterEffect.type_out("  /tune <频率> - 切换频率", 0.05, 'white')
        TypewriterEffect.type_out("  /list - 查看可联络角色", 0.05, 'white')
        
        ScreenManager.wait_for_continue()
    
    def get_available_characters(self):
        """获取当前可用的角色"""
        current_chapter = self.story_progress.get_variable('current_chapter', 1)
        characters = self.character_manager.get_characters_by_chapter(current_chapter)
        
        # 过滤已发现的和可用的角色
        available = []
        for char in characters:
            if char.discovered or char.available:
                available.append(char)
        
        return available
    
    def display_character_list(self):
        """显示可联络的角色列表 - 使用屏幕刷新"""
        ScreenManager.print_header("可联络对象", "崖边电台主持人")
        
        characters = self.get_available_characters()
        if not characters:
            TypewriterEffect.type_out("  当前没有可联络的对象", 0.05, 'gray')
            ScreenManager.wait_for_continue()
            return
            
        for idx, char in enumerate(characters, 1):
            color = self._get_character_color(char.character_id)
            status = "已发现" if char.discovered else "可用"
            TypewriterEffect.type_out(
                f"  {idx}. {char.name} ({char.frequency} kHz) - {status}", 
                0.05, color
            )
        
        ScreenManager.wait_for_continue()
    
    def _get_character_color(self, character_id: str) -> str:
        """获取角色对应的颜色"""
        color_map = {
            'main_self': 'white',
            'successful_self': 'yellow',
            'loved_self': 'green',
            'ordinary_self': 'blue',
            'female_self': 'purple',
            'mysterious_man': 'red'
        }
        return color_map.get(character_id, 'white')
    
    def _handle_tune_frequency(self):
        """处理频率切换 - 使用屏幕刷新"""
        ScreenManager.print_header("频率调节", f"当前频率: {self.current_frequency} kHz")
        
        TypewriterEffect.type_out("请输入目标频率 (kHz)：", 0.05, 'cyan')
        try:
            freq = int(input("> ").strip())
            self.current_frequency = freq
            ScreenManager.clear()
            TypewriterEffect.type_out(f"已调至 {freq} kHz", 0.05, 'green')
            if freq != 14250:
                SignalEffect.simulate_static(1.5)
            ScreenManager.wait_for_continue()
        except ValueError:
            TypewriterEffect.type_out("频率格式错误！", 0.05, 'red')
            ScreenManager.wait_for_continue()
    
    def start_story_mode(self):
        """开始故事模式 - 使用屏幕刷新"""
        ScreenManager.print_header("故事模式", "命运的频率")
        
        # 从第一章开始
        current_scene = self.story_content.get_scene("start")
        if not current_scene:
            TypewriterEffect.type_out("故事内容加载失败", 0.05, 'red')
            ScreenManager.wait_for_continue()
            return
            
        while self.game_active and current_scene:
            self.display_current_scene()
            
            if not current_scene.choices:
                break
                
            try:
                choice = input("\n> ").strip()
                if choice.lower() == 'quit':
                    break
                    
                choice_num = int(choice)
                if 1 <= choice_num <= len(current_scene.choices):
                    selected_choice = current_scene.choices[choice_num - 1]
                    
                    # 记录选择
                    self.story_progress.make_choice(
                        selected_choice.next_state,
                        selected_choice.text
                    )
                    
                    # 更新变量
                    if selected_choice.variable_changes:
                        for key, value in selected_choice.variable_changes.items():
                            self.story_progress.set_variable(key, value)
                    
                    # 移动到下一个场景
                    current_scene = self.story_content.get_scene(selected_choice.next_state)
                    
                    # 保存进度
                    self.story_progress.save_progress()
                    
                else:
                    TypewriterEffect.type_out("无效选择", 0.05, 'red')
                    ScreenManager.wait_for_continue()
                    
            except (ValueError, KeyboardInterrupt):
                TypewriterEffect.type_out("返回主菜单", 0.05, 'yellow')
                break
    
    def save_and_exit(self):
        """保存并退出"""
        self.story_progress.save_progress()
        ScreenManager.clear()
        TypewriterEffect.type_out("游戏进度已保存", 0.05, 'green')
        TypewriterEffect.type_out("崖边电台主持人已关闭", 0.05, 'cyan')
        self.game_active = False
    
    def run(self):
        """主游戏循环"""
        self.intro()
        
        while self.game_active:
            ScreenManager.print_header("崖边电台主持人", f"频率: {self.current_frequency} kHz")
            
            TypewriterEffect.type_out("请选择操作：", 0.05, 'yellow')
            TypewriterEffect.type_out("  1. 切换频率", 0.05, 'white')
            TypewriterEffect.type_out("  2. 查看可联络对象", 0.05, 'white')
            TypewriterEffect.type_out("  3. 开始故事模式", 0.05, 'white')
            TypewriterEffect.type_out("  4. 显示帮助", 0.05, 'white')
            TypewriterEffect.type_out("  5. 保存并退出", 0.05, 'white')
            
            try:
                choice = input("\n> ").strip()
                
                if choice == '1':
                    self._handle_tune_frequency()
                elif choice == '2':
                    self.display_character_list()
                elif choice == '3':
                    self.start_story_mode()
                elif choice == '4':
                    self.show_help()
                elif choice == '5':
                    self.save_and_exit()
                else:
                    TypewriterEffect.type_out("请输入 1-5 之间的数字", 0.05, 'red')
                    ScreenManager.wait_for_continue()
                    
            except (KeyboardInterrupt, EOFError):
                self.save_and_exit()
                break

# =================================================
# 主程序入口
# =================================================
if __name__ == "__main__":
    game = RadioGameEnhanced()
    game.run()
