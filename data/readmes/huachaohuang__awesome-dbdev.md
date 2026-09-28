# Awesome Database Development

Database development is interesting and challenging. You can always find interesting things to learn and challenging problems to solve. You need to know a lot of things and get them right to build a reliable and high-performance database. And it takes time, a lot of time, to think and practice. I have been working on database development for ten years. However, as the proverb goes, *the more I know, the more I realize I don't know.* So, I collect these awesome materials here to review them from time to time. I think it will be helpful to those who share the same interests as me.

## Introduction

- [Readings in Database Systems](http://www.redbook.io/)

  Readings in Database Systems (commonly known as the "Red Book") has offered readers an opinionated take on both classic and cutting-edge research in the field of data management since 1988.

- [Designing Data-Intensive Applications](https://www.oreilly.com/library/view/designing-data-intensive-applications/9781491903063/)

  In this practical and comprehensive guide, author Martin Kleppmann helps you navigate this diverse landscape by examining the pros and cons of various technologies for processing and storing data. Software keeps changing, but the fundamental principles remain the same. With this book, software engineers and architects will learn how to apply those ideas in practice, and how to make full use of data in modern applications.

- [How does a relational database work](http://coding-geek.com/how-databases-work/) (2015)

- [Elements Of Scale: Composing And Scaling Data Platforms](http://www.benstopford.com/2015/04/28/elements-of-scale-composing-and-scaling-data-platforms/) (2015)

  Today’s data platforms range greatly in complexity. From simple caching layers or polyglotic persistence right through to wholly integrated data pipelines. There are many paths. They go to many different places. In some of these places at least, nice things are found.

  So the aim for this talk is to explain how and why some of these popular approaches work. We’ll do this by first considering the building blocks from which they are composed. These are the intuitions we’ll need to pull together the bigger stuff later on.

- [Apache Kafka, Samza, and the Unix Philosophy of Distributed Data](http://www.confluent.io/blog/apache-kafka-samza-and-the-unix-philosophy-of-distributed-data) (2015)

  One of the things I realised while doing research for my book is that contemporary software engineering still has a lot to learn from the 1970s. As we’re in such a fast-moving field, we often have a tendency of dismissing older ideas as irrelevant – and consequently, we end up having to learn the same lessons over and over again, the hard way. Although computers have got faster, data has got bigger and requirements have become more complex, many old ideas are actually still highly relevant today. In this blog post I’d like to highlight one particular set of old ideas that I think deserves more attention today: the Unix philosophy. I’ll show how this philosophy is very different from the design approach of mainstream databases, and explore what it would look like if modern distributed data systems learnt a thing or two from Unix.

## System programming

- [What Every Programmer Should Know About Memory](papers/cpumemory.pdf) (2007)

  This paper explains the structure of memory subsystems in use on modern commodity hardware, illustrating why CPU caches were developed, how they work, and what programs should do to achieve optimal performance by utilizing them.

- [What Every Systems Programmer Should Know About Concurrency](papers/concurrency.pdf) (2018)

  Seasoned programmers are familiar with tools like mutexes, semaphores, and condition variables. But what makes them work? How do we write concurrent code when we can’t use them, like when we’re working below the operating system in an embedded environment, or when we can’t block due to hard time constraints? And sin

[...截断...]

ce your system transforms your code into things you didn’t write, running in orders you never asked for, how do multithreaded programs work at all? Concurrency — especially on modern hardware — is a complicated and unintuitive topic, but let’s try to cover some fundamentals.

- [Everything You Always Wanted to Know About Synchronization but Were Afraid to Ask](papers/synchronization.pdf) (2013)

  This paper presents the most exhaustive study of synchronization to date. We span multiple layers, from hardware cache-coherence protocols up to high-level concurrent software. We do so on different types of architectures, from single-socket – uniform and non-uniform – to multi-socket – directory and broadcast-based – many-cores.

### Linux kernel

- [Understanding the Linux Kernel](https://www.oreilly.com/library/view/understanding-the-linux/0596005652/)

- [Understanding the Linux Virtual Memory Manager](https://www.kernel.org/doc/gorman/)

- [ext4 Data Structures and Algorithms](https://www.kernel.org/doc/html/latest/filesystems/ext4/index.html)

  This document attempts to describe the on-disk format for ext4 filesystems. The same general ideas should apply to ext2/3 filesystems as well, though they do not support all the features that ext4 supports, and the fields will be shorter.

- [The Slab Allocator: An Object-Caching Kernel Memory Allocator](papers/slab.pdf) (1994)

  This paper presents a comprehensive design overview of the SunOS 5.4 kernel memory allocator. This allocator is based on a set of object-caching primitives that reduce the cost of allocating complex objects by retaining their state between uses.

## Storage Device

### Media

- [Hard Disk Drive (HDD)](https://en.wikipedia.org/wiki/Hard_disk_drive)
- [How HDD Works](https://www.youtube.com/watch?v=Ep-yM894mQQ) (Video)
- [The Development of HDD Technique](https://www.youtube.com/watch?v=wteUW2sL7bc) (Video)

- [Solid-State Drive (SSD)](https://en.wikipedia.org/wiki/Solid-state_drive)
- [How Flash Memory Works](https://www.youtube.com/watch?v=s7JLXs5es7I) (Video)
- [Coding for SSDs - What every programmer should know about SSDs](http://codecapsule.com/2014/02/12/coding-for-ssds-part-1-introduction-and-table-of-contents/)

### Interface

- [A History of PC Buses - From ISA to PCI Express](https://www.youtube.com/watch?v=qla-5isbK60) (Video)
- [Serial Attached SCSI (SAS)](https://en.wikipedia.org/wiki/Serial_Attached_SCSI)
- [Understanding SCSI](https://www.youtube.com/watch?v=pR7SdrXdT4M) (Video)
- [Serial AT Attachment (SATA)](https://en.wikipedia.org/wiki/Serial_ATA)
- [PCI Express (PCIe)](https://en.wikipedia.org/wiki/PCI_Express)
- [NVM Express (NVMe)](https://en.wikipedia.org/wiki/NVM_Express)

## Storage Engine

- [The Five-Minute Rule for Trading Memory for Disc Accesses](papers/five-minute-rule-1987.pdf) (1987)
- [The Five-Minute Rule 10 Years Later, and Other Computer Storage Rules of Thumb](papers/five-minute-rule-1997.pdf) (1997)
- [The Five-Minute Rule 20 Years Later, and How Flash Memory Changes the Rules](papers/five-minute-rule-2007.pdf) (2007)
- [The Five-Minute Rule 30 Years Later, and its Impact on the Storage Hierarchy](papers/five-minute-rule-2017.pdf) (2017)

- [The Design and Implementation of a Log-Structured File System](papers/lfs.pdf) (1991)

  This paper presents a new technique for disk storage management called a log-structured file system. A log-structured file system writes all modifications to disk sequentially in a log-like structure, thereby speeding up both file writing and crash recovery.

- [Efficiently Reclaiming Space in a Log Structured Store](papers/lss.pdf) (2020)

  A log structured store uses a single write I/O for a number of diverse and non-contiguous pages within a large buffer instead of using a write I/O for each page separately. This requires that pages be relocated on every write, because pages are never updated in place. Instead, pages are dynamically remapped on every write. Log structuring was invented for and 