# Radio项目重构后的目录结构

## 项目根目录
```
Radio/
├── story_system/          # 故事系统核心模块
│   ├── __init__.py        # 模块初始化文件
│   ├── story_base.py      # 基础类型定义和枚举
│   ├── characters.py      # 角色管理系统
│   ├── story_manager.py   # 故事内容整合器和进度管理
│   ├── story_chapter1.py  # 第一章：被困
│   ├── story_chapter2.py  # 第二章：真相
│   ├── story_chapter3.py  # 第三章：选择
│   └── story_chapter4.py  # 第四章：结局
├── game_engine/           # 游戏引擎模块
│   ├── __init__.py        # 模块初始化文件
│   ├── radio_game.py          # 基础游戏引擎
│   ├── radio_game_enhanced.py # 增强版游戏引擎
│   ├── radio_game_integrated.py # 集成版游戏引擎
│   └── screen_utils.py        # 屏幕工具函数
├── utils/                 # 工具模块
│   ├── __init__.py        # 模块初始化文件
│   └── demo_screen_refresh.py # 屏幕刷新演示
├── docs/                  # 文档模块
│   ├── STORY_SYSTEM_README.md # 故事系统说明文档
│   ├── 大纲.md               # 项目大纲
│   └── main_story.md         # 主线故事内容
├── saves/                 # 存档数据
│   ├── save.json          # 游戏存档
│   └── story_save.json    # 故事进度存档
├── chat.md               # 聊天记录
└── PROJECT_STRUCTURE.md  # 项目结构说明（本文件）
```

## 模块说明

### story_system/
故事系统的核心模块，实现了完全模块化的故事内容管理。所有剧情内容与游戏引擎完全分离，支持动态加载和热更新。

### game_engine/
游戏引擎相关文件，负责游戏逻辑、界面显示和用户交互。与故事系统通过适配器模式连接。

### utils/
工具类和演示脚本，包含屏幕刷新等辅助功能。

### docs/
项目文档，包括系统说明、故事大纲等。

### saves/
游戏存档和故事进度存档，支持多周目游戏。

## 使用说明

### 运行游戏
```bash
# 运行基础版本
python game_engine/radio_game.py

# 运行增强版本
python game_engine/radio_game_enhanced.py

# 运行集成版本
python game_engine/radio_game_integrated.py
```

### 独立测试故事系统
```bash
# 测试故事系统
python -c "from story_system.story_manager import StoryManager; sm = StoryManager(); sm.demo_run()"
```

### 查看项目结构
```bash
tree Radio/ -I '__pycache__|*.pyc'
