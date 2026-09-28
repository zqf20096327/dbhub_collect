# LearningNeo4j

<!--
TODO
Creating indexes
https://neo4j.com/graphacademy/online-training/introduction-to-neo4j/part-7/
-->

## Content

1. [Graph Database Fundamentals](#graph-database-fundamentals)
2. [Neo4J](#neo4j)
    * [Query Language Cypher](#cypher)
        * [Part one](#part-one)
        * [Part two](#part-two)
        * [Part three](#part-three)
        * [Part four](#part-four)
        * [Part five](#part-five)
        * [Part six](#part-six)
        * [Part seven](#part-seven)
        * [Part eight](#part-eight)
        * [Part nine](#part-nine)
        * [Part ten](#part-ten)
        * [Part eleven](#part-eleven)
        * [Part twelve](#part-twelve)
        * [Part thirteen](#part-thirteen)
        * [Part fourteen](#part-fourteen)
        * [Part fiveteen](#part-fiveteen)
        * [Part sixteen](#part-sixteen)
        * [Example](#example---simple-graph)
        * [Application - Movies](#application---movie-graph)
        * [Application - Northwind](#application---northwind-graph)
        * [Recommendations - Movies](#recommendations)
            * [Personalized recommendations](#personalized-reccomendations)
	* [Fraud Detection](#fraud-detection)
3. [Index](#index)
4. [References](#references)

--------------------

## Graph Database Fundamentals

A graph database can store any kind of data using a few simple concepts:

1. **Nodes** - graph data records

    ![nodes](resources/nodes.PNG)

2. **Labels** - specifies the type of the node

    ![nodesTypes](resources/nodesTypes.PNG)

3. **Relationships** - connect nodes

    ![nodesTypes](resources/nodesTypesRelationships.PNG)

4. **Properties** - key-value pair properties

    ![nodesTypes](resources/nodesTypesRelationshipsProperties.PNG)

The simplest graph has just a single **node** with some named values called **Properties**:

![simpleGraph](resources/simpleGraph.PNG)

Nodes are the name for data records in a graph and the data is stored as Properties that can be simple key-value pairs.

Nodes can be grouped together by applying a Label to each member. In the example above we can set to that node the label **Person**.  Is important to know that a label is not a object and can't have any properties, is used only to categorize the nodes in a graph. A node can have zero or more labels based on the definition of that node.

To add more records we can simply add more nodes.

![moreNodes](resources/moreNodes.PNG)

Similar nodes can have different properties with different type: string, number or even boolean.
The dimension of a graph like this can be infinite because there is no limit to the number of nodes that can be added.

One of the properties of a database is to connect data, in a graph database the link is made by **Relationships**. To associate two nodes we can add **Relationship** between them wich describe how the records are related.

![relationships](resources/relationships.PNG)

A relationship are data records that need to have two properties: **direction** and **type**, and can also contains properties like nodes.

![relationshipProperties](resources/relationshipProperties.PNG)

A Graph database is an online database management system with Create, Read, Update and Delete (CRUD) operations working on a graph data model.
Graph database are generally build for use with [OLTP](#otlp) systems, they are normally optimized for transactional performance, and engineered with transactional integrity and operational availability in mind.

Unlike the other databases, relationships take first priority in graph databases so the foreign keys or out-of-band processing is no more necessary to link a data to another.

By assembling the simple abstractions of nodes and relationships into connected structures, graph databases enable us to build sophisticated models that map closely to out problem domain.

Many applications' data is modeled as relational data, indeed there are some 

[...截断...]

similarities between a relational model nad a graph model:

|Relational|Graph|
|----|----|
|Rows|Nodes|
|Joins|Relationships|
|Table names|Labels|
|columns|Properties|

There are even difference between this two databases:

|Relational|Graph|
|----|----|
|Each column must have field value|Nodes with the same label arent' required to have the same set of properties|
|Joins are calculated at query time|Relationships are stored on disk when they are created|
|A row can belong to one table|A node can have many labels|
|Try to get the schema defined and then make minimal changes to it after that|It's common for the schema to evolve with the application|
|More abstract focus when modeling|Common to use actual data items when modeling|

Here is the relational model:

![relationalModelClubs](resources/relationalModelClubs.PNG)

And here is the correspondig graph model:

![graphModelClubs](resources/graphModelClubs.PNG)

The graph model can be more versatile and can be upgrade without efforts, for example we want to add the confederation and country:

![graphModelClubsExtend](resources/graphModelClubsExtend.PNG)

--------------------

## Neo4J

![HelloWorld](resources/HelloWorld.PNG)

[video youtube](https://www.youtube.com/watch?v=_D19h5s73Co)

Connected information is everywhere in the world around us. Neo4j was build to efficiently store, handle, and query higly-connected data in your data model.

Neo4J is a high performance graph store with all the feature expected of a mature and robust database. The network structure is made by nodes and relationships rather than static tables.

Some definitions:

* Index free adjacency

    With index free adjaceny, when a node or relationship is written to the database, it is stored in the database as connected and any subsequent access to the data is done using pointer navigation wich is very fast. Since Neo4j is a native graph database, it supports very large graphs where connected data can be traversed in constant time without the need for an index.

    ![Neo4j index](resources/neo4jIndex.PNG)

    To know more read -> [Index-free adjacency](#index-free-adjacency)

* ACID

    Transactionality is very important for robust applications that require an atomicity, consistency, isolation, and durability guarantees for their data. If a relationship between nodes is created, not only is the relationship created, but the nodes are updated as connected.
    All of these updates to the database must all succeed or fail.

    ![Neo4j ACID](resources/neo4jACID.PNG)

    To know more read -> [ACID](#acid-consistency-model)

* Clusters

    Neo4j supports clusters that provide high availablity, scalability for read access to the data and failover which is important to many enterprises.

    ![neo4jCluster](resources/neo4jCluster.PNG)

    To know more read -> [Cluster](#cluster)

* Graph engine

    The Neo4j graph engine is used to interpret Cypher statements and also executes kernel-level code to store and retrive data, whether it is on disk, or cached in memory.

* Bolt

    Neo4j supports Java, JavaScript, Python, C#, and Go drivers that use Neo4j's bolt protocol for binary access to the database layer.
    Bolt is an efficiant binary protocol that compresses data sent over the wire as well encrypting the data.
    It's possible to create a java application that uses the bolt driver to access the Neo4j database and the application may use other packages that allow data integration between Neo4j and other data stores or uses as common framework such as spring.

* Tools

    [Neo4j browser](https://neo4j.com/sandbox-v2/) is an application that uses the JavaScript Bolt driver to access the graph engine of the Neo4j database server.

    [Bloom](https://neo4j.com/bloom/) enables you to visualize a graph without knowing much about Cypher ([youtube video](https://www.youtube.com/watch?v=KjINhGbG-So)).

    [ETL](https://