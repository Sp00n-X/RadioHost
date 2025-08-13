
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多存档管理系统
支持多个存档槽位，存档选择和管理
"""

import os
import json
import shutil
from datetime import datetime
from typing import Dict, Any, List, Optional
from story_system.story_manager import StoryProgress

class SaveManager:
    """多存档管理器"""

    def __init__(self, saves_dir: str = "saves"):
        self.saves_dir = saves_dir
        self.max_slots = 5  # 最大存档槽位
        self.ensure_saves_dir()

    # ---------- 基础目录 ----------
    def ensure_saves_dir(self):
        """确保存档目录存在"""
        if not os.path.exists(self.saves_dir):
            os.makedirs(self.saves_dir)

    # ---------- 存档列表 ----------
    def get_save_files(self) -> List[Dict[str, Any]]:
        """获取所有存档文件信息"""
        saves = []

        for slot in range(1, self.max_slots + 1):
            save_path = os.path.join(self.saves_dir, f"save_{slot}.json")
            if os.path.exists(save_path):
                try:
                    with open(save_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        saves.append({
                            'slot': slot,
                            'path': save_path,
                            'exists': True,
                            'last_modified': os.path.getmtime(save_path),
                            'current_state': data.get('current_state', 'start'),
                            'choices_count': len(data.get('choices_made', [])),
                            'current_chapter': data.get('variables', {}).get('current_chapter', 1),
                            'play_time': self._estimate_play_time(data)
                        })
                except Exception:
                    saves.append({
                        'slot': slot,
                        'path': save_path,
                        'exists': True,
                        'last_modified': 0,
                        'current_state': 'error',
                        'choices_count': 0,
                        'current_chapter': 1,
                        'play_time': '未知'
                    })
            else:
                saves.append({
                    'slot': slot,
                    'path': save_path,
                    'exists': False,
                    'last_modified': 0,
                    'current_state': 'empty',
                    'choices_count': 0,
                    'current_chapter': 1,
                    'play_time': '新游戏'
                })

        return saves

    def _estimate_play_time(self, data: Dict[str, Any]) -> str:
        """估算游戏时间"""
        choices_count = len(data.get('choices_made', []))
        if choices_count == 0:
            return "新游戏"
        elif choices_count < 5:
            return "刚开始"
        elif choices_count < 15:
            return "进行中"
        elif choices_count < 30:
            return "深入游戏"
        else:
            return "接近完成"

    # ---------- 交互：选择槽位 ----------
    def select_save_slot(self) -> Optional[int]:
        """
        让用户选择存档槽位。
        返回 1~5 的整数，或 None（用户输入 quit）。
        """

        from game_engine.screen_utils import ScreenManager
        from game_engine.radio_game import TypewriterEffect

        ScreenManager.clear()
        ScreenManager.print_header("选择存档", "崖边电台主持人")
        saves = self.get_save_files()

        TypewriterEffect.type_out("请选择存档槽位：", 0.05, 'cyan')
        print()

        for save in saves:
            slot = save['slot']
            if save['exists']:
                last_modified = datetime.fromtimestamp(save['last_modified'])
                time_str = last_modified.strftime("%Y-%m-%d %H:%M")

                TypewriterEffect.type_out(
                    f"  {slot}. 存档 {slot} - {save['play_time']} - "
                    f"第{save['current_chapter']}章 - {save['choices_count']}个选择 - {time_str}",
                    0.05, 'white'
                )
            else:
                TypewriterEffect.type_out(
                    f"  {slot}. 空槽位 - 开始新游戏",
                    0.05, 'gray'
                )

        print()
        TypewriterEffect.type_out(
            "输入槽位编号 (1-5)，或输入 'quit' 退出：", 0.05, 'yellow'
        )

        while True:
            choice = input("> ").strip().lower()
            if choice == 'quit':
                return None
            if choice.isdigit() and 1 <= int(choice) <= self.max_slots:
                return int(choice)
            TypewriterEffect.type_out("请输入 1-5 之间的数字或 'quit'！", 0.05, 'red')

    # ---------- 存档 / 读档 ----------
    def save_to_slot(self, slot: int, story: StoryProgress):
        """把 StoryProgress 写入指定槽位"""
        if not (1 <= slot <= self.max_slots):
            raise ValueError("槽位必须在 1-5 之间")

        save_path = os.path.join(self.saves_dir, f"save_{slot}.json")
        # 先做备份，防止写入过程崩溃
        temp_path = save_path + ".tmp"

        data = story.serialize()  # 假设 StoryProgress 提供了 serialize()->dict
        with open(temp_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        # 原子替换
        if os.path.exists(save_path):
            os.replace(temp_path, save_path)
        else:
            os.rename(temp_path, save_path)

    def load_from_slot(self, slot: int) -> Optional[StoryProgress]:
        """从指定槽位读取 StoryProgress"""
        if not (1 <= slot <= self.max_slots):
            raise ValueError("槽位必须在 1-5 之间")

        save_path = os.path.join(self.saves_dir, f"save_{slot}.json")
        if not os.path.exists(save_path):
            return None

        try:
            with open(save_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return StoryProgress.deserialize(data)  # 假设 StoryProgress 支持反序列化
        except Exception as e:
            print(f"读取存档失败：{e}")
            return None

    # ---------- 删除 / 覆盖确认 ----------
    def delete_slot(self, slot: int):
        """删除指定槽位存档"""
        if not (1 <= slot <= self.max_slots):
            return
        save_path = os.path.join(self.saves_dir, f"save_{slot}.json")
        if os.path.exists(save_path):
            os.remove(save_path)

    def confirm_overwrite(self, slot: int) -> bool:
        """当槽位已有时，询问是否覆盖"""
        saves = self.get_save_files()
        save = next((s for s in saves if s['slot'] == slot), None)
        if not save or not save['exists']:
            return True  # 空槽位直接允许

        from game_engine.radio_game import TypewriterEffect
        TypewriterEffect.type_out(
            f"存档 {slot} 已存在！确定要覆盖吗？(y/n)：", 0.05, 'yellow'
        )
        return input("> ").strip().lower() in ('y', 'yes')


# ---------------- 示例用法 ----------------
if __name__ == '__main__':
    mgr = SaveManager()

    # 1. 让用户选一个槽位
    slot = mgr.select_save_slot()
    if slot is None:
        print("已退出")
        exit()

    # 2. 如果槽位已有存档，询问是否覆盖
    if not mgr.confirm_overwrite(slot):
        print("取消保存")
        exit()

    # 3. 这里假装有一个 StoryProgress 实例
    fake_story = StoryProgress()
    mgr.save_to_slot(slot, fake_story)
    print(f"已保存到存档 {slot}")
