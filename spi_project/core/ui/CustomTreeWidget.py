from PySide6.QtWidgets import QTreeWidget, QAbstractItemView
from PySide6.QtGui import QDropEvent
from PySide6.QtCore import Qt

class CustomTreeWidget(QTreeWidget):
    """自定义TreeWidget，实现特定的拖拽放置行为"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        # 启用拖拽功能
        self.setDragDropMode(QAbstractItemView.InternalMove)
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        
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