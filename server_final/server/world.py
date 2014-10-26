# -*- coding: utf-8 -*-

import const

#导入数据
from loadData.loadStatus import load_status
all_status = load_status()
all_status.load(const.status_filename)

from loadData.loadSkill import raw_skill
skills = raw_skill()
skills.load(const.skill_filename, 1)

from loadData.loadHero import raw_hero
heros = raw_hero()
heros.load(const.hero_filename)

from loadData.loadFences import raw_fences
all_fences = raw_fences()
all_fences.load(const.fence_filename, 0)

from loadData.loadLegend import raw_legend
legends = raw_legend()
legends.load(const.legend_filename, 0)

from loadData import loadReward 
reward = loadReward.reward()
reward.load(const.reward_filename, 0)

# database
from database import friendTable
db_friend = friendTable.friend_table()

from database import heroTable
db_hero = heroTable.hero_table()

from database import legendTable
db_legend = legendTable.legend_table()

from database import passwdTable
db_password = passwdTable.passwd_table()

from database import pvpTable
db_pvp = pvpTable.pvp_table()

from database import userDataTable
db_user_data = userDataTable.user_data_table()

from lib import battleField
battles = battleField.battle_field()

from service import onlineUser
onlineUsers = onlineUser.online_user()

from service import storeData
data_store = storeData.store_data()

from service import timer
task_time = timer.timer()

from service import powerResume
power_resumer = powerResume.power_resume()

from service import heroUpgrade
upgrade_hero = heroUpgrade.hero_upgrade()

import logger

