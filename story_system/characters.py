#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
角色管理系统 - 所有角色定义和管理
"""

from .story_base import CharacterProfile
from typing import List, Optional

class CharacterManager:
    """角色管理系统"""
    
    def __init__(self):
        self.characters = {}
        self._initialize_characters()
    
    def _initialize_characters(self):
        """初始化所有可能的角色（主角的不同版本）"""
        # 第一章出现的角色
        self.characters["main_self"] = CharacterProfile(
            "main_self", "你自己", "困在尖崖小屋的主角",
            "困惑、恐惧但好奇", "一个普通的现代人，在海边散步时被困",
            "平静但带着紧张", 14250
        )
        
        # 第二章出现的不同版本的主角
        self.characters["successful_self"] = CharacterProfile(
            "successful_self", "成功的你", "事业成功但孤独的你",
            "自信但疲惫", "选择了事业而放弃家庭的自己",
            "疲惫而深沉", 14251
        )
        
        self.characters["loved_self"] = CharacterProfile(
            "loved_self", "被爱的你", "拥有完美爱情的你",
            "温柔但遗憾", "选择了爱情而放弃梦想的自己",
            "温柔而忧伤", 14252
        )
        
        self.characters["ordinary_self"] = CharacterProfile(
            "ordinary_self", "平凡的你", "过着平淡生活的你",
            "平静但空虚", "选择了逃避而平庸的自己",
            "平淡而迷茫", 14253
        )
        
        self.characters["female_self"] = CharacterProfile(
            "female_self", "女性的你", "如果是女性的话",
            "敏锐而坚强", "平行世界中的女性版本",
            "清脆而坚定", 14254
        )
        
        # 神秘男子
        self.characters["mysterious_man"] = CharacterProfile(
            "mysterious_man", "神秘男子", "皮肤黝黑的神秘男子",
            "神秘而戏谑", "似乎知道所有真相的引导者",
            "低沉而充满磁性", 14255
        )
    
    def get_character(self, character_id: str) -> Optional[CharacterProfile]:
        """获取角色信息"""
        return self.characters.get(character_id)
    
    def get_available_characters(self) -> List[CharacterProfile]:
        """获取可用角色列表"""
        return [char for char in self.characters.values() if char.available]
    
    def discover_character(self, character_id: str):
        """发现新角色"""
        if character_id in self.characters:
            self.characters[character_id].discovered = True
    
    def update_trust_level(self, character_id: str, change: int):
        """更新信任等级"""
        if character_id in self.characters:
            self.characters[character_id].trust_level += change
    
    def get_characters_by_chapter(self, chapter: int) -> List[CharacterProfile]:
        """按章节获取角色"""
        chapter_chars = {
            1: ["main_self"],
            2: ["successful_self", "loved_self", "ordinary_self", "female_self"],
            3: ["successful_self", "loved_self", "ordinary_self"],
            4: ["mysterious_man", "main_self"]
        }
        
        char_ids = chapter_chars.get(chapter, [])
        return [self.characters[char_id] for char_id in char_ids if char_id in self.characters]
    
    def get_all_characters(self) -> List[CharacterProfile]:
        """获取所有角色"""
        return list(self.characters.values())
