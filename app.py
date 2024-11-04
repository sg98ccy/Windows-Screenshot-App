import sys
import os
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox, QSlider, QMessageBox
from PyQt5.QtCore import Qt, QRect, QBuffer, QIODevice, QTimer
from PyQt5.QtGui import QScreen, QPixmap, QPainter, QPen, QColor, QImage, QCursor, QKeyEvent, QIcon
import win32clipboard
from PIL import Image
from io import BytesIO

class ScreenshotTool(QWidget):
    def __init__(self): 
        super().__init__()
        self.initUI()
        self.screenshot = None

    def initUI(self):
        self.setWindowTitle('Screenshot Selector')
        # Set the icon for the PyQt window (icon located in the root directory)
        self.setWindowIcon(QIcon("./favicon.ico"))
        
        # Labels with units in pixels
        width_label = QLabel('Width (px):')
        self.width_input = QLineEdit()
        height_label = QLabel('Height (px):')
        self.height_input = QLineEdit()

        # Add focus management for the textboxes
        self.width_input.installEventFilter(self)
        self.height_input.installEventFilter(self)
        
        # Ratio selection dropdown
        self.ratio_combo = QComboBox()
        self.ratio_combo.addItem("Custom")
        self.ratio_combo.addItem("16:9")
        self.ratio_combo.addItem("16:10")
        self.ratio_combo.addItem("4:3")
        self.ratio_combo.addItem("1:1")
        self.ratio_combo.currentIndexChanged.connect(self.update_dimensions_from_ratio)

        # Slider for scaling dimensions based on selected ratio
        self.size_slider = QSlider(Qt.Horizontal)
        self.size_slider.setMinimum(1)
        self.size_slider.setMaximum(20)
        self.size_slider.setValue(10)  # Start in the middle, no scaling
        self.size_slider.valueChanged.connect(self.update_slider_scaling)
        
        capture_button = QPushButton('Select Screenshot Area')
        capture_button.clicked.connect(self.select_screenshot_area)

        input_layout = QHBoxLayout()
        input_layout.addWidget(width_label)
        input_layout.addWidget(self.width_input)
        input_layout.addWidget(height_label)
        input_layout.addWidget(self.height_input)

        main_layout = QVBoxLayout()
        main_layout.addLayout(input_layout)
        main_layout.addWidget(QLabel("Select Ratio:"))
        main_layout.addWidget(self.ratio_combo)
        main_layout.addWidget(QLabel("Scale Size:"))
        main_layout.addWidget(self.size_slider)
        main_layout.addWidget(capture_button)

        self.setLayout(main_layout)

    def eventFilter(self, source, event):
        # Hotkey functionality for switching textboxes with refined cursor behavior
        if event.type() == event.KeyPress:
            if source == self.width_input or source == self.height_input:
                # Capture left or right arrow key events
                if event.key() == Qt.Key_Right:
                    # Shift to the other box if at the end of the text
                    if source.cursorPosition() == len(source.text()):
                        if source == self.width_input:
                            self.height_input.setFocus()
                        else:
                            self.width_input.setFocus()
                        return True
                elif event.key() == Qt.Key_Left:
                    # Shift to the other box if at the start of the text
                    if source.cursorPosition() == 0:
                        if source == self.width_input:
                            self.height_input.setFocus()
                        else:
                            self.width_input.setFocus()
                        return True
                elif event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
                    # If one box is empty, shift to it instead of proceeding
                    if not self.width_input.text() and source == self.height_input:
                        self.width_input.setFocus()
                    elif not self.height_input.text() and source == self.width_input:
                        self.height_input.setFocus()
                    elif self.width_input.text() and self.height_input.text():
                        self.select_screenshot_area()
                    return True
        return super().eventFilter(source, event)

    def update_dimensions_from_ratio(self):
        # Set default dimensions based on selected ratio
        ratio = self.ratio_combo.currentText()
        if ratio == "16:9":
            self.width_input.setText("1600")
            self.height_input.setText("900")
        elif ratio == "16:10":
            self.width_input.setText("1600")
            self.height_input.setText("1000")
        elif ratio == "4:3":
            self.width_input.setText("1200")
            self.height_input.setText("900")
        elif ratio == "1:1":
            self.width_input.setText("1000")
            self.height_input.setText("1000")
        else:
            self.width_input.clear()
            self.height_input.clear()

    def update_slider_scaling(self):
        # Adjust dimensions based on slider value
        ratio = self.ratio_combo.currentText()
        scale_factor = self.size_slider.value() / 10  # Center (10) means no scaling
        if ratio != "Custom":
            try:
                # Convert text to integer
                base_width = int(self.width_input.text())
                base_height = int(self.height_input.text())
                # Apply scaling based on slider position
                self.width_input.setText(str(int(base_width * scale_factor)))
                self.height_input.setText(str(int(base_height * scale_factor)))
            except ValueError:
                pass  # Handle cases where inputs are not valid integers

    def select_screenshot_area(self):
        self.hide()
        screen = QApplication.primaryScreen()
        self.original_pixmap = screen.grabWindow(0)
        self.screenshot_selector = ScreenshotSelector(
            self.original_pixmap, 
            int(self.width_input.text()), 
            int(self.height_input.text())
        )
        self.screenshot_selector.screenshotTaken.connect(self.save_screenshot)
        self.screenshot_selector.cancelled.connect(self.show)
        self.screenshot_selector.showFullScreen()

    def save_screenshot(self, pixmap):
        # Save to file in a 'Screenshot Outputs' folder in the current directory
        save_path = os.path.join(os.getcwd(), "Screenshot Outputs")
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"screenshot_{timestamp}.png"
        file_path = os.path.join(save_path, file_name)
        
        pixmap.save(file_path, "PNG")
        print(f"Screenshot saved as '{file_path}'")

        # Convert QPixmap to PIL Image
        buffer = QBuffer()
        buffer.open(QBuffer.ReadWrite)
        pixmap.save(buffer, "PNG")
        pil_img = Image.open(BytesIO(buffer.data()))

        # Convert image to BMP format for clipboard
        output = BytesIO()
        pil_img.convert("RGB").save(output, "BMP")
        data = output.getvalue()[14:]  # Remove BMP header
        output.close()

        # Copy to clipboard
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
        win32clipboard.CloseClipboard()
        print("Screenshot copied to clipboard")

        # Show notification
        self.show_notification("Screenshot completed and copied to clipboard!")
        self.show()

    def show_notification(self, message):
        # Create a custom notification message box
        msg_box = AutoCloseMessageBox(self, message)
        msg_box.exec_()

class AutoCloseMessageBox(QMessageBox):
    def __init__(self, parent, message, timeout=2000):
        super().__init__(parent)
        self.setIcon(QMessageBox.Information)
        self.setText(message)
        self.setWindowTitle("Notification")
        self.setStandardButtons(QMessageBox.Ok)

        # Set timer to automatically close after the specified timeout (in milliseconds)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.close)
        self.timer.start(timeout)

    def keyPressEvent(self, event: QKeyEvent):
        # Close the message box when Esc is pressed
        if event.key() == Qt.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(event)

class ScreenshotSelector(QWidget):
    from PyQt5.QtCore import pyqtSignal
    screenshotTaken = pyqtSignal(QPixmap)
    cancelled = pyqtSignal()

    def __init__(self, pixmap, width, height):
        super().__init__()
        self.original_pixmap = pixmap
        self.setGeometry(0, 0, self.original_pixmap.width(), self.original_pixmap.height())
        self.begin = None
        self.end = None
        self.width = width
        self.height = height
        self.setMouseTracking(True)
        self.setCursor(Qt.BlankCursor)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.original_pixmap)
        
        # Draw darkened overlay
        overlay = QColor(0, 0, 0, 150)
        painter.fillRect(self.rect(), overlay)
        
        # Draw the translucent selection box
        cursor_pos = self.mapFromGlobal(QCursor.pos())
        box_rect = QRect(cursor_pos.x() - self.width // 2, 
                         cursor_pos.y() - self.height // 2, 
                         self.width, self.height)
        
        # Draw translucent fill inside the box
        painter.setCompositionMode(QPainter.CompositionMode_SourceOver)
        painter.fillRect(box_rect, QColor(255, 255, 255, 50))
        
        # Draw the box outline
        painter.setPen(QPen(Qt.white, 2, Qt.SolidLine))
        painter.drawRect(box_rect)
        
        # Draw the original image inside the box
        painter.setClipRect(box_rect)
        painter.drawPixmap(self.rect(), self.original_pixmap)
        painter.setClipRect(self.rect())

        # Draw grid lines and center crosshair lines
        grid_color = QColor(255, 255, 255, 100)  # Semi-transparent white for grid
        painter.setPen(QPen(grid_color, 1, Qt.SolidLine))
        
        # Number of sections (subdivisions) in each direction
        sections_x = 4
        sections_y = 4

        # Draw vertical grid lines
        section_width = self.width // sections_x
        for i in range(1, sections_x):
            x = box_rect.left() + i * section_width
            painter.drawLine(x, box_rect.top(), x, box_rect.bottom())

        # Draw horizontal grid lines
        section_height = self.height // sections_y
        for i in range(1, sections_y):
            y = box_rect.top() + i * section_height
            painter.drawLine(box_rect.left(), y, box_rect.right(), y)

        # Draw center crosshair lines
        crosshair_color = QColor(255, 255, 255, 150)  # Slightly more visible for center crosshair
        painter.setPen(QPen(crosshair_color, 1, Qt.SolidLine))
        
        # Vertical line for the center crosshair
        painter.drawLine(
            box_rect.center().x(), box_rect.top(),
            box_rect.center().x(), box_rect.bottom()
        )
        
        # Horizontal line for the center crosshair
        painter.drawLine(
            box_rect.left(), box_rect.center().y(),
            box_rect.right(), box_rect.center().y()
        )

    def mousePressEvent(self, event):
        self.take_screenshot()

    def mouseMoveEvent(self, event):
        self.update()

    def take_screenshot(self):
        cursor_pos = self.mapFromGlobal(QCursor.pos())
        x = cursor_pos.x() - self.width // 2
        y = cursor_pos.y() - self.height // 2
        screenshot = self.original_pixmap.copy(x, y, self.width, self.height)
        self.screenshotTaken.emit(screenshot)
        self.close()

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.take_screenshot()
        elif event.key() == Qt.Key_Escape:
            self.cancelled.emit()
            self.close()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    tool = ScreenshotTool()
    tool.show()
    sys.exit(app.exec_())
