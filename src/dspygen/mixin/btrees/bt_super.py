# from random import choice
#
# fromutils.test_fsm_superhero import NarcolepticSuperhero, SuperheroState
#
#
# class BTNode:
#     def run(self):
#         raise NotImplementedError
#
#
# class Selector(BTNode):
#     def __init__(self, children):
#         self.children = children
#
#     def run(self):
#         for child in self.children:
#             if child.run() == True:
#                 return True
#         return False
#
#
# class Sequence(BTNode):
#     def __init__(self, children):
#         self.children = children
#
#     def run(self):
#         for child in self.children:
#             if child.run() == False:
#                 return False
#         return True
#
#
# class ActionNode(BTNode):
#     def __init__(self, action):
#         self.action = action
#
#     def run(self):
#         return self.action()
#
#
# class ConditionNode(BTNode):
#     def __init__(self, condition_func):
#         self.condition_func = condition_func
#
#     def run(self):
#         return self.condition_func()
#
#
# class NarcolepticSuperheroAction(ActionNode):
#     def __init__(self, hero, action):
#         super().__init__(action)
#         self.hero = hero
#
#     def run(self):
#         action_method = getattr(self.hero, self.action)
#         action_method()
#         return True  # or some condition based on hero's state
#
#
# def is_hero_exhausted(hero):
#     return hero.is_exhausted()
#
#
# def is_world_in_danger():
#     # This could be a simulated or real condition check
#     return choice([True, False])
#
#
# def create_complex_hero_behavior_tree(hero):
#     return Selector([
#         Sequence([
#             ConditionNode(lambda: hero.state == SuperheroState.ASLEEP),
#             NarcolepticSuperheroAction(hero, 'wake_up'),
#         ]),
#         Sequence([
#             ConditionNode(is_world_in_danger),
#             NarcolepticSuperheroAction(hero, 'distress_call'),
#             NarcolepticSuperheroAction(hero, 'complete_mission'),
#             Selector([
#                 Sequence([
#                     ConditionNode(lambda: is_hero_exhausted(hero)),
#                     NarcolepticSuperheroAction(hero, 'clean_up_exhausted')
#                 ]),
#                 NarcolepticSuperheroAction(hero, 'clean_up')
#             ])
#         ]),
#         Sequence([
#             ConditionNode(lambda: hero.state != SuperheroState.ASLEEP and not is_world_in_danger()),
#             NarcolepticSuperheroAction(hero, 'work_out'),
#             NarcolepticSuperheroAction(hero, 'eat'),
#             NarcolepticSuperheroAction(hero, 'nap')
#         ])
#     ])
#
#
#
# def main():
#     hero = NarcolepticSuperhero("SleepyMan")
#     bt = create_complex_hero_behavior_tree(hero)
#     bt.run()
#     assert hero.state == SuperheroState.ASLEEP.name, "Hero should be asleep"
#
#
# if __name__ == '__main__':
#     main()
