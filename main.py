"""AI 桌面女友 - 主入口。

启动流程：
1. 加载配置（config.json）
2. 初始化 SQLite 记忆
3. 启动 Qt 应用
4. 显示桌面悬浮窗 + 系统托盘
5. 双击悬浮窗或托盘 -> 打开聊天对话框

运行：
    python main.py
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Optional

from PySide6.QtCore import QPoint
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication, QMessageBox

# 让 src 包能被导入
sys.path.insert(0, str(Path(__file__).resolve().parent))

from src.core.config import AppConfig
from src.core.memory import ChatMemory
from src.ui.bubble import SpeechBubble
from src.ui.chat_dialog import ChatDialog
from src.ui.floating_window import FloatingWindow
from src.ui.tray import TrayIconManager


class App:
    """应用主控制器：把 UI 组件粘起来。"""

    def __init__(self, config: AppConfig) -> None:
        self.config = config
        self.memory = ChatMemory(config.db_path)

        avatar_path = config.assets_dir / "avatar.png"

        self.floating = FloatingWindow(
            avatar_path=avatar_path,
            size=config.ui.avatar_size,
            always_on_top=config.ui.always_on_top,
        )

        self.bubble = SpeechBubble()

        self.tray = TrayIconManager(
            icon_path=avatar_path,
            parent_widget=self.floating,
        )

        self.chat_dialog: Optional[ChatDialog] = None

        # 信号绑定
        self.floating.doubleClicked.connect(self.open_chat)
        self.floating.rightClicked.connect(self._on_floating_right_click)

        self.tray.openChatRequested.connect(self.open_chat)
        self.tray.toggleVisibilityRequested.connect(self.toggle_floating)
        self.tray.clearHistoryRequested.connect(self.clear_history)
        self.tray.quitRequested.connect(QApplication.quit)

    # ---------- 启动 / 欢迎 ----------

    def show(self) -> None:
        self.floating.show()
        # 欢迎气泡
        QApplication.processEvents()  # 让悬浮窗先布局完成拿到位置
        self.bubble.set_text(self.config.persona.greeting)
        self.bubble.show_near(self.floating.pos(), self.floating.width())

        # 校验配置缺失时弹提示
        ok, err = self.config.validate()
        if not ok:
            QMessageBox.warning(
                self.floating,
                "配置未完成",
                f"{err}\n\n打开 config.json 填好后重启即可。",
            )

    # ---------- 槽函数 ----------

    def open_chat(self) -> None:
        if self.chat_dialog is None:
            self.chat_dialog = ChatDialog(self.config, self.memory)
        self.chat_dialog.show()
        self.chat_dialog.raise_()
        self.chat_dialog.activateWindow()

    def toggle_floating(self) -> None:
        if self.floating.isVisible():
            self.floating.hide()
        else:
            self.floating.show()

    def clear_history(self) -> None:
        n = self.memory.clear()
        # 若聊天窗已打开，重建
        if self.chat_dialog is not None:
            self.chat_dialog.close()
            self.chat_dialog = None
        self.bubble.set_text(f"清空啦，{n} 条记录都删除了 🌸")
        self.bubble.show_near(self.floating.pos(), self.floating.width())

    def _on_floating_right_click(self, global_pos: QPoint) -> None:
        self.tray.popup_menu(global_pos)


def main() -> int:
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)  # 关闭窗口不退出（托盘还在）

    # 加载配置
    try:
        config = AppConfig.load()
    except FileNotFoundError as e:
        QMessageBox.critical(None, "启动失败", str(e))
        return 1

    main_app = App(config)
    main_app.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
