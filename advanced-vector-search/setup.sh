#!/bin/bash
# these scripts will contain everything that needs to be run before the example
# downloading data, model, preprocessing etc.
bash ./get_data.sh siftsmall && \
rm -rf workspace && \
bash ./generate_training_data.sh