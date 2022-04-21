#!/usr/bin/env python

"""Example extractor based on the clowder code."""

import logging
import os
from pyclowder.extractors import Extractor
import pyclowder.files
import pyclowder.datasets
import opensmile
from datetime import datetime


class OpenSmileExtractor(Extractor):
    """Count the number of characters, words and lines in a text file."""
    def __init__(self):
        Extractor.__init__(self)

        # add any additional arguments to parser
        # self.parser.add_argument('--max', '-m', type=int, nargs='?', default=-1,
        #                          help='maximum number (default=-1)')

        # parse command line and load default logging configuration
        self.setup()

        # setup logging for the exctractor
        logging.getLogger('pyclowder').setLevel(logging.DEBUG)
        logging.getLogger('__main__').setLevel(logging.DEBUG)

    def process_message(self, connector, host, secret_key, resource, parameters):
        # Process the file and upload the results
        # uncomment to see the resource
        # print(resource)

        logger = logging.getLogger(__name__)
        inputfile = resource["local_paths"][0]
        file_id = resource['id']
        dataset_id = resource['parent'].get('id')

        # These process messages will appear in the Clowder UI under Extractions.
        connector.message_process(resource, "Loading contents of file...")

        # # Call actual program
        # # Execute word count command on the input file and obtain the output
        # smile = opensmile.Smile(
        #     feature_set=opensmile.FeatureSet.ComParE_2016,
        #     feature_level=opensmile.FeatureLevel.Functionals,
        # )

        # ##############################################
        # # 1. Create metadata dictionary
        # y = smile.process_file(inputfile)
        # 
        # m = y.to_dict('records')[0]
        # result = {
        #     'audspec_lengthL1norm_sma_range': m['audspec_lengthL1norm_sma_range'],
        #     'audspec_lengthL1norm_sma_maxPos': m['audspec_lengthL1norm_sma_maxPos'],
        #     'audspec_lengthL1norm_sma_minPos': m['audspec_lengthL1norm_sma_minPos']
        # }
        # # connector.message_process(resource, "Found %s lines and %s words..." % (lines, words))
        # 
        # # Store results as metadata
        # metadata = self.get_metadata(result, 'file', file_id, host)
        # 
        # # Normal logs will appear in the extractor log, but NOT in the Clowder UI.
        # logger.debug(metadata)
        # 
        # # Upload metadata to original file
        # pyclowder.files.upload_metadata(connector, host, secret_key, file_id, metadata)

        # ##############################################
        # # 2. store table as new file and upload
        # original_filename = resource["name"]
        # filename = os.path.splitext(original_filename)[0] + "_summary.csv"
        # y.to_csv(filename, index=False)
        # dataset_id = resource['parent'].get('id')
        # pyclowder.files.upload_to_dataset(connector, host, secret_key, dataset_id, filename)

        # ##############################################
        # # 3. store as preview
        # pyclowder.files.upload_preview(connector, host, secret_key, file_id, filename)

        ##############################################
        # 4. look around other files in the same dataset
        files_in_dataset = pyclowder.datasets.get_file_list(connector, host, secret_key, dataset_id)

        ##############################################
        # # 5. download and manipulate metadata
        # metadata_list = []
        # for file in files_in_dataset:
        #     file_id = file["id"]
        #     metadata = pyclowder.files.download_metadata(connector, host, secret_key, file_id, extractor=None)
        #     metadata_list.append(metadata)

        # ##############################################
        # # 6. add  your own logic to parse the metadata and generate visualization
        # # pyclowder.files.upload_preview(connector, host, secret_key, file_id, preview_fname)
        # # pyclowder.files.upload_to_dataset(connector, host, secret_key, dataset_id, preview_fname)

        ##############################################
        # # 7. overwrite the same file
        # overwrite_fname = "file_to_overwrite.txt"
        # # create a dummy overwrite file
        # with open(overwrite_fname, 'w') as f:
        #     curDT = datetime.now()
        #     f.write(curDT.strftime("%H:%M:%S"))
        # for file in files_in_dataset:
        #     if file["filename"] == overwrite_fname:
        #         # delete old one
        #         url = '%sapi/files/%s?key=%s' % (host, file["id"], secret_key)
        #         result = connector.delete(url, verify=connector.ssl_verify if connector else True)
        # # post new one
        # pyclowder.files.upload_to_dataset(connector, host, secret_key, dataset_id, overwrite_fname)

        ##############################################
        # 8. list files in a folder


if __name__ == "__main__":
    extractor = OpenSmileExtractor()
    extractor.start()