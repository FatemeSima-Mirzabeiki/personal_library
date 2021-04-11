# this is for clear screen
from os import system, name


def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')


class Media:
    """
    Media is a base class
    each types of media is a subclass. like: Book, Podcast , ...
    I define some class methods. they use in menu(add, show,...)
    """
    _media = []

    # here I initialize common attributes between all media
    def __init__(self, title, price, publish_year):
        self.title = title.lower()
        self.price = price
        self.publish_year = publish_year
        self.progress = 0
        self.status = "not started"

    # this method returns the status of media based on progress
    def get_status(self):
        if self.progress == 0:
            self.status = "not started"
        elif self.progress == 100:
            self.status = "finished"
        else:
            self.status = "in progress..."
        return self.status

    def __str__(self):
        self.get_status()
        return f"title : {self.title}\n" \
               f"price : {self.price}$\n" \
               f"publish year : {self.publish_year}\n" \
               f"status = {self.status}\n"

    @classmethod
    def add_media(cls):
        clear()
        choice_ = input('\n\n\nwhat do you want?'
                        '\nENTER 1 ---> add a Book'
                        '\nENTER 2 ---> add a Podcast'
                        '\nENTER 3 ---> add a AudioBook'
                        '\nENTER 4 ---> add a Magazine'
                        '\nENTER "back" IF YOU WANT TO BACK TO THE MENU...\n')
        if choice_.lower() == "back":
            return
        clear()
        title = input("enter the title: ")
        price = input("enter the price: ")
        publish_year = input("enter the publish year: ")
        if choice_ == "1":
            Book.add(title, price, publish_year)
        elif choice_ == "2":
            PodcastEpisode.add(title, price, publish_year)
        elif choice_ == "3":
            Audiobook.add(title, price, publish_year)
        elif choice_ == "4":
            Magazine.add(title, price, publish_year)

    @classmethod
    def show(cls):
        clear()
        if not Media._media:
            print("your bookshelf is empty...\n\n")
        else:
            print("\n\n\n...this is your bookshelf...\n\n")
            for media in Media._media:
                print(f"*{media.__class__.__name__}*\n")
                print(media)
                print("\n-----------------------------------")

    @classmethod
    def sort(cls):
        clear()
        if not Media._media:
            print("your bookshelf is empty...\n\n")
        else:
            print("sorted bookshelf(based on progress):")
            Media._media = sorted(Media._media, key=lambda x: x.progress, reverse=True)
            Media.show()

    @classmethod
    def call_listen_read(cls):
        clear()
        if not Media._media:
            print("your bookshelf is empty...\n\n")
        else:
            choice_ = input('\n\n\nwhat do you want?'
                            '\nENTER 1 ---> listen'
                            '\nENTER 2 ---> read'
                            '\nENTER "back" IF YOU WANT TO BACK TO THE MENU...\n')
            if choice_.lower() == "back":
                return
            elif choice_ == "1":
                choice_ = input('\n\n\nwhich one?'
                                '\nENTER 1 ---> podcasts'
                                '\nENTER 2 ---> audiobooks'
                                '\nENTER "back" IF YOU WANT TO BACK TO THE MENU...\n')
                if choice_.lower() == "back":
                    return
                elif choice_ == "1":
                    PodcastEpisode.show()
                    PodcastEpisode.find_podcast()
                elif choice_ == "2":
                    Audiobook.show()
                    Audiobook.find_audiobook()
            elif choice_ == "2":
                choice_ = input('\n\n\nwhich one?'
                                '\nENTER 1 ---> books'
                                '\nENTER 2 ---> magazines'
                                '\nENTER "back" IF YOU WANT TO BACK TO THE MENU...\n')
                if choice_.lower() == "back":
                    return
                elif choice_ == "1":
                    Book.show()
                    Book.find_book()
                elif choice_ == "2":
                    Magazine.show()
                    Magazine.find_magazine()


class Book(Media):
    """
    Book is a subclass of Media
    in this class, I override some methods and define other methods(like read or class methods)
    """
    _books = []

    def __init__(self, title, price, publish_year, book_language, author, pages):
        super().__init__(title, price, publish_year)
        self.book_language = book_language
        self.author = author
        self.pages = pages
        self.read_pages = 0

    def read(self, pages):
        if pages < 0 or (pages + self.read_pages) > self.pages:
            print("Error...")
        elif pages == 0 and self.read_pages == 0:
            print(f"OOPS, you haven`t read {self.title}.")
        else:
            self.read_pages += pages
            if self.read_pages == self.pages:
                print(f"WOW! you have finished {self.title}.")
            else:
                print(f"you have read {self.read_pages} more pages from {self.title}. \
                        There are {self.pages - self.read_pages} pages left")
            self.set_progress()

    def set_progress(self):
        self.progress = round(self.read_pages / self.pages, 2) * 100

    def __str__(self):
        info = f"author(s) : {self.author}\n" \
               f"number of pages : {self.pages}\n" \
               f"book language : {self.book_language}\n" \
               f"you have read {self.read_pages} pages of it\n"
        return super().__str__() + info

    @classmethod
    def add(cls, title, price, publish_year, media_type=None):
        book_language = input("book language: ").lower()
        author = input("author(s): ").lower()
        pages = int(input("number of pages: "))
        if media_type == "magazine" or media_type == "audiobook":
            return book_language, author, pages
        book = Book(title, price, publish_year, book_language, author, pages)
        Media._media.append(book)
        Book._books.append(book)

    @classmethod
    def show(cls):
        clear()
        print("\n\n\n...this is your books...\n\n")
        for book in Book._books:
            print(f"*{book.title}*\n")
        print("\n-----------------------------------")

    @classmethod
    def find_book(cls):
        while 1:
            name_ = input('\n\nenter the name of book(if you want to back, enter "back"):')
            if name_ == "back":
                return
            for book in Book._books:
                if name_ == book.title:
                    pages = int(input("How many pages did you read? "))
                    book.read(pages)
                    return
            print("\nyou entered the wrong name... try again...\n")


class PodcastEpisode(Media):
    _podcasts = []
    """
    Podcast is a subclass of Media
    in this class, I override some methods and define other methods(like listen or class methods)
    """

    def __init__(self, title, price, publish_year, audio_language, speaker, time):
        Media.__init__(self, title, price, publish_year)
        self.audio_language = audio_language
        self.speaker = speaker
        self.time = time
        self.listened = 0

    def listen(self, time):
        # hint: if "time" is more than time of podcast, also new "listened" is more than time of podcast
        if time < 0 or (time + self.listened) > self.time:
            print("Error...")
        elif time == 0 and self.listened == 0:
            print(f"OOPS, you haven`t listen {self.title}.")
        else:
            self.listened += time
            if self.listened == self.time:
                print(f"WOW! you have finished {self.title}.")
            else:
                print(f"you have read {self.listened} more minutes from {self.title}. \
                        There are {self.time - self.listened} minutes left")
            self.set_progress()

    def set_progress(self):
        self.progress = round(self.listened / self.time, 2) * 100

    def __str__(self):
        info = f"speaker(s) : {self.speaker}\n" \
               f"time : {self.time}\n" \
               f"you have listened {self.listened} minutes of it\n" \
               f"audio language : {self.audio_language}\n"
        return super().__str__() + info

    @classmethod
    def add(cls, title, price, publish_year, media_type=None):
        audio_language = input("audio language: ").lower()
        speaker = input("speaker(s): ").lower()
        time = int(input("time: "))
        if media_type == "audiobook":
            return audio_language, speaker, time
        podcast = PodcastEpisode(title, price, publish_year, audio_language, speaker, time)
        Media._media.append(podcast)
        PodcastEpisode._podcasts.append(podcast)

    @classmethod
    def show(cls):
        clear()
        print("\n\n\n...this is your podcasts...\n\n")
        for podcast in PodcastEpisode._podcasts:
            print(f"*{podcast.title}*\n")
        print("\n-----------------------------------")

    @classmethod
    def find_podcast(cls):
        while 1:
            name_ = input('\n\nenter the name of podcast(if you want to back, enter "back"):')
            if name_ == "back":
                return
            for podcast in PodcastEpisode._podcasts:
                if name_ == podcast.title:
                    time = int(input("How many minutes did you listen? "))
                    podcast.listen(time)
                    return
            print("\nyou entered the wrong name... try again...\n")


# Magazine is a subclass of Book
class Magazine(Book):
    _magazines = []

    def __init__(self, title, price, publish_year, book_language, author, pages, issue):
        super().__init__(title, price, publish_year, book_language, author, pages)
        self.issue = issue

    def __str__(self):
        return super().__str__() + f"issue : {self.issue}\n"

    @classmethod
    def add(cls, title, price, publish_year):
        book_language, author, pages = Book.add(title, price, publish_year, media_type="magazine")
        issue = input("issue: ").lower()
        magazine = Magazine(title, price, publish_year, book_language, author, pages, issue)
        Media._media.append(magazine)
        Magazine._magazines.append(magazine)

    @classmethod
    def show(cls):
        clear()
        print("\n\n\n...this is your magazines...\n\n")
        for magazine in Magazine._magazines:
            print(f"*{magazine.title}*\n")
        print("\n-----------------------------------")

    @classmethod
    def find_magazine(cls):
        while 1:
            name_ = input('\n\nenter the name of magazine(if you want to back, enter "back"):')
            if name_ == "back":
                return
            for magazine in Magazine._magazines:
                if name_ == magazine.title:
                    pages = int(input("How many pages have you read? "))
                    magazine.read(pages)
                    return
            print("\nyou entered the wrong name... try again...\n")


# Audiobook is a subclass of PodcastEpisode and Book
class Audiobook(PodcastEpisode, Book):
    _audiobooks = []

    def __init__(self, title, price, publish_year, book_language, audio_language,
                 speaker, author, time, page):
        PodcastEpisode.__init__(self, title, price, publish_year, audio_language, speaker, time)
        Book.__init__(self, title, price, publish_year, book_language, author, page)

    def __str__(self):
        return super().__str__()

    @classmethod
    def add(cls, title, price, publish_year):
        book_language, author, pages = Book.add(title, price, publish_year, media_type="audiobook")
        audio_language, speaker, time = PodcastEpisode.add(title, price,
                                                           publish_year, media_type="audiobook")
        audiobook = Audiobook(title, price, publish_year, book_language, audio_language,
                              speaker, author, time, pages)
        Media._media.append(audiobook)
        Audiobook._audiobooks.append(audiobook)

    @classmethod
    def show(cls):
        clear()
        print("\n\n\n...this is your audiobooks...\n\n")
        for audiobook in Audiobook._audiobooks:
            print(f"*{audiobook.title}*\n")
        print("\n-----------------------------------")

    @classmethod
    def find_audiobook(cls):
        while 1:
            name_ = input('\n\nenter the name of audiobook(if you want to back, enter "back"):')
            if name_ == "back":
                return
            for audiobook in Audiobook._audiobooks:
                if name_ == audiobook.title:
                    time = int(input("How many minutes have you have listened? "))
                    audiobook.listen(time)
                    return
            print("\nyou entered the wrong name... try again...\n")


# main menu: 
while 1:
    choice = input('\n\n\nwhat do you want?'
                   '\nENTER 1 ---> show your bookshelf'
                   '\nENTER 2 ---> add media(Book/Magazine/Podcast/AudioBook)'
                   '\nENTER 3 ---> add read page(s) or listened time'
                   '\nENTER 4 ---> sort your bookshelf'
                   '\nENTER "quit" IF YOU WANT TO FINISH THE PROGRAM...\n')

    if choice == "1":
        Media.show()
    elif choice == "2":
        Media.add_media()
    elif choice == "3":
        Media.call_listen_read()
    elif choice == "4":
        Media.sort()
    elif choice.lower() == "quit":
        break
    else:
        continue
