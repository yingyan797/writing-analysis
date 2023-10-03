symbs = "~`!@#$%^&*()_-+={[}]|:;<,>.?/\'\"\\"
seps = " .?!\n"

def addWord(ws, w):
    i = 0
    while i < len(w) and w[i] in symbs:
        i += 1
    j = len(w) - 1
    while j >=0 and w[j] in symbs:
        j -= 1
    word = w
    if j >= i:
        word = w[i:j+1]
    if len(word) >= 4:
      if ws.get(word) != None:
          ws[word] += 1
      else:
          ws[word] = 1 

def statistics(response):
    words = {}
    word = ""

    wordCount = 0
    sumWordLength = 0
    sentCount = 0

    i = 0
    wl = 0
    while i < len(response):
        wordSep = False
        sentSep = False
        while i < len(response) and response[i] in seps:
            if not wordSep:
                wordSep = True
                wordCount += 1
                sumWordLength += wl
                wl = 0
                addWord(words,word)
                word = ""
            if not sentSep and response[i] != " ":
                sentSep = True
                sentCount += 1
            i += 1
        if not wordSep and not sentSep:
            if response[i] not in symbs:
                wl += 1
            word += response[i].lower()
            i += 1

    reportMult = []
    report1 = []
    for w in words:
        freq = words[w]
        if freq > 1:
            reportMult.append((freq,w))
        else:
            report1.append(w) 
    reportMult.sort(reverse=True)
    report1.sort()

    if sentCount == 0:
        sentCount = 1
    return wordCount,sumWordLength,sentCount, reportMult, report1

def check(fileName, output):
    response = open(fileName, "r").read()
    wc, swl, sc, rm, r1 = statistics(response)
    sample = ""
    if len(response) <= 80:
        sample = response
    else:
        sample = response[:49] + " ...... " + response[len(response)-29:]
    report = "***Writing analysis***\n\nOriginal passage (clipped): \n=====\n" + sample + "\n=====\n" +"\nMost frequently occuring words (4 letters or more): \n"
    for (f,w) in rm:
        report += ("  \""+w + "\"" + " "*max(20-len(w), 1) + str(f) + " times\n")
    report += "\n=====\nThe following words appear only once:\n"
    for w in r1:
        report += w+","
    message = "\n=====\n\nStatistics:\nTotal word count: "+str(wc)+"; Average word legnth: "+str(swl/wc)+"; Average number of words in each sentence: "+str(wc/sc)+"\n"
    report += message
    
    open(output, "w").write(report)
    return message

f0 = "passage.txt"
f1 = "analysis.txt"
print(check(f0, f1))
