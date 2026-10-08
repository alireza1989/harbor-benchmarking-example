`/app/data/customers.csv` has duplicate customers. Two rows are the same
customer when their `email` values match after trimming whitespace and
lowercasing.

Write a deduplicated copy to `/app/out/customers_clean.csv`:

- keep the header and the original column order
- keep the first occurrence of each customer, in the original row order
- do not modify `/app/data/customers.csv`
