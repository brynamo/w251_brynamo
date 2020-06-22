## Section 1 Questions:
1. In the time allowed, how many images did you annotate?
  1. I was able to annotate all images in the 3 hour window
2. Home many instances of the Millennium Falcon did you annotate? How many TIE Fighters?
  2. Roughly 281 Millennium Falcon and 185 TIE annotations.
3. Based on this experience, how would you handle the annotation of large image data set?
  3. I think it would be helpful to train a smaller set, then leverage a network to support additional labels (with human validation). Alternatively Mechanical Turk would be helpful, but there is an issue potentially with data quality.
4. Think about image augmentation? How would augmentations such as flip, rotation, scale, cropping, and translation effect the annotations?
  4. They would need to be re-annotated


## Section 2 Questions:
Describe the following augmentations in your own words
1. Flip - There are two types (horizontal and vertical) they each flip the image against the opposite axis (i.e. horisontal flips on the vertical axis).
2. Rotation - This rotates the image as if you were spinning an actual image.
3. Scale - Scaling is increasing the size of the image and can be combined with a crop to create a new one
4. Crop - This is cutting an image down to a specific dimension
5. Translation - This is moving the image within it's view window so that some features are no longer visible and others are in a different location
6. Noise - This adds image noise (small pixes that are the wrong color and intensity) to the image making it less clear.


## Section 3 Questions:
1. Image annotations require the coordinates of the objects and their classes; in your option, what is needed for an audio annotation?
    1. You need when the item of interest started and when it ended. You also need to know movement (is it close/far, coming/going). Also it would be important to know the source of the sound (human, machine, etc.). There is a lot of information that would be helpful in annotation that is not always so clear cut.