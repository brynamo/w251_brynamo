# HW9 Questions + Answers:

1. How long does it take to complete the training run? (hint: this session is on distributed training, so it will take a while)
  * This took roughly 24 hours on P100s.
2. Do you think your model is fully trained? How can you tell?
  * I think that the model is trained as well as it will be given the current parameters. The reason I believe this is because the eval loss and BLEU Score was not changing significantly and was wondering near it's optimal (a little above before returning down).
3. Were you overfitting?
  * I don't think it was overfitting because the BLEU score was not higher than .4 after an initial high score.
4. Were your GPUs fully utilized?
  * No they were not, and generally had around 62% free.
5. Did you monitor network traffic (hint: apt install nmon ) ? Was network the bottleneck?
  * Looking at network traffic, I would expect this to be the bottleneck because they were constantly near peak I/O.
6. Take a look at the plot of the learning rate and then check the config file. Can you explan this setting?
  * Looking at the learning rate, it started off relatively high (1.00e-3) before decaying to around (4.000e-4). This changed with each step and is because of the Adam optimizer. This is allow for the learning rate to change over time so that the model does not overshoot the global minimum the further into the training. This is an optimization that allows for rapid learning early and then more delicate learning later.
7. How big was your training set (mb)? How many training lines did it contain?
  *  The training set was 664Mb for German and 593Mb for English. There were 9049736 sentences based on output from `trainer_interface.cc` (`/sentencepiece/src/trainer_interface.cc(406) LOG(INFO) Done! preprocessed 9049736 sentences.
`).
8. What are the files that a TF checkpoint is comprised of?
  * They are comprised of the exact values of all parameters, the `tf.Variable` objects that the model is using. It does not contain any information about the computation defined by the model.
9. How big is your resulting model checkpoint (mb)?
  * The checkpoint was 730+Mb.
10. Remember the definition of a "step". How long did an average step take?
  * The average step was about 300ms with roughly 1000 steps every 5 min.
11. How does that correlate with the observed network utilization between nodes?
  * The network utilization was rather constant, and the average step length was also quite constant which would imply that these two are connected, especially considering the fact that the memory usage was under 50%.
