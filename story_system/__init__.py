"""
故事系统模块
包含所有故事相关的核心功能
"""

from .story_base import *
from .characters import CharacterManager, CharacterProfile
from .story_manager import StoryProgress, StoryContent
from .story_chapter1 import get_chapter1_content
from .story_chapter2 import get_chapter2_content
from .story_chapter3 import get_chapter3_content
from .story_chapter4 import get_chapter4_content

__all__ = [
    'CharacterManager',
    'CharacterProfile', 
    'StoryProgress',
    'StoryContent',
    'get_chapter1_content',
    'get_chapter2_content',
    'get_chapter3_content',
    'get_chapter4_content'
]
