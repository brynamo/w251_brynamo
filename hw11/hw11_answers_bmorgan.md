# Questions for HW 11:

1. What parameters did you change?
2. What values did you try?
3. Did you try any other changes that made things better or worse?
4. Did they improve or degrade the model? Did you have a test run with 100% of the scores above 200?
5. Based on what you observed, what conclusions can you draw about the different parameters and their values?
6. What is the purpose of the epsilon value?
7. Describe "Q-Learning".

# Answers for HW 11

1. The main parameters were:
  - Layer density for the first and second layers
  - Number of epochs
  - Activation functions

2. After trying a few different ones, I ultimately used:
  - Layer Density: 512 for first layer and 256 for the second
  - Number of Epochs: 2
  - Activation functions: ReLU for the first and Tanh for the second

3. I additionally changed the epsilon decay, thinking that this would help mitigate too much exploration given that this was a relatively simple problem to be solved.

4. Changing the epsilon decay seems to have helped as the average reward by 300 episodes was roughly 135. *bryan* Unfortunately though there were no test runs that were greater

5. Based on what I observed, the layer density has a significant impact as well as the number of epochs. Additionally, the activation functions used as well as the epsilon value has a large impact on the rate at which the model learns to land the lander and whether it generally progresses or degrades.

6. The epsilon value helps determine the balance between experimentation and "staying the course". Essentially it's a balance between picking the optimum known action or a random action to gain more information.

7. Q-Learning is a reinforcement learning algorithm that balances a positive feedback loop (agent action -> environment reward/punishment -> updated agent action) that balances the need for exploration and doing the best known action. The way this is done, is by using a Q-table which is comprised of the state:action pairs. This is initialized with all 0s for the Q-values and initially a random action is taken but as the agent moves through episodes, the table gets filled in more and more. The epsilon value helps dictate whether to follow the table directly or whether to take a random action, which is how Q-learning is able to balance discovering new information (the random action) and following known best practices (using the Q-table). 
