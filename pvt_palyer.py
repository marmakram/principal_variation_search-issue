#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from sample_players import DataPlayer


class CustomPlayer(DataPlayer):
    """
    def score(self, state):
        own_loc = state.locs[self.player_id]
        opp_loc = state.locs[1 - self.player_id]     
        own_liberties = state.liberties(own_loc)
        opp_liberties = state.liberties(opp_loc)
        return len(own_liberties) - 2*len(opp_liberties)"""
    
    def pvs(self, gameState, alpha, beta, depth, color):
        if depth <= 0 or gameState.terminal_test():
            return color

        stMove = True
        for a in gameState.actions():
            r = gameState.result(a)
            if stMove:
                stMove = False
                score = -self.pvs(r, -beta, -alpha, -color, depth -1)
            else:
                score = -self.pvs(r, -alpha-1, -alpha, -color, depth -1)
                if alpha < score and score < beta:
                    score = -self.pvs(r, -beta, -score, -color   , depth -1)
            if alpha < score:
                alpha = score
                best_move = a
            if(alpha >= beta):
                break
        return alpha

    def principal_variation_search(self, gameState, depth=9):
        alpha = float("-inf")
        beta = float("inf")
        color = 1
        best_move = None

        for a in gameState.actions():
            score = self.pvs(gameState.result(a), alpha, beta, color, depth-1)
            if alpha < score:
                alpha = score
                best_move = a   
        return best_move 
       

    def alpha_beta_search(self, gameState, depth = 4):
        alpha = float("-inf")
        al = float("-inf")
        beta = float("inf")
        best_score = float("-inf")
        best_move = None
        
        for a in gameState.actions():
            v = self.min_value(gameState.result(a), alpha, beta, depth)
            alpha = max(alpha, v)
            if v > best_score:
                best_score = v
                best_move = a
        return best_move
    
    def min_value(self, gameState, alpha, beta, depth):
        if gameState.terminal_test():
            return gameState.utility(0)
        if depth <= 0: return 0
            #rself.score(gameState)
        v = float("inf")
        for a in gameState.actions():
            v = min(v, self.max_value(gameState.result(a), alpha, beta, depth-1))
            if v <= alpha:
                return v
            beta = min(v, beta)
        return v

    def max_value(self, gameState, alpha, beta, depth):
        if gameState.terminal_test():
            return gameState.utility(0)
        if depth <= 0: return 0
            #return self.score(gameState)
        v = float("-inf")
        for a in gameState.actions():
            v = max(v, self.min_value(gameState.result(a), alpha, beta, depth-1))
            if v >= beta:
                return v
            alpha = max(v, alpha)
        return v

    def get_action(self, state):

        import random
        #self.queue.put(random.choice(state.actions()))
        """if state.ply_count < 2:
        self.queue.put(random.choice(state.actions()))
        else:
        self.queue.put(self.alpha_beta_search(state))"""
        self.queue.put(self.principal_variation_search(state))

