## API Endpoints (WIP)

| Endpoint         | Parameters                           | Purpose                      |
| ---------------- | ------------------------------------ | ---------------------------- |
| `/api/linktrack` | `org_id`, `assessment_id`, `address` | Track assessment link clicks |



## Databases

| Database           | Filename             | Table    | Columns                                                      |
| ------------------ | -------------------- | -------- | ------------------------------------------------------------ |
| Reports            | `reports.db`         | `org_id` | `id`, `reportee`, `reporter`, `receiver`, `note`, `body`, `timestamp` |
| Whitelists         | `whitelists.db`      | `org_id` | `id`, `address`                                              |
| Blacklists         | `blacklists.db`      | `org_id` | `id`, `address`                                              |
| Assessment Senders | `testaddrlists.db`   | `org_id` | `id`, `address`                                              |
| Assessment Targets | `testtargetlists.db` | `org_id` | `id`, `address`                                              |
| Assessments        | `assessments.db`     | `org_id` | `id`, `assessment_id`                                        |
| Assessment Opens   | `opentracklists.db`  | `org_id` | `id`, `assessment_id`, `address`                             |
| Assessment Clicks  | `linktracklists.db`  | `org_id` | `id`, `assessment_id`, `address`                             |
