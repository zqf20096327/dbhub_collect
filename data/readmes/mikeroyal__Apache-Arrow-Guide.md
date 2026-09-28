<h1 align="center">
 <img src="https://user-images.githubusercontent.com/45159366/136712029-ea850e73-0ca0-47a8-ac9d-4e363c5e14ce.png">
  <br />
  Apache Arrow Guide
</h1>

#### A guide covering Apache Arrow including the applications, libraries and tools that will make you better and more efficient with Apache Arrow development.

 **Note: You can easily convert this markdown file to a PDF in [VSCode](https://code.visualstudio.com/) using this handy extension [Markdown PDF](https://marketplace.visualstudio.com/items?itemName=yzane.markdown-pdf).**

<img src="https://user-images.githubusercontent.com/45159366/136712035-f3cf3d10-978b-45b0-9edd-25b3c61a95ed.png">

<p align="center">
<img src="https://user-images.githubusercontent.com/45159366/136712036-c7d73185-9d48-4290-8ef9-60f5e922eb95.png">
 <br />
</p>

 Apache Arrow native implementations and bindings for systems languages. Source: [Apache Arrow](https://arrow.apache.org/)

# Table of Contents

1. [Apache Arrow Learning Resources](https://github.com/mikeroyal/Apache-Arrow-Guide#Apache-Arrow-learning-resources)

2. [Apache Arrow Tools, Libraries, and Frameworks](https://github.com/mikeroyal/Apache-Arrow-Guide#Apache-Arrow-tools-libraries-and-frameworks)

3. [Machine Learning](https://github.com/mikeroyal/Apache-Arrow-Guide#machine-learning)

4. [Algorithms](https://github.com/mikeroyal/Apache-Arrow-Guide#Algorithms)

5. [Deep Learning Development](https://github.com/mikeroyal/Apache-Arrow-Guide#Deep-Learning-Development)

6. [Reinforcement Learning Development](https://github.com/mikeroyal/Apache-Arrow-Guide#Reinforcement-Learning-Development)

7. [Computer Vision Development](https://github.com/mikeroyal/Apache-Arrow-Guide#computer-vision-development)

8. [Natural Language Processing (NLP) Development](https://github.com/mikeroyal/Apache-Arrow-Guide#nlp-development)

9. [Bioinformatics](https://github.com/mikeroyal/Apache-Arrow-Guide#bioinformatics)

10. [Databases](https://github.com/mikeroyal/Apache-Arrow-Guide#databases)

11. [CUDA Development](https://github.com/mikeroyal/Apache-Arrow-Guide#cuda-development)

12. [MATLAB Development](https://github.com/mikeroyal/Apache-Arrow-Guide#matlab-development)

13. [Java Development](https://github.com/mikeroyal/Apache-Arrow-Guide#java-development)

14. [C/C++ Development](https://github.com/mikeroyal/Apache-Arrow-Guide#cc-development)

15. [C# Development](https://github.com/mikeroyal/Apache-Arrow-Guide#c-development)

16. [Python Development](https://github.com/mikeroyal/Apache-Arrow-Guide#python-development)

17. [JavaScript Development](https://github.com/mikeroyal/Apache-Arrow-Guide#javascript-development)

18. [Go Development](https://github.com/mikeroyal/Apache-Arrow-Guide#go-development)

19. [Scala Development](https://github.com/mikeroyal/Apache-Arrow-Guide#scala-development)

20. [R Development](https://github.com/mikeroyal/Apache-Arrow-Guide#r-development)

21. [Ruby Development](https://github.com/mikeroyal/Apache-Arrow-Guide#ruby-development)

22. [Rust Development](https://github.com/mikeroyal/Apache-Arrow-Guide#rust-development)


# Apache Arrow Learning Resources
[Back to the Top](https://github.com/mikeroyal/Apache-Arrow-Guide#table-of-contents)

[Apache Arrow](https://arrow.apache.org/) is a language-independent columnar memory format for flat and hierarchical data, organized for efficient analytic operations on modern hardware like CPUs and GPUs. Languages that have Arrow libraries (under development) include C, C++, Go, Java, JavaScript, Python, Ruby and Rust.

[Apache Arrow Documentation](http://arrow.apache.org/docs)

[Accelerating End-to-End Data Science Workflows | Deep Learning Institute | NVIDIA](https://courses.nvidia.com/courses/course-v1:DLI+S-DS-01+V1/about)

[Introducing Apache Arrow | Cloudera](https://blog.cloudera.com/introducing-apache-arrow-a-fast-interoperable-in-memory-columnar-data-structure-standard/)

[Understanding Apache Arrow Flight | Dremio](https://www.dremio.com/understanding-apache-

[...截断...]

arrow-flight)

[Apache Arrow in PySpark | Apache Spark](http://spark.apache.org/docs/latest/api/python/user_guide/arrow_pandas.html)

[PySpark Usage Guide for Pandas with Apache Arrow | Apache Spark](https://spark.apache.org/docs/2.4.0/sql-pyspark-pandas-with-arrow.html)

[Apache Arrow Training Courses | NobleProg](https://www.nobleprog.com/apache-arrow-training)

[Apache Spark Quick Start](https://spark.apache.org/docs/latest/quick-start.html)

[What is Apache Spark? | IBM](https://www.ibm.com/cloud/learn/apache-spark)

[Introduction to Apache Spark and Analytics | AWS](https://aws.amazon.com/big-data/what-is-spark/)

[Apache Spark 3.0: For Analytics & Machine Learning | NVIDIA](https://www.nvidia.com/en-us/deep-learning-ai/solutions/data-science/apache-spark-3/)

[.NET for Apache Spark™ | Big data analytics](https://dotnet.microsoft.com/apps/data/spark)

[Apache Spark Basics | MATLAB & Simulink](https://www.mathworks.com/help//compiler/spark/apache-spark-basics.html)

[MATLAB Hadoop and Spark | MATLAB & Simulink](https://www.mathworks.com/products/compiler/hadoop-and-spark.html)

[Top Apache Spark Courses Online | Coursera](https://www.coursera.org/courses?query=apache%20spark)

[Top Apache Spark Courses Online | Udemy](https://www.udemy.com/topic/apache-spark/)

[Apache Spark In-Depth (Spark with Scala) | Udemy](https://www.udemy.com/course/apache-spark-in-depth-spark-with-scala/)

[Learn Apache Spark with Online Courses | edX](https://www.edx.org/learn/apache-spark)

[Apache Spark Essential Training Online Class | LinkedIn Learning](https://www.linkedin.com/learning/apache-spark-essential-training)

[Cloudera Developer Training for Apache Spark™ and Hadoop | Cloudera](https://www.cloudera.com/about/training/courses/developer-training-for-spark-and-hadoop.html)

[Databricks Certified Associate Developer for Apache Spark 3.0 certification | Databricks](https://academy.databricks.com/exam/databricks-certified-associate-developer)

[Apache Spark Training Courses | NobleProg](https://www.nobleprog.com/apache-spark-training)

# Apache Arrow Tools, Libraries, and Frameworks
[Back to the Top](https://github.com/mikeroyal/Apache-Arrow-Guide#table-of-contents)

[Apache Parquet](https://parquet.apache.org/) is a columnar storage format available to any project in the Hadoop ecosystem, regardless of the choice of data processing framework, data model or programming language.

[DataFusion](https://arrow.apache.org/datafusion) is an extensible query execution framework, written in Rust, that uses [Apache Arrow](https://arrow.apache.org/) as its in-memory format. DataFusion supports both an SQL and a DataFrame API for building logical query plans as well as a query optimizer and execution engine capable of parallel execution against partitioned data sources (CSV and Parquet) using threads.

[Fletcher](https://github.com/abs-tudelft/fletcher) is a framework that helps to integrate FPGA accelerators with tools and frameworks that use Apache Arrow in their back-ends.

[Apache Flink™](https://flink.apache.org/) is a framework and distributed processing engine for stateful computations over unbounded and bounded data streams. Flink has been designed to run in all common cluster environments, perform computations at in-memory speed and at any scale.

[Apache Cassandra™](https://cassandra.apache.org/) is an open source NoSQL distributed database trusted by thousands of companies for scalability and high availability without compromising performance. Cassandra provides linear scalability and proven fault-tolerance on commodity hardware or cloud infrastructure make it the perfect platform for mission-critical data.

[Apache Flume](https://flume.apache.org/) is a distributed, reliable, and available service for efficiently collecting, aggregating, and moving large amounts of streaming event data.

[Apache Mesos](http://mesos.apache.org/) is a cluster manager that provides efficient resource isolation and sharing across distributed applications, or