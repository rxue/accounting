#set page(paper: "a4")
#set text(size: 12pt)

*{company_name}*

= Income Statement

#align(right)[Period: {period}]

== Gross Income

#table(
  columns: (1fr, auto),
  align: (left, right),
  stroke: none,
  {income_rows}
)

== Expenses

#table(
  columns: (1fr, auto),
  align: (left, right),
  stroke: none,
  {expense_rows}
  table.hline(start: 1),
  [*Total Expenses*], [*-{total_expenses}*],
)

#table(
  columns: (1fr, auto),
  align: (left, right),
  stroke: none,
  table.hline(start: 1),
  [*Net Income*], [*{net_income}*],
)
