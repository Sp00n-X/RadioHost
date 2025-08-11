#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
输入管理器 - 控制键盘输入
用于在打字机效果输出时阻止用户输入
"""

import sys
import tty
import termios
import threading
import time
from typing import Optional

class InputManager:
    """输入管理器 - 管理键盘输入"""
    
    def __init__(self):
        self._input_blocked = False
        self._original_settings = None
        self._lock = threading.Lock()
    
    def block_input(self):
        """阻止键盘输入（除了Ctrl+C）"""
        with self._lock:
            if self._input_blocked:
                return
            
            try:
                # 保存当前终端设置
                self._original_settings = termios.tcgetattr(sys.stdin.fileno())
                
                # 设置终端为原始模式
                tty.setraw(sys.stdin.fileno())
                
                # 禁用回显和信号处理
                new_settings = termios.tcgetattr(sys.stdin.fileno())
                new_settings[3] = new_settings[3] & ~(termios.ECHO | termios.ICANON)
                new_settings[6][termios.VMIN] = 0  # 非阻塞读取
                new_settings[6][termios.VTIME] = 0
                
                termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, new_settings)
                self._input_blocked = True
                
            except (termios.error, tty.error):
                # 在某些环境下可能不支持，忽略错误
                self._input_blocked = False
    
    def unblock_input(self):
        """恢复键盘输入"""
        with self._lock:
            if not self._input_blocked or self._original_settings is None:
                return
            
            try:
                # 恢复原始终端设置
                termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, self._original_settings)
                self._input_blocked = False
                self._original_settings = None
                
            except termios.error:
                # 忽略恢复错误
                self._input_blocked = False
    
    def is_input_blocked(self) -> bool:
        """检查输入是否被阻止"""
        return self._input_blocked
    
    def flush_input(self):
        """清空输入缓冲区"""
        if not self._input_blocked:
            try:
                # 清空标准输入缓冲区
                import select
                while sys.stdin in select.select([sys.stdin], [], [], 0.0)[0]:
                    sys.stdin.read(1)
            except (ImportError, OSError):
                # 在某些系统上可能不支持select，忽略
                pass
    
    def __enter__(self):
        """上下文管理器入口"""
        self.block_input()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        self.unblock_input()
    
    def safe_input(self, prompt: str = "") -> str:
        """安全的输入方法（自动处理输入阻止状态）"""
        # 确保输入未被阻止
        was_blocked = self._input_blocked
        if was_blocked:
            self.unblock_input()
        
        try:
            return input(prompt)
        finally:
            # 如果之前是被阻止的，恢复阻止状态
            if was_blocked:
                self.block_input()

# 全局输入管理器实例
input_manager = InputManager()

class InputBlocker:
    """输入阻止器上下文管理器"""
    
    def __init__(self, flush: bool = True):
        """
        初始化输入阻止器
        
        Args:
            flush: 是否在阻止前清空输入缓冲区
        """
        self.flush = flush
    
    def __enter__(self):
        """进入上下文时阻止输入"""
        if self.flush:
            input_manager.flush_input()
        input_manager.block_input()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """退出上下文时恢复输入"""
        input_manager.unblock_input()
        if exc_type is KeyboardInterrupt:
            # 如果是Ctrl+C，确保终端状态正常
            input_manager.unblock_input()
            print("\n")  # 换行以便后续输出
            return False  # 让异常继续传播
        return False
