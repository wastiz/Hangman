from GameTime import GameTime
from Model import Model
from View import View
from tkinter import simpledialog


class Controller:
    def __init__(self, db_name=None):
        self.__model = Model()
        self.__view = View(self, self.__model)
        if db_name is not None:
            self.__model.database = db_name
        self.__game_time = GameTime(self.__view.lbl_time)

    def main(self):
        self.__view.main()

    def btn_scoreboard_click(self):
        window = self.__view.create_scoreboard_window()
        data = self.__model.read_scores_data()
        self.__view.draw_scoreboard(window, data)

    def buttons_no_game(self):
        self.__view.btn_new['state'] = 'normal'
        self.__view.btn_cancel['state'] = 'disabled'
        self.__view.btn_send['state'] = 'disabled'
        self.__view.char_input.delete(0, 'end')   # Sisestuskast tühjaks
        self.__view.char_input['state'] = 'disabled'

    def buttons_to_game(self):
        self.__view.btn_new['state'] = 'disabled'
        self.__view.btn_cancel['state'] = 'normal'
        self.__view.btn_send['state'] = 'normal'
        self.__view.char_input['state'] = 'normal'
        self.__view.char_input.focus()

    # TODO Seadista mudelis uus mäng. Juhuslik sõna andmebaasist vaja kätte saada
    # TODO Näita äraarvatavat sõna aga iga tähe asemel on allkriips. Kirjastiil on big_font
    # TODO Veateadete label muuda tekst "Vigased tähed:"
    def btn_new_click(self):   # Uus mäng
        self.buttons_to_game()
        # Muuda pilti id-ga 0
        self.__view.change_image(0)
        self.__model.setup_new_game()
        self.__view.lbl_result.config(text=self.__model.hidden_word)
        self.__view.lbl_error.config(text="Vigased tähed:")
        self.__game_time.reset()
        self.__game_time.start()

    def btn_cancel_click(self):
        self.__game_time.stop()
        self.__view.change_image(-1)
        self.buttons_no_game()
        self.__view.lbl_result.config(text="MÄNGIME!")

    def btn_send_click(self):
        # TODO Kontrollida kas mäng on läbi.

        print(self.__model.wrong_guesses)
        if self.__model.wrong_guesses >= 11:
            print('You have lost')
            self.btn_cancel_click()
            self.__view.show_message('lose')
            return

        print(self.__view.char_input.get())

        # TODO Loe sisestus kastist saadud info ja suuna mudelisse infot töötlema
        self.__model.process_user_input(self.__view.char_input.get())
        # TODO Muuda teksti tulemus aknas (äraarvatav sõna)
        print(self.__model.hidden_word)
        self.__view.lbl_result.config(text=self.__model.hidden_word)
        # TODO Muuda teksti Vigased tähed
        vigased = "Vigased tähed: " + self.__model.get_wrong_guesses_as_string()
        self.__view.lbl_error.config(text=vigased)
        # TODO Tühjanda sisestus kast (ISESESIVALT TUNNIS KOHE)
        self.__view.char_input.delete(0, 'end')
        self.__view.change_image(self.__model.wrong_guesses)

        # TODO KUI on vigu tekkinud, muuda alati vigade tekst punaseks ning näita vastavalt vea numbrile õiget pilti
        # TODO on mäng läbi. MEETOD siin samas klassis.
        # if self.__model.get_wrong_guesses() > 0:
        #     self.__view.change_image(self.__model.get_wrong_guesses())

        if self.__model.hidden_word == self.__model.random_word:
            print('You have won!')
            # TODO JAH puhul peata mänguaeg
            # TODO Seadista nupud õigeks (meetod juba siin klassis olemas)
            self.btn_cancel_click()
            self.__view.show_message('won')
            # TODO Küsi mängija nime (simpledialog.askstring)
            player_name = simpledialog.askstring("Enter your name", "Enter your name:")
            # TODO Saada sisestatud mängija nimi ja mängu aeg sekundites mudelisse kus toimub kogu muu tegevus kasutajanimega
            if player_name:
                self.__model.add_player_score(player_name, self.__game_time.counter)
                return
