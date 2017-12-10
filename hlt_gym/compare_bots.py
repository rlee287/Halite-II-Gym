import subprocess
import re
import random

_WINNING_RANK_STRING = "rank #1"
_BOT_NAME_REGEX="received from player ., .+"
_BOT_NAME_POSITION = 6
_SPACE_DELIMITER = ' '
_BOT_ID_POSITION = 1


def _determine_winner(game_result):
    """
    From the game result string, extract the winner's id.
    :param game_result: The result of running a game on the Halite binary
    :return:
    """
    return next(line for line in game_result.splitlines()
                if re.compile(_WINNING_RANK_STRING).search(line)).split(_SPACE_DELIMITER)[_BOT_ID_POSITION]

def _find_names(game_result):
    final_list=list()
    iterate=(line for line in game_result.splitlines() if re.compile(_BOT_NAME_REGEX).search(line))
    for item in iterate:
        # Properly handle bots whose name includes spaces
        final_str=' '.join(item.split(_SPACE_DELIMITER)[6:])
        # Remove last period
        final_list.append(final_str[:-1])
    return final_list

def _play_game(binary, bot_commands, additional_args):
    """
    Plays one game considering the specified bots and the game and map constraints.
    :param binary: The halite binary
    :param map_width: The map width
    :param map_height: The map height
    :param bot_commands: The commands to run each of the bots
    :return: The game's result string
    """
    game_run_command = '\"{}\" '.format(binary)
    game_run_command += additional_args
    game_run_command += " -- "
    for bot_command in bot_commands:
        game_run_command += " \"{}\"".format(bot_command)
    print(game_run_command)
    return subprocess.check_output(game_run_command, shell=True).decode()


def play_games(binary, bot_commands, number_of_runs, additional_args):
    """
    Runs number_of_runs games using the designated bots and binary, recording the tally of wins per player
    :param binary: The Halite binary.
    :param map_width: The map width
    :param map_height: The map height
    :param bot_commands: The commands to run each of the bots (must be either 2 or 4)
    :param number_of_runs: How many runs total
    :return: Nothing
    """
    print("Comparing Bots!")
    result = {}
    len_bots=list()
    #if not(len(bot_commands) == 4 or len(bot_commands) == 2):
    #    raise IndexError("The number of bots specified must be either 2 or 4.")
    for current_run in range(0, number_of_runs):
        match_output = _play_game(binary, bot_commands, additional_args)
        winner = _determine_winner(match_output)
        winner=winner.rstrip(',')
        if len(len_bots)==0:
            list_of_players = _find_names(match_output)
            numbered_list=list_of_players[:]
            for index in range(len(numbered_list)):
                numbered_list[index]="#"+str(index)+":"+numbered_list[index]
            for index in range(len(list_of_players)):
                numbered_list.append(" #{} %    ".format(index))
            len_bots=[len(s) for s in numbered_list]
            string_title="| #   |"+"|".join(numbered_list)+"|"
            print("-"*len(string_title))
            print(string_title)
            print("="*len(string_title))
        result[winner] = result.setdefault(winner, 0) + 1
        print("| "+str(current_run+1).ljust(4)+"|",end="")
        for i in range(len(list_of_players)):
            key="#"+str(i)
            num_wins=result.get(key,0)
            len_to_pad=len(numbered_list[i])
            print((" "+str(num_wins)).ljust(len_to_pad)+"|",end="")
        for i in range(len(list_of_players)):
            key="#"+str(i)
            num_wins=result.get(key,0)
            percentage=round(num_wins/(current_run+1),4)
            len_to_pad=len(numbered_list[i+len(list_of_players)])
            print((" "+"{:.2%}".format(percentage)).ljust(len_to_pad)+"|",end="")
        print("\n",end="")
        print("-"*len(string_title))
    max_num_win_key=""
    max_num_win_val=0
    for i in range(len(list_of_players)):
        key="#"+str(i)
        num_wins=result.get(key,0)
        if max_num_win_val<num_wins:
            max_num_win_key=key
            max_num_win_val=num_wins
    print("Bot "+max_num_win_key+
          " won the most, winning {}/{} times.".format(max_num_win_val,number_of_runs))
