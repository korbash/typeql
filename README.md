## Why you need TypeQL

Check my article [TypeQL: SQL for analysts that knows everything about your data](https://korbash.github.io/typeql/)

## 🎯 Goal & Status

This project is a **new language for analytical queries** that compiles into SQL.
Its goal is to make analytical expressions **structure-oriented, type-safe, and supported by autocomplete**.

Right now, I’m building the **core of the language and its type system**.
Based on a described database structure, you can already write queries with IDE checks and autocomplete suggestions that rely on the schema.
The next steps are SQL compilation and automatic generation of database structures (with hints and metadata derived from the DB itself).

---

## 💡 Key ideas

### 1. Database as a set of objects and one-way links

The database is represented as a **set of objects** (tables, entities, fields) and **one-way links** between them.
A link exists if an instance of the first object can **uniquely determine** an instance of the second.

This forms a **directed graph of dependencies**, described in the file `generated_bd_schema`.
For example:
you can get a `Buyer` from a `Deal`, but not the other way around — the link goes from `Deal` to `Buyer`.

This idea enables strong typing, autocomplete, and safe navigation between related objects.
The concept is inspired by [David Spivak’s work](https://categoricaldata.net/cql/Broad_SoftEng.pdf) and similar ideas in GraphQL.

---

### 2. Structure-oriented queries

A query is a **list of parameters that come from the same source (`Source`)**.
Each parameter becomes a column in the final SQL result.

---

### Types of parameters

1. **Simple parameters** — moving down through dependencies from the current source.
   A chain can be **as long as needed**, passing through multiple levels:

   ```python
   deals.buyer.email
   deals.seller.regDate
   deals.seller.company.region.name
   ```

   Each step (`buyer`, `seller`, `company`, `region`) is a one-way link
   that uniquely determines the next object.

2. **Functions over parameters from the same source** —
   arithmetic or logical operations that don’t change the `Source`:

   ```python
   total_usd  = deals.amount_usd + deals.tax_usd
   profit_pct = round((deals.profit / deals.amount_usd) * 100)
   ```

   The type system ensures that such operations are allowed **only between parameters with the same source**.

3. **Metrics (aggregated parameters)** — the result of an aggregation function
   that **changes the source**.
   Each aggregation defines:
   - a function (`aggSum`, `aggAvg`, `aggCount`, `aggUniq`);
   - the parameter to aggregate (`param[source]`);
   - the path to the dimension used for grouping (`path_to_groupby_dim`).

   Example:

   ```python
   user_spend = aggSum(deals.amount_usd, deals.buyer)
   ```

   Here, we sum `amount_usd` from `DealsSrc` for each `buyer`.
   The result has type `number[UserSrc]`,
   meaning `user_spend` is now defined for every user
   and can be used as a parameter in queries with `UserSrc`.

You could check **examples** folder with complete queries

---

### Type system and autocomplete rules

- operations are allowed **only between parameters with the same `Source`**;
- the compiler always knows **what fields and links exist for a given type**
  and suggests them in autocomplete through `.`;
- after aggregation, the result’s `Source` is automatically updated.

---

### 3. The `>>` operator

The `>>` operator connects **two independent objects**,
similar to the `.` operator but without requiring a shared chain of origin.
It lets you reuse calculated metrics in new contexts.

---

### 4. Extensibility and expressiveness

The language supports functions and loops —
everything you expect from a real programming language.
Its main strength is **strong typing and context-aware autocomplete**,
both driven by the structure of the database itself.

In the future, integration with BI systems will allow building more powerful filters
with less code, again relying on the database structure.

---

## ⚙️ Installation

Requires **Python ≥ 3.12**.
To install dependencies (currently none), it’s recommended to use [uv](https://docs.astral.sh/uv/getting-started/installation/):

```bash
uv python install 3.13
uv sync
```

You can install uv from the link above or via `pipx`:

```bash
pipx install uv
```
