
# coding: utf-8

# ## 1. Of cats and cookies
# <p><a href="https://www.facebook.com/cookiecatsgame">Cookie Cats</a> is a hugely popular mobile puzzle game developed by <a href="http://tactile.dk">Tactile Entertainment</a>. It's a classic "connect three"-style puzzle game where the player must connect tiles of the same color to clear the board and win the level. It also features singing cats. We're not kidding! Check out this short demo:</p>
# <p><a href="https://youtu.be/GaP5f0jVTWE"><img src="https://s3.amazonaws.com/assets.datacamp.com/production/project_184/img/cookie_cats_video.jpeg" style="width: 500px"></a></p>
# <p>As players progress through the levels of the game, they will occasionally encounter gates that force them to wait a non-trivial amount of time or make an in-app purchase to progress. In addition to driving in-app purchases, these gates serve the important purpose of giving players an enforced break from playing the game, hopefully resulting in that the player's enjoyment of the game being increased and prolonged.</p>
# <p><img src="https://s3.amazonaws.com/assets.datacamp.com/production/project_184/img/cc_gates.png" alt=""></p>
# <p>But where should the gates be placed? Initially the first gate was placed at level 30, but in this notebook we're going to analyze an AB-test where we moved the first gate in Cookie Cats from level 30 to level 40. In particular, we will look at the impact on player retention. But before we get to that, a key step before undertaking any analysis is understanding the data. So let's load it in and take a look!</p>

# In[180]:


# Importing pandas
import pandas as pd

# Reading in the data
df = pd.read_csv('datasets/cookie_cats.csv')

# Showing the first few rows
df.head()


# In[181]:


get_ipython().run_cell_magic('nose', '', '\nimport pandas as pd\n        \ndef test_yearly_correctly_loaded():\n    correct_df = pd.read_csv(\'datasets/cookie_cats.csv\')\n    assert correct_df.equals(df), \\\n        "The variable df should contain the data in datasets/cookie_cats.csv"')


# ## 2. The AB-test data
# <p>The data we have is from 90,189 players that installed the game while the AB-test was running. The variables are:</p>
# <ul>
# <li><code>userid</code> - a unique number that identifies each player.</li>
# <li><code>version</code> - whether the player was put in the control group (<code>gate_30</code> - a gate at level 30) or the group with the moved gate (<code>gate_40</code> - a gate at level 40).</li>
# <li><code>sum_gamerounds</code> - the number of game rounds played by the player during the first 14 days after install.</li>
# <li><code>retention_1</code> - did the player come back and play <strong>1 day</strong> after installing?</li>
# <li><code>retention_7</code> - did the player come back and play <strong>7 days</strong> after installing?</li>
# </ul>
# <p>When a player installed the game, he or she was randomly assigned to either <code>gate_30</code> or <code>gate_40</code>. As a sanity check, let's see if there are roughly the same number of players in each AB group. </p>

# In[182]:


# Counting the number of players in each AB group.
df.groupby('version')['version'].count()


# In[183]:


get_ipython().run_cell_magic('nose', '', "\ndef test_nothing():\n    assert True, \\\n    'Nothing to test here'")


# ## 3. The distribution of game rounds
# <p><img src="https://s3.amazonaws.com/assets.datacamp.com/production/project_184/img/mr_waffles_smiling.png" style="width:200px; float:left"> </p>
# <p>It looks like there is roughly the same number of players in each group, nice!</p>
# <p>The focus of this analysis will be on how the gate placement affects player retention, but just for fun: Let's plot the distribution of the number of game rounds players played during their first week playing the game.</p>

# In[184]:


plot_df = df.groupby('sum_gamerounds').count().reset_index()
plot_df.head()


# In[185]:


# This command makes plots appear in the notebook
get_ipython().run_line_magic('matplotlib', 'inline')

# Counting the number of players for each number of gamerounds 
plot_df = df.groupby('sum_gamerounds').count().reset_index()

# Plotting the distribution of players that played 0 to 100 game rounds
ax = plot_df.head(n=100).plot('sum_gamerounds', 'userid')
ax.set_xlabel("# of Rounds")
ax.set_ylabel("Count of Players")
ax.set_title("Game Rounds Played during First Week");


# In[186]:


get_ipython().run_cell_magic('nose', '', "\ndef test_y_axis():\n    assert ax.get_lines()[0].get_ydata().sum() == 77673, \\\n    'The plot should be assigned to ax and have userid on the Y-axis'\n    \ndef test_x_axis():\n    assert ax.get_lines()[0].get_xdata().sum() == 4950, \\\n    'The plot should be assigned to ax and have sum_gamerounds on the X-axis'")


# ## 4. Overall 1-day retention
# <p>In the plot above we can see that some players install the game but then never play it (0 game rounds), some players just play a couple of game rounds in their first week, and some get really hooked!</p>
# <p>What we want is for players to like the game and to get hooked. A common metric in the video gaming industry for how fun and engaging a game is <em>1-day retention</em>: The percentage of players that comes back and plays the game <em>one day</em> after they have installed it.  The higher 1-day retention is, the easier it is to retain players and build a large player base. </p>
# <p>As a first step, let's look at what 1-day retention is overall.</p>

# In[187]:


# The % of users that came back the day after they installed
df['retention_1'].mean()


# In[188]:


get_ipython().run_cell_magic('nose', '', "\ndef test_nothing():\n    assert True, \\\n    'Nothing to test here'")


# ## 5. 1-day retention by AB-group
# <p><img src="https://s3.amazonaws.com/assets.datacamp.com/production/project_184/img/belle_cookie.png" style="width:200px; float:right"> </p>
# <p>So, a little less than half of the players come back one day after installing the game. Now that we have a benchmark, let's look at how 1-day retention differs between the two AB-groups.</p>

# In[189]:


# Calculating 1-day retention for each AB-group
df.groupby('version')['retention_1'].mean()


# In[190]:


get_ipython().run_cell_magic('nose', '', "\ndef test_nothing():\n    assert True, \\\n    'Nothing to test here'")


# ## 6. Should we be confident in the difference?
# <p>It appears that there was a slight decrease in 1-day retention when the gate was moved to level 40 (44.2%) compared to the control when it was at level 30 (44.8%). It's a small change, but even small changes in retention can have a large impact. But while we are certain of the difference in the data, how certain should we be that a gate at level 40 will be worse in the future?</p>
# <p>There are a couple of ways we can get at the certainty of these retention numbers. Here we will use bootstrapping: We will repeatedly re-sample our dataset (with replacement) and calculate 1-day retention for those samples. The variation in 1-day retention will give us an indication of how uncertain the retention numbers are.</p>

# In[191]:


# Creating a list with bootstrapped means for each AB-group
boot_1d = []
iterations=500
for i in range(iterations):
    boot_mean = df.sample(frac=1, replace=True).groupby(
        'version')['retention_1'].mean()
    boot_1d.append(boot_mean)
    
# Transforming the list to a DataFrame
boot_1d = pd.DataFrame(boot_1d)
    
# A Kernel Density Estimate plot of the bootstrap distributions
ax = boot_1d.plot.kde()
ax.set_title('Bootstrapped 1-Day Retention Means for each AB-group')
ax.set_xlabel('Mean 1-Day Retention');


# In[192]:


get_ipython().run_cell_magic('nose', '', "\ndef test_boot_1d():\n    assert isinstance(boot_1d, pd.DataFrame) and boot_1d.shape == (500, 2), \\\n        'boot_1d should be a DataFrame with two columns and 500 rows with the bootstrapped 1-day retentions from both AB-groups.'")


# ## 7. Zooming in on the difference
# <p>These two distributions above represent the bootstrap uncertainty over what the underlying 1-day retention could be for the two AB-groups. Just eyeballing this plot, we can see that there seems to be some evidence of a difference, albeit small. Let's zoom in on the difference in 1-day retention</p>
# <p>(<em>Note that in this notebook we have limited the number of bootstrap replication to 500 to keep the calculations quick. In "production" we would likely increase this to a much larger number, say, 10 000.</em>)</p>

# In[193]:


# checking first few rows of boot_1d 
boot_1d.head()


# In[194]:


# Adding a column with the % difference between the two AB-groups
boot_1d['diff'] = ((boot_1d.gate_30 - boot_1d.gate_40)
                   / boot_1d.gate_40 * 100)

# Plotting the bootstrap % difference
ax = boot_1d['diff'].plot.kde()
ax.set_xlabel('Percent Difference in Means')
ax.set_title('Bootstrap % Difference in 1-Day Retention Means');


# In[195]:


get_ipython().run_cell_magic('nose', '', '\ndef test_diff():\n    correct_diff = (boot_1d[\'gate_30\'] - boot_1d[\'gate_40\']) /  boot_1d[\'gate_40\'] * 100\n    assert correct_diff.equals(boot_1d[\'diff\']), \\\n    \'Make sure that boot_1d["diff"] is calculated as (gate_30 - gate_40) / gate_40 * 100 .\'')


# ## 8. The probability of a difference
# <p><img src="https://s3.amazonaws.com/assets.datacamp.com/production/project_184/img/ziggy_smiling.png" style="width:200px; float:left"> </p>
# <p>From this chart, we can see that the most likely % difference is around 1% - 2%, and that most of the distribution is above 0%, in favor of a gate at level 30. But what is the <em>probability</em> that the difference is above 0%? Let's calculate that as well.</p>

# In[196]:


# Calculating the probability that 1-day retention is greater when the gate is at level 30
prob = (boot_1d['diff'] > 0).sum() / len(boot_1d['diff'])
# or prob = (boot_1d['diff'] > 0).mean()

# Pretty printing the probability
'{0:.1%}'.format(prob)


# In[197]:


get_ipython().run_cell_magic('nose', '', '\ndef test_prob():\n    correct_prob = (boot_1d[\'diff\'] > 0).sum() / len(boot_1d)\n    assert correct_prob == prob, \\\n    \'prob should be the proportion of boot_1d["diff"] above zero\'')


# ## 9. 7-day retention by AB-group
# <p>The bootstrap analysis tells us that there is a high probability that 1-day retention is better when the gate is at level 30. However, since players have only been playing the game for one day, it is likely that most players haven't reached level 30 yet. That is, many players won't have been affected by the gate, even if it's as early as level 30. </p>
# <p>But after having played for a week, more players should have reached level 40, and therefore it makes sense to also look at 7-day retention. That is: What percentage of the people that installed the game also showed up a week later to play the game again.</p>
# <p>Let's start by calculating 7-day retention for the two AB-groups.</p>

# In[198]:


# Calculating 7-day retention for both AB-groups
df.groupby('version')['retention_7'].mean()


# In[199]:


get_ipython().run_cell_magic('nose', '', "\ndef test_nothing():\n    assert True, \\\n    'Nothing to test here'")


# ## 10. Bootstrapping the difference again
# <p>Like with 1-day retention, we see that 7-day retention is slightly lower (18.2%) when the gate is at level 40 than when the gate is at level 30 (19.0%). This difference is also larger than for 1-day retention, presumably because more players have had time to hit the first gate. We also see that the <em>overall</em> 7-day retention is lower than the <em>overall</em> 1-day retention; fewer people play a game a week after installing than a day after installing.</p>
# <p>But as before, let's use bootstrap analysis to figure out how certain we should be of the difference between the AB-groups.</p>

# In[200]:


# Creating a list with bootstrapped means for each AB-group
boot_7d = []
for i in range(500):
    boot_mean = df.sample(frac=1, replace=True).groupby(
        'version')['retention_7'].mean()
    boot_7d.append(boot_mean)
    
# Transforming the list to a DataFrame
boot_7d = pd.DataFrame(boot_7d)

# Adding a column with the % difference between the two AB-groups
boot_7d['diff'] = ((boot_7d['gate_30'] - boot_7d['gate_40']) / 
                   boot_7d['gate_40'] * 100)

# Ploting the bootstrap % difference
ax = boot_7d['diff'].plot.kde()
ax.set_xlabel("% difference in means")
ax.set_title('Bootstrap % Difference in 7-Day Retention Means');

# Calculating the probability that 7-day retention is greater when the gate is at level 30
prob = (boot_7d['diff'] > 0).mean()

# Pretty printing the probability
'{0:.1%}'.format(prob)


# In[201]:


get_ipython().run_cell_magic('nose', '', '\ndef test_boot_7d():\n    assert isinstance(boot_7d, pd.DataFrame) and boot_7d.shape == (500, 3), \\\n        \'boot_7d should be a DataFrame with three columns and 500 rows with the bootstrapped 7-day retentions from both AB-groups.\'\n        \ndef test_prob():\n    correct_prob = (boot_7d[\'diff\'] > 0).sum() / len(boot_7d)\n    assert correct_prob == prob, \\\n    \'prob should be the proportion of boot_7d["diff"] above zero\'')


# ## 11.  The conclusion
# <p>The bootstrap result tells us that there is strong evidence that 7-day retention is higher when the gate is at level 30 than when it is at level 40. The conclusion is: If we want to keep retention high — both 1-day and 7-day retention — we should <strong>not</strong> move the gate from level 30 to level 40. There are, of course, other metrics we could look at, like the number of game rounds played or how much in-game purchases are made by the two AB-groups. But retention <em>is</em> one of the most important metrics. If we don't retain our player base, it doesn't matter how much money they spend in-game.</p>
# <p><img src="https://s3.amazonaws.com/assets.datacamp.com/production/project_184/img/cookie_yellow.png" style="width:100px; float:center"> </p>
# <p>So, why is retention higher when the gate is positioned earlier? One could expect the opposite: The later the obstacle, the longer people are going to engage with the game. But this is not what the data tells us. The theory of <em>hedonic adaptation</em> can give one explanation for this. In short, hedonic adaptation is the tendency for people to get less and less enjoyment out of a fun activity over time if that activity is undertaken continuously. By forcing players to take a break when they reach a gate, their enjoyment of the game is prolonged. But when the gate is moved to level 40, fewer players make it far enough, and they are more likely to quit the game because they simply got bored of it. </p>

# In[202]:


# So, given the data and the bootstrap analysis
# Should we move the gate from level 30 to level 40 ?
move_to_level_40 = False


# In[203]:


get_ipython().run_cell_magic('nose', '', "\ndef test_conclusion():\n    assert move_to_level_40 == False, \\\n    'That is not a reasonable conclusion given the data and the analysis.'")

