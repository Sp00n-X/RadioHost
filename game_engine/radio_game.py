#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
崖边电台主持人 - 集成故事系统的完整版本
基于"尖崖上的小屋：命运的抉择"剧情
"""

import sys
import time
import json
import random
import threading
from datetime import datetime

# 导入故事系统
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from story_system import StoryProgress, StoryContent, CharacterManager
from game_engine.input_manager_v2 import LightweightInputBlocker

class TypewriterEffect:
    """打字机效果输出"""
    
    @staticmethod
    def type_out(text: str, delay: float = 0.05, color: str = None):
        """逐字输出文字（带输入阻止）"""
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
        
        # 使用轻量级输入阻止器，不影响终端格式
        with LightweightInputBlocker(flush=True):
            if color and color in colors:
                sys.stdout.write(colors[color])
            
            # 逐字符输出，保持原有格式
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
        with LightweightInputBlocker(flush=True):
            TypewriterEffect.type_out(random.choice(static_chars), 0.1, 'gray')
            time.sleep(duration)

class Character:
    """可通话角色"""
    
    def __init__(self, name: str, callsign: str, color: str):
        self.name = name
        self.callsign = callsign
        self.color = color
        self.trust_level = 0
        self.available = True

class RadioGame:
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
        self.in_story_mode = False
        self.current_character = None
        self.current_channel = None
        
        # 兼容旧版本的characters
        self.characters = {}
        
    def load_save(self):
        """加载存档（兼容旧版本）"""
        try:
            with open('save.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                'branch': 'start',
                'trust_levels': {},
                'discovered_clues': []
            }
    
    def save_game(self):
        """保存游戏"""
        self.story_progress.save_progress()
        TypewriterEffect.type_out("游戏进度已保存。", 0.05, 'green')
    
    def intro(self):
        """游戏开场 - 简化版"""
        TypewriterEffect.type_out("=== 崖边电台主持人 ===", 0.1, 'cyan')
        
        # 在等待期间阻止输入
        with LightweightInputBlocker(flush=True):
            time.sleep(1)
        
        SignalEffect.simulate_static(1.0)
    
    def display_scene(self, scene):
        """显示故事场景"""
        if not scene:
            return
        
        # 显示场景标题
        if scene.title:
            TypewriterEffect.type_out(f"\n=== {scene.title} ===", 0.05, 'cyan')
        
        # 显示场景内容
        for content in scene.content:
            TypewriterEffect.type_out(content, 0.05)
            # 在等待期间阻止输入
            with LightweightInputBlocker(flush=True):
                time.sleep(0.5)
        
        # 显示选择选项
        if scene.choices:
            TypewriterEffect.type_out("\n请选择:", 0.05, 'yellow')
            for i, choice in enumerate(scene.choices, 1):
                TypewriterEffect.type_out(f"{i}. {choice.text}", 0.03, 'white')
        
        # 处理用户选择
        if scene.choices:
            while True:
                try:
                    choice = input("\n请输入选择 (1-{}): ".format(len(scene.choices)))
                    choice_index = int(choice) - 1
                    if 0 <= choice_index < len(scene.choices):
                        selected_choice = scene.choices[choice_index]
                        self.story_progress.make_choice(selected_choice.next_state, selected_choice.text)
                        
                        # 处理变量变化
                        if selected_choice.variable_changes:
                            for key, value in selected_choice.variable_changes.items():
                                self.story_progress.set_variable(key, value)
                        
                        # 处理特殊动作
                        if selected_choice.action:
                            self._handle_special_action(selected_choice.action)
                        
                        break
                    else:
                        TypewriterEffect.type_out("无效选择，请重试。", 0.05, 'red')
                except ValueError:
                    TypewriterEffect.type_out("请输入数字。", 0.05, 'red')
    
    def _handle_special_action(self, action: str):
        """处理特殊动作（简化版）"""
        if action == "save":
            self.save_game()
    
    def start_story_mode(self):
        """开始故事模式 - 持续运行直到故事结束"""
        self.in_story_mode = True
        TypewriterEffect.type_out("进入故事模式...", 0.05, 'cyan')
        
        try:
            while self.in_story_mode:
                # 获取当前场景
                current_scene = self.story_progress.get_current_scene()
                if current_scene:
                    self.display_scene(current_scene)
                    
                    # 检查是否到达结局
                    if self._is_ending_scene(current_scene):
                        self.in_story_mode = False
                        break
                else:
                    # 如果没有当前场景，显示开场
                    start_scene = self.story_content.get_scene("start")
                    if start_scene:
                        self.display_scene(start_scene)
                    else:
                        TypewriterEffect.type_out("没有找到可用的场景。", 0.05, 'red')
                        break
                        
        except KeyboardInterrupt:
            TypewriterEffect.type_out("\n\n游戏中断。", 0.05, 'red')
            self.save_game()
            raise
        except Exception as e:
            TypewriterEffect.type_out(f"发生错误: {e}", 0.05, 'red')
            self.save_game()
            raise
    
    def _is_ending_scene(self, scene):
        """检查是否为结局场景"""
        if not scene:
            return False
        
        ending_ids = ['ending1_accept', 'ending2_knowledge', 'ending3_loop']
        return scene.id in ending_ids
    
    def show_help(self):
        """显示帮助信息（简化版）"""
        help_text = """
=== 崖边电台主持人 - 帮助 ===
操作说明:
  - 按照提示进行选择
  - 不同的选择会影响故事走向
  - Ctrl+C 退出游戏并自动保存
        """
        TypewriterEffect.type_out(help_text, 0.03, 'yellow')
    
    def run(self):
        """主游戏循环 - 直接进入故事模式"""
        self.intro()
        
        # 直接进入故事模式
        self.start_story_mode()
        
        # 游戏结束
        TypewriterEffect.type_out("游戏结束。", 0.05, 'cyan')
        self.save_game()

def main():
    """主函数"""
    game = RadioGame()
    game.run()

if __name__ == "__main__":
    main()
