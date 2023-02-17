from tinydb import TinyDB, Query

# DB_CONFIG QUERIES
def save_paths_dict(alias: str = None):
    """
        Parameters:
        ----------
        
        alias: str 
            Alias of the desired save path´s information.
            If None, returns all information.
        
        Returns:
        --------
            dict
                A dictionary with the values of the specified alias of table "save_path"
                in config.json
            list
                A list with all the dictionaries of table "save_path" in config.json if
                alias is not given
    """

    db_config = TinyDB ("config.json")
    save_path_table = db_config.table("save_path")
    
    if alias == None:
        return save_path_table.all()
    else:
        data = Query()
        return save_path_table.search(data.alias == alias)[0]

# DB_SHOW QUERIES
def add_show (show_name: str, last_episode: int, url_list: str):
    """
        Parameters:
        ----------
        
        show_name: str 
            Name of the show to add
        last_episode: int
            Number of the current episode
        url_list: str
            String of the url where the list of episodes is.
    """
    
    db_shows = TinyDB("show_db.json")
    db_shows.insert({"show": show_name, 
                     "current_episode": last_episode, 
                     "list_url": url_list })

def show_data (show_name: str):
    """
        Parameters:
        ----------
        
        show_name: str 
            Alias of the desired show´s information.
        
        Returns:
        --------
            dict
                A dictionary with all the values of the specified show of table "_default"
                in show_db.json
    """
    
    db_shows = TinyDB("show_db.json")
    data = Query()
    return db_shows.search(data.show == show_name)[0]

def all_shows(atribute: str = "show"):
    """
        Parameters:
        ----------
        
        atribute: str 
            Key from the value to get from all elements in show_db.json.
            "show" is the default value
        
        Returns:
        --------
            list
                a list with the atribute of all elements in show_db.json.
    """
    
    db_shows = TinyDB("show_db.json")
    list = db_shows.all()
    shows = []
  
    for element in list:
        shows.append(element[atribute])

    return(shows)

def delete_show(show_name: str):
    """
        Parameters:
        ----------
        
        show_name: str 
            Name of the show to delete
    """
    
    db_shows = TinyDB("show_db.json")
    data = Query()
    db_shows.remove(data.show == show_name)

def increase_chapter(show_name: str):
    """
        Parameters:
        ----------
        
        show_name: str 
            Name of the show to update its current episode
    """
    db_shows = TinyDB("show_db.json")
    data = Query()
    current_episode = show_data(show_name)["current_episode"] + 1
    db_shows.update({"current_episode": current_episode}, data.show == show_name)