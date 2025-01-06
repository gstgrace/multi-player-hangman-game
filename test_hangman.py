import unittest
from unittest.mock import Mock, patch
from main import HangmanGame, Player


class TestHangmanGame(unittest.TestCase):

    def setUp(self):
        """Mock the pygame window and any other necessary parts of pygame"""
        self.mock_window = Mock()
        self.players = [Player("Test Player 1"), Player("Test Player 2")]
        self.game = HangmanGame(self.mock_window, None, len(self.players), self.players, 0)
        self.game.start('easy')
        self.patcher = patch('pygame.display.update')  # Patch pygame's display update method
        self.mock_display_update = self.patcher.start()

    def tearDown(self):
        """Stop patching pygame's display update method after each test"""
        self.patcher.stop()

    def test_game_initialization(self):
        """Test game initialization and setup"""
        self.assertEqual(self.game.current_round, 1)
        self.assertEqual(self.game.total_players, len(self.players))
        self.assertEqual(self.game.game_state, "playing")
        self.assertIsNotNone(self.game.current_word)

    @patch('main.HangmanGame.reset_game_state')
    def test_handle_end_of_round_advances_round(self, mock_reset_game_state):
        """Test if the handle_end_of_round method advances the round correctly"""
        self.game.total_players = 1
        self.game.current_round = 1
        self.game.total_rounds = 3
        self.game.handle_end_of_round()
        self.assertEqual(self.game.current_round, 2)
        mock_reset_game_state.assert_called_once()

    def test_is_word_guessed_correctly(self):
        """Test if the game correctly identifies when a word is guessed correctly"""
        self.game.current_word = "test"
        self.game.guessed = set("test")
        self.assertTrue(self.game._is_word_guessed())

    @patch('pygame.draw.rect')
    @patch('main.HangmanGame.display_status')
    def test_display_status_is_called(self, mock_display_status, mock_draw_rect):
        """Test if the display_status method is called during the game run"""
        self.game.run()
        mock_display_status.assert_called_once()

    @patch('pygame.draw.rect')
    @patch('pygame.display.update')
    @patch('main.HangmanGame._draw')
    def test_draw_is_called_during_run(self, mock_draw, mock_display_update, mock_draw_rect):
        """Test if the _draw method is called during the game run"""
        self.game.run()
        mock_draw.assert_called()

    @patch('pygame.draw.rect')
    @patch('main.HangmanGame.wait_for_user_input')
    def test_wait_for_user_input_called_in_end_of_game_state(self, mock_wait_for_user_input, mock_draw_rect):
        """Test if the wait_for_user_input method is called in an end-of-game state"""
        self.game.game_state = "end_of_game_single_player"
        self.game.run()
        mock_wait_for_user_input.assert_called_once()

    @patch('main.HangmanGame.display_game_over_single_player')
    def test_handle_end_of_round_single_player(self, mock_display_game_over_single_player):
        """Test if the display_game_over_single_player method is called at the end of a single-player round"""
        self.game.total_players = 1
        self.game.current_round = self.game.total_rounds
        self.game.handle_end_of_round()
        mock_display_game_over_single_player.assert_called_once()

    @patch('main.HangmanGame.display_first_player_end')
    def test_handle_end_of_round_multiplayer_first_player(self, mock_display_first_player_end):
        """
        Test if the display_first_player_end method is called at
        the end of a multiplayer round for the first player
        """
        self.game.total_players = 2
        self.game.current_round = self.game.total_rounds
        self.game.current_player_index = 0
        self.game.handle_end_of_round()
        mock_display_first_player_end.assert_called_once()

    @patch('main.HangmanGame.display_game_over_two_players')
    def test_handle_end_of_round_multiplayer_second_player(self, mock_display_game_over_two_players):
        """
        Test if the display_game_over_two_players method is called
        at the end of a multiplayer round for the second player
        """
        self.game.total_players = 2
        self.game.current_round = self.game.total_rounds
        self.game.current_player_index = 1
        self.game.handle_end_of_round()
        mock_display_game_over_two_players.assert_called_once()


if __name__ == '__main__':
    unittest.main()
