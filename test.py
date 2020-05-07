from urllib.request import urlopen

def main():
    download_file("https://www.uio.no/studier/emner/matnat/fys/FYS3140/v16/old-exam-problems/exam2014.pdf")
    # download_file("http://stlab.adobe.com/wiki/images/d/d3/Test.pdf")

def download_file(download_url):
    response = urlopen(download_url)
    file = open("document.pdf", 'wb')

    url = 'http://www.hrecos.org//images/Data/forweb/HRTVBSH.Metadata.pdf'
    r = requests.get(url, stream=True)

    with open('/tmp/metadata.pdf', 'wb') as fd:
        for chunk in r.iter_content(chunk_size):
            fd.write(chunk)
    file.write(response.read())
    file.close()
    print("Completed")

if __name__ == "__main__":
    main()
