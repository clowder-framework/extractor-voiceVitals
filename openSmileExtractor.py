#!/usr/bin/env python

"""Example extractor based on the clowder code."""

import logging
import os
from pyclowder.extractors import Extractor
import pyclowder.files
import pyclowder.datasets
import opensmile


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

        # These process messages will appear in the Clowder UI under Extractions.
        connector.message_process(resource, "Loading contents of file...")

        # Call actual program
        # Execute word count command on the input file and obtain the output
        smile = opensmile.Smile(
            feature_set=opensmile.FeatureSet.ComParE_2016,
            feature_level=opensmile.FeatureLevel.Functionals,
        )

        # 1. Create metadata dictionary
        y = smile.process_file(inputfile)

        m = y.to_dict('records')[0]
        result = {
            'audspec_lengthL1norm_sma_range': m['audspec_lengthL1norm_sma_range'],
            'audspec_lengthL1norm_sma_maxPos': m['audspec_lengthL1norm_sma_maxPos'],
            'audspec_lengthL1norm_sma_minPos': m['audspec_lengthL1norm_sma_minPos']
        }
        # connector.message_process(resource, "Found %s lines and %s words..." % (lines, words))

        # Store results as metadata
        metadata = self.get_metadata(result, 'file', file_id, host)

        # Normal logs will appear in the extractor log, but NOT in the Clowder UI.
        logger.debug(metadata)

        # Upload metadata to original file
        pyclowder.files.upload_metadata(connector, host, secret_key, file_id, metadata)

        # 2. store table as new file and upload
        original_filename = resource["name"]
        filename = os.path.splitext(original_filename)[0] + "_summary.csv"
        y.to_csv(filename, index=False)
        dataset_id = resource['parent'].get('id')
        pyclowder.files.upload_to_dataset(connector, host, secret_key, dataset_id, filename)

        # 3. store as preview
        pyclowder.files.upload_preview(connector, host, secret_key, file_id, filename)

        # 4. look around other files in the same dataset
        files_in_dataset = pyclowder.datasets.get_file_list(connector, host, secret_key, dataset_id)
        metadata_list = []
        for file in files_in_dataset:
            file_id = file["id"]
            metadata = pyclowder.files.download_metadata(connector, host, secret_key, file_id, extractor=None)
            metadata_list.append(metadata)

        # your own logic to parse the metdata and generate visualization
        preview_fname = batch_visualization(metadata_list)
        # pyclowder.files.upload_preview(connector, host, secret_key, file_id, preview_fname)
        # pyclowder.files.upload_to_dataset(connector, host, secret_key, dataset_id, preview_fname)


def batch_visualization(metadata_list,):
    # do something with your metadata
    print(metadata_list)
    preview_fname = "your_preview_fname.png"
    return preview_fname


if __name__ == "__main__":
    extractor = OpenSmileExtractor()
    extractor.start()

    # uncomment to test
# if __name__ == "__main__":
    # metadata_list= [
    #     [{'@context': ['https://clowder.ncsa.illinois.edu/contexts/metadata.jsonld', {}],
    #     'id': '62265872e4b09fbb1ccb7244',
    #   'attached_to': {'resource_type': 'cat:file', 'url': 'http://clowder:9000/files/62265870e4b09fbb1ccb723b'},
    #   'created_at': 'Mon Mar 07 19:09:38 GMT 2022',
    #   'agent': {'@type': 'cat:extractor', 'name': 'ncsa.openSmileExtractor',
    #             'extractor_id': 'http://clowder:9000/extractors/ncsa.openSmileExtractor/2.0'},
    #   'content': {'audspec_lengthL1norm_sma_range': 0.31050658226013184,
    #               'audspec_lengthL1norm_sma_maxPos': 0.34090909361839294,
    #               'audspec_lengthL1norm_sma_minPos': 0.9772727489471436}}],
    #     [],
    #     [{'@context': ['https://clowder.ncsa.illinois.edu/contexts/metadata.jsonld', {}],
    #       'id': '622656c1e4b09fbb18939969',
    #       'attached_to': {'resource_type': 'cat:file', 'url': 'http://clowder:9000/files/622656b5e4b09fbb189398aa'},
    #       'created_at': 'Mon Mar 07 19:02:25 GMT 2022',
    #       'agent': {'@type': 'cat:extractor', 'name': 'ncsa.openSmileExtractor',
    #                 'extractor_id': 'http://clowder:9000/extractors/ncsa.openSmileExtractor/1.0'},
    #       'content': {'audspec_lengthL1norm_sma_range': 0.31050658226013184,
    #                   'audspec_lengthL1norm_sma_maxPos': 0.34090909361839294,
    #                   'audspec_lengthL1norm_sma_minPos': 0.9772727489471436}},
    #      {'@context': ['https://clowder.ncsa.illinois.edu/contexts/metadata.jsonld', {}],
    #       'id': '622656c0e4b09fbb18939957',
    #       'attached_to': {'resource_type': 'cat:file', 'url': 'http://clowder:9000/files/622656b5e4b09fbb189398aa'},
    #       'created_at': 'Mon Mar 07 19:02:24 GMT 2022',
    #       'agent': {'@type': 'cat:extractor', 'name': 'ncsa.openSmileExtractor',
    #                 'extractor_id': 'http://clowder:9000/extractors/ncsa.openSmileExtractor/1.0'},
    #       'content': {'audspec_lengthL1norm_sma_range': 0.31050658226013184,
    #                   'audspec_lengthL1norm_sma_maxPos': 0.34090909361839294,
    #                   'audspec_lengthL1norm_sma_minPos': 0.9772727489471436}},
    #      {'@context': ['https://clowder.ncsa.illinois.edu/contexts/metadata.jsonld', {}],
    #       'id': '622656bfe4b09fbb18939945',
    #       'attached_to': {'resource_type': 'cat:file', 'url': 'http://clowder:9000/files/622656b5e4b09fbb189398aa'},
    #       'created_at': 'Mon Mar 07 19:02:23 GMT 2022',
    #       'agent': {'@type': 'cat:extractor', 'name': 'ncsa.openSmileExtractor',
    #                 'extractor_id': 'http://clowder:9000/extractors/ncsa.openSmileExtractor/1.0'},
    #       'content': {'audspec_lengthL1norm_sma_range': 0.31050658226013184,
    #                   'audspec_lengthL1norm_sma_maxPos': 0.34090909361839294,
    #                   'audspec_lengthL1norm_sma_minPos': 0.9772727489471436}},
    #      {'@context': ['https://clowder.ncsa.illinois.edu/contexts/metadata.jsonld', {}],
    #       'id': '622656bee4b09fbb18939933',
    #       'attached_to': {'resource_type': 'cat:file', 'url': 'http://clowder:9000/files/622656b5e4b09fbb189398aa'},
    #       'created_at': 'Mon Mar 07 19:02:22 GMT 2022',
    #       'agent': {'@type': 'cat:extractor', 'name': 'ncsa.openSmileExtractor',
    #                 'extractor_id': 'http://clowder:9000/extractors/ncsa.openSmileExtractor/1.0'},
    #       'content': {'audspec_lengthL1norm_sma_range': 0.31050658226013184,
    #                   'audspec_lengthL1norm_sma_maxPos': 0.34090909361839294,
    #                   'audspec_lengthL1norm_sma_minPos': 0.9772727489471436}},
    #      {'@context': ['https://clowder.ncsa.illinois.edu/contexts/metadata.jsonld', {}],
    #       'id': '622656bde4b09fbb18939921',
    #       'attached_to': {'resource_type': 'cat:file', 'url': 'http://clowder:9000/files/622656b5e4b09fbb189398aa'},
    #       'created_at': 'Mon Mar 07 19:02:21 GMT 2022',
    #       'agent': {'@type': 'cat:extractor', 'name': 'ncsa.openSmileExtractor',
    #                 'extractor_id': 'http://clowder:9000/extractors/ncsa.openSmileExtractor/1.0'},
    #       'content': {'audspec_lengthL1norm_sma_range': 0.31050658226013184,
    #                   'audspec_lengthL1norm_sma_maxPos': 0.34090909361839294,
    #                   'audspec_lengthL1norm_sma_minPos': 0.9772727489471436}},
    #      {'@context': ['https://clowder.ncsa.illinois.edu/contexts/metadata.jsonld', {}],
    #       'id': '622656bce4b09fbb1893990f',
    #       'attached_to': {'resource_type': 'cat:file', 'url': 'http://clowder:9000/files/622656b5e4b09fbb189398aa'},
    #       'created_at': 'Mon Mar 07 19:02:20 GMT 2022',
    #       'agent': {'@type': 'cat:extractor', 'name': 'ncsa.openSmileExtractor',
    #                 'extractor_id': 'http://clowder:9000/extractors/ncsa.openSmileExtractor/1.0'},
    #       'content': {'audspec_lengthL1norm_sma_range': 0.31050658226013184,
    #                   'audspec_lengthL1norm_sma_maxPos': 0.34090909361839294,
    #                   'audspec_lengthL1norm_sma_minPos': 0.9772727489471436}},
    #      {'@context': ['https://clowder.ncsa.illinois.edu/contexts/metadata.jsonld', {}],
    #       'id': '622656bbe4b09fbb189398fd',
    #       'attached_to': {'resource_type': 'cat:file', 'url': 'http://clowder:9000/files/622656b5e4b09fbb189398aa'},
    #       'created_at': 'Mon Mar 07 19:02:19 GMT 2022',
    #       'agent': {'@type': 'cat:extractor', 'name': 'ncsa.openSmileExtractor',
    #                 'extractor_id': 'http://clowder:9000/extractors/ncsa.openSmileExtractor/1.0'},
    #       'content': {'audspec_lengthL1norm_sma_range': 0.31050658226013184,
    #                   'audspec_lengthL1norm_sma_maxPos': 0.34090909361839294,
    #                   'audspec_lengthL1norm_sma_minPos': 0.9772727489471436}},
    #      {'@context': ['https://clowder.ncsa.illinois.edu/contexts/metadata.jsonld', {}],
    #       'id': '622656bae4b09fbb189398ea',
    #       'attached_to': {'resource_type': 'cat:file', 'url': 'http://clowder:9000/files/622656b5e4b09fbb189398aa'},
    #       'created_at': 'Mon Mar 07 19:02:18 GMT 2022',
    #       'agent': {'@type': 'cat:extractor', 'name': 'ncsa.openSmileExtractor',
    #                 'extractor_id': 'http://clowder:9000/extractors/ncsa.openSmileExtractor/1.0'},
    #       'content': {'audspec_lengthL1norm_sma_range': 0.31050658226013184,
    #                   'audspec_lengthL1norm_sma_maxPos': 0.34090909361839294,
    #                   'audspec_lengthL1norm_sma_minPos': 0.9772727489471436}},
    #      {'@context': ['https://clowder.ncsa.illinois.edu/contexts/metadata.jsonld', {}],
    #       'id': '622656b9e4b09fbb189398d8',
    #       'attached_to': {'resource_type': 'cat:file', 'url': 'http://clowder:9000/files/622656b5e4b09fbb189398aa'},
    #       'created_at': 'Mon Mar 07 19:02:17 GMT 2022',
    #       'agent': {'@type': 'cat:extractor', 'name': 'ncsa.openSmileExtractor',
    #                 'extractor_id': 'http://clowder:9000/extractors/ncsa.openSmileExtractor/1.0'},
    #       'content': {'audspec_lengthL1norm_sma_range': 0.31050658226013184,
    #                   'audspec_lengthL1norm_sma_maxPos': 0.34090909361839294,
    #                   'audspec_lengthL1norm_sma_minPos': 0.9772727489471436}},
    #      {'@context': ['https://clowder.ncsa.illinois.edu/contexts/metadata.jsonld', {}],
    #       'id': '622656b8e4b09fbb189398c7',
    #       'attached_to': {'resource_type': 'cat:file', 'url': 'http://clowder:9000/files/622656b5e4b09fbb189398aa'},
    #       'created_at': 'Mon Mar 07 19:02:16 GMT 2022',
    #       'agent': {'@type': 'cat:extractor', 'name': 'ncsa.openSmileExtractor',
    #                 'extractor_id': 'http://clowder:9000/extractors/ncsa.openSmileExtractor/1.0'},
    #       'content': {'audspec_lengthL1norm_sma_range': 0.31050658226013184,
    #                   'audspec_lengthL1norm_sma_maxPos': 0.34090909361839294,
    #                   'audspec_lengthL1norm_sma_minPos': 0.9772727489471436}},
    #      {'@context': ['https://clowder.ncsa.illinois.edu/contexts/metadata.jsonld', {}],
    #       'id': '622656b6e4b09fbb189398b4',
    #       'attached_to': {'resource_type': 'cat:file', 'url': 'http://clowder:9000/files/622656b5e4b09fbb189398aa'},
    #       'created_at': 'Mon Mar 07 19:02:14 GMT 2022',
    #       'agent': {'@type': 'cat:extractor', 'name': 'ncsa.openSmileExtractor',
    #                 'extractor_id': 'http://clowder:9000/extractors/ncsa.openSmileExtractor/1.0'},
    #       'content': {'audspec_lengthL1norm_sma_range': 0.31050658226013184,
    #                   'audspec_lengthL1norm_sma_maxPos': 0.34090909361839294,
    #                   'audspec_lengthL1norm_sma_minPos': 0.9772727489471436}}]
    # ]
    #
    # batch_visualization(metadata_list)
