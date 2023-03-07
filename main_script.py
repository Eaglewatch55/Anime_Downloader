from requests_html import HTMLSession
from pathlib import Path, PurePosixPath
from os import remove, rename
import pysftp
from typing import Union

def new_episode(url):
    """
            Parameters:
        ----------
            url: str 
                URL to check avilability.
        
        Returns:
        --------
            bool
                Returns True if code is less than 400. False otherwise.         
    """
    
    with HTMLSession() as session:
        r = session.get(url,timeout=10000)
        return(r.ok)

# ----- SCRAP PARA BUSCAR LINK ZIPPYSHARE
def scrap_download_link (anime_episode_url):
    """
        Parameters:
        ----------
            anime_episode_url: str 
                URL to locate the zyppyshare´s download link.
        
        Returns:
        --------
            str
                Returns the link in case of locating it succesfully.
                Returns False otherwise.
    """
    
    with HTMLSession() as session:
        r = session.get(anime_episode_url, timeout=10000)
        #Busca tabla de descargas
        download_table = r.html.find("#DwsldCn",first = True)
        # El .links regresa variable tipo "set"
        links = download_table.links    

    # SEARCH "zippyshare.com" on the list
    for link in links:
        if "zippyshare.com" in link:
            return (link)
    return(False)

# ----- SCRAP EN PARA BUSCAR LINK MP4
def zipp_scrap (url_zip):
    """
        Parameters:
        ----------
            url_zip: str 
                URL zyppyshare´s download link to locate the video´s source URL
                in the download button.
        
        Returns:
        --------
            str
                Returns the link in case of locating it succesfully.
                Returns False otherwise.
    """
    
    with HTMLSession() as session:
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
    """
        Parameters:
        ----------
            url_mp4: str 
                Video´s source URL to extract .mp4 file.
            ep_name: str
                Episode´s with .mp4 extension.
            save_path: Path
                Location directory to temporarly store the file.

        Returns:
        --------
            bool
                True if succesful procedure. False otherwise.
    """
    #! Añadir revisión de archivo existente en temporal
    with HTMLSession() as session:
        try:
            r = session.get(url_mp4, stream=True)
            chunk_size = 1024
            
            with open(f"{save_path}/{ep_name}","wb") as f:
                for chunk in r.iter_content(chunk_size=chunk_size):
                    f.write(chunk)
            
            return True
        except:
            return False

def allocate_to_directory (path_config: dict, source: Path, destination: Union[Path, PurePosixPath], filename: str):
    """
        Parameters:
        ----------
            path_config: dict
                Information of the destiny path
            source: Path
                Directory of the folder, where the file is.
            destination: Path or PurePosixPath
                Directory of the desired destination folder. Can be Path or PurePosixPath,
                depending of m_type.
            filename: str
                Name of the file, including extension.

        Returns:
        --------
            bool
                True if successfully moved.
                False if an exception occurred.
    """
    # Local limitation: Only moves within the same disk
    # Not using shutil.move by personal preferance, since I don´t want
    # to copy, paste and delete, only move.
    
    # SELECT THE TYPE OF ALLOCATION
    if path_config["transmission"] == "local":
        try:
            if not source.exists():
                return False
            
            if not destination.exists():
                destination.mkdir()
                
            rename(src= source / filename, dst= destination / filename)
            return True
        
        except:
            print("Local Failure")
            return False
        
    elif path_config["transmission"] == "sftp":
        try:
            cnopts = pysftp.CnOpts()
            cnopts.hostkeys = None

            with pysftp.Connection(path_config["host"], 
                                username = path_config["user"], 
                                password = path_config["pass"], 
                                cnopts = cnopts) as sftp:
                
                #CHECK DESTINATION FOLDER, IF DOESNT EXISTS, CREATES IT    
                if not sftp.isdir(str(destination)):
                    sftp.mkdir(str(destination))
                
                # TRANSFORM PATH OBJECT TO STRING, SINCE PYSFTP DOESNT SUPPORT IT    
                source = str(source / filename)
                destination = str(destination / filename)
                sftp.put(source, destination)
                remove(source)
                return True
        
        except:
            print("Sftp Failure")
            return False        
    else:
        print("Transmission type not valid")
        return False