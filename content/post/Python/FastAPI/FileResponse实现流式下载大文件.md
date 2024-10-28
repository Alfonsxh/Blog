---
title: "FileResponse实现流式下载大文件"
date: 2024-10-28T19:02:51+08:00
lastmod: 2024-10-28T19:02:51+08:00
draft: true
keywords: ["Python", "FastAPI"]
description: "fastapi实现流式下载的一种方式"
tags: ["Python", "FastAPI"]                    # 归档 
categories: ["Python", "FastAPI"]                # 分类
author: "Alfons"

comment: true                 # 是否显示评论
# toc: true                     # 是否展示目录
# autoCollapseToc: false        # 是否展示下拉式目录
# postMetaInFooter: true        # 是否在页脚显示文章源信息
# hiddenFromHomePage: false     # 是否在首页隐藏

# 文章license
# contentCopyright: '<a href= "https://creativecommons.org/licenses/by-nc-sa/4.0/deed.en"> Creative Commons BY-NC-ND 3.0 </a>'

# reward: false                 # 是否展示支付二维码

# 数学公式
# mathjax: false
# mathjaxEnableSingleDollar: false
# mathjaxEnableAutoNumber: false

# 隐藏页眉和页脚
# hideHeaderAndFooter: false

# enableOutdatedInfoWarning: false

# 流程图
# flowchartDiagrams:
#   enable: true
#   options: ""

# 序列图
# sequenceDiagrams: 
#   enable: true
#   options: ""

---

FastAPI 框架中提供了下载文件的 Response -> FileResponse，但是默认的 FileResponse 返回类型，没有办法实现大文件的流式下载，需要进一步的加工。

<!--more-->

## FileResponse 实现

FastAPI（fastapi==0.61.2） 中 FileResponse 对象的定义如下:

```python
class FileResponse(Response):
    chunk_size = 4096
    
    ....
    
    def set_stat_headers(self, stat_result: os.stat_result) -> None:
        content_length = str(stat_result.st_size)
        last_modified = formatdate(stat_result.st_mtime, usegmt=True)
        etag_base = str(stat_result.st_mtime) + "-" + str(stat_result.st_size)
        etag = hashlib.md5(etag_base.encode()).hexdigest()

        self.headers.setdefault("content-length", content_length)
        self.headers.setdefault("last-modified", last_modified)
        self.headers.setdefault("etag", etag)

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if self.stat_result is None:
            try:
                stat_result = await aio_stat(self.path)
                self.set_stat_headers(stat_result)
            except FileNotFoundError:
                raise RuntimeError(f"File at path {self.path} does not exist.")
            else:
                mode = stat_result.st_mode
                if not stat.S_ISREG(mode):
                    raise RuntimeError(f"File at path {self.path} is not a file.")
            ....
```

可以看到，在调用 FileResponse 时，会优先设置 headers，其中包括了 `content-length`，这个标记将使浏览器默认下载全部的文件内容，再保存到本地

因此，我们可以通过删除 `content-length`，来实现文件的流式下载

```python
class QStreamingFileResponse(FileResponse):  # type: ignore

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:

        await send({
            "type": "http.response.start",
            "status": self.status_code,
            "headers": self.raw_headers,
        })
        if self.send_header_only:
            await send({"type": "http.response.body", "body": b"", "more_body": False})
        else:
            async with aiofiles.open(self.path, mode="rb") as file:
                more_body = True
                while more_body:
                    chunk = await file.read(self.chunk_size)
                    more_body = len(chunk) == self.chunk_size
                    await send({
                        "type": "http.response.body",
                        "body": chunk,
                        "more_body": more_body,
                    })
        if self.background is not None:
            await self.background()

@router.get("/file", response_class=QStreamingFileResponse)
async def get_proxy_big_file(
    request: Request,
    file_path: pathlib.Path,
) -> QStreamingFileResponse:
    return QStreamingFileResponse(
            path=str(file_path),
            filename=file_path.name,
            media_type='application/octet-stream',
        )
```