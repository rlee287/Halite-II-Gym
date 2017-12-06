import subprocess
import re

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

def _play_game(binary, map_width, map_height, bot_commands, additional_args):
    """
    Plays one game considering the specified bots and the game and map constraints.
    :param binary: The halite binary
    :param map_width: The map width
    :param map_height: The map height
    :param bot_commands: The commands to run each of the bots
    :return: The game's result string
    """
    game_run_command = '\"{}\" -d "{} {}"'.format(binary, map_width, map_height)
    game_run_command += additional_args
    game_run_command += " -- "
    for bot_command in bot_commands:
        game_run_command += " \"{}\"".format(bot_command)
    #print(game_run_command)
    return subprocess.check_output(game_run_command, shell=True).decode()


def play_games(binary, map_width, map_height, bot_commands, number_of_runs, additional_args):
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
        match_output = _play_game(binary, map_width, map_height, bot_commands, additional_args)
        winner = _determine_winner(match_output)
        winner=winner.rstrip(',')
        if len(len_bots)==0:
            list_of_players = _find_names(match_output)
            len_bots=[len(s) for s in list_of_players]
            string_title="| #   |"+"|".join(list_of_players)+"|"
            print("-"*len(string_title))
            print(string_title)
            print("="*len(string_title))
        result[winner] = result.setdefault(winner, 0) + 1
        print("| "+str(current_run+1).ljust(4)+"|",end="")
        #import pdb;pdb.set_trace()
        for i,length in enumerate(len_bots):
            key="#"+str(i)
            num_wins=result.get(key,0)
            print((" "+str(num_wins)).ljust(length)+"|",end="")
        print("\n",end="")
        print("-"*len(string_title))
        #print("Finished {} runs.".format(current_run + 1))
        #print("Win Ratio: {}".format(result))
    #print("="*len(string_title))
