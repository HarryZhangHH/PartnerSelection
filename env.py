class Environment():
    """
    PD payoff matrix
                Cooperate | Defect
    Cooperate         R,R | S,T
    Defect            T,S | P,P

    R: reward
    P: punishment
    T: temptation
    S: sucker
    T > R > P >S
    2R > T+S
    """
    
    def __init__(self, config):
        self.config = config
        self.episode = 0
        self.running_score = 0.0

    def play(self, agent1, agent2, episodes):
        for i in range(episodes):
            a1, a2 = agent1.act(agent2), agent2.act(agent1)
            _, r1, r2 = self.step(a1, a2)
            agent1.update(r1, a1, a2)
            agent2.update(r2, a2, a1)
        return r1, r2
    
    def step(self, a1, a2):
        """
        action:
        0 = cooperate
        1 = defect
        """
        episode = self.episode
        self.episode += 1
        assert a1 is not None, "action of agent 1 is None"
        assert a2 is not None, "action of agent 2 is None"
        if a1==0 and a2==0:
            r1, r2 = self.config.reward, self.config.reward
        elif a1==0 and a2==1:
            r1, r2 = self.config.sucker, self.config.temptation
        elif a1==1 and a2==0:
            r1, r2 = self.config.temptation, self.config.sucker
        elif a1==1 and a2==1:
            r1, r2 = self.config.punishment, self.config.punishment
        
        return episode, r1, r2

    def update(self, reward):
        self.running_score = reward + self.config.discount * self.running_score

    def reset(self):
        self.episode = 0
        self.running_score = 0.0