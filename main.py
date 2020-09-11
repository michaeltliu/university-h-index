from scholarly import scholarly
import requests
import bisect

USER_PROFILE_PREFIX = "/citations?hl=en&amp;user="
AFTER_AUTHOR_INDICATOR = "x26after_author\\x3d"
INSTITUTION_NAME_HEADER = "<h2 class=\"gsc_authors_header\">"

publications = []
hasSignificantFaculty = True
lastUpdatedH = 0

# Expects an increasing, sorted array
def calculateHindex():
    global publications
    global lastUpdatedH

    arr = publications[:]
    arr.reverse()
    ind = lastUpdatedH - 1
    while ind < len(arr) and ind < arr[ind]:
        ind += 1
    lastUpdatedH = ind
    return ind

origin = input("Enter the URL of the first page of the institution's Google scholar page (the only HTTP get parameters should be view_op, org, and hl): ")
text = requests.get(origin).text
header = text.find(INSTITUTION_NAME_HEADER)
end = text.find(" <", header)
univ = text[header + len(INSTITUTION_NAME_HEADER) : end]
print("\n" + univ + "\n")

url = origin

while hasSignificantFaculty:
    r = requests.get(url)
    htmlSrc = r.text

    facultyIDSet = set()

    index = htmlSrc.find(USER_PROFILE_PREFIX)
    while index != -1:
        quote = htmlSrc.find("\"", index)
        facultyID = htmlSrc[index + len(USER_PROFILE_PREFIX) : quote]

        if facultyID not in facultyIDSet:
            facultyIDSet.add(facultyID)

            author = scholarly.search_author_id(facultyID)
            print("Filling publication and citation data for " + author.name)
            author.fill(['publications', 'counts'])

            print("Checking if faculty is significant enough to continue")
            citedby = 0
            for i in author.cites_per_year.values():
                citedby += i

            if citedby < lastUpdatedH:
                hasSignificantFaculty = False
                break

            print("Adding " + author.name + "\'s publications: ", end = "")
            c = 0
            for pub in author.publications:
                if int(pub.bib['cites']) < lastUpdatedH:
                    break
                bisect.insort(publications, int(pub.bib['cites']))
                c += 1
            print(str(c) + " out of " + str(len(author.publications)) + " were added")
        
        index = htmlSrc.find(USER_PROFILE_PREFIX, quote)
        print()

    calculateHindex()
    print("Most recent h-index value: " + str(lastUpdatedH) + "\n")

    nextIndex = htmlSrc.find(AFTER_AUTHOR_INDICATOR)
    slash = htmlSrc.find("\\", nextIndex + len(AFTER_AUTHOR_INDICATOR))
    after_author = htmlSrc[nextIndex + len(AFTER_AUTHOR_INDICATOR) : slash]

    single = htmlSrc.find("\'", nextIndex)
    astart = htmlSrc[slash + 14 : single]

    url = origin + "&after_author=" + after_author + "&astart=" + astart
    print("Starting page " + str(int(astart)/10 + 1) + "\n")
print("Final h-index value: " + str(lastUpdatedH))