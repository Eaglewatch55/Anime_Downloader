import tkinter as tkt
from tkinter import END, Scrollbar, ttk
import db_query as query
import main_script as script
from os import system 
from time import sleep
from pathlib import Path, PurePosixPath


# BUTTON FUNCTIONS
def scan_button ():
    shows = []
    shows = query.all_shows("show")
    alias_path = cb_save.get()
    path_info = query.save_paths_dict(alias_path)
    update_log(f"Descarga en {alias_path}")
    
    for show in shows:
        show_data = query.show_data(show)
        next_episode = show_data["current_episode"]+1
        
        ep_url = show_data["list_url"].replace("/anime/","/ver/")+ "-" + str(next_episode)
        
        if script.new_episode(ep_url):
            update_log(f"{show} episodio {next_episode} disponible")
            update_log("Obteniendo enlace de descarga...")
            url_zippy = script.scrap_download_link(ep_url)
        else:
            update_log(f"{show} episodio {next_episode} no disponible")   
            continue 
            
        # ADD 0 TO NAME
        if next_episode < 10:
            episode_name= f"E0{str(next_episode)}.mp4"
        else:
            episode_name= f"E{str(next_episode)}.mp4"

        if url_zippy != False:
            mp4_link = script.zipp_scrap(url_zippy)
        else:
            update_log(f"Error al obtener url de {episode_name}")
            continue

        if mp4_link != False:
            update_log(f"Descargando {episode_name}")
        else:
            update_log("Archivo no disponible")
            continue
        
        temp_path = Path("D:/Temp/CAPITULOS DESCARGA/Temporal")
        
        # SAVE EPISODE TO LOCAL PATH, THEN MOVE IT
        if script.download(mp4_link, episode_name, temp_path):
            update_log("Descarga temporal realizada")
        else:
            update_log("Descarga fallida")
            continue
        
        if path_info["transmission"] == "local":
            dest_path = Path(path_info["directory"], show_data["folder_name"]) 
        elif path_info["transmission"] == "sftp":
            dest_path = PurePosixPath(path_info["directory"], show_data["folder_name"])
        else:
            update_log("Save´s path transmission type invalid")
            continue
            
        if script.allocate_to_directory(path_info, temp_path, dest_path, episode_name):
            update_log("Reubicación realizada")
            query.increase_chapter(show)
        else:
            update_log("Reubicación fallida")
            continue
        

    if cb_shutdown.get == "Si":
        update_log("Apagando el sistema en 10 segundos")
        system("shutdown -s -t " + 10)
        sleep(5)        
        quit()

# REVISAR FUNCIONAMIENTO       
def add_button(show, chapter, url):

    if show in query.all_shows("show") :
        update_log("Nombre de show existente")
        return
    
    if url in query.all_shows("list_url"):
        update_log("URL ya existente")
        return
    
    try:
        chapter = int(chapter)
    except TypeError:
        update_log("Número de capitulo no válido")
        return
        
    if "www3.animeflv.net" in url.split("/"):
        try:
            query.add_show(show,chapter,url)
        except:
            update_log("Error al agregar el show. Dominio no es animeflv.net")
            return
        else:
            update_log("Show agregado exitosamente")
            cb_show["values"]= query.all_shows("show")
    else:
        update_log("Dominio no válido")
        return


def delete_button ():
    show = cb_show.get()
    query.delete_show(show)
    update_log(f"{show} eliminado")
    cb_show["values"]= query.all_shows("show")

# UTILITY FUNCTIONS
def update_log (message):
    tx_logs.insert(END,f"{message}\n")


def path_filtering (alias, *columns):
    path_list = query.save_paths_dict()
    
    for line in path_list:
        
        if line["alias"] == alias:
            result = []
            
            for element in columns:
                result.append(line[element])
    
    return result

# SELF-RUNING VALIDATION
if __name__ == "__main__":    
    # VENTANA GENERAL
    window = tkt.Tk()
    window.title("Descargador de AnimeFlv")
    scrollbar = Scrollbar(window, orient= "vertical")
    lb_messages = tkt.Label(window, text= "Mensajes:")
    tx_logs = tkt.Text(window, yscrollcommand= scrollbar.set, height= 4, width=40)

    #Añadir pestañas
    tab_control = ttk.Notebook (window)

    tab_scan = ttk.Frame(tab_control)
    tab_control.add(tab_scan, text="Escanear y Descargar")

    tab_add = ttk.Frame(tab_control)
    tab_control.add(tab_add, text="Agregar Show")

    tab_delete = ttk.Frame(tab_control)
    tab_control.add(tab_delete, text="Eliminar Show")

    tab_control.grid(row=0,column=0)

    # Pestaña ESCANEAR
    lb_scan = tkt.Label(tab_scan, text= "Escanear y descargar nuevos capitulos")
    bt_scan = tkt.Button(tab_scan, text= "Escanear y Descargar", command= scan_button)
    lb_save = tkt.Label(tab_scan, text= "Save Location:")
    cb_save = ttk.Combobox(tab_scan,state="readonly")
    list_path = list(element["alias"] for element in query.save_paths_dict())
    cb_save["values"] = list_path
    lb_shutdown = tkt.Label(tab_scan, text= "Apagar tras finalizar:")
    cb_shutdown = ttk.Combobox(tab_scan,state="readonly", values=["Si","No"])

    #Pestaña AGREGAR
    lb_add_desc = tkt.Label(tab_add, text="Ingrese los datos para agregar show a seguimiento")
    lb_show = tkt.Label(tab_add, text="Nombre:")
    lb_chapter = tkt.Label(tab_add, text="Captiulo Actual:")
    lb_url = tkt.Label(tab_add, text="URL de lista:")
#    lb_folder = tkt.Label(tab_add, text="Nombre de Carpeta:")

    bx_show = tkt.Entry(tab_add, width= 10)
    bx_chapter = tkt.Entry(tab_add, width= 10)
    bx_url = tkt.Entry(tab_add, width= 15)

    bt_add = tkt.Button(tab_add,text="Agregar", command= add_button(bx_show.get(), bx_chapter.get(), bx_url.get()))

    #Pestaña ELIMINAR
    lb_del_desc = tkt.Label(tab_delete, text= "Seleccione el elemento a eliminar")
    lb_del_show = tkt.Label(tab_delete, text="Show:")
    cb_show = ttk.Combobox(tab_delete,state="readonly", values=query.all_shows("show"))
    bt_delete = tkt.Button(tab_delete, text= "Eliminar", command= delete_button)

    # ---- ACOMODO ELEMENTOS ----
    lb_messages.grid(row=1,column=0)
    tx_logs.grid(row=2,column=0)

    #Pestaña Escanear
    lb_scan.grid(row=0,columnspan=2)
    lb_save.grid(row=1, column=0)
    cb_save.grid(row=1, column=1)
    lb_shutdown.grid(row=2, column=0)
    cb_shutdown.grid(row=2, column=1)
    bt_scan.grid(row=3,columnspan=2)

    #Pestaña Agregar
    lb_add_desc.grid(row=0,columnspan=2)
    lb_show.grid(row=1,column=0)
    bx_show.grid(row=1,column=1)
    lb_chapter.grid(row=2,column=0)
    bx_chapter.grid(row=2,column=1)
    lb_url.grid(row=3,column=0)
    bx_url.grid(row=3,column=1)
    bt_add.grid(row=4,columnspan=2)

    # Pestaña Eliminar
    lb_del_desc.grid(row=0,columnspan=2)
    lb_del_show.grid(row=1,column=0)
    cb_show.grid(row=1,column=1)
    bt_delete.grid(row=2,column=1)

    window.mainloop()
