#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project ：Blog 
# @File    ：merge.py
# @Author  ：Alfons
# @Date    ：2022/6/14 21:57
import pathlib
import subprocess

# --------------- 目录配置 ---------------
# 新blog目录配置
new_blog_dir = pathlib.Path(__file__).parent
new_post_dir = new_blog_dir / "content" / "post"

# 旧blog目录配置
old_blog_dir = new_blog_dir.parent / "odl_blog"


def merge_md(
    old_md_dir: pathlib.Path,
    new_md_dir: pathlib.Path,
    new_md_tag: str,
):
    # 新md路径创建
    new_md_dir.mkdir(parents=True, exist_ok=True)

    # 遍历旧md文件目录下的文件，进行迁移
    for index, old_md_file in enumerate(old_md_dir.glob("**/*")):

        # 排除README
        if old_md_file.name.lower().startswith("readme") or not old_md_file.name.lower().endswith("md"):
            print(f"{old_md_file.name} not allow!!!")
            continue

        # 新md文件路径
        new_md_path = new_md_dir / str(old_md_file)[len(str(old_md_dir)) + 1:]
        new_md_path.parent.mkdir(parents=True, exist_ok=True)

        print(f"「{index}」开始迁移: {old_md_file} -> {new_md_path}")

        # 读取旧md文件git信息
        md_first_create_time = subprocess.run(
            f'echo `git log --pretty=format:"%ad" --date=format:"%Y-%m-%d %H:%M:%S" {old_md_file.name} | tail -1`',
            shell=True,
            cwd=old_md_file.parent,
            capture_output=True,
        ).stdout.strip().decode()

        md_last_change_time = subprocess.run(
            f'echo `git log -1 --pretty=format:"%ad" --date=format:"%Y-%m-%d %H:%M:%S" {old_md_file.name}`',
            shell=True,
            cwd=old_md_file.parent,
            capture_output=True,
        ).stdout.strip().decode()

        print(f"「{index}」{old_md_file.name} create time: {md_first_create_time}")
        print(f"「{index}」{old_md_file.name} last time: {md_last_change_time}")

        # 读取旧md文件内容
        if old_md_contents := old_md_file.read_text().splitlines():
            md_title = old_md_contents[0].strip()[1:].strip()
        else:
            md_title = old_md_file.name

        if old_md_file.parent != old_md_dir:
            md_tag = f'"{new_md_tag}", "{old_md_file.parent.name}"'
        else:
            md_tag = f'"{new_md_tag}"'

        # 格式化旧文件
        #   - 添加头
        #   - 添加 <!--more-->
        #   - 修改 images 路径
        new_md_contents = [
                              '---',
                              f'title: "{md_title}"',
                              f'date: {md_first_create_time}',
                              f'lastmod: {md_last_change_time}',
                              'draft: false',
                              f'keywords: [{md_tag}]',
                              f'description: "{md_title}"',
                              f'tags: [{md_tag}]',
                              f'categories: [{md_tag}]',
                              'author: "Alfons"',
                              '---',
                          ] + old_md_contents[1:]

        # 写入新文件
        new_md_path.write_text('\n'.join(new_md_contents))

        print(f"「{index}」结束迁移: {old_md_file} -> {new_md_path}")


if __name__ == '__main__':
    merge_info = [
        (old_blog_dir / "Python", new_post_dir / "Python", "Python"),
        (old_blog_dir / "Algorithms", new_post_dir / "Algorithms", "Algorithms"),
        (old_blog_dir / "Books", new_post_dir / "Books", "Books"),
        (old_blog_dir / "C++", new_post_dir / "C++", "C++"),
        (old_blog_dir / "Linux", new_post_dir / "Linux", "Linux"),
        (old_blog_dir / "设计模式", new_post_dir / "设计模式", "设计模式"),
        (old_blog_dir / "极客时间", new_post_dir / "极客时间", "极客时间"),
    ]

    for _old_md_dir, _new_md_dir, _new_md_tag in merge_info:
        merge_md(
            old_md_dir=_old_md_dir,
            new_md_dir=_new_md_dir,
            new_md_tag=_new_md_tag,
        )
