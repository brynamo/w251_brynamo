# HW12 Questions
1. How much disk space is used after step 4?
  - After running the cluster for over 24 hours and crawling over 35,000 URLS during step 4 the current usage is at:
|Filesystem|Type|Size|Used|Avail|Use%|Mounted on|
|----------|----|----|----|-----|----|----------|
|gpfsfpo|gpfs|300G|9.7G|291G|4%|/gpfs/gpfsfpo|

2. Did you parallelize the crawlers in step 4? If so, how?
  - I did not initially, due to difficulties getting the cluster up and stable. To run in parallel though, I would have broken the initial list down into 3 equal size lists and had the crawler program running on all 3 nodes and saved to the same directory in the GPFS so to speed things up.
3. Describe the steps to de-duplicate the web pages you crawled.
  - To de-duplicate the we pages, there is a built method called `lazynlp.dedup_lines` that takes in the files and deduplicates them into a new directory.
4. Submit the list of files you that your LazyNLP spiders crawled (ls -la).
  - In file hw12/data_files_output.txt
