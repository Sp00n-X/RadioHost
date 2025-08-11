#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基础类型定义和枚举
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

class StoryState(Enum):
    """故事状态枚举"""
    START = "start"
    CHAPTER1_TRAPPED = "chapter1_trapped"
    CHAPTER1_EXPLORING = "chapter1_exploring"
    CHAPTER1_FIRST_CONTACT = "chapter1_first_contact"
    CHAPTER1_PHOTO = "chapter1_photo"
    CHAPTER1_LOCKED = "chapter1_locked"
    CHAPTER1_RADIO = "chapter1_radio"
    CHAPTER1_ROCKING_CHAIR = "chapter1_rocking_chair"
    CHAPTER1_DIALOGUE_END = "chapter1_dialogue_end"
    CHAPTER2_ACT1_SCENE1 = "chapter2_act1_scene1"
    CHAPTER2_ACT1_CONTACT1 = "chapter2_act1_contact1"
    CHAPTER2_MULTIPLE_CONTACTS = "chapter2_multiple_contacts"
    CHAPTER2_CODE_NAME = "chapter2_code_name"
    CHAPTER2_MAN_APPEARS = "chapter2_man_appears"
    CHAPTER3_CHOICE_INTRO = "chapter3_choice_intro"
    CHAPTER3_FIRST_VIEW = "chapter3_first_view"
    CHAPTER3_SECOND_VIEW = "chapter3_second_view"
    CHAPTER3_THIRD_VIEW = "chapter3_third_view"
    CHAPTER4_FINAL_CHOICE = "chapter4_final_choice"
    ENDING1_ACCEPT = "ending1_accept"
    ENDING2_KNOWLEDGE = "ending2_knowledge"
    ENDING3_LOOP = "ending3_loop"

@dataclass
class StoryChoice:
    """故事选择选项"""
    text: str
    next_state: str
    action: Optional[str] = None
    condition: Optional[str] = None
    variable_changes: Optional[Dict[str, Any]] = None

@dataclass
class StoryScene:
    """故事场景"""
    id: str
    title: str
    content: List[str]
    choices: List[StoryChoice]
    audio_effect: Optional[str] = None
    transition_effect: Optional[str] = None
    character_id: Optional[str] = None
    variable_changes: Optional[Dict[str, Any]] = None

class CharacterProfile:
    """角色档案"""
    
    def __init__(self, character_id: str, name: str, description: str, 
                 personality: str, background: str, voice_style: str,
                 frequency: int, trust_level: int = 0):
        self.character_id = character_id
        self.name = name
        self.description = description
        self.personality = personality
        self.background = background
        self.voice_style = voice_style
        self.frequency = frequency
        self.trust_level = trust_level
        self.available = True
        self.discovered = False
        
        # 添加callsign和color属性
        self.callsign = character_id.upper()
        self.color = self._get_character_color(character_id)
    
    def _get_character_color(self, character_id: str) -> str:
        """根据角色ID获取颜色"""
        color_map = {
            'main_self': 'cyan',
            'successful_self': 'green',
            'loved_self': 'purple',
            'ordinary_self': 'gray',
            'female_self': 'yellow',
            'mysterious_man': 'red'
        }
        return color_map.get(character_id, 'white')
    
    def to_dict(self):
        return {
            'character_id': self.character_id,
            'name': self.name,
            'description': self.description,
            'personality': self.personality,
            'background': self.background,
            'voice_style': self.voice_style,
            'frequency': self.frequency,
            'trust_level': self.trust_level,
            'available': self.available,
            'discovered': self.discovered
        }
