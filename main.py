from scholarly import scholarly
import requests
import bisect

USER_PROFILE_PREFIX = "/citations?hl=en&amp;user="
AFTER_AUTHOR_INDICATOR = "x26after_author\\x3d"

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

origin = input("Enter the URL of the first page of the institution's Google scholar page (the only HTTP get parameters should be view_op, org, hl, and maybe oi): ")
url = origin

while hasSignificantFaculty:
    r = requests.get(url)
    htmlSrc = r.text

    facultyIDSet = set()

    index = htmlSrc.find(USER_PROFILE_PREFIX)
    while index != -1:
        quote = htmlSrc.find("\"", index)
        facultyID = htmlSrc[index + len(USER_PROFILE_PREFIX) : quote]
        print(facultyID)

        if facultyID not in facultyIDSet:
            facultyIDSet.add(facultyID)

            author = scholarly.search_author_id(facultyID)
            print("Filling author publications and counts")
            author.fill(['publications', 'counts'])

            citedby = 0
            for i in author.cites_per_year.values():
                citedby += i

            if citedby < lastUpdatedH:
                hasSignificantFaculty = False
                break

            print("Adding in author publications")
            for pub in author.publications:
                if int(pub.bib['cites']) < lastUpdatedH:
                    break
                bisect.insort(publications, int(pub.bib['cites']))
        index = htmlSrc.find(USER_PROFILE_PREFIX, quote)

    calculateHindex()
    print("Last updated h-index: " + str(lastUpdatedH))

    nextIndex = htmlSrc.find(AFTER_AUTHOR_INDICATOR)
    slash = htmlSrc.find("\\", nextIndex + len(AFTER_AUTHOR_INDICATOR))
    after_author = htmlSrc[nextIndex + len(AFTER_AUTHOR_INDICATOR) : slash]

    single = htmlSrc.find("\'", nextIndex)
    astart = htmlSrc[slash + 14 : single]

    url = origin + "&after_author=" + after_author + "&astart=" + astart
    print(url)