from scholarly import scholarly
import requests

USER_PROFILE_PREFIX = "/citations?hl=en&amp;user="
AFTER_AUTHOR_INDICATOR = "x26after_author\\x3d"

publications = set()
hasSignificantFaculty = True

url = input("Enter the URL of the first page of the university's Google scholar page: ")
while hasSignificantFaculty:
    r = requests.get(url)
    htmlSrc = r.text

    facultyIDSet = set()

    index = htmlSrc.find(USER_PROFILE_PREFIX)
    while index != -1:
        quote = htmlSrc.find("\"", index)
        facultyID = htmlSrc[index + len(USER_PROFILE_PREFIX) : quote]
        facultyIDSet.add(facultyID)

        if facultyID not in facultyIDSet:
            author = scholarly.search_author_id(facultyID)
            author.fill(['publications'])
            

        index = htmlSrc.find(USER_PROFILE_PREFIX, quote)

    nextIndex = htmlSrc.find(AFTER_AUTHOR_INDICATOR)
    slash = htmlSrc.find("\\", nextIndex + len(AFTER_AUTHOR_INDICATOR))
    after_author = htmlSrc[nextIndex + len(AFTER_AUTHOR_INDICATOR) : slash]

    single = htmlSrc.find("\'", nextIndex)
    astart = htmlSrc[slash + 14 : single]

    url = url + "&after_author=" + after_author + "&astart=" + astart
    print(url)
