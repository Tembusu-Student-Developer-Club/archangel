# IMPORTS
import networkx as nx
import time
import random

# FROMS
from MyLogger import MyLogger
from graph import get_graph_from_edges, draw_graph, get_full_cycles_from_graph, \
    full_cycle_to_edges, get_one_full_cycle, convert_full_cycle_to_graph, \
    get_one_full_cycle_from_graph, get_hamiltonian_path_from_graph, \
    is_there_definitely_no_hamiltonian_cycle, hamilton
from random import randint

# Constants
GENDER_MALE = "male"
GENDER_FEMALE = "female"
GENDER_NONBINARY = "non-binary"
GENDER_NOPREF = "no preference"

DISPLAY_GRAPH = True

MINIMUM_MATCHED_PLAYERS_BEFORE_CSVOUTPUT = 0.8
# Proportion minimum of total player count in accepted csv before 2 csvs
# will be outputted (1st accepted players list, 2nd rejected players list

RELAX_NO_SAME_HOUSE_REQUIREMENT_PERCENTAGE = 0.35
# Changing this value changes how much we care about the houses of players being the same
# If 1 - we don't care, and house de-conflicting is ignored. 0 means we won't allow any players of the same house to be
# matched.
RELAX_GENDERPREF_REQUIREMENT_PERCENTAGE = 0.35

# Get Logger
logger = MyLogger()


def get_enum_column_data(player, column):
    column_key = column.replace("_", "")

    if player.__dict__[column_key] == "":
        raise ValueError(f'{column} provided for {player.username} is invalid')
    else:
        return player.__dict__[column_key]


def is_enum_attribute_different(angel_player, mortal_player, column):
    return get_enum_column_data(angel_player, column) != get_enum_column_data(mortal_player, column)


def are_enum_columns_respected(angel_player, mortal_player, enum_columns):
    enum_columns_is_respected = True

    for column in enum_columns:
        print("column is", column)

        random_relax_requirement = random.random() < enum_columns[column]['relax_percentage']
        if random_relax_requirement:
            enum_attribute_different = True
        else:
            enum_attribute_different = is_enum_attribute_different(angel_player, mortal_player, column)

        enum_columns_is_respected = enum_columns_is_respected and enum_attribute_different

    if enum_columns_is_respected:
        print(f"enum columns not respected\n")
    return enum_columns_is_respected


def is_gender_pref_respected(player_being_checked, other_player):
    if player_being_checked.genderpref == GENDER_NOPREF:
        # If they have no preference, always respected
        # print (f"No gender pref")
        return True
    else:
        # Otherwise check if the other_player gender is what is wanted
        gender_pref_respected = player_being_checked.genderpref == other_player.gender
        return gender_pref_respected


def are_gender_prefs_respected(angel_player, mortal_player):
    random_relax_genderpref_requirement = random.random() < RELAX_GENDERPREF_REQUIREMENT_PERCENTAGE
    if random_relax_genderpref_requirement:
        gender_pref_is_respected = True
    else:
        gender_pref_is_respected = is_gender_pref_respected(angel_player, mortal_player) and \
                                   is_gender_pref_respected(mortal_player, angel_player)

    if not gender_pref_is_respected:
        print(f"gender pref not respected")

    return gender_pref_is_respected


def is_there_edge_between_players(angel_player, mortal_player, enum_columns):
    """
    Checks if two players are valid as an angel-mortal pair i.e. an "edge"
    exists between them. E.g. If we are enforcing a heterogenous gender mix for these
    players - check their gender preferences and return False (no edge)
    between them
    """
    print(f"Checking {angel_player} and {mortal_player}")

    # Check if gender choice is respected
    gender_pref_is_respected = are_gender_prefs_respected(angel_player, mortal_player)

    # Check if enum columns is respected
    enum_columns_is_respected = are_enum_columns_respected(angel_player, mortal_player, enum_columns)
    valid_pairing = gender_pref_is_respected and enum_columns_is_respected

    print(f"\n")

    return valid_pairing


def get_player_edges_from_player_list(player_list, enum_columns):
    player_edges = []
    # iterate through all players in list - compare each player to all others
    for player in player_list:
        for other_player in player_list:
            if other_player != player:
                if is_there_edge_between_players(player, other_player, enum_columns):
                    player_edges.append((player, other_player))
                else:
                    logger.info(f"{player} and {other_player} have conflicts")  # to keep track who was rejected
    return player_edges


def angel_mortal_arrange(player_list, enum_columns):
    """
    Depending on the gender preferences to follow, run the edge-finding
    algorithm, generate a graph and find a Hamiltonian circuit.
    """
    print(f"Arranging player list: {player_list}")
    # Convert the list of players into a list of valid edges
    player_edges = get_player_edges_from_player_list(player_list, enum_columns)
    # Generate the overall graph from all edges
    overall_graph = get_graph_from_edges(player_edges)
    print(f"Number of nodes in overall graph: {overall_graph.number_of_nodes()}")
    # Find all connected components and find cycles for all
    graphs = list(overall_graph.subgraph(c) for c in
                  nx.strongly_connected_components(
                      overall_graph))  # #.strongly_connected_component_subgraphs(overall_graph) is deprecated in
    # version 2.4 https://stackoverflow.com/questions/61154740/attributeerror-module-networkx-has-no-attribute
    # -connected-component-subgraph

    print(f"\nConnected components detected: {len(graphs)}")

    print(f"Printing original player list: ")
    for player in player_list:
        print(f"{player}")
    print(f"Original player list size: {len(player_list)}")
    print(f"\n\n")

    list_of_player_chains = []

    for G in graphs:

        print(f"Printing players in current graph:")
        for graph_player in G.nodes():
            print(f"{graph_player}")

        # Draw this intermediate graph
        print(f"Number of nodes in graph: {G.number_of_nodes()}")
        if DISPLAY_GRAPH:
            draw_graph(G)
        # Find out if there is DEFINITELY no hamiltonian cycle
        is_there_full_cycle = is_there_definitely_no_hamiltonian_cycle(G)
        print(f"Is there DEFINITELY no full cycle? - {is_there_full_cycle}")
        # Sleep for a few seconds
        time.sleep(2)
        '''
        # Output all cycles that encompass all nodes (valid pairings)
        full_cycles = get_full_cycles_from_graph(G)
        # Pick any full cycle to draw, or draw nothing if there are no full cycles
        full_cycle = get_one_full_cycle(full_cycles)
        '''
        full_cycle = hamilton(G)  # get_one_full_cycle_from_graph(G)
        # full_cycle = get_hamiltonian_path_from_graph(G)
        # Draw the full cycle if it exists
        if full_cycle is not None and (G.number_of_nodes() >= (MINIMUM_MATCHED_PLAYERS_BEFORE_CSVOUTPUT * len(
                player_list))):  # do not print CSV if number of nodes is < 80% of participants
            G_with_full_cycle = convert_full_cycle_to_graph(full_cycle)
            draw_graph(G_with_full_cycle)
            list_of_player_chains.append(full_cycle)
            # find out which nodes were missing
            players_not_in_csv = set(player_list) - set(list(G.nodes()))
            logger.info(
                f"CSV has been printed. However, the following players {players_not_in_csv} are not inside. Please "
                f"match them manually.")
            print(
                f"Found a full cycle! CSV is printed. However, the following players {players_not_in_csv} are not "
                f"inside. Please match them manually.")
        else:
            print(
                f"There is no full cycle - sorry! This means that the current set of players cannot form a perfect "
                f"chain given the arrange requirements. No CSV printed.")
            logger.info(f"CSV not printed - no full cycle found")

    return list_of_player_chains
