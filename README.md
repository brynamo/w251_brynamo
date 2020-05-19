# w251_brynamo

HW3 Notes:
### Links
- Repo w/ HW3 scripts: https://github.com/brynamo/w251_brynamo
- Images SQL URL: cos://us-geo/hw3-output-images

### Notes
- Ran 2 mosquitto brokers with basic config
- Used alpine containers for all mosquitto related things
- Used cuda container for img processing
- Used ubuntu to save images to receive and upload to COS
- QoS was set to 2 because we were not sending too many images and so wanted to focus on sending exactly 1. If we were running this for a longer period of time or had this out in the field I would have selected 0 because we do not need TOO many photos of a person's face.
