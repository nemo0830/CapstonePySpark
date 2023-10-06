import random

def random_assign_team_based_on_tier(df):
    tier_dic = {"tier1": [], "tier2": [], "tier3": [], "tier4": []}
    team_tier_list = zip(df['team_name'].tolist(), df['tier_num'].tolist())
    for elem in team_tier_list:
        tier_dic[elem[1]] = tier_dic[elem[1]] + [elem[0]]

    row_num = len(tier_dic["tier1"])
    res = []
    for i in range(row_num):
        row = ["Group" + str(i)]
        for key, val in tier_dic.items():
            team = random.choice(val)
            row.append(team)
            tier_dic[key].remove(team)
        res.append(row)
    return res