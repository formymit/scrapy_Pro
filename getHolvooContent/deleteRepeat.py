
str = 'http://www.holvoo.net/article/articleView.do?id=2ab1fce0-8902-4ff2-8e09-9a5807dc4af0'

def deleteRepat(fileName):


    with open(fileName + '.txt', 'r') as file:
        data = file.readline()
        while data:
            print(len(data))

            if len(data)>= len(str) - 5:
                with open('holvoo_urls02_filtered.txt', 'a') as f:
                    f.write(data)
            data = file.readline()

# deleteRepat('songTitles')
deleteRepat('holvoo_urls02')