# DM8106_T9_Frequent_Item_Detection


## Feedback from Ninh
For task, I think you should consider top-k (the top-k frequent items) or heavy hitter (item frequency > threshold). One of these tasks should be enough for the project. Why? It would help you to narrow down the search for algorithms to test.
It is nice to have drift, or estimate frequency... However, in principle we could not estimate f(x) for any x with limited memory, so we would not care much the item with low f(x). This is the reason we consider top-k or heavy hitter in data stream.
When you narrow down the task, and the corresponding research questions, then you can refine the project objectives...
Libraries are great, you might select one of them ;-)
So far, you have counter-based (reservoir sampling, MisraGries, Space-Saving) vs sketch-based. They are all good to answer your questions.
For dataset: you might consider the dataset has skew frequency distribution, otherwise, it will be difficult to achieve high accuracy.