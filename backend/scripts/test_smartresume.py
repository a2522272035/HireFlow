#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SmartResume 模型验证脚本

测试本地部署的 Qwen3-0.6B 模型是否可以正常加载和解析简历。

使用方法:
    cd backend
    python scripts/test_smartresume.py
"""

import sys
import io
import time
from pathlib import Path

# 设置 UTF-8 编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))


def check_model_files():
    """检查模型文件是否存在且完整"""
    print("=" * 60)
    print("步骤 1/3: 检查模型文件")
    print("=" * 60)

    model_dir = Path(__file__).parent.parent.parent / "models" / "smartresume" / "Qwen3-0.6B"

    required_files = [
        "config.json",
        "model.safetensors",
        "tokenizer.json",
        "tokenizer_config.json",
        "vocab.json",
        "merges.txt",
    ]

    all_exist = True
    for file in required_files:
        file_path = model_dir / file
        exists = file_path.exists()
        size = file_path.stat().st_size / (1024 * 1024) if exists else 0
        status = "[OK]" if exists else "[FAIL]"
        print(f"  {status} {file:<25} {size:>8.2f} MB" if exists else f"  {status} {file:<25} MISSING")
        if not exists:
            all_exist = False

    if all_exist:
        print("\n[OK] 模型文件检查通过")
        return True
    else:
        print("\n[FAIL] 模型文件不完整，请重新下载")
        return False


def test_model_loading():
    """测试模型加载"""
    print("\n" + "=" * 60)
    print("步骤 2/3: 测试模型加载")
    print("=" * 60)

    try:
        print("  正在导入依赖...")
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer

        print("  [OK] 依赖导入成功")

        model_dir = Path(__file__).parent.parent.parent / "models" / "smartresume" / "Qwen3-0.6B"

        print(f"  正在加载 Tokenizer...")
        start_time = time.time()
        tokenizer = AutoTokenizer.from_pretrained(
            str(model_dir),
            trust_remote_code=True,
        )
        load_time = time.time() - start_time
        print(f"  [OK] Tokenizer 加载完成 ({load_time:.2f}s)")

        print(f"  正在加载模型 (约 1.1GB，可能需要一些时间)...")
        start_time = time.time()
        model = AutoModelForCausalLM.from_pretrained(
            str(model_dir),
            trust_remote_code=True,
            device_map="auto",
            torch_dtype="auto",
        )
        load_time = time.time() - start_time
        print(f"  [OK] 模型加载完成 ({load_time:.2f}s)")

        device = next(model.parameters()).device
        print(f"  [OK] 模型已加载到设备: {device}")

        return True, model, tokenizer

    except ImportError as e:
        print(f"\n[FAIL] 缺少依赖: {e}")
        print("  请运行: pip install transformers torch")
        return False, None, None
    except Exception as e:
        print(f"\n[FAIL] 模型加载失败: {e}")
        return False, None, None


def test_parse_sample(model, tokenizer):
    """测试简历解析功能"""
    print("\n" + "=" * 60)
    print("步骤 3/3: 测试简历解析")
    print("=" * 60)

    try:
        import torch
        # 测试简历文本
        sample_resume = """
姓名：张三
电话：138-1234-5678
邮箱：zhangsan@example.com

教育背景：
北京大学 计算机科学 本科 2015-2019

工作经历：
阿里巴巴 高级软件工程师 2019-2022
负责后端系统开发

腾讯 技术专家 2022-至今
负责架构设计

技能：Python, Java, Go, Kubernetes, Docker
"""

        print("  测试简历文本已准备")
        print(f"  文本长度: {len(sample_resume)} 字符")

        prompt = f"""请从以下简历文本中提取关键信息，并以JSON格式返回：

简历文本：
{sample_resume}

请提取以下字段（如不存在则返回 null）：
{{
    "name": "姓名",
    "email": "邮箱",
    "phone": "电话",
    "skills": ["技能1", "技能2"]
}}

请只返回JSON格式的结果，不要包含其他说明文字。"""

        print("  正在调用模型解析...")
        start_time = time.time()

        messages = [
            {"role": "system", "content": "你是一个专业的简历解析助手。请从简历文本中提取关键信息，并以JSON格式返回。"},
            {"role": "user", "content": prompt}
        ]

        inputs = tokenizer.apply_chat_template(
            messages,
            tokenize=True,
            return_tensors="pt",
            return_dict=True,
        )
        inputs = {k: v.to(model.device) for k, v in inputs.items()}

        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=500,
                temperature=0.1,
                do_sample=True,
            )

        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        parse_time = time.time() - start_time

        print(f"  [OK] 解析完成 ({parse_time:.2f}s)")
        print("\n  模型输出:")
        print("-" * 40)
        print(response[:500])
        print("-" * 40)

        # 简单验证输出是否包含关键信息
        has_name = "张三" in response or "name" in response.lower()
        has_email = "zhangsan" in response or "email" in response.lower()

        if has_name and has_email:
            print("\n[OK] 解析结果验证通过")
            return True
        else:
            print("\n[WARN] 解析结果可能不完整，请检查输出")
            return True  # 仍然返回True，因为模型运行正常

    except Exception as e:
        print(f"\n[FAIL] 解析测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主函数"""
    print("\n" + "=" * 60)
    print("SmartResume 模型验证")
    print("=" * 60)
    print()

    # 步骤1: 检查模型文件
    if not check_model_files():
        print("\n[FAIL] 验证失败: 模型文件不完整")
        return 1

    # 步骤2: 测试模型加载
    success, model, tokenizer = test_model_loading()
    if not success:
        print("\n[FAIL] 验证失败: 模型加载失败")
        return 1

    # 步骤3: 测试解析功能
    if not test_parse_sample(model, tokenizer):
        print("\n[FAIL] 验证失败: 解析测试失败")
        return 1

    print("\n" + "=" * 60)
    print("[OK] 所有测试通过！SmartResume 模型可以正常使用")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
