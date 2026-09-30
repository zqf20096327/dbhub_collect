# Benchmarking openGauss Against PostgreSQL： A Comparative Analysis

## Introduction

Aimed at comparing the efficiency of openGauss and PostgreSQL, we designed three parts of the experiments in the project. The first part contains the basic operations of databases including of and using the combination of these operations. The second part concentrates on the optimization of on the two databases. The third part combining the introduction of Gaussdb in its official documents, tests its announced product strengths like and SQL Bypass for simple statements.

## Environment Needed

$$
\begin{aligned}
    &\text{DBMS Version}
    &&\text{openGauss 3.1.1}\\
    &\text{\quad}
    &&\text{PostgreSQL 14-22.04 beta}\\
    &\text{Libpqxx Version}
    &&\text{7.9.3}\\
    &\text{C++}
    &&\text{C++ 20}\\
\end{aligned}
$$

The project use C++ to interact with DBMS, so you need to introduce libpqxx under the directory. An example "CMakeLists.txt" file is as follow.

```
cmake_minimum_required(VERSION 3.5.0)
project(gauss VERSION 0.1.0 LANGUAGES C CXX)
set(CMAKE_CXX_STANDARD 20)
add_executable(gauss main.cpp)
add_subdirectory(libpqxx build-pqxx)
target_link_libraries(gauss PRIVATE pqxx)
```

## Files

"project3.pdf" is a detailed report of the process of the project.

"xxx.cpp" are the codes used in the project.