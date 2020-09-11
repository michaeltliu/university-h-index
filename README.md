# University H-index Calculator

This program scrapes data from Google Scholar to determine the h-index of a given institution or university. 

From Wikipedia, "the h-index is defined as the maximum value of h such that the given author/journal has published h papers that have each been cited at least h times. The index is designed to improve upon simpler measures such as the total number of citations or publications".

To be clear, we are not computing the simple mean of the h-indices of all members/faculty affiliated with the institution. We are computing the h-index as if the entire faculty were a single, hyper-productive individual.

### Dependencies:
- Python 3.7 or above
- Scholarly: `pip3 install scholarly`

### To run:
1. `python3 main.py`
2. Search Google Scholar for the desired institution. At the top of the search results, there will a link that directs to the institution's page. Copy the link address and paste it into stdin.
3. Wait! The program takes a while to run, but provides regular updates as to what it's doing. Once you see the "most recent h-index" value begin to plateau, you can assume the final value will be in that ballpark.

### Note:
- For each faculty member, there will be a line that prints out how many of their publications were "added". This number will often not be 100% of their total publications. This is not an error -- insignificant publications are skipped in order to save on time and memory.
- The vast majority of the program's runtime comes from waiting on the Scholarly API. The API is inherently slow. There's nothing I can do about it.