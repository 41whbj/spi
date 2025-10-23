此文件夹展示导入文件夹和yml的模板及用例，下文也提供对应的模板、用例。

### yml文件

测试组对应的mode_group.yml的模板及用例，测试组现无导入功能，只能跟随文件夹导入：

```yaml
"mode_group":
  "新建分组1": []

# use example

# "mode_group":
#   "新建分组1":
#     - "name": "测试数据1"
#       "data": "AA 11"
#   "新建分组2":
#     - "name": "测试数据2"
#       "data": "AA 22"
#     - "name": "测试数据3"
#       "data": "AA 22"
```

数据组对应的data_group的模板及用例，数据组可在项目界面通过导入按钮导入：

```yaml
"data_group_name": ""
"spi_config":
  "vcc": ""
  "io": ""
  "speed": ""
  "clk": ""
  "bit": ""
  "s_or_q": ""
  "rx_size": ""
"data_group": []

# use example

# "data_group_name": "数据组1"
# "spi_config":
#   "vcc": "关闭"
#   "io": "1.8V" 
#   "speed": "937.5K"
#   "clk": "LOW/1EDG"
#   "bit": "MSB"
#   "s_or_q": "全单线SPI"
#   "rx_size": "32字节"
# "data_group":
#   - "name": "测试数据3"
#     "data": "AA 11"
#   - "name": "测试数据4"
#     "data": "AA 22"
```

### 文件夹

导入文件夹project_config的结构组成：

```
project_config/
├── top.yml                  # 项目顶层配置文件，命名必须为top.yml
├── mode_group/
|   ├── mode_group.yml       # 测试组分组
├── group/
│   ├── test1.yml            # 数据组1
│   └── test2.yml            # 数据组2
|   └── ·····
└── markdown/
    ├── 示例.md               # 说明文档，支持图片导入，但图片缩放会有问题
    └── 示例.assets/
        └── png# 文档相关图片资源
```

top.yml的的模板及用例：

```yaml
"project_name": ""
"data_group_path": []
"markdown_path": []

# use example

# "project_name": "SPI测试项目"
# "data_group_path":                                        
#  - "project_config/group/test1.yml"
#  - "project_config/group/test2.yml"
# "markdown_path": "markdown/示例.md"
```

