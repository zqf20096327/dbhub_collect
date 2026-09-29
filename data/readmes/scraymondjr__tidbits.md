# tidbits

## Debugging
Debugging is asking questions to find an answer, where the answer is typically a description of a bug.

The complexity of a software solution can be determined by asking: How many questions does it take to debug a problem?

Distributed software is often said to be inherently complex and that implied complexity can be seen from asking the above question. A typical distributed system will have at least a few components in it. When a problem occurs, a debugger typically must span multiple of these components to try to discover the root cause of the problem. This means that debugging a distributed solution normally requires asking at least one question per component. Contrast this to a non-distributed system where a single process is responsible for the entire workload. If a problem occurs, a debugger would not need to ask any questions as to where the problem is originating: it is in the one and only process. 

