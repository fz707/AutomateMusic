

from selenium import webdriver
import requests
import bs4

# create the selenium browser
browser = webdriver.Chrome(executable_path="C:\\chromedriver.exe")
#Choose spotify or soundcloud
# browser.get("https://www.spotify.com/us/")
browser.get("https://soundcloud.com")

# main menu
print()
print(">>> Welcome to the Music Automation Assistant")
print(">>> Use the directory to find music")
print(">>> Search Soundcloud for Tracks, Artist, and Mixes")
print()


#List of URLS
top_url = "https://soundcloud.com/charts/top"
new_url = "https://soundcloud.com/charts/new"
track_url = "https://soundcloud.com/search/sounds?q="
artist_url = "https://soundcloud.com/search/people?q="
mix_url_end = "&filter.duration=epic"

# new or top menu
while True:
    print(">>> Menu")
    print(">>> 1 - Search for a track")
    print(">>> 2 - Search for an artist")
    print(">>> 3 - Search for a mix")
    print(">>> 4 - Top charts")
    print(">>> 5 - New & hot charts")
    print(">>> 0 - Exit")
    print()
    selection = int(input(">>> Your choice: "))
    if selection == 0:
        browser.quit()
        break
    print()

    # search for a track
    if selection == 1:
        name = input("Name of the track: ")
        print()
        "%20".join(name.split(" "))
        browser.get(track_url + name)
        while True:
            print(">>> Play first song? Y or N?")
            c1=input(">>> Y or N?")
            if c1=="Y":
                browser.implicitly_wait(3)
                browser.find_element_by_class_name("soundTitle__playButton").click()
                break
            elif c1=="N":
                break
            else:
                print("Wrong Input")
                continue
        continue

    # search for an artist
    if selection == 2:
        name = input("Name of the artist: ")
        print()
        "%20".join(name.split(" "))
        browser.get(artist_url + name)
        continue

    if selection == 3:
        name = input("Name of the mix: ")
        print()
        "%20".join(name.split(" "))
        browser.get(track_url + name + mix_url_end)
        continue

    # genre menu
    while True:
        print(">>> Genres Available:")
        print()

        # genre menu
        url = ''
        if selection == 4:
            url = top_url
        else:
            url = new_url

        # parse the html with beautiful soup
        request = requests.get(url)
        soup = bs4.BeautifulSoup(request.text, "lxml")
        # print request.text

        genres = soup.select("a[href*=genre]")[2:]
        # print each genre

        genre_links = []

        # print out the available genres
        for index, genre in enumerate(genres):
            print(str(index) + ": " + genre.text)
            genre_links.append(genre.get("href"))

        print()
        selection = input(">>> Your choice (x to re-select chart type): ")
        print()

        if selection == 'x':
            break
        else:
            selection = int(selection)

        # print(genre_links[choice])

        url = "http://soundcloud.com" + genre_links[selection]
        request = requests.get(url)
        soup = bs4.BeautifulSoup(request.text, "lxml")

        tracks = soup.select("h2")[3:]
        track_links = []
        track_names = []


        for index, track in enumerate(tracks):
            track_links.append(track.a.get("href"))
            track_names.append(track.text)
            print(str(index + 1) + ": " + track.text)
            print()

        # song selection loop
        while True:
            selection = input(">>> Your choice (x to re-select genre): ")
            print()

            if selection == 'x':
                break
            else:
                selection = int(selection) - 1

            print("Now playing: " + track_names[selection])
            print()
            browser.get("http://soundcloud.com" + track_links[selection])
            browser.implicitly_wait(3)
            browser.find_element_by_class_name("fullHero__playerArea").click()

print("Have a good one!")
