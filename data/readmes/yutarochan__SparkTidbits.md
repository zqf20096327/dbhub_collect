# SparkTidbits
Bunch of cookbook style code snippets, notes and other trivial Spark &amp; Scala tips for myself. 

---
**Flatten a List of Tuples**

Spark complains that there isn't an explicit conversion, and so you need to define that as follows:

	val tupleList = List((1,2), (3,4), (5,6))
  	tupleList.flatten {case (a,b) => List(a,b)}
  	>> List(1, 2, 3, 4, 5, 6)
---
**Handling Some/None Types In Array**

Some operations result in an None/Some type when performing a specific function. To get definite values or filter out None types, map the operation with a conditional as follows:
	
	// Define xxx as some arbitrary function which can possibly return Some or None.
	val json = lines.map(x => if (xxx != None) xxx.get)
	val json = lines.map(x => xxx).map(x => if (x != None) x.get)
