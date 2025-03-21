"""
Drag and drop support for sound buttons
"""
from PyQt6.QtCore import Qt, QMimeData, QUrl
from PyQt6.QtGui import QDrag
from PyQt6.QtWidgets import QWidget, QApplication

class SoundDragDrop:
    """Mixin class for drag and drop support for sound buttons"""
    
    def mousePressEvent(self, event):
        """Handle mouse press event for drag and drop"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_start_position = event.position().toPoint()
        
        # Call the parent class's mousePressEvent
        super().mousePressEvent(event)
    
    def mouseMoveEvent(self, event):
        """Handle mouse move event for drag and drop"""
        if not (event.buttons() & Qt.MouseButton.LeftButton):
            return
        
        # Check if the mouse has moved far enough to start a drag
        if (event.position().toPoint() - self.drag_start_position).manhattanLength() < QApplication.startDragDistance():
            return
        
        # Create a drag object
        drag = QDrag(self)
        mime_data = QMimeData()
        
        # Store the sound data
        mime_data.setText(self.sound.file_path)
        mime_data.setData("application/x-thamyris-sound", self.sound.to_dict().__str__().encode())
        
        drag.setMimeData(mime_data)
        
        # Start the drag operation
        drag.exec(Qt.DropAction.CopyAction | Qt.DropAction.MoveAction)
    
    @staticmethod
    def setup_drop_area(widget, callback):
        """Set up a widget as a drop area for sounds"""
        widget.setAcceptDrops(True)
        
        # Store the original methods
        original_dragEnterEvent = widget.dragEnterEvent if hasattr(widget, 'dragEnterEvent') else None
        original_dropEvent = widget.dropEvent if hasattr(widget, 'dropEvent') else None
        
        def dragEnterEvent(self, event):
            """Handle drag enter event"""
            if event.mimeData().hasText() or event.mimeData().hasFormat("application/x-thamyris-sound"):
                event.acceptProposedAction()
            elif original_dragEnterEvent:
                original_dragEnterEvent(event)
        
        def dropEvent(self, event):
            """Handle drop event"""
            if event.mimeData().hasText() or event.mimeData().hasFormat("application/x-thamyris-sound"):
                # Get the file path from the mime data
                file_path = event.mimeData().text()
                
                # Call the callback with the file path
                callback(file_path)
                
                event.acceptProposedAction()
            elif original_dropEvent:
                original_dropEvent(event)
        
        # Replace the methods
        widget.dragEnterEvent = dragEnterEvent.__get__(widget, type(widget))
        widget.dropEvent = dropEvent.__get__(widget, type(widget))
