marathon_goals = {'place': 20, 'hunger': 0, 'thirst': 0}
marathon_actions = {'run': {'place': -1, 'hunger': +2, 'thirst': +2},
           'bite': {'hunger': -2},
           'eat': {'place': +1, 'hunger': -6},
           'sip': {'thirst': -2},
           'drink': {'place': +1, 'thirst': -6}
            }

#Turns go from 0 to -10 so that it is never considered the best goal. This is because there is no action to gain turns back.
combat_goals = {'damage': 0, 'enemy': 20, 'turns': 0}
combat_actions = {'weak attack': {'enemy': -2, 'damage': +1, 'turns': -1},
           'strong attack': {'enemy': -3, 'damage': +2, 'turns': -2},
           'minor heal': {'damage': -1, 'turns': -1},
           'major heal': {'damage': -2, 'turns': -2}
            }

def check_utility(action, goal):
    if goal in actions[action]:
        #Action value is inverted value in actions.
        action_value = -(actions[action][goal])
        #If the action value would cause the current goal to go below the place goal...
        if scenario == 'marathon':
            if (((goals[goal] - action_value) < goals['place']) and (goal != 'place')):
                #...then calculate the overflow and add it to the action value.
                overflow = ((goals[goal] - action_value) - goals['place'])
                action_value += overflow
        return action_value
    else:
        return 0

def perform_action(action):
    for goal, change in list(actions[action].items()):
        if change > 0:
            goals[goal] = min(goals[goal]+change, 20)
        elif goal == 'turns':
            goals[goal] = goals[goal]+change
        else:
            goals[goal] = max(goals[goal]+change, 0)

def choose_action():
    best_goal, best_goal_value = max(list(goals.items()), key=lambda item: item[1])
    best_action = None
    best_utility = None
    for key, value in actions.items():
        if best_goal in value:
            if best_action is None:
                best_action = key
                best_utility = check_utility(best_action, best_goal)
            else:
                new_utility = check_utility(key, best_goal)
                if new_utility > best_utility:
                    best_action = key
                    best_utility = new_utility
    return best_action

def print_actions():
    print('Actions:')
    for name, effects in list(actions.items()):
        print(" * [%s]: %s" % (name, str(effects)))

#--------------------------------------------------
#Below is the code for the Marathon scenario loop.
#--------------------------------------------------

def run_until_finished():
    print_actions()
    print('3...2...1...Go!')
    running = True
    while running:
        print('Goals:', goals)
        action = choose_action()
        print('Best action:', action)
        perform_action(action)
        print('New goals:', goals)
        print('-------------------------')
        if ((goals['place'] == 1) and (goals['hunger'] <= 5) and (goals['thirst'] <= 5)):
            running = False
    print('Race over!')

#-------------------------------------------
#End of the code for the Marathon scenario.
#-------------------------------------------

#----------------------------------------------------------------------
#Below is the Marathon loop code code tweaked for the Combat scenario.
#----------------------------------------------------------------------

def fight_until_finished():
    print_actions()
    print('3...2...1...Begin!')
    fighting = True
    while fighting:
        print('Goals:', goals)
        action = choose_action()
        print('Best action:', action)
        perform_action(action)
        print('New goals:', goals)
        print('-------------------------')
        if ((goals['damage'] < 5) and (goals['enemy'] == 0) and (goals['turns'] > -10)):
            fighting = False
            print('Victory!')
        elif ((goals['damage'] == 10) or (goals['turns'] == -10)):
            fighting = False
            print('Defeat!')

#-----------------------------------------------------------
#End of the code specifically for the Combat scenario.
#-----------------------------------------------------------

if __name__ == '__main__':
    scenario = input('Would you like to run the marathon or combat scenario? ')
    scenario = scenario.lower()
    if scenario == 'marathon':
        goals = marathon_goals
        actions = marathon_actions
        run_until_finished()
    elif scenario == 'combat':
        goals = combat_goals
        actions = combat_actions
        fight_until_finished()
