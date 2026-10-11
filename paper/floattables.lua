-- Turn pandoc's longtables into floating tabulars, so short tables never split across pages
-- and LaTeX can place them with the figures.
function Table(tbl)
  local tex = pandoc.write(pandoc.Pandoc({tbl}), "latex")
  local spec = tex:match("\\begin{longtable}%[%]{(.-)}\n\\caption") or tex:match("\\begin{longtable}%[%]{(.-)}\n\\toprule")
  local caption = tex:match("\\caption{(.-)}\\tabularnewline")
  local head = tex:match("\\toprule\\noalign{}\n(.-)\\midrule\\noalign{}\n\\endfirsthead")
  local body = tex:match("\\endlastfoot\n(.-)\\end{longtable}")
  if not (spec and head and body) then
    return nil
  end
  local out = {"\\begin{table}[tbp]"}
  if caption then
    table.insert(out, "\\caption{" .. caption .. "}")
  end
  table.insert(out, "\\begin{tabular}{" .. spec .. "}")
  table.insert(out, "\\toprule")
  table.insert(out, head .. "\\midrule")
  table.insert(out, body .. "\\bottomrule")
  table.insert(out, "\\end{tabular}")
  table.insert(out, "\\end{table}")
  return pandoc.RawBlock("latex", table.concat(out, "\n"))
end
