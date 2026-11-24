-- Pandoc Lua filter for md2latex-ptit report preparation
-- Normalizes Markdown structure before LaTeX emission across LuaLaTeX, XeLaTeX, and pdfLaTeX.

local stringify = pandoc.utils.stringify

local config = {
  strip_cover = "none",
  strip_heading_numbers = true,
  code_listings = true,
  code_verbatim = false,
  prefer_vector_pdf = true,
  callout_boxes = true,
  adaptive_tables = true,
  landscape_figures = {},
}

local CALLOUT_MAP = {
  NOTE = { title = "Note", style = "calloutnote" },
  TIP = { title = "Tip", style = "callouttip" },
  IMPORTANT = { title = "Important", style = "calloutimportant" },
  WARNING = { title = "Warning", style = "calloutwarning" },
  CAUTION = { title = "Caution", style = "calloutcaution" },
}

local LISTINGS_LANG_MAP = {
  sql = "SQL",
  plsql = "SQL",
  postgresql = "SQL",
  mysql = "SQL",
  sqlite = "SQL",
  oracle = "SQL",
  json = "json",
  jsonc = "json",
  yaml = "yaml",
  yml = "yaml",
  python = "Python",
  py = "Python",
  java = "Java",
  bash = "bash",
  sh = "bash",
  shell = "bash",
  zsh = "bash",
  c = "C",
  cpp = "C++",
  ["c++"] = "C++",
  tex = "TeX",
  latex = "TeX",
  html = "HTML",
  xml = "XML",
}

local function meta_bool(val, default)
  if val == nil then
    return default
  end
  if type(val) == "boolean" then
    return val
  end
  local s = string.lower(stringify(val))
  if s == "true" or s == "yes" or s == "1" then
    return true
  end
  if s == "false" or s == "no" or s == "0" then
    return false
  end
  return default
end

local function meta_str(val, default)
  if val == nil then
    return default
  end
  local s = stringify(val)
  if s == "" then
    return default
  end
  return s
end

local function basename(path)
  return path:match("([^/\\]+)$") or path
end

local function file_exists(path)
  local candidates = { path }
  if PANDOC_STATE and PANDOC_STATE.resource_path then
    for _, dir in ipairs(PANDOC_STATE.resource_path) do
      if dir and dir ~= "" and dir ~= "." then
        table.insert(candidates, dir .. "/" .. path)
      end
    end
  end
  for _, candidate in ipairs(candidates) do
    local f = io.open(candidate, "rb")
    if f then
      f:close()
      return true
    end
  end
  return false
end

local function trim(s)
  return (s:gsub("^%s+", ""):gsub("%s+$", ""))
end

local function escape_latex_chars(s, break_identifiers)
  local out = {}
  local len = #s
  local break_set = { ["_"] = true, ["."] = true, ["/"] = true, ["("] = true, [":"] = true }
  for i = 1, len do
    local c = s:sub(i, i)
    local nxt = i < len and s:sub(i + 1, i + 1) or ""
    if c == "\\" then
      table.insert(out, "\\textbackslash{}")
    elseif c == "{" then
      table.insert(out, "\\{")
    elseif c == "}" then
      table.insert(out, "\\}")
    elseif c == "$" then
      table.insert(out, "\\$")
    elseif c == "&" then
      table.insert(out, "\\&")
    elseif c == "#" then
      table.insert(out, "\\#")
    elseif c == "%" then
      table.insert(out, "\\%")
    elseif c == "~" then
      table.insert(out, "\\textasciitilde{}")
    elseif c == "^" then
      table.insert(out, "\\textasciicircum{}")
    elseif c == "_" then
      table.insert(out, "\\_")
    else
      table.insert(out, c)
    end
    if break_identifiers and break_set[c] and i < len and nxt ~= c then
      table.insert(out, "\\allowbreak{}")
    end
  end
  return table.concat(out)
end

local function escape_pdf_bookmark(s)
  local out = {}
  for i = 1, #s do
    local c = s:sub(i, i)
    if c == "\\" then
      table.insert(out, "\\textbackslash{}")
    elseif c == "{" then
      table.insert(out, "\\{")
    elseif c == "}" then
      table.insert(out, "\\}")
    elseif c == "~" then
      table.insert(out, "\\textasciitilde{}")
    elseif c == "^" then
      table.insert(out, "\\textasciicircum{}")
    elseif c == "#" or c == "$" or c == "%" or c == "&" or c == "_" then
      table.insert(out, "\\" .. c)
    else
      table.insert(out, c)
    end
  end
  return table.concat(out)
end

local function strip_inlines_bytes(inlines, nbytes)
  local remaining = nbytes
  local result = pandoc.List()
  for _, inl in ipairs(inlines) do
    if remaining <= 0 then
      result:insert(inl)
    elseif inl.t == "Str" then
      local t = inl.text
      if #t <= remaining then
        remaining = remaining - #t
      else
        result:insert(pandoc.Str(t:sub(remaining + 1)))
        remaining = 0
      end
    elseif inl.t == "Space" or inl.t == "SoftBreak" then
      if remaining >= 1 then
        remaining = remaining - 1
      else
        result:insert(inl)
      end
    else
      remaining = 0
      result:insert(inl)
    end
  end
  while #result > 0 and (result[1].t == "Space" or result[1].t == "SoftBreak") do
    result:remove(1)
  end
  return result
end

local function inlines_to_latex(inlines)
  if #inlines == 0 then
    return ""
  end
  local rendered = pandoc.write(pandoc.Pandoc({ pandoc.Plain(inlines) }), "latex")
  return trim(rendered)
end

local function match_labeled_prefix(text, stem_patterns)
  for _, pat in ipairs(stem_patterns) do
    local s, e = text:find(pat)
    if s == 1 and e then
      local tail = text:sub(e + 1)
      local sep = tail:match("^(%s*:%s+)")
        or tail:match("^(%s*%.%s+)")
        or tail:match("^(%s*—%s+)")
        or tail:match("^(%s*–%s+)")
        or tail:match("^(%s*%-%s+)")
        or tail:match("^(%s+)")
      if sep and e + #sep < #text then
        return text:sub(1, e + #sep)
      end
    end
  end
  return nil
end

local CAPTION_STEM_PATTERNS = {
  "^HÌNH%s+[A-Za-z0-9%.%-_]+",
  "^[Hh]ình%s+[A-Za-z0-9%.%-_]+",
  "^[Ff][Ii][Gg][Uu][Rr][Ee]%s+[A-Za-z0-9%.%-_]+",
  "^[Ff][Ii][Gg]%.?%s+[A-Za-z0-9%.%-_]+",
}

local APPENDIX_STEM_PATTERNS = {
  "^[Aa][Pp][Pp][Ee][Nn][Dd][Ii][Xx]%s+[A-Za-z0-9]+",
  "^Phụ%s+[Ll]ục%s+[A-Za-z0-9]+",
  "^PHỤ%s+LỤC%s+[A-Za-z0-9]+",
}

local function clean_caption_inlines(inlines)
  local text = stringify(inlines)
  local prefix = match_labeled_prefix(text, CAPTION_STEM_PATTERNS)
  if prefix then
    return strip_inlines_bytes(inlines, #prefix), true
  end
  return inlines, false
end

local function resolve_figure_src(src)
  if not config.prefer_vector_pdf then
    return src
  end
  local base = src:match("^(.+)%.[pP][nN][gG]$")
    or src:match("^(.+)%.[jJ][pP][eE]?[gG]$")
    or src:match("^(.+)%.[wW][eE][bB][pP]$")
  if base then
    local pdf_src = base .. ".pdf"
    if file_exists(pdf_src) then
      return pdf_src
    end
  end
  return src
end

local function has_class(el, cls)
  if el and el.attr and el.attr.classes then
    for _, c in ipairs(el.attr.classes) do
      if c == cls then
        return true
      end
    end
  end
  return false
end

local function is_landscape_src(src)
  if config.landscape_figures[src] then
    return true
  end
  local b = basename(src)
  return config.landscape_figures[b] == true
end

local function make_caption(inlines)
  local long_blocks = { pandoc.Plain(inlines) }
  local ok, cap = pcall(pandoc.Caption, nil, long_blocks)
  if ok and cap then
    return cap
  end
  return pandoc.Caption(long_blocks)
end

local function extract_caption_paragraph(block)
  if not block or block.t ~= "Para" then
    return nil
  end
  if #block.content == 1 and (block.content[1].t == "Emph" or block.content[1].t == "Strong") then
    local cleaned, matched = clean_caption_inlines(block.content[1].content)
    if matched then
      return cleaned
    end
    return nil
  end
  local cleaned, matched = clean_caption_inlines(block.content)
  if matched then
    return cleaned
  end
  return nil
end

local function read_meta(meta)
  if meta["code-verbatim"] ~= nil then
    config.code_verbatim = meta_bool(meta["code-verbatim"], config.code_verbatim)
  end
  local prep = meta.prep
  if type(prep) == "table" then
    config.strip_cover = meta_str(prep["strip-cover"], config.strip_cover)
    config.strip_heading_numbers = meta_bool(prep["strip-heading-numbers"], config.strip_heading_numbers)
    config.code_listings = meta_bool(prep["code-listings"], config.code_listings)
    config.code_verbatim = meta_bool(prep["code-verbatim"], config.code_verbatim)
    config.prefer_vector_pdf = meta_bool(prep["prefer-vector-pdf"], config.prefer_vector_pdf)
    config.callout_boxes = meta_bool(prep["callout-boxes"], config.callout_boxes)
    if prep["adaptive-tables"] ~= nil then
      config.adaptive_tables = meta_bool(prep["adaptive-tables"], true)
    end
  end
  if config.code_verbatim then
    meta["code-verbatim"] = true
  end
  local lf = meta["landscape-figures"]
  if type(lf) == "table" then
    for _, item in ipairs(lf) do
      local s = stringify(item)
      if s ~= "" then
        config.landscape_figures[s] = true
        config.landscape_figures[basename(s)] = true
      end
    end
  end
  return meta
end

local function process_header(el)
  local text = stringify(el.content)
  local is_appendix = false

  if el.level == 1 then
    local prefix = match_labeled_prefix(text, APPENDIX_STEM_PATTERNS)
    if prefix then
      is_appendix = true
      el.content = strip_inlines_bytes(el.content, #prefix)
    end
  end

  if not is_appendix and config.strip_heading_numbers then
    local updated_text = stringify(el.content)
    local num_prefix = updated_text:match("^(%d+%.%d+[%.%d]*%.?%s*[:%-]?%s+)")
      or updated_text:match("^(%d+%.%s+)")
      or updated_text:match("^([A-Z]%.%d+[%.%d]*%.?%s*[:%-]?%s+)")
    if num_prefix then
      el.content = strip_inlines_bytes(el.content, #num_prefix)
    end
  end

  local has_code = false
  el:walk({
    Code = function(_)
      has_code = true
    end,
  })
  if has_code then
    el.attr.attributes["data-pdf-bookmark"] = escape_pdf_bookmark(stringify(el.content))
    el = el:walk({
      Code = function(inl)
        local tex = escape_latex_chars(inl.text, true)
        return pandoc.RawInline("latex", string.format("\\texttt{%s}", tex))
      end,
    })
  end

  if is_appendix then
    el.attr.attributes["data-appendix"] = "true"
  end

  return el
end

local function process_code(el)
  local tex = escape_latex_chars(el.text, true)
  return pandoc.RawInline("latex", string.format("\\texttt{%s}", tex))
end

local function process_codeblock(el)
  local lang_raw = el.classes and el.classes[1] or nil
  local lang = lang_raw and LISTINGS_LANG_MAP[string.lower(lang_raw)] or nil

  if not config.code_listings then
    if config.code_verbatim then
      return pandoc.RawBlock("latex", "\\begin{Verbatim}[breaklines=true,fontsize=\\small]\n" .. el.text .. "\n\\end{Verbatim}")
    end
    return nil
  end

  local header = "\\begin{lstlisting}"
  if not config.code_verbatim and lang then
    header = string.format("\\begin{lstlisting}[language=%s]", lang)
  end
  return pandoc.RawBlock("latex", header .. "\n" .. el.text .. "\n\\end{lstlisting}")
end

local function process_blockquote(el)
  if not config.callout_boxes or #el.content == 0 then
    return nil
  end
  local first = el.content[1]
  if first.t ~= "Para" and first.t ~= "Plain" then
    return nil
  end
  local first_text = stringify(first.content)
  local kind = first_text:match("^%[!([A-Za-z]+)%]")
  if not kind then
    return nil
  end
  local spec = CALLOUT_MAP[string.upper(kind)]
  if not spec then
    return nil
  end

  local inner_blocks = pandoc.List()
  local marker_len = #("[!" .. kind .. "]")
  local trimmed_first = strip_inlines_bytes(first.content, marker_len)
  if #trimmed_first > 0 then
    inner_blocks:insert(pandoc.Para(trimmed_first))
  end
  for i = 2, #el.content do
    inner_blocks:insert(el.content[i])
  end

  local out = pandoc.List({
    pandoc.RawBlock("latex", string.format("\\begin{reportcallout}{%s}{%s}", spec.title, spec.style)),
  })
  out:extend(inner_blocks)
  out:insert(pandoc.RawBlock("latex", "\\end{reportcallout}"))
  return out
end

local function replace_html_breaks(block)
  return block:walk({
    RawInline = function(inl)
      if inl.format == "html" and string.lower(inl.text):match("^<br%s*/?>$") then
        return pandoc.RawInline("latex", "\\newline ")
      end
      return nil
    end,
  })
end

local function cell_text_weight(cell)
  local s = trim(stringify(cell.contents))
  local len = #s
  if len == 0 then
    return 4
  end
  return math.max(4, math.min(len, 60))
end

local function process_table(el)
  el = replace_html_breaks(el)
  local ncols = #el.colspecs
  if ncols == 0 or not config.adaptive_tables then
    return el
  end

  local col_weights = {}
  for c = 1, ncols do
    col_weights[c] = 6
  end

  local function scan_rows(rows)
    for _, row in ipairs(rows or {}) do
      for c = 1, math.min(ncols, #row.cells) do
        local w = cell_text_weight(row.cells[c])
        if w > col_weights[c] then
          col_weights[c] = w
        end
      end
    end
  end

  if el.head then
    scan_rows(el.head.rows)
  end
  for _, body in ipairs(el.bodies or {}) do
    scan_rows(body.head)
    scan_rows(body.body)
  end
  if el.foot then
    scan_rows(el.foot.rows)
  end

  local sum_w = 0
  for c = 1, ncols do
    col_weights[c] = math.sqrt(col_weights[c])
    sum_w = sum_w + col_weights[c]
  end

  local new_colspecs = {}
  for c = 1, ncols do
    local align = el.colspecs[c][1]
    local frac = math.max(0.06, col_weights[c] / sum_w)
    table.insert(new_colspecs, { align, frac })
  end
  -- Re-normalize after lower bound clamping
  local frac_sum = 0
  for c = 1, ncols do
    frac_sum = frac_sum + new_colspecs[c][2]
  end
  for c = 1, ncols do
    new_colspecs[c][2] = tonumber(string.format("%.4f", new_colspecs[c][2] / frac_sum))
  end
  el.colspecs = new_colspecs

  if not config.adaptive_tables or ncols < 2 then
    return el
  end

  local size_cmd = ncols >= 5 and "\\scriptsize" or "\\footnotesize"
  return {
    pandoc.RawBlock("latex", "{" .. size_cmd),
    el,
    pandoc.RawBlock("latex", "}"),
  }
end

local function process_image(el)
  el.src = resolve_figure_src(el.src)
  return el
end

local function extract_single_image(block)
  if block.t == "Figure" then
    local found_img = nil
    block.content:walk({
      Image = function(img)
        if not found_img then
          found_img = img
        end
      end,
    })
    return found_img, block.caption and block.caption.long or {}
  end
  if (block.t == "Para" or block.t == "Plain") and #block.content == 1 and block.content[1].t == "Image" then
    local img = block.content[1]
    return img, {}
  end
  return nil, nil
end

local function process_doc_blocks(doc)
  local blocks = doc.blocks
  -- 1. Strip leading frontmatter/cover blocks per prep.strip-cover mode
  if config.strip_cover == "before-first-h1" then
    local filtered = pandoc.List()
    local seen_h1 = false
    for _, b in ipairs(blocks) do
      if not seen_h1 and b.t == "Header" and b.level == 1 then
        seen_h1 = true
      end
      if seen_h1 then
        filtered:insert(b)
      end
    end
    blocks = filtered
  elseif config.strip_cover == "first-h1-cover" then
    local filtered = pandoc.List()
    local state = "before_cover_h1"
    local promote_delta = 0
    for _, b in ipairs(blocks) do
      if state == "before_cover_h1" then
        if b.t == "Header" and b.level == 1 then
          state = "in_cover_body"
        end
      elseif state == "in_cover_body" then
        if b.t == "Header" then
          state = "after_cover"
          if b.level > 1 then
            promote_delta = b.level - 1
          end
          if promote_delta > 0 then
            b.level = math.max(1, b.level - promote_delta)
          end
          filtered:insert(b)
        end
      else
        if b.t == "Header" and promote_delta > 0 and b.attr.attributes["data-appendix"] ~= "true" then
          b.level = math.max(1, b.level - promote_delta)
        end
        filtered:insert(b)
      end
    end
    blocks = filtered
  end

local function latex_heading_cmd(level)
  local use_chapter = PANDOC_WRITER_OPTIONS and PANDOC_WRITER_OPTIONS.top_level_division == "top-level-chapter"
  local map = use_chapter
    and { "chapter", "section", "subsection", "subsubsection", "paragraph", "subparagraph" }
    or { "section", "subsection", "subsubsection", "paragraph", "subparagraph", "subparagraph" }
  return map[math.max(1, math.min(6, level))] or "section"
end

local function emit_header_block(b)
  local bookmark = b.attr and b.attr.attributes["data-pdf-bookmark"] or nil
  if not bookmark then
    return b
  end
  b.attr.attributes["data-pdf-bookmark"] = nil
  local tex_title = inlines_to_latex(b.content)
  local cmd = latex_heading_cmd(b.level)
  local star = has_class(b, "unnumbered") and "*" or ""
  local label_tex = (b.attr and b.attr.identifier and b.attr.identifier ~= "")
    and string.format("\\label{%s}", b.attr.identifier)
    or ""
  return pandoc.RawBlock("latex", string.format("\\%s%s{\\texorpdfstring{%s}{%s}}%s", cmd, star, tex_title, bookmark, label_tex))
end

  -- 2. Emit \appendix once before first appendix chapter and merge adjacent captions / landscape figures
  local final_blocks = pandoc.List()
  local appendix_emitted = false
  local i = 1
  while i <= #blocks do
    local b = blocks[i]
    if b.t == "Header" and b.attr and b.attr.attributes["data-appendix"] == "true" then
      b.attr.attributes["data-appendix"] = nil
      if not appendix_emitted then
        final_blocks:insert(pandoc.RawBlock("latex", "\\appendix"))
        appendix_emitted = true
      end
      final_blocks:insert(emit_header_block(b))
      i = i + 1
    elseif b.t == "Header" then
      final_blocks:insert(emit_header_block(b))
      i = i + 1
    else
      local img, cap_blocks = extract_single_image(b)
      if img then
        local src = resolve_figure_src(img.src)
        local is_land = has_class(b, "landscape") or has_class(img, "landscape") or is_landscape_src(img.src) or is_landscape_src(src)
        local cap_inlines = nil

        if cap_blocks and #cap_blocks > 0 then
          local cap_plain = cap_blocks[1]
          if cap_plain and (cap_plain.t == "Plain" or cap_plain.t == "Para") and #cap_plain.content > 0 then
            cap_inlines = clean_caption_inlines(cap_plain.content)
          end
        end

        if (not cap_inlines or #cap_inlines == 0) and i < #blocks then
          local adj_cap = extract_caption_paragraph(blocks[i + 1])
          if adj_cap then
            cap_inlines = adj_cap
            i = i + 1
          end
        end

        if is_land then
          local cap_tex = cap_inlines and inlines_to_latex(cap_inlines) or ""
          final_blocks:insert(pandoc.RawBlock("latex", string.format("\\landscapefigure{%s}{%s}", src, cap_tex)))
        elseif b.t == "Figure" then
          img.src = src
          if cap_inlines then
            b.caption = make_caption(cap_inlines)
          end
          b.content = { pandoc.Plain({ img }) }
          final_blocks:insert(b)
        elseif cap_inlines and #cap_inlines > 0 then
          img.src = src
          local fig = pandoc.Figure({ pandoc.Plain({ img }) }, make_caption(cap_inlines), img.attr or pandoc.Attr())
          final_blocks:insert(fig)
        else
          img.src = src
          final_blocks:insert(b)
        end
        i = i + 1
      else
        final_blocks:insert(b)
        i = i + 1
      end
    end
  end

  doc.blocks = final_blocks
  return doc
end

return {
  { Meta = read_meta },
  {
    Header = process_header,
    Table = process_table,
  },
  {
    Code = process_code,
    CodeBlock = process_codeblock,
    BlockQuote = process_blockquote,
    Image = process_image,
  },
  { Pandoc = process_doc_blocks },
}
