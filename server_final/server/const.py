# -*- coding: utf-8 -*-

add_hp_type_const_hp = 1
# 加固定值hp
add_hp_type_percentage_hp = 2
# 按照血量最大值百分比加血
add_hp_type_harm_percentage_hp = 3
# 按照伤害量的百分比加血
add_hp_type_add_hp_and_harm_const = 4

add_atk_type_const_atk = 1
# 攻击前加固定值的零时攻击力
add_atk_type_percentage_atk = 2
# 攻击前按比例加零时攻击力
add_atk_type_const_atk_forever = 3
# 永久加固定值攻击力
add_atk_type_percentage_atk_forever = 4
# 永久按比例加攻击力(TODO: 加入顺序可能存在问题，有待考虑是否需要加入这种效果)

damage_type_const = 1
# 直接造成一定量的固定伤害
damage_type_random = 2
# 对某个人造成伤害，伤害值为某个范围内的随机数
damage_type_percentage_hp_max = 3
# 对某个人造成伤害，伤害值为该人hp最大值的某个比例
damage_type_percentage_harm = 4
# 对某个人造成伤害，伤害值为伤害值的某个比例

set_death_type_only = 1
# 致死，不做其他操作
set_death_type_add_atk_forever = 2
# 致死，并永久增加攻击力


block_type_block_const = 1
# 抵挡固定伤害并反弹固定伤害
block_type_block_all = 2
# 抵挡所有伤害并反弹固定伤害
block_type_block_most_harm = 3
# 抵挡伤害，使受到伤害值最多为x

check_hp_comp_type_self_more = 1
check_hp_comp_type_self_less = 2

status_last_time_one_step = 1
# 持续一个回合的状态
status_last_time_always = 2
# 一直持续的状态


status_filename = 'data/status.xlsx'
skill_filename = 'data/skill.xlsx'
hero_filename = 'data/hero.xlsx'
legend_filename = 'data/legend.xlsx'
legend_upgrade_filename = 'data/legend_upgrade.xlsx'
hero_upgrade_filename = 'data/hero_upgrade.xlsx'
fence_filename = 'data/fences.xlsx'
reward_filename = 'data/reward.xlsx'
test_war_filename = 'data/test_war.xlsx'

status_harm_type_const = 1
status_harm_type_ratio = 2


num_of_heap = 3

legend_race = 'legend'

host = "127.0.0.1"
port = 4855
#port = 8888
#port = 10000
client_num = 100

connection_keep_time = 500.0

sid = 'sid'

cid = 'cid'

identification_id = 'identification'

account_service_id = 'accountService'

login_command_id = 'login'
register_command_id = 'register'
username_data_id = 'username'
password_data_id = 'password'
result_data_id = 'result'

battle_service_id = 'battleService'
start_battle_command_id = 'startFight'
step_one_battle_command_id = 'fightOneTurn'
step_all_battle_command_id = 'fightToEnd'
battle_result_command_id = 'battleResult'
move_card_command_id = 'battleMoveCard'

move_from_heap = 'fromPile'
move_from_po = 'fromIndex'
move_to_heap = 'toPile'
move_to_po = 'toIndex'

pvp_service_id = 'pvp'
pvp_get_list = 'get'
pvp_fight = 'fight'

friend_service_id = 'friend'
friend_add = 'add'
friend_remove = 'remove'
friend_get = 'get'
friend_get_random = 'random'
friend_data_id = 'friend'

chat_service_id = 'ServChat'
chat_command_id = 'ChatMessage'
#chat_one_command_id = 'one'
#chat_all_command_id = 'all'
chat_data_id = 'data'

update_service_id = 'DataUpdate'
update_heap_command_id = 'Formation'
upgrade_card_command_id = 'Enforcement'
upgrade_card_data_id = 'enforced'
food_card_data_id = 'consumed'

power_max = 90
power_cost_per_fight = 5
friend_num_max = 20

probability_of_new_hero = [0.4, 0.7, 1]

per_store_time = 5 * 6

num_random_friend = 5
num_random_pvp = 5

