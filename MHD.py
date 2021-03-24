from random import shuffle
import numpy as np
from collections import defaultdict, OrderedDict
import pandas as pd


class Montyhall:

    def __init__(self):
        trophy = [False, False, True]
        shuffle(trophy)
        door1, door2, door3 = trophy
        choices = {'one': door1, 'two': door2, 'three': door3}
        user_choices = ['one', 'two', 'three']
        self.choices = choices
        self.user_choices = user_choices

    def first_choice(self):
        result = self.choices[self.choice]
        alternatives = self.choices.copy()
        del alternatives[self.choice]
        if len(set(alternatives.values())) == 1:
            reveal, change_decision = list(alternatives.keys())
        else:
            for k, v in alternatives.items():
                if v == False:
                    reveal = k
                else:
                    change_decision = k

        return result, reveal, change_decision

    def stayOrSwitch(self):
        if self.decision == 'random':
            choice = [self.change_decision, self.choice]
            shuffle(choice)
            choice = choice[0]
            return self.choices[choice]
        elif self.decision == 'switch':
            return self.choices[self.change_decision]
        else:
            return self.choices[self.choice]

    def expirement(self, num_of_rounds, num_of_trials, decision):
        self.decision = decision
        winning_percentages = list()
        wins_counting_list = list()
        trials_count = 0
        wins_counter = 0
        for n in range(num_of_rounds):
            final_results = list()
            for i in range(num_of_trials):
                shuffle(self.user_choices)
                self.choice = self.user_choices[0]
                self.result, self.reveal, self.change_decision = self.first_choice()
                result = self.stayOrSwitch()
                if result:
                    wins_counter += 1
                final_results.append(result)
                trials_count += 1

                if trials_count % 1000 == 0:
                    wins_counting_list.append(wins_counter)
            final_percent = final_results.count(True) / num_of_trials * 100
            winning_percentages.append(final_percent)
        return round(sum(winning_percentages) / len(winning_percentages), 2), winning_percentages, wins_counting_list


def get_wins_percentages_frequency(bell_curves_data):
    freq = OrderedDict()
    for n in range(1, 201):
        freq[n / 2] = bell_curves_data.count(n / 2)

    return freq


# In[5]:


exp = Montyhall()

# In[45]:


switch_final_percentage, switch_winning_percentages, switch_wins_counting_list = exp.expirement(1000, 1000, 'switch')
stay_final_percentage, stay_winning_percentages, stay_wins_counting_list = exp.expirement(1000, 1000, 'stay')
random_final_percentage, random_winning_percentages, random_wins_counting_list = exp.expirement(1000, 1000, 'random')

# In[73]:



df = pd.DataFrame()

bell_curves_data = pd.Series(stay_winning_percentages + random_winning_percentages + swithc_winning_percentages)
# bell_curves_data = [round(n*2)/2 for n in bell_curves_data]
# bell_curves_data = get_wins_percentages_frequency(bell_curves_data)


# df['freq_index'] = pd.Series(bell_curves_data.keys())
df['bell_curve_freq'] = pd.Series(bell_curves_data)

df['switch_wins_counting_list'] = pd.Series(switch_wins_counting_list)
df['stay_wins_counting_list'] = pd.Series(stay_wins_counting_list)
df['random_wins_counting_list'] = pd.Series(random_wins_counting_list)

df['exp_index'] = pd.Series(range(0, 1000 ** 2, 1000))

df['switch_winning_percentages'] = pd.Series(switch_winning_percentages)
df['stay_winning_percentages'] = pd.Series(stay_winning_percentages)
df['random_winning_percentages'] = pd.Series(random_winning_percentages)

df['stay_winning_percent.'] = pd.Series([switch_final_percentage, 100 - switch_final_percentage,
                                         stay_final_percentage, 100 - stay_final_percentage,
                                         random_final_percentage, 100 - random_final_percentage,
                                         50, 50])

df['pie_chart_measures'] = pd.Series(['switch_winning_percent', 'switch_losing_percent',
                                      'stay_winning_percent', 'stay_losing_percent',
                                      'random_winning_percentage', 'random_losing_percentage',
                                      'losing', 'winning'])


df.to_excel('monty_hall.xlsx', index=False)


