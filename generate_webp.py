#!/usr/bin/env python3
"""
E7 Asset WebP Generator
为e7asset目录下没有WebP版本的PNG文件生成WebP格式
"""

import os
import subprocess
import sys
from pathlib import Path
from typing import List, Set, Tuple

def find_png_files(directory: Path) -> List[Path]:
    """查找目录下所有的PNG文件"""
    png_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.png'):
                png_files.append(Path(root) / file)
    return png_files

def find_webp_files(directory: Path) -> Set[Path]:
    """查找目录下所有的WebP文件"""
    webp_files = set()
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.webp'):
                webp_files.add(Path(root) / file)
    return webp_files

def get_webp_path(png_path: Path) -> Path:
    """根据PNG文件路径生成对应的WebP文件路径"""
    return png_path.with_suffix('.webp')

def check_ffmpeg() -> bool:
    """检查ffmpeg是否可用"""
    try:
        subprocess.run(['ffmpeg', '-version'], 
                      capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def convert_png_to_webp(png_path: Path, webp_path: Path, 
                       lossless: bool = True, quality: int = 100) -> bool:
    """
    使用ffmpeg将PNG转换为WebP
    
    Args:
        png_path: PNG文件路径
        webp_path: 输出WebP文件路径
        lossless: 是否使用无损压缩
        quality: 质量设置（1-100）
    
    Returns:
        bool: 转换是否成功
    """
    try:
        # 确保输出目录存在
        webp_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 构建ffmpeg命令
        cmd = [
            'ffmpeg',
            '-i', str(png_path),
            '-c:v', 'libwebp',
            '-y',  # 覆盖已存在的文件
        ]
        
        if lossless:
            cmd.extend(['-lossless', '1'])
        else:
            cmd.extend(['-quality', str(quality)])
        
        cmd.append(str(webp_path))
        
        # 执行转换
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            return True
        else:
            print(f"转换失败 {png_path}: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"转换出错 {png_path}: {e}")
        return False

def get_file_size(file_path: Path) -> int:
    """获取文件大小（字节）"""
    try:
        return file_path.stat().st_size
    except OSError:
        return 0

def format_size(size_bytes: int) -> str:
    """格式化文件大小显示"""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.1f} MB"

def main():
    """主函数"""
    print("E7 Asset WebP Generator")
    print("=" * 50)
    
    # 检查ffmpeg
    if not check_ffmpeg():
        print("错误: 未找到ffmpeg，请先安装ffmpeg")
        print("macOS: brew install ffmpeg")
        sys.exit(1)
    
    # 获取脚本所在目录
    script_dir = Path(__file__).parent
    print(f"扫描目录: {script_dir}")
    
    # 查找所有PNG文件
    print("正在扫描PNG文件...")
    png_files = find_png_files(script_dir)
    print(f"找到 {len(png_files)} 个PNG文件")
    
    # 查找所有WebP文件
    print("正在扫描WebP文件...")
    webp_files = find_webp_files(script_dir)
    print(f"找到 {len(webp_files)} 个WebP文件")
    
    # 找出缺失WebP版本的PNG文件
    missing_webp = []
    for png_file in png_files:
        webp_file = get_webp_path(png_file)
        if webp_file not in webp_files:
            missing_webp.append((png_file, webp_file))
    
    print(f"\n需要生成 {len(missing_webp)} 个WebP文件")
    
    if not missing_webp:
        print("所有PNG文件都有对应的WebP版本！")
        
        # 显示现有文件的统计信息
        total_png_size = sum(get_file_size(f) for f in png_files)
        total_webp_size = sum(get_file_size(f) for f in webp_files)
        total_saved = total_png_size - total_webp_size
        
        print(f"\n现有文件统计:")
        print(f"PNG总大小: {format_size(total_png_size)}")
        print(f"WebP总大小: {format_size(total_webp_size)}")
        print(f"已节省空间: {format_size(total_saved)}")
        return
    
    # 询问压缩选项
    print("\n压缩选项:")
    print("1. 无损压缩 (推荐)")
    print("2. 有损压缩 (更小文件)")
    choice = input("请选择压缩方式 (1-2, 默认1): ").strip()
    
    lossless = True
    quality = 100
    
    if choice == "2":
        lossless = False
        quality_input = input("请输入质量 (1-100, 默认80): ").strip()
        try:
            quality = int(quality_input) if quality_input else 80
            quality = max(1, min(100, quality))
        except ValueError:
            quality = 80
    
    # 询问用户是否继续
    response = input(f"\n是否开始转换这 {len(missing_webp)} 个文件？(y/N): ").strip().lower()
    if response not in ['y', 'yes']:
        print("取消转换")
        return
    
    # 开始转换
    print(f"\n开始转换 (压缩方式: {'无损' if lossless else f'有损-质量{quality}'})...")
    success_count = 0
    total_size_saved = 0
    failed_files = []
    
    for i, (png_file, webp_file) in enumerate(missing_webp, 1):
        print(f"[{i}/{len(missing_webp)}] 转换: {png_file.name}")
        
        # 获取原始文件大小
        original_size = get_file_size(png_file)
        
        # 转换文件
        if convert_png_to_webp(png_file, webp_file, lossless=lossless, quality=quality):
            # 获取转换后文件大小
            webp_size = get_file_size(webp_file)
            size_saved = original_size - webp_size
            total_size_saved += size_saved
            
            print(f"  ✓ 成功 - 原始: {format_size(original_size)}, "
                  f"WebP: {format_size(webp_size)}, "
                  f"节省: {format_size(size_saved)}")
            success_count += 1
        else:
            print(f"  ✗ 失败")
            failed_files.append(png_file)
    
    # 显示总结
    print("\n" + "=" * 50)
    print(f"转换完成!")
    print(f"成功: {success_count}/{len(missing_webp)}")
    print(f"总节省空间: {format_size(total_size_saved)}")
    
    if failed_files:
        print(f"\n失败的文件:")
        for failed_file in failed_files:
            print(f"  - {failed_file}")
    
    # 显示最终统计
    print(f"\n最终统计:")
    all_png_files = find_png_files(script_dir)
    all_webp_files = find_webp_files(script_dir)
    total_png_size = sum(get_file_size(f) for f in all_png_files)
    total_webp_size = sum(get_file_size(f) for f in all_webp_files)
    total_saved = total_png_size - total_webp_size
    
    print(f"PNG总大小: {format_size(total_png_size)}")
    print(f"WebP总大小: {format_size(total_webp_size)}")
    print(f"总节省空间: {format_size(total_saved)}")
    if total_png_size > 0:
        compression_ratio = (total_saved / total_png_size) * 100
        print(f"压缩率: {compression_ratio:.1f}%")

if __name__ == "__main__":
    main()
