import sys
import bs4
import shutil
import urllib
import argparse
import requests
import subprocess 

def progress(count, total, suffix=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', suffix))
    sys.stdout.flush()  # As suggested by Rom Ruben


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('folders', nargs = '*')
    parser.add_argument('--subfolders', help='store stuff in subfolder.'\
            +'  Automatic if nargs > 1',
            action='store_true')
    args = parser.parse_args()
    return args

def main(args):
    folders = args.folders or ['test_file.html']
    local_file = not bool(args.folders)

    subfolders = (len(folders) > 1) or args.subfolders

    for www_folder in folders:
        title, links = read_folder(www_folder, local=local_file)
        outfolder = './{}'.format((title+'/') if subfolders else '')
        subprocess.call(["mkdir", "-p", '{}'.format(outfolder)])

        N = len(links)
        for i, url in enumerate(links):
            progress(i,N)
            local_filename = outfolder+url.split('/')[-1]
            #r = requests.get(url)
            # TODO: Error handling TODO: Paralellize
            urllib.request.urlretrieve(url, local_filename)

                

def read_folder(folder_name, local=False, feed_read = True):
    """Uses \\?vrtx\\=feed as ending to get webpage entries, and then
    downloads them"""

    if feed_read:
        if not folder_name.endswith('?vrtx=feed'):
            folder_name += '?vrtx=feed'

    if local:
        response = open(folder_name)
    else:
        response = urllib.request.urlopen(folder_name)  # TODO: Error handling here

    html_doc = response.read()          # TODO: Error handling here?
    response.close()

    soup = bs4.BeautifulSoup(html_doc, 'html.parser')
    title = soup.title.get_text()

    links = [e.find('link').get('href') for e in soup.find_all('entry')]
    return title, links





if __name__ == "__main__":
    args = get_args()
    main(args)
