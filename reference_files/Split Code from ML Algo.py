split_result = {}
for i in trange(2,10):
    split_result[str(i)+","+str(i)]=[]
    for c in trange(1, 11):   #Dealer card 2-10, A
        lose_counts = 0
        win_counts = 0
        draw_counts = 0
        split_gain = 0
        nonsplit_gain = 0
        for j in range(steps):
            for k in range(3):     #k-0,1, Split card, k-2, not split
                d = Dealer(c)
                while True:
                    secondcard = randint(1,13)
                    if secondcard>10:
                        secondcard = 10
                    if secondcard!=i:
                        break
                if k==2:
                    secondcard = i
                p = Player(i, secondcard)
                hit_count = 0
                player_lose = False
                doublescaler = 1
                while True:
                    score = p.calculatescore()
                    if score>18 and score<=21:
                        break
                    if score>21:
                        player_lose = True
                        break
                    if p.flag_ace:
                        cardsum = np.sum(np.array(p.cards))
                        if cardsum-1<11:
                            key = 'A,'+str(cardsum-1)
                        else:
                            key = str(score)
                    else:
                        key = str(score)
                    action = policy[key][c-1]
                    if hit_count==0: 
                        if action=='D' or action=='D/S':
                            doublescaler = 2
                    if (hit_count==0 and action=='D/S') or action=='D' or action=='H':
                        p.hit()
                        hit_count += 1
                    else:
                        score = p.calculatescore()
                        if score>21:
                            lose_counts += 1*doublescaler
                            if k<2:
                                split_gain -= 1*doublescaler
                            else:
                                nonsplit_gain -= 1*doublescaler
                            player_lose = True
                            break
                        else:
                            player_lose = False
                            break
                if player_lose==False:
                    dealerscore = d.play()
                    if dealerscore>21:
                        win_counts += 1*doublescaler
                        if k<2:
                            split_gain += 1*doublescaler
                        else:
                            nonsplit_gain += 1*doublescaler
                    else:
                        if score<dealerscore:
                            lose_counts += 1*doublescaler
                            if k<2:
                                split_gain -= 1*doublescaler
                            else:
                                nonsplit_gain -= 1*doublescaler
                        elif score>dealerscore:
                            win_counts += 1*doublescaler
                            if k<2:
                                split_gain += 1*doublescaler
                            else:
                                nonsplit_gain += 1*doublescaler
                        else:
                            draw_counts += 1
                else:
                    if k<2:
                        split_gain -= 1*doublescaler
                    else:
                        nonsplit_gain -= 1*doublescaler
                del d, p
        split_result[str(i)+","+str(i)].append([split_gain,nonsplit_gain])   
 
split_policy = {}
for key in split_result:
    split_policy[key] = []
    for i in range(10):
        if split_result[key][i][0]<split_result[key][i][1]:
            policykey = str(int(key.split(',')[0])*2)
            split_policy[key].append(policy[policykey][i])
        else:
            split_policy[key].append('P')
 
split_policy_result = 'Player;2;3;4;5;6;7;8;9;10;A\n'
for key in split_policy:
    split_policy_result += key+';'+';'.join(split_policy[key][1:])+';'+split_policy[key][0]+'\n'
with open('split_policy.csv', 'w') as f:
    f.write(split_policy_result)
df_split = pd.read_csv('split_policy.csv', header=0, index_col=0, sep=';')
df_split.head(100)