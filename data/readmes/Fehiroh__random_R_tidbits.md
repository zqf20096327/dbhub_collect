# random_R_tidbits
This is a repository that includes articles and bits of code I've found useful and would like to store for later usage

### fuzzy_join, BiocManager, and IRanges
fuzzy_join is an amazing library, but it sometimes gets into compatibility scuffles with various versions of R due to issues with 
it's dependencies, namely Biocmanager and IRanges. Here's a great way to make sure both BiocManager and IRanges get installed:  

```r
if (!requireNamespace("BiocManager", quietly = TRUE))
  install.packages("BiocManager")

BiocManager::install("IRanges")
```
