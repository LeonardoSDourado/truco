from random import shuffle
import time

class Player:
    def __init__(self, name = None, score = 0):
        self.name = name
        self.score = score
        self.hand = []
        self.last_used_card = str()
        self.round_won = 0

    def __str__(self):
        return "Name: {0} - Score: {1} - Hand: {2}".format(self.name, self.score, self.hand)
        
class CardGame:
    def __init__(self):
        self.suits = {'diamond': u'\u2666', 'spade': u'\u2660', 'heart': u'\u2665',  'club': u'\u2663'}
        self.value = ['4','5','6','7','Q','J','K','A','2','3']
        self.graphic_suits = ['♦','♠','♥','♣']
        self.card_deck = []
        self.main_cards = []
        self.players = []
        self.cards_on_the_table = []

    def createDeck(self):
        self.card_deck.clear()
        
        for i in self.suits:
            for j in self.value:
                self.card_deck.append([self.suits[i],j])

        shuffle(self.card_deck)
        
    def join(self, player):
        self.players.append(player)
        player.score = 0

    def showPlayers(self):
        for i in self.players:
            print(i.name)

    def hit_main_card_from_deck(self):
        if len(self.card_deck) > 0:
            self.main_cards.append(self.card_deck.pop())
            
    def player_receive_from_deck(self, player):
        if len(self.card_deck) > 0:
            player.hand.append(self.card_deck.pop())

    def show_main_card(self):
        if len(self.main_cards) > 0:
            self.show_card(self.main_cards[-1])
        else:
            print("Empty!")

    def deal_the_cards(self):
        self.createDeck()
        temp = list()
        for i in self.card_deck:
            if i != self.main_cards:
                temp.append(i)
                
        self.card_deck = list(temp)
        
        if not len(self.main_cards) == 1:
            self.hit_main_card_from_deck()
            
        cards = 3
        
        for player in self.players:
            for i in range(0, cards):
                self.player_receive_from_deck(player)

    def play_round(self):
        
        for player in self.players:
            if player.name != "Machine":
                print("\n\n")
                print("Main card")
                self.show_main_card()
                print("Card on the table")
                self.show_cards_on_the_table()
                print()
                print(player.name)
                self.show_hand(player)
                self.fall_card(player)
                player.last_used_card = self.cards_on_the_table[-1]
                continue
            else:
                cards_by_power = list(player.hand)
                cards_by_power = self.order_cards_by_power(self.main_cards[-1], cards_by_power)
                print("\n\n")
                print("Main card")
                self.show_main_card()
                print("Card on the table")
                self.show_cards_on_the_table()
                print()
                print(player.name)
                time.sleep(5)
                for card in cards_by_power:
                    if len(self.cards_on_the_table) != 0:
                        if self.card_a_is_lower(self.main_cards[-1], self.cards_on_the_table[0], card):
                            self.fall_card_machine(player, card)
                            player.last_used_card = self.cards_on_the_table[-1]
                            break
                        if card == cards_by_power[-1]:
                            self.fall_card_machine(player, cards_by_power[0])
                            player.last_used_card = self.cards_on_the_table[-1]
                            break
                    else:
                        if len(player.hand) == 3:
                            self.fall_card_machine(player, cards_by_power[1])
                            player.last_used_card = self.cards_on_the_table[-1]
                            break
                        elif len(player.hand) == 2:
                            self.fall_card_machine(player, cards_by_power[-1])
                            player.last_used_card = self.cards_on_the_table[-1]
                            break
                        else:
                            self.fall_card_machine(player, cards_by_power[-1])
                            player.last_used_card = self.cards_on_the_table[-1]
                            break          
                            
        if self.compare_cards(self.players) == 1:
            self.players[0].round_won += 1
        elif self.compare_cards(self.players) == 2:
            self.players[1].round_won += 1
            self.players.reverse()
        
        self.cards_on_the_table.clear()
        
        if self.check_winner():
            return True

    def fall_card_machine(self, player, card):
        self.cards_on_the_table.append(card)
        player.hand.pop(player.hand.index(card))
        
    def fall_card(self, player):
        while True:
            card = str()
            try:
                card = input("Which card do you want to fall?(1..n) ")
                if len(player.hand) >= (int(card)-1) and int(card) > 0:
                    self.cards_on_the_table.append(player.hand[int(card)-1])
                    player.hand.pop(int(card)-1)
                    break
                raise Exception
            except Exception as ex:
                if card == "--help":
                    while True:
                        self.help()
                        input2 = input("Help: ")
                        if input2 == "--resume":
                            break
                else:
                    print("Enter the correct value!")
                    time.sleep(10)
                    print(ex)
    def help(self):
        print("                 Truco's Rules")
        print("1. There are not cards with the values 8, 9 and 10.")
        print("2. The power of cards are in the following order from strongest to weakest: 3 2 A K J Q 7 6 5 4.")
        print("3. In the beginning of the game one card is hit from the deck, the cards with the next value in the sequence become the strongest cards.\nSample: If the card hit from deck in the benning of the game was 5, the cards with the value 6 become the strongest cards in the game, stronger than 3, the others cards values follow the rule 2.")
        print("4. Among cards with the same value, the suit will define the strongest.\nThe power of suits are in the following order from strongest to weakest: ♣ ♥ ♠ ♦")
        print("5. In the beginning the game each player receives 3 cards.")
        print("6. Wins 1 point that player that wins 2 rounds first in a match of 3 rounds.")
        print("7. Who wins the round starts the next round.")
        print("This game is more complex than it, but this program is recommended for beginners.")
        
    def order_cards_by_power(self, main_card, machine_hand):
        cards_by_power = list()
        lowerst_card = str()
        lower_index = len(self.value)
        counter = 0
        
        if len(machine_hand) > 0:
        
            for i in range(0,len(machine_hand)):

                for card in machine_hand:
                    if counter == 0:
                        lower_index = self.get_value_index(card)
                        lowerst_card = card
                        counter += 1
                    else:
                        if self.card_a_is_lower(main_card, card, lowerst_card):
                            lower_index = self.get_value_index(card)
                            lowerst_card = card
                    
                cards_by_power.append(lowerst_card)
                machine_hand.pop(machine_hand.index(lowerst_card))
                counter = 0

        return cards_by_power

    def get_value_index(self, card):
        return self.value.index(card[1])

    def get_suit_index(self, card):
        return self.graphic_suits.index(card[0])

    def card_a_is_lower(self, main_card, card_a, card_b):
        
        main_card_index = self.get_value_index(main_card)
        card_a_value_index = self.get_value_index(card_a)
        card_b_value_index = self.get_value_index(card_b)
        card_a_suit_index = self.get_suit_index(card_a)
        card_b_suit_index = self.get_suit_index(card_b)
        
        if (main_card_index+1) != card_a_value_index and (main_card_index+1) != card_b_value_index:
            if card_a_value_index > card_b_value_index:
                return False
            elif card_a_value_index < card_b_value_index:
                return True
            elif card_a_value_index == card_b_value_index:
                if card_a_suit_index > card_b_suit_index:
                    return False
                elif card_a_suit_index < card_b_suit_index:
                    return True
        elif (main_card_index+1) == card_a_value_index and (main_card_index+1) != card_b_value_index:
            return False
        elif (main_card_index+1) != card_a_value_index and (main_card_index+1) == card_b_value_index:
            return True
        elif (main_card_index+1) == card_a_value_index and (main_card_index+1) == card_b_value_index:
            if card_a_suit_index > card_b_suit_index:
                return False
            elif card_a_suit_index < card_b_suit_index:
                return True
                    
    def play(self):
        
        game_rounds = 3
        self.deal_the_cards()
        
        for game_round in range(0,game_rounds):
            if self.play_round():
                break

    def check_winner(self):
        if self.players[0].round_won == 2:
            self.players[0].score += 1
            self.reset_round_variables()
            self.main_cards.clear()
            print("\n\nYou won {0}!".format(self.players[0].name))
            return True
        elif self.players[1].round_won == 2:
            self.players[1].score += 1
            self.reset_round_variables()
            self.main_cards.clear()
            print("\n\nYou won {0}!".format(self.players[1].name))
            return True

    def clear_hands(self):
        for player in self.players:
            player.hand.clear()
    
    def compare_cards(self, players):
        if len(players) > 1:
            
            player1_has_powerst_card = (self.value.index(self.main_cards[-1][1])+1) == (self.value.index(players[0].last_used_card[1]))
            player2_has_powerst_card = (self.value.index(self.main_cards[-1][1])+1) == (self.value.index(players[1].last_used_card[1]))
            player1_card_has_same_value_than_player2 = (self.value.index(players[0].last_used_card[1])) == (self.value.index(players[1].last_used_card[1]))
            player1_card_suit_index = self.graphic_suits.index(players[0].last_used_card[0])
            player2_card_suit_index = self.graphic_suits.index(players[1].last_used_card[0])
            
            if player1_has_powerst_card and not player1_card_has_same_value_than_player2:
                return 1
            elif player2_has_powerst_card and not player1_card_has_same_value_than_player2:
                return 2
            elif player1_has_powerst_card and player1_card_has_same_value_than_player2:
                if player1_card_suit_index > player2_card_suit_index:
                    return 1
                elif player1_card_suit_index < player2_card_suit_index:
                    return 2

            player1_card_value_index = self.value.index(players[0].last_used_card[1])
            player2_card_value_index = self.value.index(players[1].last_used_card[1])
            
            if player1_card_value_index > player2_card_value_index:
                return 1
            elif player1_card_value_index < player2_card_value_index:
                return 2
            elif player1_card_value_index == player2_card_value_index:
                if player1_card_suit_index > player2_card_suit_index:
                    return 1
                elif player1_card_suit_index < player2_card_suit_index:
                    return 2

    def reset_round_variables(self):
        for player in self.players:
            player.round_won = 0
            player.last_used_card = str()
            player.hand.clear()
        self.cards_on_the_table.clear()

    def show_cards_on_the_table(self):
        if len(self.cards_on_the_table) > 0:
            self.show_card(self.cards_on_the_table[-1])
        else:
            print("Empty!")

    def show_card(self, card):
        if len(card) > 1:
            print("+-------+")
            print("|{0:<2}     |".format(card[1]))
            print("|       |")
            print("|   {0}   |".format(card[0]))
            print("|       |")
            print("|     {0:>2}|".format(card[1]))
            print("+-------+")

    def show_hand(self, player):
        grouped_cards = []
        counter = 0
        if len(player.hand) > 0:
            for line in range(0,8):
                for card in player.hand:
                    counter += 1
                    if line == 0:
                        if player.hand[-1] == card:
                            print("{0:>2}       ".format(counter),sep='')
                        else:
                            print("{0:>2}       ".format(counter), sep='', end='')
                    if line == 1:
                        if player.hand[-1] == card:
                            print("+-------+")
                        else:
                            print("+-------+", end='')
                    elif line == 2:
                        if player.hand[-1] == card:
                            print("|{0:<2}     |".format(card[1]))
                        else:
                            print("|{0:<2}     |".format(card[1]), end='')
                    elif line == 3:
                        if player.hand[-1] == card:
                            print("|       |")
                        else:
                            print("|       |", end='')
                    elif line == 4:
                        if player.hand[-1] == card:
                            print("|   {0}   |".format(card[0]))
                        else:
                            print("|   {0}   |".format(card[0]), end='')
                    elif line == 5:
                        if player.hand[-1] == card:
                            print("|       |")
                        else:
                            print("|       |", end='')
                    elif line == 6:
                        if player.hand[-1] == card:
                            print("|     {0:>2}|".format(card[1]))
                        else:
                            print("|     {0:>2}|".format(card[1]), end='')
                    elif line == 7:
                        if player.hand[-1] == card:
                            print("+-------+")
                        else:
                            print("+-------+", end='')

if __name__ == "__main__":
    player_name = input("Enter your name: ")
    player1 = Player(player_name, 0)
    player2 = Player("Machine", 0)
    app = CardGame()
    app.join(player1)
    app.join(player2)
    app.play()
