from requests_html import HTMLSession
import db_query as query


def new_episode(url):
    session = HTMLSession()
    r = session.get(url,timeout=10000)
    return(r.ok)

# ----- SCRAP PARA BUSCAR LINK ZIPPYSHARE
def scrap_download_link (anime_episode_url):
    session = HTMLSession()
    r = session.get(anime_episode_url, timeout=10000)
    #Busca tabla de descargas
    download_table = r.html.find("#DwsldCn",first = True)
    # El .links regresa variable tipo "set"
    links = download_table.links    

    #Busca zippyshare
    for link in links:
        if "zippyshare.com" in link:
            return (link)
    return(False)

# ----- SCRAP EN PARA BUSCAR LINK MP4
def z_scrap (url_zip):
    session = HTMLSession()
    r_scrap = session.get(url_zip, timeout=10000)
    
    r_scrap.html.render()

    dlbutt = r_scrap.html.find("#dlbutton", first = True)

    #Divide el url base y buscsa de los atributos del boton la liga
    base_url = url_zip.split("/v")
    try:
        part_url = dlbutt.attrs["href"]
        return(base_url[0] + part_url)
    except:
        return(False)


# ----- DESCARGAR ARCHIVO MP4
def download (url_mp4, ep_name, save_path):
    
    try:
        session = HTMLSession()
        r = session.get(url_mp4, stream=True)
        chunk_size = 1024
        
        with open(f"{save_path}/{ep_name}","wb") as f:
            for chunk in r.iter_content(chunk_size=chunk_size):
                f.write(chunk)
        
        return(True)
    except:
        return(False)

def send_sftp ():
    pass

