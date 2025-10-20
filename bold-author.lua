-- bold-author.lua (v2 - Robust Version)
-- Bolds an author's name in the bibliography.

local author_patterns = {
  "Borcherding, N%.?C?%.?",
  "Borcherding, Nicholas C?%.?",
  "N%.?C?%.? Borcherding",
  "Nicholas C?%.? Borcherding",
  "Borcherding N.?C?.?" -- Matches 'Borcherding N', 'Borcherding NC', etc.
}

-- This is the function that will be applied to each paragraph
-- inside the bibliography.
local function bold_author_in_para(para)
  local new_inlines = pandoc.List()
  
  for _, inline in ipairs(para.content) do
    if inline.tag == 'Str' then
      local current_text = inline.text
      local found_match = false
      
      for _, pattern in ipairs(author_patterns) do
        local match_start, match_end = current_text:find(pattern)
        
        if match_start then
          -- Split the string into three parts: before, matched, and after
          local before = current_text:sub(1, match_start - 1)
          local matched_text = current_text:sub(match_start, match_end)
          local after = current_text:sub(match_end + 1)
          
          -- Add the part before the match, if it exists
          if #before > 0 then
            new_inlines:insert(pandoc.Str(before))
          end
          
          -- Add the bolded match
          new_inlines:insert(pandoc.Strong(pandoc.Str(matched_text)))
          
          -- The rest of the string becomes the new 'current_text'
          -- to be processed further in the next loop iteration (if needed)
          -- or added at the end.
          current_text = after
          found_match = true
          break -- Stop checking other patterns for this segment
        end
      end
      
      -- If any text remains (either original or the 'after' part), add it.
      if #current_text > 0 then
        new_inlines:insert(pandoc.Str(current_text))
      end
      
    else
      -- If the element is not a string (e.g., a space, link), add it as is.
      new_inlines:insert(inline)
    end
  end
  
  para.content = new_inlines
  return para
end

-- We only want to run this filter on the bibliography div.
return {
  {
    Div = function(div)
      if div.identifier == 'refs' or div.classes:includes('references') then
        return div:walk { Para = bold_author_in_para }
      end
    end
  }
}