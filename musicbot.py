# musicbot.py v1.03
# by me (Tyler Geist)
# 12/4/19
import lyricsgenius as genius

#inits api
catoken = 'FNs-avceJFaRfvisVPhkRlnCA-FqRoGvu9gOitm8R3Uj7PVoP4iqCBIWMMoVY6Ii'
api = genius.Genius(catoken, skip_non_songs = True, remove_section_headers = True, verbose = False)

#dictionary of bad words with bad word score
badwordz = {
    ("hell","?"):1,
    ("damn","damnit","goddamn","goddamnit"):1,
    ("sex", "?"):1,
    ("fuck","fucking","fuckin","motherfucker","fucker","motherfucking","motherfuckin"):2,
    ("shit","bullshit","shitting","shittin"):2,
    ("bitch","bitchen","bitchin","bitching","bitches"):2,
    ("ass", "asshole"):3,
    ("dick","dildo","penis"):3,
    ("pussy","vagina"):3,
    ("boobs","titties","tits","tit"):3,
    ("hoe","ho","slut"):3,
    ("faggot", "fag", "fags"):3,
    ("nigga","niggas","nigger"):4
}

# gets song and prepares song object
# song object includes:
#  - ["title"] : title
#  - ["album"] : album name
#  - ["year"] : release year
#  - ["lyrics"] : lyrics
#  - ["image"] : url to song image
#  - ["artist"] : artist name
#  - ["length"] : number of lyrics
#  - ["btotal"] : total number of bad words
#  - ["bcount"] : list showing number of types of bad words
#  - ["bindex"] : bad word index, average of all bad word scores
#  - ["bpercent"] : bad word percent
#  - ["bwordslist"] : list of bad words in song
#  - ["bwords"] : string of bad words (no repeats)

def prepsong(sname, aname):
    # gets the song
    song = api.search_song(sname, aname, get_full_info = True)
    if song == None:
        return None
    songdict = song.to_dict()
    # dictionary contains
    lyrics = songdict["lyrics"]
    
    # adds artist to object, sorry "dictionary"
    songdict["artist"] = song.artist
    
    # replaces every character with space
    replacechars = ["\n",",","-","?","!",".","(",")",'"']
    for char in replacechars:
        lyrics = lyrics.replace(char," ")
    
    # gets indexes of '
    indexes = []
    i = 0
    for i in range(len(lyrics)):
        if lyrics[i] == "'":
            indexes.append(i)

    # replaces ' with " "
    i = len(indexes) - 1
    while i >= 0:
        llyrics = list(lyrics)
        llyrics[indexes[i]] = " "
        lyrics = "".join(llyrics)
        i -= 1
    
    # replaces all double spaces with single space
    lyrics.replace("  ", " ")
    
    # creates list of all lyrics
    llist = lyrics.split()
    
    # makes every element lowercase
    for i in range(len(llist)):
        llist[i] = llist[i].lower()
    
    # get number of words in the taking into account words with ' in them
    songdict["length"] = len(llist) - len(indexes)
    
    # creates bcount, a list showing number of types of bad words
    songdict["bcount"] = [0,0,0,0,0]
    # creates bwordslist, list of the bad words
    songdict["bwordslist"] = []
    for word in llist:
        for wordz in badwordz:
            if word in wordz:
                songdict["bcount"][badwordz[wordz]] += 1
                songdict["bwordslist"].append(word)
    
    # sets up bindex and bsum to calculate bindex
    bindexa = 0
    bsum = 0
    songdict["bindex"] = 0
    for i in range(len(songdict["bcount"])):
        if(i > 0):
            bindexa += i * songdict["bcount"][i]
            bsum += songdict["bcount"][i]
            if(songdict["bcount"][i] > 0):
                songdict["bindex"] = i
    
    norepeats = []
    songdict["words"] = ""
    for word in songdict["bwordslist"]:
        if word not in norepeats:
            norepeats.append(word)
            if(len(songdict["words"]) > 0):
                songdict["words"] = songdict["words"] + ", " + word
            else:
                songdict["words"] = songdict["words"] + word
    
    # sets bcount[0] to correct number of non bad words
    songdict["bcount"][0] = songdict["length"] - bsum
    # actually calculates bindex
    if(bsum > 0):
        songdict["bindexa"] = round((bindexa/bsum),1)
    else:
        songdict["bindexa"] = 0
    # calculates bad word percent
    songdict["bpercent"] = round(((songdict["bcount"][1] + songdict["bcount"][2] + songdict["bcount"][3] + songdict["bcount"][4]) / songdict["length"]) * 100, 2)
    songdict["btotal"] = bsum
    return(songdict)

while(True):
    sname = input("Name of song: ")
    aname = input("Name of artist: ")
    
    song = prepsong(sname, aname)
    
    if song != None:
        
        print("")
        print("Title: " + song["title"])
        print("Artist: " + song["artist"])
        if(song["album"] != None):
            print("Album: " + song["album"])
        else:
            print("No album found")
        if(song["btotal"] > 0):
            print("Explicit index: " + str(song["bindex"]))
            print("Average bad word score: " + str(song["bindexa"]))
            print("Percentage bad words: " + str(song["bpercent"]) + "%")
            print("Total bad words: " + str(song["btotal"]) + " (" + str(song["bcount"][1]) + " mild (" + str(round(song["bcount"][1]/song["btotal"] * 100, 2)) + "%), " + str(song["bcount"][2]) + " bad (" + str(round(song["bcount"][2]/song["btotal"] * 100, 2)) + "%), " + str(song["bcount"][3]) + " sexual (" + str(round(song["bcount"][3]/song["btotal"] * 100, 2)) + "%), " + str(song["bcount"][4]) + " racial (" +  str(round(song["bcount"][4]/song["btotal"] * 100, 2)) + "%))")
            print("Bad words in song: (" + song["words"] + ")")
        else:
            print("CLEAN")
            
        print("")
        
    else:
        print("")
        print("Song not found")
        print("")
