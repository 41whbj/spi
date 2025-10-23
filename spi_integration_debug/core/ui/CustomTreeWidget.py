from PySide6.QtWidgets import QTreeWidget, QAbstractItemView, QStyledItemDelegate, QLineEdit
from PySide6.QtGui import QDropEvent, QPainter, QColor, QPen
from PySide6.QtCore import Qt
from PySide6.QtCore import QRect
from PySide6.QtWidgets import QStyle

class NonEditableDelegate(QStyledItemDelegate):
    """不可编辑委托，用于禁止某些列的编辑"""
    def createEditor(self, parent, option, index):
        # 返回None表示该单元格不可编辑
        return None

class EditableDelegate(QStyledItemDelegate):
    """可编辑委托，用于提供白色背景的编辑器以避免干扰"""
    
    def createEditor(self, parent, option, index):
        """创建编辑器"""
        editor = QLineEdit(parent)

        print("进入EditableDelegate委托")
        
        # 设置编辑器样式，背景为白色以避免干扰
        editor.setStyleSheet("""
        QLineEdit {
            background-color: white;
            border: 1px solid #0078D7;
            selection-background-color: #0078D7;
            selection-color: white;
        }
        """)
        
        return editor

class TestGroupDelegate(QStyledItemDelegate):
    """测试组委托，用于自定义测试组和数据项的样式，并控制子项高度"""

    def __init__(self, parent=None, child_item_height=30):
        super().__init__(parent)
        self.child_item_height = child_item_height

    def paint(self, painter: QPainter, option, index):
        # 获取项
        item = self.parent().itemFromIndex(index)

        # 判断是否是第一列并且是顶级项（测试组）
        if index.column() == 0 and item and item.parent() is None:
            # 保存画家状态
            painter.save()

            try:
                # 绘制背景（根据选中状态选择颜色）
                bg_color = QColor("#ffffff")  # 默认背景色
                text_color = QColor("#404040")  # 默认文字色

                if option.state & QStyle.State_Selected:
                    bg_color = QColor("#e6f7ff")
                    text_color = QColor("#202020")
                elif option.state & QStyle.State_MouseOver:
                    bg_color = QColor("#f0f0f0")

                painter.fillRect(option.rect, bg_color)

                # 绘制复选框
                self.drawCheckbox(painter, option, item)

                # 绘制文本（加粗）
                self.drawText(painter, option, item, text_color)

                # 可选：绘制下划线
                # self.drawBottomLine(painter, option)
            finally:
                # 确保总是恢复画家状态
                painter.restore()

            # 直接返回，跳过默认绘制
            return

        # 对于普通项（子项或非首列），使用系统默认绘制 + 自定义高度支持
        super().paint(painter, option, index)

    def createEditor(self, parent, option, index):
        """创建编辑器，确保所有项都可以编辑"""
        # 获取项
        item = self.parent().itemFromIndex(index)
        
        # 对于所有项，创建QLineEdit编辑器并设置白色背景
        editor = QLineEdit(parent)
        editor.setStyleSheet("""
        QLineEdit {
            background-color: white;
            border: 1px solid #0078D7;
            selection-background-color: #0078D7;
            selection-color: white;
        }
        """)
        
        return editor

    def sizeHint(self, option, index):
        # 获取默认的尺寸提示
        size = super().sizeHint(option, index)

        # 获取项
        item = self.parent().itemFromIndex(index)

        # 检查是否是非顶级项（子项）
        if item and item.parent() is not None:
            # 设置子项高度
            size.setHeight(self.child_item_height)

        return size

    def drawText(self, painter, option, item, text_color):
        """绘制文本（加粗）"""
        # 获取文本矩形区域
        text_rect = self.getTextRect(option.rect)

        # 设置字体（加粗）
        font = painter.font()
        font.setBold(True)
        font.setFamily("Microsoft YaHei")
        painter.setFont(font)
        painter.setPen(text_color)

        # 获取文本
        text = item.text(0)

        # 绘制文本
        painter.drawText(text_rect, Qt.AlignLeft | Qt.AlignVCenter, text)

    def drawCheckbox(self, painter, option, item):
        """自定义绘制复选框"""
        # 获取复选框矩形区域
        checkbox_rect = self.getCheckboxRect(option.rect)

        # 获取项的选中状态
        checked = item.checkState(0) == Qt.Checked

        # 绘制复选框边框
        pen = painter.pen()
        painter.setPen(QPen(Qt.gray, 1))
        painter.setBrush(Qt.NoBrush if not checked else QColor("#0078d4"))
        painter.drawRect(checkbox_rect)

        # 如果选中，绘制"√"符号
        if checked:
            painter.setPen(QPen(Qt.white, 2))
            painter.drawLine(
                checkbox_rect.left() + 3, checkbox_rect.top() + 7,
                checkbox_rect.left() + 6, checkbox_rect.top() + 10
            )
            painter.drawLine(
                checkbox_rect.left() + 6, checkbox_rect.top() + 10,
                checkbox_rect.left() + 12, checkbox_rect.top() + 4
            )

        # 恢复画笔
        painter.setPen(pen)

    def drawBottomLine(self, painter, option):
        """绘制底部横线"""
        # 保存当前画笔
        pen = painter.pen()

        # 设置横线样式
        line_pen = QPen()
        line_pen.setColor(QColor("#5205EB"))  # 黑灰色线条
        line_pen.setWidth(1)  # 线条宽度为1像素
        painter.setPen(line_pen)

        # 绘制底部横线
        bottom_y = option.rect.bottom()
        painter.drawLine(
            option.rect.left(), bottom_y,
            option.rect.right(), bottom_y
        )

        # 恢复原来的画笔
        painter.setPen(pen)

    def getCheckboxRect(self, item_rect):
        """计算复选框的矩形区域"""
        checkbox_size = 16
        margin = 4
        return QRect(
            item_rect.left() + margin,
            item_rect.top() + (item_rect.height() - checkbox_size) // 2,
            checkbox_size,
            checkbox_size
        )

    def getTextRect(self, item_rect):
        """计算文本的矩形区域"""
        checkbox_width = 25  # 复选框宽度+间距
        return QRect(
            item_rect.left() + checkbox_width,
            item_rect.top(),
            item_rect.width() - checkbox_width,
            item_rect.height()
        )

class CustomTreeWidget(QTreeWidget):
    """自定义TreeWidget，实现特定的拖拽放置行为"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        # 启用拖拽功能
        self.setDragDropMode(QAbstractItemView.InternalMove)
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        # 存储列的可编辑性设置
        self.column_editable = {}
        
        # 注册自定义委托
        self.test_group_delegate = TestGroupDelegate(self, child_item_height=28)
        self.setItemDelegate(self.test_group_delegate)
        
        # 创建白色背景的编辑委托
        self.editable_delegate = EditableDelegate(self)
        
    def setColumnEditable(self, column, editable):
        """设置指定列是否可编辑"""
        self.column_editable[column] = editable
        if not editable:
            # 为不可编辑的列设置自定义委托
            self.setItemDelegateForColumn(column, NonEditableDelegate(self))
        else:
            # 为可编辑的列使用白色背景的编辑委托
            self.setItemDelegateForColumn(column, self.editable_delegate)
    
    def dropEvent(self, event: QDropEvent):
        """重写dropEvent以控制放置行为"""
        # print("自定义dropEvent被调用")  # 调试信息
        
        # 获取被拖拽的数据
        mime_data = event.mimeData()
        
        if mime_data.hasFormat('application/x-qabstractitemmodeldatalist'):
            # 获取目标位置的项
            pos = event.position().toPoint() if hasattr(event, 'position') else event.pos()
            target_item = self.itemAt(pos)
            
            # 获取被拖拽的项
            source_item = self.currentItem()
            
            if source_item:
                # 检查被拖拽的项是否是顶级项（测试组）
                is_source_top_level = source_item.parent() is None
                
                if target_item:
                    # 检查目标项是否是顶级项（测试组）
                    is_target_top_level = target_item.parent() is None
                    
                    # 如果被拖拽的是顶级项（测试组）
                    if is_source_top_level:
                        # 只允许在顶级项之间移动（同级移动）
                        if is_target_top_level:
                            # 允许移动到顶级项之间（但不能成为其他顶级项的子项）
                            drop_indicator = self.dropIndicatorPosition()
                            if drop_indicator != QAbstractItemView.OnItem:
                                # 只允许在项之间放置，不允许在项上放置
                                # print("允许顶级项移动")
                                super().dropEvent(event)
                            else:
                                # print("拒绝放置在项上")
                                event.ignore()
                        else:
                            # 不允许将顶级项拖拽到非顶级项上
                            # print("拒绝放置在非顶级项上")
                            event.ignore()
                    else:
                        # 被拖拽的是子项（测试数据）
                        # 禁止child item通过拖拽变成顶级项
                        if is_target_top_level:
                            # 允许将子项拖拽到顶级项上（作为子项）
                            drop_indicator = self.dropIndicatorPosition()
                            if drop_indicator == QAbstractItemView.OnItem:
                                # 只有当放置在项上时才允许（作为子项）
                                # print("允许子项作为子项添加")
                                super().dropEvent(event)
                            else:
                                # 当放置在项之间时，检查是否在同一父项内
                                # print("允许子项在同一父项内排序")
                                # 需要特殊处理：确保子项保持在原来的父项中
                                source_parent = source_item.parent()
                                target_parent = target_item
                                
                                # 如果源和目标有相同的父项，则允许重新排序
                                if source_parent == target_parent:
                                    super().dropEvent(event)
                                else:
                                    # 否则拒绝这种拖拽操作
                                    # print("拒绝子项在不同父项间移动")
                                    event.ignore()
                        else:
                            # 不允许将子项拖拽到非顶级项上
                            # 但允许在同一父项内的子项之间移动
                            source_parent = source_item.parent()
                            target_parent = target_item.parent()
                            
                            if source_parent == target_parent:
                                # print("允许子项在相同父项内排序")
                                super().dropEvent(event)
                            else:
                                # print("拒绝子项放置在不同父项的非顶级项上")
                                event.ignore()
                else:
                    # 没有目标项，可能是拖拽到空白区域
                    if not is_source_top_level:
                        # 不允许子项变成顶级项
                        # print("拒绝子项成为顶级项")
                        event.ignore()
                    else:
                        # 允许顶级项移动到空白区域
                        # print("允许顶级项移动到空白区域")
                        super().dropEvent(event)
            else:
                # 默认处理
                # print("默认处理")
                super().dropEvent(event)
        else:
            # print("非mime数据拖放")
            super().dropEvent(event)