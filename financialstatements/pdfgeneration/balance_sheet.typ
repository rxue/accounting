#set page(paper: "a4")
#set text(size: 12pt)

*Company name: OutlierX Oy*

= Balance Sheet

#align(right)[As of: {as_of_date}]

== Assets

=== Current Assets

#table(
  columns: (1fr, auto),
  align: (left, right),
  stroke: none,
  {current_assets_rows}
)

#table(
  columns: (1fr, auto),
  align: (left, right),
  stroke: none,
  table.hline(start: 1),
  [*Total Assets*], [*{total_assets}*],
)
