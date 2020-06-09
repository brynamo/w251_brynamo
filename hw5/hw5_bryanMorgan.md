# HW 5 for w251

## Questions:

1. What is TensorFlow? Which company is the leading contributor to TensorFlow?
    - TensorFlow is a deep learning framework, published by Google and allows for E2E training of models. The main contributor is Google.
2. What is TensorRT? How is it different from TensorFlow?
    - TensorRT is an SDK for leveraging GPU training and optimizing deep learning inference. These two are different because TensorFlow is a full E2E ecosystem that allows for DL model creation while TensorRT is focused on inference optimization with GPUs at run time. Essentially, TensorRT supports and optimizes models built in TensorFlow.
3. What is ImageNet? How many images does it contain? How many classes?
    - ImageNet is a research project that supplies different corpus of "meaningful concepts" based on WordNet. Essentially it is a DB of images that can be used in research projects for CV training. There are +14 million images, with 21,841 categories.
4. Please research and explain the differences between MobileNet and GoogleNet (Inception) architectures.
    - MobileNet is an optimized tranditional CNN that is designed to run on mobile devices. Conversely, GoogleNet/Inception has a different architecture that creates multiple different transformations from an input map and concatenates them into a single output.
5. In your own words, what is a bottleneck?
    - A bottleneck is often a specific process that requires significant and sometimes intractable computation cost. Additionally, a bottleneck cannot be paralallelized, meaning it impacts the E2E performance of the process in question.
6. How is a bottleneck different from the concept of layer freezing?
    - A bottleneck layer is used to compress features into smaller dimensional space which limits the number of features and associated weights that need to be updated/calculated. Layer freezing on the other hand is the process of "freezing" (no longer updating) hidden layers so that they do not need to be updated for each epoch. This also assists in decreasing computation cost as the networks are trained.
7. In the TF1 lab, you trained the last layer (all the previous layers retain their already-trained state). Explain how the lab used the previous layers (where did they come from? how were they used in the process?)
    - This is tranfer learning, and we are using a model that has already been trained on a related problem and using that for the first layers to create features that will be useful for our classification at the ened, while retraining the fully connected layer at the end for our retrained model to do the flower discrimination.
8. How does a low --learning_rate (step 7 of TF1) value (like 0.005) affect the precision? How much longer does training take?
    - By decreasing the learning rate, we increase the amount of time significantly, it also increases precision.
9. How about a --learning_rate (step 7 of TF1) of 1.0? Is the precision still good enough to produce a usable graph?
    - This was "good enogh" in some situations (like this learning exercise), but in other contexts such as cancer detection it does not have the precision we would require. It really depends on the problem at hand.
10. For step 8, you can use any images you like. Pictures of food, people, or animals work well. You can even use ImageNet images. How accurate was your model? Were you able to train it using a few images, or did you need a lot?
    - The model was more accurate with the more images it was given, but you could get something working with roughly 30 per category.
11. Run the TF1 script on the CPU (see instructions above) How does the training time compare to the default network training (section 4)? Why?
    - It is slower with just the CPU. This is because GPUs are well designed for large matrix operations which is what is required for training the tensorflow model.
12. Try the training again, but this time do export ARCHITECTURE="inception_v3" Are CPU and GPU training times different?
    - The different seemed more extreme, which makes sense considering the additional complexity with the inception_v3 architecture.
13. Given the hints under the notes section, if we trained Inception_v3, what do we need to pass to replace ??? below to the label_image script? Can we also glean the answer from examining TensorBoard?
    - We need to put in --input_layer="input" --input_height=299 --input_width=299



