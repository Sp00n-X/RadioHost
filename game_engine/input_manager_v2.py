#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
轻量级输入管理器 - 不干扰终端格式
"""

import sys
import select
import threading
import time
from typing import Optional

class LightweightInputManager:
    """轻量级输入管理器 - 不修改终端设置"""
    
    def __init__(self):
        self._input_blocked = False
        self._lock = threading.Lock()
    
    def block_input(self):
        """阻止输入（通过清空缓冲区）"""
        with self._lock:
            if self._input_blocked:
                return
            
            try:
                # 清空输入缓冲区
                self.flush_input()
                self._input_blocked = True
            except Exception:
                # 忽略错误
                self._input_blocked = False
    
    def unblock_input(self):
        """恢复输入"""
        with self._lock:
            self._input_blocked = False
    
    def is_input_blocked(self) -> bool:
        """检查输入是否被阻止"""
        return self._input_blocked
    
    def flush_input(self):
        """清空输入缓冲区"""
        try:
            # 使用select检查是否有输入
            while sys.stdin in select.select([sys.stdin], [], [], 0.0)[0]:
                sys.stdin.read(1)
        except (ImportError, OSError, ValueError):
            # 在某些系统上可能不支持select，忽略
            pass
    
    def __enter__(self):
        """上下文管理器入口"""
        self.block_input()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        self.unblock_input()

# 全局实例
lightweight_input_manager = LightweightInputManager()

class LightweightInputBlocker:
    """轻量级输入阻止器"""
    
    def __init__(self, flush: bool = True):
        self.flush = flush
    
    def __enter__(self):
        """进入上下文时阻止输入"""
        if self.flush:
            lightweight_input_manager.flush_input()
        lightweight_input_manager.block_input()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """退出上下文时恢复输入"""
        lightweight_input_manager.unblock_input()
