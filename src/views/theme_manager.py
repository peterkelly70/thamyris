"""
Theme manager - Handles application theming
"""
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtWidgets import QApplication

from models.settings import Theme

class ThemeManager:
    """Class for managing application themes"""
    
    @staticmethod
    def apply_theme(theme: Theme):
        """Apply a theme to the application"""
        if theme == Theme.LIGHT:
            ThemeManager.apply_light_theme()
        elif theme == Theme.DARK:
            ThemeManager.apply_dark_theme()
        elif theme == Theme.CUSTOM:
            # Custom theme would be implemented here
            ThemeManager.apply_dark_theme()  # Default to dark for now
    
    @staticmethod
    def apply_light_theme():
        """Apply light theme to the application"""
        app = QApplication.instance()
        if not app:
            return
        
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(240, 240, 240))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(0, 0, 0))
        palette.setColor(QPalette.ColorRole.Base, QColor(255, 255, 255))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(245, 245, 245))
        palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(255, 255, 220))
        palette.setColor(QPalette.ColorRole.ToolTipText, QColor(0, 0, 0))
        palette.setColor(QPalette.ColorRole.Text, QColor(0, 0, 0))
        palette.setColor(QPalette.ColorRole.Button, QColor(240, 240, 240))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(0, 0, 0))
        palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 0, 0))
        palette.setColor(QPalette.ColorRole.Link, QColor(0, 0, 255))
        palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))
        
        app.setPalette(palette)
        
        # Set stylesheet for additional customization
        app.setStyleSheet("""
            QGroupBox {
                border: 1px solid #cccccc;
                border-radius: 5px;
                margin-top: 1ex;
                font-weight: bold;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 3px;
            }
        """)
    
    @staticmethod
    def apply_dark_theme():
        """Apply dark theme to the application"""
        app = QApplication.instance()
        if not app:
            return
        
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(255, 255, 255))
        palette.setColor(QPalette.ColorRole.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ColorRole.ToolTipText, QColor(255, 255, 255))
        palette.setColor(QPalette.ColorRole.Text, QColor(255, 255, 255))
        palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(255, 255, 255))
        palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 0, 0))
        palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))
        
        app.setPalette(palette)
        
        # Set stylesheet for additional customization
        app.setStyleSheet("""
            QGroupBox {
                border: 1px solid #555555;
                border-radius: 5px;
                margin-top: 1ex;
                font-weight: bold;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 3px;
            }
            QPushButton {
                background-color: #444444;
                border: 1px solid #555555;
                border-radius: 4px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #555555;
            }
            QPushButton:pressed {
                background-color: #333333;
            }
            QTabWidget::pane {
                border: 1px solid #555555;
                border-radius: 4px;
            }
            QTabBar::tab {
                background-color: #444444;
                border: 1px solid #555555;
                border-bottom-color: #555555;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                padding: 5px;
            }
            QTabBar::tab:selected {
                background-color: #333333;
            }
            QTabBar::tab:hover {
                background-color: #555555;
            }
        """)
