# Working with the global user dataset

## Introduction

The global user database (LINK) is about 128 GB, effectively being a 943 x 69 million matrix. This (for me at least) posed challenges of its own, since it's not normal for me to work with databases of this size. Below I give some notes that may help someone who looks at this later.

## Excel

The most fundamental problem with it is that it can only handle 1048576 (2<sup>20</sup>) of rows, which is a shame, because it's otherwise a really powerful and intuitive tool.

So suppose you are fine with that. Then importing the CSV is pretty easy - the legacy import wizard is often a better choice as that directly imports the CSV to the spreadsheet rather than the "modern" method of creating a "connection". 

Once you're done with that, some analysis can be done pretty easily. Load Analytics ToolPak. Then O(*n*) based operations can be done easily (for instance, descriptive statistics on *n* columns). However, trying to perform O(*n*<sup>2</sup>) operations (such as trying to compute the covariance matrix for *n* columns) is not worth it for larger values of *n*. The main issue is that Analytics ToolPak is single-threaded. 

## SQL

