import os
from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog

try:
    from pytube import YouTube
    print("successfully imported youtube")
except:
    os.system('cmd /c "pip install pytube3"')
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    print("successfully imported selenium")
except:
    os.system('cmd /c "pip install selenium"')
try:
    from bs4 import BeautifulSoup as bs4
    print("successfully imported bs4")

except:
    os.system('cmd /c "pip install bs4"')


path = os.getcwd() + '\chromedriver.exe'



window = Tk()

window.title("Ghar ka YTD")

window.geometry("620x320")

lbl = Label(window, text="Paste video link: ", width=15)

lbl2 = Label(window, text="Select the type: ", width=15)

txt = Entry(window, width=40)

prel = Label(window, text="Enter file prefix(optional):", width=30)

pref = Entry(window)

SAVE_PATH = ""

text = Text(window, height=1, width=40)

lbl3 = Label(window, text="", width=50)

selected = IntVar()


def download(link, index):
    try:
        if pref.get():
            index = pref.get()
        print('creating object')
        yt = YouTube(link)
        print(yt)
        print('created object')
        d_video = yt.streams.filter(progressive=True,
                                    file_extension='mp4').order_by(
            'resolution').desc().first()
        print(d_video)
        print(f'downloading {str(index)}')
        d_video.download(output_path=SAVE_PATH, filename_prefix=str(index))
        print(f'downloaded {str(index)}')
    except:
        res = "Some error"
        lbl3.configure(text=res)
        print("some error")


def get_links(driver, url):
    try:
        driver.get(url)
        content = driver.page_source
        soup = bs4(content)
        print(soup)
        links = [a['href'] for a in soup.find_all('a', href=True, attrs={'id': 'wc-endpoint'})]
        print(links)
        print(len(links))
        links = list(set(links))
        print(links)
        return links
    except:
        print("some error")
        res = "Some error"
        lbl3.configure(text=res)

def clicked():
    print("inside clicked")
    res = "Downloaded at Save Path: " + str(SAVE_PATH)
    lbl3.configure(text=res)
    url = txt.get()
    type = selected.get()


    op = Options()
    op.add_argument("--headless")
    driver = webdriver.Chrome(options=op, executable_path=path)


    print("driver initiated")
    if type==2:
        links = get_links(driver, url)
        for link in links:
            k = link[-2:]
            if '=' in k:
                index = k.replace('=', '0')
            else:
                index = k
            download(link, index)
    else:
        download(url, "")

def browse():
    global SAVE_PATH
    filename = filedialog.askdirectory()
    SAVE_PATH = filename
    print(filename)
    text.insert(INSERT, filename)

rad1 = Radiobutton(window,text='Single Video', value=1, variable=selected)

rad2 = Radiobutton(window,text='Playlist', value=2, variable=selected)

btn2 = Button(window, text="Select Save directory", command=browse)

btn = Button(window, text="Download", command=clicked)

lbl.grid(column=0, row=0, pady=10)

txt.grid(column=1, row=0, pady=10)

lbl2.grid(column=0, row=1, pady=10)

rad1.grid(column=1, row=1, pady=10)

rad2.grid(column=1, row=2, pady=10)

text.grid(column=1, row=3, pady=10)

btn2.grid(column=0, row=3, pady=10)

prel.grid(column=0, row=4, pady=10)

pref.grid(column=1, row=4, pady=10)

btn.grid(column=1, row=5, pady=10)

lbl3.grid(column=1, row=6, pady=10)

window.mainloop()
