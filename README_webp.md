# E7 Asset WebP Generator

这是一个用于为e7asset目录下没有WebP版本的PNG文件生成WebP格式的Python脚本。

## 功能特性

- 🔍 **智能检测**: 自动扫描目录，找出缺失WebP版本的PNG文件
- 🎯 **无损压缩**: 支持无损和有损两种压缩模式
- 📊 **详细统计**: 显示文件大小、节省空间和压缩率
- ⚡ **批量处理**: 一次性处理所有缺失的文件
- 🛡️ **安全可靠**: 不会覆盖已存在的WebP文件

## 使用方法

### 1. 安装依赖

确保系统已安装ffmpeg：

```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt update
sudo apt install ffmpeg

# Windows
# 下载ffmpeg并添加到PATH
```

### 2. 运行脚本

```bash
cd /path/to/e7asset
python3 generate_webp.py
```

### 3. 选择压缩选项

脚本会提供两种压缩选项：

1. **无损压缩** (推荐)
   - 保持原始图像质量
   - 文件大小适中
   - 适合需要保持完美质量的场景

2. **有损压缩**
   - 可以设置质量参数 (1-100)
   - 文件更小
   - 适合对文件大小敏感的场景

## 输出示例

```
E7 Asset WebP Generator
==================================================
扫描目录: /path/to/e7asset
正在扫描PNG文件...
找到 771 个PNG文件
正在扫描WebP文件...
找到 771 个WebP文件

需要生成 0 个WebP文件
所有PNG文件都有对应的WebP版本！

现有文件统计:
PNG总大小: 882.6 MB
WebP总大小: 521.2 MB
已节省空间: 361.4 MB
```

## 技术细节

- 使用ffmpeg的libwebp编码器进行转换
- 支持递归扫描子目录
- 自动创建输出目录
- 提供详细的转换进度和结果统计

## 注意事项

- 脚本会跳过已存在的WebP文件
- 转换过程中会显示每个文件的处理状态
- 如果转换失败，会在最后列出失败的文件
- 建议在转换前备份重要文件

## 文件结构

```
e7asset/
├── generate_webp.py    # 主脚本
├── README_webp.md      # 使用说明
├── portrait/           # 图像文件目录
│   ├── *.png          # PNG文件
│   └── *.webp         # WebP文件
└── ...
```
