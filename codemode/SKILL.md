---
name: codemode
description: Chạy JavaScript do model viết trong sandbox QuickJS (worker thread) với 4 tools hệ thống read/write/exec/mcp. Dùng khi cần gộp nhiều bước đọc-ghi-chạy lệnh-gọi MCP thành một script duy nhất thay vì gọi từng tool lẻ — các nested tool calls không đi vào LLM context, chỉ output và return value đi vào.
---

# Codemode — gộp nhiều bước đọc/ghi file, chạy shell, gọi MCP thành một script JS trong sandbox

Hệ thống đã đăng ký sẵn codemode làm mặc định: chạy JS do model viết trong QuickJS VM
(WebAssembly), capability duy nhất là gọi các tools được inject từ host.
Dựa trên `@earendil-works/pi-codemode@1.2.0` (pin exact). Code tại `~/workspace/codemode/`,
binary tại `~/.local/bin/codemode`, state tại `~/.config/codemode/store.json`.
Repo public: `thoitiettxl-cyber/muse-codemode` (kèm `smoke.sh` — 10 checks).
Mọi thứ nằm dưới `~`, nên theo AGENTS.md:62 sẽ còn sau VM replace (home là volume btrfs riêng mount tại `/home/hatch`).

## Khi nào dùng thay vì gọi tool lẻ

- Cần **chuỗi nhiều bước** (đọc file → xử lý → ghi file → chạy lệnh → gọi MCP) mà mỗi bước
  phụ thuộc kết quả bước trước: viết một script, chạy một lần, chỉ nhận output + return value.
- Cần **lặp / rẽ nhánh / try-catch** quanh các tool calls mà không tốn nhiều turn LLM.
- KHÔNG dùng khi chỉ cần 1-2 tool call đơn giản — gọi trực tiếp nhanh hơn.

## Cách dùng

```bash
codemode script.js              # chạy script từ file
echo 'return 1+1' | codemode    # hoặc từ stdin
codemode --declarations         # in TypeScript declarations của 4 tools (luôn đúng với code)
codemode --json script.js       # output JSON máy đọc được
codemode --timeout-ms 120000 script.js
codemode --no-store script.js   # không dùng store() persistent
```

Script là body của một async function: top-level `await` và `return` dùng được.
Dòng đầu có thể là: `// @options: {"max_output_tokens": 2000, "timeout_ms": 30000}`
(`timeout_ms` là deadline cứng cho cả script, `max_output_tokens` cắt output).

Trong script có: `tools.read/write/exec/mcp`, `ALL_TOOLS`, `text()`, `image()`,
`console.*`, `exit()`, `store(key, value)` / `load(key)` (persist qua các lần chạy).

Exit code: 0 ok, 1 lỗi script, 2 timeout, 3 aborted, 4 lỗi sandbox/host,
5 dòng `// @options:` sai, 6 sai cách dùng.

## Tools mặc định (xem `codemode --declarations` để có bản mới nhất)

- `read({path, encoding?, maxBytes?})` — đọc file dưới `$HOME` (relative resolve từ `$HOME`).
- `write({path, content, encoding?})` — ghi file dưới `$HOME`, tự tạo thư mục cha.
- `exec({command, args?, cwd?, timeoutMs?, shell?, maxOutputBytes?})` — chạy lệnh;
  **luôn có timeout** (mặc định 30s, tối đa 120s), lệnh treo bị SIGKILL và báo lỗi;
  `cwd` mặc định `$HOME` và phải nằm dưới `$HOME`; `shell:true` để dùng pipe/glob qua bash.
- `mcp({server, name, args?, timeoutMs?})` — gọi tool MCP qua **session persistent**
  (connect 1 lần/run, tái dùng cho mọi call — workflow nhiều bước giữ được
  server-side state giữa các call); servers: openai-docs, xai-docs,
  anthropic-docs, cloudflare, context7, exa, ksht, firecrawl, inspo.

Mọi path trong `read`/`write`/`exec.cwd` đều bị chặn nếu thoát khỏi `$HOME`.

## Ví dụ script mẫu

```js
// đọc package.json, đếm dependencies, ghi báo cáo, trả về số lượng
const src = await tools.read({ path: "workspace/codemode/package.json" });
const deps = Object.keys(JSON.parse(src).dependencies ?? {});
const out = await tools.write({
  path: "workspace/codemode/deps.txt",
  content: deps.join("\n") + "\n",
});
text(`wrote ${out.bytes} bytes`);
const ls = await tools.exec({ command: "ls", args: ["workspace/codemode"] });
text(ls.stdout);
return deps.length;
```

```js
// gọi MCP: tra docs của quickjs qua context7 (resolve libraryId trước, timeout riêng 20s)
const lib = await tools.mcp({
  server: "context7",
  name: "resolve-library-id",
  args: { query: "QuickJS memory limit", libraryName: "quickjs" },
  timeoutMs: 20000,
});
text(String(lib).slice(0, 500)); // chọn libraryId (dạng "/org/project") từ kết quả
const doc = await tools.mcp({
  server: "context7",
  name: "query-docs",
  args: { libraryId: "/quickjs-ng/quickjs", query: "QuickJS memory limit" },
  timeoutMs: 20000,
});
text(doc.slice(0, 500));
return "done";
```

## Lưu ý

- Script lỗi (throw không catch, tool reject) → `result.ok=false`, CLI exit 1, stderr có stack `codemode.js:<line>`.
- Script treo không gọi tool (vòng lặp vô hạn) → fail `timeout`, worker bị terminate, runner không treo.
- `store()`/`load()` lưu vào `~/.config/codemode/store.json`, dùng `--no-store` để tắt.
- Giới hạn: VM QuickJS là interpreter (tính toán nặng chậm hơn V8); không có timers/fetch/process/require trong script — mọi I/O đều qua tools.
