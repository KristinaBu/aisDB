class Controller:
    def __init__(self):
        self.main_window = None
        self.about_window = None
        self.admin_menu = None
        self.admin_cust_menu = None
        self.admin_supl_menu = None
        self.cust_menu = None
        self.cust_artworks = None

    def set_windows(self, main_window, about_window, admin_menu, admin_cust_menu, admin_supl_menu, cust_menu,
                    cust_artworks):
        self.main_window = main_window
        self.about_window = about_window
        self.admin_menu = admin_menu
        self.admin_cust_menu = admin_cust_menu
        self.admin_supl_menu = admin_supl_menu
        self.cust_menu = cust_menu
        self.cust_artworks = cust_artworks

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
        pass

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


    # Customer menu
    def show_cust_artworks_window(self):
        self.cust_artworks.show()
        pass
    def show_cust_myartworks_window(self):
        pass
    def show_cust_popular_window(self):
        pass
    def show_cust_lk_window(self):
        pass

