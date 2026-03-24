# TypeQL: SQL for Analysts That Knows Everything About Data

For as long as I've been using SQL, it's been frustrating me (the only saving grace is that nowadays you can generate it with LLMs). Today I want to tell you about my prototype language for creating large and complex analytical queries that compiles to SQL.

Before I start praising my creation, I need to thoroughly criticize SQL. So, what don't I like about it:

## Problems with SQL

- **No functions and loops** (some databases implement them, but they're not in the standard). And this is clearly necessary if we want to write large queries and reuse code
- **Overcomplicated syntax** — WHERE, HAVING, QUALIFY essentially perform filtering operations (this problem was solved by another interesting project, PRQL)
- **Want a good LSP server** that relies more on the database structure, knows what can be joined with what, what types of relationships there are (1:m, m:1), and doesn't let you add strings to numbers at the code writing stage

I could criticize SQL at length and in detail, as each of us could, but it's time to move forward.

## A New Approach

I want to propose a language that will be:
- based on data structure
- metric-oriented

What is data structure? In the classical approach, it's a list of tables, each table has columns, each column has a type and some constraints:

- **PRIMARY KEY** — unique value, semantically the field by which you're supposed to search for the needed row in the table
- **FOREIGN KEY** — reference to a column in another table (usually a primary key). A row in the dependent table must be uniquely determined
- **UNIQUE** — unique value
- **NOT NULL** — it's not null
- **CHECK** — arbitrary constraint, for example `status IN ('created', 'completed')` or `age > 0`

That's essentially it. If SQL used this information about the database — that would already be great. But since we're creating a new language, we can describe the data structure in a new way.

Let's abstract from which tables our data is physically stored in, and think about it from the perspective of the real world.

In the real (object-oriented) world, we have:

- **Types** (table structure — what columns it has and what constraints they have)
- **Objects** (table rows) — must have some type
- **Parameters** of objects (table columns)
- Other objects can also be parameters
- For each object, the values of its parameters are uniquely determined

For example, let's say I have an exchange described by 3 tables:

```sql
CREATE TABLE users (
  id INT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(100),
  invited_by INT,

  FOREIGN KEY (invited_by) REFERENCES users(id)
);

-- goods of 2 types: either pets or machines
CREATE TABLE goods (
  id INT PRIMARY KEY,
  is_alive BOOLEAN NOT NULL,
  sex VARCHAR(100), -- pets have gender
  brand VARCHAR(100) -- machines have brand
);

CREATE TABLE deals (
  id INT PRIMARY KEY,
  seller INT NOT NULL,
  buyer INT NOT NULL,
  good_id INT NOT NULL,
  price DECIMAL(10,2) NOT NULL,
  currency VARCHAR(100) NOT NULL,
  deal_date DATETIME NOT NULL,

  FOREIGN KEY (seller) REFERENCES users(id),
  FOREIGN KEY (buyer) REFERENCES users(id),
  FOREIGN KEY (good_id) REFERENCES goods(id)
);
```

Let's convert this to an object-oriented representation, writing it in pseudo-Python:

```python
class User:
    def id() -> NumberSQL: ...
    def name() -> StringSQL: ...
    def email() -> StringSQL | Null: ...
    def invited_by() -> User | Null: ...

class Pet:
    def id() -> NumberSQL: ...
    def is_alive() -> BooleanSQL: ...
    def sex() -> StringSQL: ...

class Machine:
    def id() -> NumberSQL: ...
    def is_alive() -> BooleanSQL: ...
    def brand() -> StringSQL: ...

class Deal:
    def id() -> NumberSQL: ...
    def seller() -> User: ...
    def buyer() -> User: ...
    def good() -> Pet | Machine: ...
    def price() -> NumberSQL: ...
    def currency() -> StringSQL: ...
    def deal_date() -> DateTimeSQL: ...
```

This representation is very close to the 4th normal form, even slightly broader — it allows describing discriminated unions like `def good() -> Pet | Machine: ...`. You can't describe such a dependency beautifully in a database.

But the main idea is that I now look at data as a structure of dependent objects. As an analyst, I take a deal, and I want to know what I can uniquely determine from this deal. And my representation answers exactly this question.

The idea is not new — a similar representation was described by David Spivak, for example [here](https://arxiv.org/abs/1009.1166). And while preparing for this article, I stumbled upon a project that went even further by applying full type theory to describe database structure: [https://typedb.com](https://typedb.com) (a project with a very similar idea). How did I not find it before!

Generally, by design, this schema doesn't need to be written by hand — it's automatically generated from the database. And some additional information that's not in the database structure can be passed through tags in comments on database columns. I'll write about this in more detail at the end.

So, we already have a data structure — the IDE knows it and can suggest!

Already wonderful! It even displays comments for each parameter!

## Metric-Oriented Approach

But it's time to move forward to creating a full-fledged Query Language. Here we remember that we're making a metric-oriented language, so the result of any query is a metric (dimension → parameter binding), where dimension is one of our types (or Cartesian product of several), and parameter, as before, is what is uniquely determined by the dimension.

For example, for each deal we can calculate the price in dollars:

```python
d = BD().deals  # this is the dimension of our metric — an element of the Deals class
price_usd = caseSQL({
    d.currency == 'RUB': d.price * 0.0127,
    d.currency == 'EUR': d.price * 1.1,
    d.currency == 'USD': d.price,
})  # depending on the currency, multiply by the needed exchange rate

d.price_usd = price_usd  # now the IDE will suggest it
```

(I should note that this is the syntax I would like to see; in reality, I couldn't achieve it — had to make it more cumbersome)

That is, the result of any query is a new parameter that seamlessly integrates into the structure, and can be reused in other queries! Moreover, we can use all the power of a normal programming language — functions and loops.

For example, we can define our metric as a function:

```python
def price_usd(rub_rate: float, eur_rate: float):
    return caseSQL({
        d.currency == 'RUB': d.price * rub_rate,
        d.currency == 'EUR': d.price * eur_rate,
        d.currency == 'USD': d.price,
    })

d.price_usd = price_usd  # so the IDE suggests it
```

By the way, the idea that a metric-oriented language for analytical queries is good is also not new, described for example [here](https://arxiv.org/abs/1203.2547).

## Metric Formalism

Hurray, we've learned to calculate simple metrics! In the Python implementation, I defined a metric as a generic type: `result[source]`, where `result` is the parameter type, and `source` is the type indicating the dimension. The metric from our example has type `NumberSQL[DealsSrc]`.

Let's describe what we can already do with metrics in the new formalism. We can perform any scalar function (allowed in SQL) if:

- The arguments have the same source. The result will have the same source: `f(a[s], b[s], c[s]) -> metrica[s]`. But `f(a[s1], b[s2])` will throw an error
- Their types are allowed for this function (`NumberSQL + NumberSQL` — ok, `NumberSQL + StringSQL` — not ok)

Hurray, we can calculate any scalar metrics! Now we need to deal with aggregation.

## Aggregation

Here everything is simple. For aggregation I need:

- An aggregation function (there are only 5: `aggSum`, `aggAvg`, `aggMin`, `aggMax`, `aggCount`, `aggUniq`)
- A metric (which we will aggregate) `metrica[source]`
- A path to the new dimension `newSource[source]` (actually also a metric). This can be a tuple of several paths `(newS1[source], newS2[source])`

As a result, we get a metric with a new source (dimension) `metrica[newSource]`. Or, if there were several paths, the new source will be their Cartesian product `metrica[cartesian[newS1, newS2]]`.

In general, the behavior is completely analogous to such a query:

```sql
SELECT
    path,
    SUM(metrica) -- or another aggregation function
FROM some_table
GROUP BY path
```

Example of a metric with explicit type indication for clarity (in reality, everything is computed):

```python
result: NumberSQL[UserSrc] = aggSum(
    deals.price: NumberSQL[DealsSrc],
    deals.buyer: User[DealsSrc]
)
```

The only difference is that the result remains a metric and can be further reused.

## That's Basically It

By this point, we've learned to do only 4 things:

**For parameters:**
- Calculate scalar functions from parameters
- Calculate aggregation functions

**For dimensions (sources):**
- Create new dimensions through Cartesian product of existing ones
- Create new dimensions through sum of existing ones (what's denoted by `|` in Python, and in SQL it's `UNION ALL`)

Strangely enough, this is already enough for us to express any SELECT query (missing ORDER BY, but that's a minor detail). Of course, we'd also like window functions — although they can be expressed through subqueries, it's very inconvenient. So we should figure out how to add them to my syntax.

About filtering: you can filter rows now through `caseSQL`, for example like this:

```python
success_deals = caseSQL({
    deals.status == "success": deals
}, default=Null)
```

But since the operation is frequent, probably we should allocate a separate function for it.

That's essentially my entire idea of a metric-oriented and well-typed language to replace SQL. Interested to know what people think — write, I'll read everything.

Here [https://github.com/korbash/typeql](https://github.com/korbash/typeql) I implemented a prototype compiler to SQL. It can't compile yet and the data schema is also hardcoded, but you can look at query examples and test how the IDE helps write queries: knows who has which parameters, doesn't let you add metrics with different sources, doesn't let you add strings and numbers.

## Technical Difficulties

I must say that when writing the compiler, I ran into difficulties — I hit the limits of typing in Python, already having to use various workarounds. Even found a bug in Pyright.

I spent a long time looking for a language that could handle my type checking needs. One of the main features is that it should work well with sum types. If a user gets a metric with type `Pet | Machine`, the language should understand which parameters Pet has, which Machine has, and suggest them all in autocomplete.

And this feature, strangely enough, is rare among languages. It exists in Python and TypeScript, but languages known for good work with types don't fit well for this parameter: Lean, OCaml, Haskell — all miss the mark. Scala possibly, but I'm not sure.

TypeScript fits best, but you can't overload operators there, and that's a big minus in my case.

In general, the question of which language to write such a library in remains open. If anyone has ideas — I'd be happy to hear them.

## Schema Generation from Database

Regarding schema generation from the database, things are not so bad here. All databases support comments on columns, and in these comments through special tags like `@id`, `@ignore`, `@virt(currency.id)`, `@link(pets, machines)` you can pass additional information about the schema — what couldn't be conveyed by standard means through PRIMARY / FOREIGN KEY.

They're easy to parse, besides them there can be regular human comments. Tags are compact — they don't interfere with reading the comment.

## Applications

Actually, it all started with the fact that I was very frustrated that in BI systems it's difficult to embed filters. You can't just write a query and have filters pull themselves in — for each one you need to specify what valid values it has or what query to use to get them. This is if we're talking about tools like Superset, Metabase. If we're talking about DataLens, Tableau, there's a different problem — they essentially combine everything into one big table (through a view, but still) and then work with it. And here the data structure is lost.

One of the main advantages of my language is that it always knows the type for each metric. For example, I want to add a filter on buyers. In the code, it's enough to write something like:

```python
buyerFilter: User[DealsSrc] = filter(deals.buyer)
```

(I indicated the type for better understanding)

In the dashboard, you don't need to specify anything additionally — it already knows everything. From the filter it knows we're filtering by users, what parameters a user has is known from the data structure, you can configure filtering by all of them right in the UI — whether by registration date, country, or age. And default parameters can be passed right in the query code.

Therefore, the language is primarily for embedding in BI and data exploration systems. In the future, possibly in ELT pipelines like SQLMesh or dbt. For non-analytical queries, my language will probably be useless.

---

**Original article in Russian:** [TypeQL: SQL для аналитиков, который знает о данных всё](https://habr.com/ru/articles/973966/)
