class Controller:
    def __init__(self):
        self.main_window = None
        self.about_window = None
        self.admin_menu = None
        self.admin_cust_menu = None
        self.admin_supl_menu = None
        self.cust_menu = None
        self.cust_artworks = None
        self.cust_myartworks = None
        self.cust_popular = None
        self.cust_prof = None
        self.admin_menu_inventory = None
        self.artw_edit = None
        self.artw_look = None
        self.adm_artist = None
        self.adm_artw = None

    def set_windows(self, main_window, about_window, admin_menu, admin_cust_menu, admin_supl_menu, cust_menu,
                    cust_artworks, cust_myartworks, cust_popular, cust_prof,admin_menu_inventory,artw_edit,
                    artw_look, adm_artist, adm_artw):
        self.main_window = main_window
        self.about_window = about_window
        self.admin_menu = admin_menu
        self.admin_cust_menu = admin_cust_menu
        self.admin_supl_menu = admin_supl_menu
        self.cust_menu = cust_menu
        self.cust_artworks = cust_artworks
        self.cust_myartworks = cust_myartworks
        self.cust_popular = cust_popular
        self.cust_prof = cust_prof
        self.admin_menu_inventory = admin_menu_inventory
        self.artw_edit = artw_edit
        self.artw_look = artw_look
        self.adm_artist = adm_artist
        self.adm_artw = adm_artw

    def exit_all(self):
        # TODO: заполнить
        self.about_window.close()
        self.admin_menu.close()

    def show_main_window(self):
        self.about_window.hide()
        #self.main_window.show()

    def show_about_window(self):
        self.main_window.hide()
        self.about_window.show()

    def show_admin_menu(self):
        self.main_window.hide()
        self.admin_menu.show()

    def show_cust_menu(self):
        self.cust_menu.show()
        pass

    def show_admin_cust_window(self):
        self.admin_cust_menu.show()
        pass

    def show_admin_supl_window(self):
        self.admin_supl_menu.show()

    def show_admin_money_exit(self):
        pass

    def show_admin_artworks_window(self):
        self.admin_menu_inventory.show()

    def show_admin_cust_data_window(self):
        pass

    def show_admin_cust_geo_window(self):
        pass

    def show_admin_supl_data_window(self):
        pass

    def show_admin_supl_makePuchase_window(self):
        pass

    def show_admin_supl_addSupl_window(self):
        pass


    #CRUD
    def edit_artw(self):
        self.artw_edit.show()
        pass

    def look_artw(self):
        self.artw_look.show()
        pass

    def show_adm_artist(self):
        self.adm_artist.show()

    def show_adm_artw(self):
        self.adm_artw.show()


    # Customer menu
    def show_cust_artworks_window(self):
        self.cust_artworks.show()
        pass
    def show_cust_myartworks_window(self):
        self.cust_myartworks.show()
        pass
    def show_cust_popular_window(self):
        self.cust_popular.show()
        pass
    def show_cust_lk_window(self):
        self.cust_prof.show()
        pass

