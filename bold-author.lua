-- bold-author.lua : make occurrences of the target author bold in the References section
local target = pandoc.utils.stringify(pandoc.MetaString("(?i)Borcherding,?%s*N(?:%.?%s*C%.)?"))
-- Only act inside the bibliography div {.references}
local in_refs = false

function Div(el)
if el.identifier == "refs" then
in_refs = true
local res = pandoc.walk_block(el, { Str = bold_me })
in_refs = false
return res
end
return nil
end

function bold_me(el)
if in_refs then
local txt = el.text
-- wrap regex matches with **...**
  local new = txt:gsub(target, function(m) return "**" .. m .. "**" end)
if new ~= txt then
return pandoc.RawInline("markdown", new)
end
end
return nil
end
