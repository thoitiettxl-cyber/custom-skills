---
name: native-web-search
description: "Quick web-research pattern: separate the query from its purpose, get a concise summary with full source URLs per finding. Use when you need fast internet research with explicit URLs and disagreements called out."
---

# Tìm kiếm web nhanh theo pattern query + purpose — dùng khi cần research nhanh, tóm tắt gọn kèm URL nguồn đầy đủ cho từng phát hiện

(Bản gốc đi kèm `search.mjs` chạy trên Pi runtime — đã bỏ theo quyết định của Boss.
Skill này chỉ giữ lại pattern, ánh xạ sang công cụ search của hệ mình.)

## Pattern

Tách bạch hai thứ trong mọi lần research:

- **query**: cái cần tìm (vd "latest python release")
- **purpose**: vì sao cần (vd "update dependency notes") — purpose quyết định
  thông tin nào đáng giữ, thông tin nào bỏ.

## Cách chạy trong hệ mình

- Research nhanh: `browser.search`, đặt `verticals` phù hợp
  (`news`, `sports`, `weather`, `finance`, `datetime`).
- Research sâu, cần đối chiếu nhiều nguồn: `browser.deep_research`.
- Fallback khi cần: Exa / Firecrawl qua MCP.

## Output expectations

Mọi kết quả research theo pattern này phải có:

- 3–7 key findings; mỗi finding gồm: tiêu đề, vì sao nó quan trọng **cho
  purpose đã nêu**, và full canonical URL (`https://...`)
- chỗ nào các nguồn mâu thuẫn nhau thì gọi tên rõ, không giấu
- kết thúc bằng khuyến nghị ngắn: nên tin nguồn nào trước

## Prompt mẫu (khi giao research cho subagent hoặc model khác)

```
Search the internet for: <query>

Purpose: <purpose>

Return a concise research summary with:
- 3 to 7 key findings
- for every finding: title, why it matters for this purpose, and a full canonical URL (https://...)
- if multiple sources disagree, call that out
- finish with a short recommendation on which source(s) to trust first.
```

## Notes

- Mỗi finding phải gắn URL đọc được thật — không bịa URL để lấp chỗ trống.
- Phân biệt rõ "đã đọc từ nguồn" và "suy luận" (xem skill `verify-before-claiming`).
