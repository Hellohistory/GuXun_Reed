# 项目说明

未来将要支持的**PCCK** 是自定义的文件类型，用于服务于本软件的需要。

本文档旨在解释如何使用和处理 `.pcck` 文件类型，并介绍了项目上的一些功能。

## 关于 .pcck 文件

`.pcck` 文件是一种对 JSON 格式的拓展，用于存储图床相关的信息。每个 `.pcck` 文件内包含一个 JSON 数组，数组中的每个对象描述一个图床实体。以下是 `.pcck` 文件的基本结构：

```json
[
    {
        "picture_bed_name": ""
    },
    {
        "file_name": "",
        "file_extension": "",
        "ID": "",
        "bookmark": ""
    }
]
```

- `picture_bed_name`：指定使用的图床的名称。
- `file_name`：文件名。
- `file_extension`：文件扩展名。
- `ID`：文件的唯一标识。
- `bookmark`：文件的书签信息。

## 项目功能

本项目实现了一种将图床外链本地化的视图。目前支持的图床包括：

1. **Picshack**

不同图床提供的查看和下载内容不同，因此需要对每种图床进行独立的处理。

## 支持功能

基于已实现的功能，对 `.pcck` 文件进行了一些支持。以下是支持的功能列表：

1. **图床选择和信息记录**：在 `.pcck` 文件中记录所选图床的名称和相关信息。
2. **文件信息记录**：记录每个文件的名称、扩展名、唯一标识和书签信息。
3. **本地化视图**：实现图床外链的本地化视图，使用户能够更方便地查看和管理文件。
4. **Picshack 支持**：目前支持 Picshack 图床，根据其特定的查看和下载内容进行处理。

## 下一步计划

1. **新增图床支持**：考虑将更多图床纳入支持范围，扩展用户的选择。
2. **图床特定处理**：根据不同图床的特点，优化文件的本地化视图和处理方式。

