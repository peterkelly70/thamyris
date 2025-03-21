"""
Main application entry point with GUI initialization
"""
import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from dotenv import load_dotenv

from controllers.app_controller import AppController

def main():
    """Main application entry point"""
    # Load environment variables
    load_dotenv()
    
    # Create Qt application
    app = QApplication(sys.argv)
    app.setApplicationName("Thamyris")
    app.setApplicationVersion("1.0.0")
    
    # Set application style
    app.setStyle("Fusion")
    
    # Create and start the application controller
    controller = AppController()
    controller.start()
    
    # Start the Qt event loop
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
