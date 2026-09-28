<!-- TOC start (generated with https://github.com/derlin/bitdowntoc) -->

# GateSmashers-DBMS

Unlock the power of structured data with our meticulously curated repository of notes from a renowned Database Management System (DBMS) lecture series. Dive deep into the world of databases as we distill complex concepts and real-world applications into easily digestible insights. Whether you're a student striving for academic excellence or a professional looking to bolster your database expertise, our notes are your gateway to mastering the art of data management. Explore, learn, and take control of data like never before with this comprehensive DBMS lecture series compendium

🔗 [Database Management Systems - Playlist](https://www.youtube.com/playlist?list=PLxCzCOWd7aiFAN6I8CuViBuCdJgiOkT2Y)

## Table of Content

### Note: 🚧 Missing Lecture Notes will be updated soon

   * [**Lecture 05**: **Schema in a Database**](#lecture-05-schema-in-a-database)
   * [**Lecture 06**: **Three Schema Architecture in DBMS**](#lecture-06-three-schema-architecture-in-dbms)
   * [**Lecture 07**: **Data Independence and 3 Schema Architecture**](#lecture-07-data-independence-and-3-schema-architecture)
   * [**Lecture 08**: **Candidate Key in Databases**](#lecture-08-candidate-key-in-databases)
   * [**Lecture 09**: **Primary Key in Databases**](#lecture-09-primary-key-in-databases)
   * [**Lecture 10**: **Foreign Key in Databases -** **Part 1**](#lecture-10-foreign-key-in-databases---part-1)
   * [**Lecture 11**: **Foreign Key in Databases - Part 2**](#lecture-11-foreign-key-in-databases---part-2)
   * [**Lecture 14**: **Entity-Relationship (ER) Model Basics**](#lecture-14-entity-relationship-er-model-basics)
   * [**Lecture 15**: **Types of Attributes in Relational Databases**](#lecture-15-types-of-attributes-in-relational-databases)
   * [**Lecture 16**: **Degree of Relationship in Database** **(One-to-One)**](#lecture-16-degree-of-relationship-in-database-one-to-one)
   * [**Lecture 17**: **Degree of Relationship in Database (One-to-Many)**](#lecture-17-degree-of-relationship-in-database-one-to-many)
   * [**Lecture 18**: **Degree of Relationship in Database (Many-to-Many)**](#lecture-18-degree-of-relationship-in-database-many-to-many)
   * [Lecture 69: **Introduction to Transaction Concurrency**](#lecture-69-introduction-to-transaction-concurrency)
   * [Lecture70: **ACID Properties in Database Transactions**](#lecture70-acid-properties-in-database-transactions)
   * [Lecture71: **Transaction States**](#lecture71-transaction-states)
   * [Lecture72: **Serial Schedule vs. Parallel** **Schedule in Transactions**](#lecture72-serial-schedule-vs-parallel-schedule-in-transactions)
   * [Lecture73: **Read-Write Problem (Read-Write Conflict)**](#lecture73-read-write-problem-read-write-conflict)
   * [Lecture74: **Irrecoverable Schedule**](#lecture74-irrecoverable-schedule)
   * [Lecture75: **Cascading vs. Cascade-less Schedules**](#lecture75-cascading-vs-cascade-less-schedules)
   * [Lecture76: **Serializability in Database Transactions**](#lecture76-serializability-in-database-transactions)
   * [**Lecture 77**: **Finding Conflict Equivalent Schedules**](#lecture-77-finding-conflict-equivalent-schedules)
   * [**Lecture 78**: **Conflict Serializability**](#lecture-78-conflict-serializability)
   * [**Lecture 79**: **View Serializability**](#lecture-79-view-serializability)
   * [**Lecture 80**: **Concurrency Control Protocols - Shared-Exclusive Locking**](#lecture-80-concurrency-control-protocols---shared-exclusive-locking)
   * [**Lecture 81**: **Shared-Exclusive Locking Protocol - Problems and Considerations**](#lecture-81-shared-exclusive-locking-protocol---problems-and-considerations)
   * [**Lecture 82**: **Two-Phase Locking Protocol (2PL)**](#lecture-82-two-phase-locking-protocol-2pl)
   * [**Lecture 83**: **Problems in Two-Phase Locking Protocol (2PL)**](#lecture-83-problems-in-two-phase-locking-protocol-2pl)
   * [**Lecture 84**: **Strict 2PL and Ri

[...截断...]

gorous 2PL**](#lecture-84-strict-2pl-and-rigorous-2pl)
   * [**Lecture 85**: **Timestamp Ordering Protocol**](#lecture-85-timestamp-ordering-protocol)
   * [**Lecture 86**: **Numeric Question on Basic Timestamp Ordering Protocol**](#lecture-86-numeric-question-on-basic-timestamp-ordering-protocol)
   * [Lecture87: **Why Indexing is used?**](#lecture87-why-indexing-is-used)
   * [Lecture88: **Numerical Example on I/O Cost in Indexing Part 1**](#lecture88-numerical-example-on-io-cost-in-indexing-part-1)
   * [Lecture89: **Numerical Example on I/O Cost in Indexing Part 2**](#lecture89-numerical-example-on-io-cost-in-indexing-part-2)
   * [Lecture90: **Types of Indexes in Databases**](#lecture90-types-of-indexes-in-databases)
   * [Lecture91: **Primary Index in Databases**](#lecture91-primary-index-in-databases)
   * [Lecture92: **Clustered index in Databases**](#lecture92-clustered-index-in-databases)
   * [Lecture93: **Secondary Index in Databases**](#lecture93-secondary-index-in-databases)

<!-- TOC end -->

## [**Lecture 05**](https://youtu.be/pDX4NR4eY3A): **Schema in a Database**
- **Introduction:**
	- Schema is a fundamental concept used in various areas of databases.
	- Provides a logical representation of data in the database.
- **What is Schema?**
	- Schema: Logical representation of a database.
	- Physical vs. Logical Representation:
		- Physical: How data is stored on hard drives or backend servers.
		- Logical: How data is represented conceptually.
	- Example: In Relational Database Management Systems (RDBMS), data is logically represented as tables or relations.
	- Entities and Relations: Entities (e.g., Student, Course) represented as tables with attributes (columns).
	- Schema Design: Defining the structure of entities, e.g., attributes for a Student entity (e.g., Roll Number, Name, Address).
	- Schema = Logical Structure: Tables, attributes, relationships, and constraints.
- **Implementing Schema:**
	- Implementation of schema is done using SQL (Structured Query Language).
	- SQL, especially Data Definition Language (DDL) commands, used for schema design and implementation.
	- DDL Commands: Create table, Alter table, Drop table, etc.
	- Schema Implementation: Translates the logical representation into a structured database.
	- Example: Roll Number (integer), Name (varchar/character), Address (character).
- **Three Schema Architecture:**
	- Conceptual Schema: Represents data logically.
	- Logical Schema: Defines the structure and relationships of the data.
	- Physical Schema: Specifies how data is physically stored and accessed.
	- Conceptual schema is the main focus for logical representation.
- **Schema as a Structure:**
	- Schema can be seen as a structure.
	- It may consist of multiple related tables.
	- A schema is a collection of tables, forming the logical structure of the database.
- **Conclusion:**
	- Schema is a logical representation of a database.
	- It is used to define the structure and relationships of data.
	- Schema design can be implemented using SQL, especially DDL commands.
	- In databases, schema is a fundamental concept used in various aspects of data management and querying.
## [**Lecture 06**](https://youtu.be/5fs1ldO6B5c): **Three Schema Architecture in DBMS**
- **Introduction:**
	- Three Schema Architecture enhances data independence and provides data abstraction.
- **Schema Definition:**
	- Schema refers to the structure or organization of data.
	- In a database context, schema defines how data is organized, stored, and accessed.
- **Three Schema Architecture:**
	- Three Schema Architecture consists of three levels:
		- 1. **External Schema (View Level):**
			- Also known as View Level.
			- Concerned with how data is presented to different user groups.
			- Each user group may have its own view or representation of the data.
			- Example: Students and faculty members in a university may have different views of the same data.
		- 2. **Conceptual Schema (Logical Level):**
			- Defines the 