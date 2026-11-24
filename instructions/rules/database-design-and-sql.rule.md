---
trigger: glob
globs: "**/*.sql, **/*.ddl, **/*.dml, **/*.dbml, **/*.drawio, **/*.erd, **/*.mwb"
description: "Relational database modeling and SQL engineering standards: ER/EER conceptual fidelity, 1NF-BCNF normalization proofs, exact DECIMAL arithmetic, uniform naming, symmetric trigger enforcement, cycle detection, and 5-category SQL verification."
---

# Database Design and SQL Implementation Standards

Governs conceptual entity-relationship modeling, logical normalization, and physical relational database (RDBMS) SQL implementation across schema designs, trigger/procedural logic, analytical queries, and verification scripts.

## 1. Conceptual and Logical Modeling Discipline

1. **Conceptual ER / EER Fidelity:**
   - Distinguish Strong Entities from Weak Entities (specifying identifying owner entity, identifying relationship, and partial key discriminator).
   - Distinguish Simple, Composite (decomposed into atomic columns upon relational mapping), Multi-valued (mapped to separate child `1:N` tables), and Derived attributes (never stored redundantly unless explicitly justified as audited cached fields with recalculation rules).
   - Document exact Cardinality Ratios (`1:1`, `1:N`, `M:N`, n-ary/ternary, or aggregation) and Participation Constraints (`Total` vs. `Partial`) in the relationship matrix.
   - Keep conceptual narratives strictly technology-agnostic (`0` DBMS keywords such as `VARCHAR`, `AUTO_INCREMENT`, `ENGINE=InnoDB`, or `SIGNAL SQLSTATE` inside conceptual requirements or ER descriptions).
2. **Formal Normalization Analysis (`1NF -> 2NF -> 3NF -> BCNF`):**
   - Every relation specification must declare five elements: `(a)` Relational Schema with Primary Key attributes marked, `(b)` non-trivial Functional Dependencies ($F$), `(c)` all Candidate Keys (Primary Key plus Alternate Keys), `(d)` Prime vs. Non-Prime attributes, and `(e)` step-by-step evaluation through `1NF` (atomic domains, zero repeating groups), `2NF` (zero partial dependencies of non-prime attributes on proper subsets of any candidate key), `3NF` (zero transitive dependencies of non-prime attributes on any candidate key), and `BCNF` where required (every non-trivial determinant is a superkey).
   - Every schema decomposition (such as refining composite keys for `2NF` on interval assignments or eliminating transitive supplier links for `3NF` on order dispatches) must preserve **Lossless Join** and **Dependency Preservation**.

## 2. Physical RDBMS and SQL Implementation Standards

1. **Transactional Storage Engine and Unicode Encoding:**
   - Enforce ACID-compliant transactional tables and full UTF-8 character sets (`ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci` on MySQL; UTF-8 transactional tables on PostgreSQL/ANSI engines) on all relations to guarantee foreign-key integrity, rollback safety, and multilingual character support.
2. **Exact Decimal Arithmetic and Temporal Invariants:**
   - Use `DECIMAL(p, s)` or `NUMERIC(p, s)` for all monetary values (`Budget`, `Salary`, `UnitPrice`, `ContractValue`), rates and percentages (`TaxRate`, `ProgressPct`, `CompletionScore`), quantities (`OrderQty`, `StockQty`), and logged durations (`HoursLogged`, `RunHours`). Strictly prohibit `FLOAT`, `DOUBLE`, and `REAL` for financial, billing, or inventory calculations.
   - Use native `DATE`, `DATETIME`, or `TIMESTAMP` types paired with explicit `CHECK` constraints for chronological and range invariants (`end_date >= start_date`, `amount >= 0`).
3. **Uniform Object Naming Contract:**
   - Apply uniform prefixes across DDL, constraint, index, and trigger scripts:
     - Primary Key: `PK_<TABLE>`
     - Foreign Key: `FK_<TABLE>_<ColumnOrRole>`
     - Unique Key: `UQ_<TABLE>_<ColumnOrScope>`
     - Check Constraint: `CK_<TABLE>_<Rule>`
     - Index: `IDX_<TABLE>_<ColumnOrScope>`
     - Trigger: `TRG_<ACTION>_<RuleSummary>`
4. **Referential Integrity and Circular Dependency Resolution:**
   - Declare explicit `ON UPDATE` and `ON DELETE` referential actions (`CASCADE` for weak entities and multivalued attribute child tables; `RESTRICT` or `NO ACTION` for operational parent records retaining history; `SET NULL` for optional links such as supervisor or department-head references).
   - Resolve mutual foreign-key cycles (such as `DEPARTMENT` head reference and `EMPLOYEE` department reference) by creating the initial table with a nullable foreign key and adding the closing foreign-key constraint afterward via deferred `ALTER TABLE` (or deferrable constraints where supported by the engine).
5. **Trigger, Procedural, and Query Discipline:**
   - Signal business-rule violations using standardized error codes (`SIGNAL SQLSTATE '45000'` in MySQL or `RAISE EXCEPTION` with an explicit `SQLSTATE` code in PostgreSQL) carrying rule-numbered messages (`'Rule N Violation: ...'`) so enforcement errors remain testable and unambiguous.
   - Enforce row-level and aggregate invariants symmetrically across both `BEFORE INSERT` and `BEFORE UPDATE` triggers (excluding the current row on `UPDATE` via primary-key inequality so updates do not false-trigger against themselves), and audit `DELETE` paths whenever derived balances or parent invariants depend on row removal.
   - Handle RDBMS-specific constraint restrictions explicitly (for example, MySQL Error 3823 forbids `CHECK` constraints referencing columns used in FK referential actions; enforce self-loop prevention inside triggers alongside `WITH RECURSIVE` DAG cycle detection on adjacency tables such as `TASK_DEPENDENCY`).
   - Keep DDL, triggers/routines, seed DML, analytical queries, and verification scripts cleanly modularized and idempotently re-runnable in strict dependency order (`Schema DDL -> Triggers & Routines -> Seed DML -> Queries -> Verification`).

## 3. Five-Category SQL Verification Matrix

Do not report any schema, trigger, or query deliverable as complete without fresh execution evidence across all five categories:

| Verification Category | Mandatory Pass Criteria |
| --- | --- |
| **1. Clean Sequential Execution** | Full script sequence from fresh database initialization through DDL, triggers/routines, seed DML, and reporting queries executes with `0` SQL errors. |
| **2. Boundary and Exact Precision** | Exact numeric thresholds pass while `+0.01` overruns reject (for example, `12.00` daily hours pass and `12.01` reject); `DECIMAL` sums reconcile with `0` rounding drift. |
| **3. Declarative Constraint Rejections** | Out-of-range `CHECK` inputs, duplicate `UNIQUE` alternate keys, and disallowed `FK` parent modifications or deletions reject cleanly. |
| **4. Trigger Enforcement and Bypass Audit** | Every business-rule trigger pairs compliance `SELECT` audits with negative `INSERT` and `UPDATE` tests raising the expected `SQLSTATE`, plus `DELETE` bypass verification. |
| **5. Cross-Artifact Schema Parity** | Table names, column names, PKs, FKs, and rule IDs in physical SQL match conceptual ER diagrams, normalization proofs, and documentation `100%`. |
