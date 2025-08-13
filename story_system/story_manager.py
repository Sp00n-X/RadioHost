#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
故事内容整合器和进度管理器
"""

import json
import os
from datetime import datetime
from typing import Dict, Any
from .story_base import StoryState
from .characters import CharacterManager

class StoryContent:
    """故事内容整合器"""
    
    def __init__(self):
        self.scenes = {}
        self._load_all_content()
    
    def _load_all_content(self):
        """加载所有章节内容"""
        from .story_chapter1 import get_chapter1_content
        from .story_chapter2 import get_chapter2_content
        from .story_chapter3 import get_chapter3_content
        from .story_chapter4 import get_chapter4_content
        
        # 合并所有章节内容
        self.scenes.update(get_chapter1_content())
        self.scenes.update(get_chapter2_content())
        self.scenes.update(get_chapter3_content())
        self.scenes.update(get_chapter4_content())
    
    def get_scene(self, scene_id: str):
        """获取指定场景"""
        return self.scenes.get(scene_id)

class StoryProgress:
    """故事进度管理"""
    
    def __init__(self, save_file: str = "story_save.json"):
        self.save_file = save_file
        self.current_state = StoryState.START
        self.choices_made = []
        self.variables = {
            'player_code_name': None,
            'view_count': 0,
            'first_view_choice': None,
            'second_view_choice': None,
            'third_view_choice': None,
            'man_appeared': False,
            'loop_count': 0,
            'current_chapter': 1
        }
        self.chapter_progress = {
            "chapter1": False,
            "chapter2": False,
            "chapter3": False,
            "chapter4": False
        }
        self.endings_unlocked = []
        self.character_manager = CharacterManager()
        self.story_content = StoryContent()
        self.load_progress()
    
    def load_progress(self):
        """加载进度"""
        if os.path.exists(self.save_file):
            try:
                with open(self.save_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.current_state = StoryState(data.get('current_state', 'start'))
                    self.choices_made = data.get('choices_made', [])
                    self.variables.update(data.get('variables', {}))
                    self.chapter_progress.update(data.get('chapter_progress', {}))
                    self.endings_unlocked = data.get('endings_unlocked', [])
                    
                    # 加载角色状态
                    char_data = data.get('characters', {})
                    for char_id, char_info in char_data.items():
                        char = self.character_manager.get_character(char_id)
                        if char:
                            char.trust_level = char_info.get('trust_level', 0)
                            char.available = char_info.get('available', True)
                            char.discovered = char_info.get('discovered', False)
                            
            except Exception as e:
                print(f"加载存档失败: {e}")
    
    def save_progress(self):
        """保存进度"""
        try:
            # 准备角色数据
            char_data = {}
            for char_id, char in self.character_manager.characters.items():
                char_data[char_id] = char.to_dict()
            data = {
                'current_state': self.current_state.value if hasattr(self.current_state, 'value') else str(self.current_state),
                'choices_made': self.choices_made,
                'variables': self.variables,
                'chapter_progress': self.chapter_progress,
                'endings_unlocked': self.endings_unlocked,
                'characters': char_data
            }
            with open(self.save_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存存档失败: {e}")
    
    def make_choice(self, choice_id: str, choice_text: str):
        """记录选择"""
        self.choices_made.append({
            'state': self.current_state.value if hasattr(self.current_state, 'value') else str(self.current_state),
            'choice_id': choice_id,
            'choice_text': choice_text,
            'timestamp': str(datetime.now())
        })
        
        # 检查是否完成章节
        if choice_id.startswith('chapter2_') and not self.chapter_progress['chapter2']:
            self.update_chapter_progress(2)
            self.set_variable('current_chapter', 2)
        elif choice_id.startswith('chapter3_') and not self.chapter_progress['chapter3']:
            self.update_chapter_progress(3)
            self.set_variable('current_chapter', 3)
        elif choice_id.startswith('chapter4_') and not self.chapter_progress['chapter4']:
            self.update_chapter_progress(4)
            self.set_variable('current_chapter', 4)
    
    def set_variable(self, key: str, value: Any):
        """设置变量"""
        self.variables[key] = value
    
    def get_variable(self, key: str, default=None):
        """获取变量"""
        return self.variables.get(key, default)
    
    def update_chapter_progress(self, chapter: int):
        """更新章节进度"""
        self.chapter_progress[f"chapter{chapter}"] = True
    
    def get_current_scene(self):
        """获取当前场景"""
        current_state = self.current_state.value if hasattr(self.current_state, 'value') else str(self.current_state)
        return self.story_content.get_scene(current_state)
    
    def serialize(self) -> Dict[str, Any]:
        """序列化故事进度为字典"""
        # 准备角色数据
        char_data = {}
        for char_id, char in self.character_manager.characters.items():
            char_data[char_id] = char.to_dict()
        
        return {
            'current_state': self.current_state.value if hasattr(self.current_state, 'value') else str(self.current_state),
            'choices_made': self.choices_made,
            'variables': self.variables,
            'chapter_progress': self.chapter_progress,
            'endings_unlocked': self.endings_unlocked,
            'characters': char_data
        }
    
    @classmethod
    def deserialize(cls, data: Dict[str, Any]) -> 'StoryProgress':
        """从字典反序列化故事进度"""
        story_progress = cls()
        
        # 恢复基本状态
        story_progress.current_state = StoryState(data.get('current_state', 'start'))
        story_progress.choices_made = data.get('choices_made', [])
        story_progress.variables.update(data.get('variables', {}))
        story_progress.chapter_progress.update(data.get('chapter_progress', {}))
        story_progress.endings_unlocked = data.get('endings_unlocked', [])
        
        # 恢复角色状态
        char_data = data.get('characters', {})
        for char_id, char_info in char_data.items():
            char = story_progress.character_manager.get_character(char_id)
            if char:
                char.trust_level = char_info.get('trust_level', 0)
                char.available = char_info.get('available', True)
                char.discovered = char_info.get('discovered', False)
        
        return story_progress
