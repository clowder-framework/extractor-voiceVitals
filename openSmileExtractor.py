import opensmile


def openSmileExtractor(input_file_path):
    """
    Easist example that stores the extraction as a metadata

    :param input_file_path: Full path to the input file
    :return: Result dictionary containing metadata about lines, words, and characters in the input file
    """

    # Execute word count command on the input file and obtain the output
    smile = opensmile.Smile(
        feature_set=opensmile.FeatureSet.ComParE_2016,
        feature_level=opensmile.FeatureLevel.Functionals,
    )

    # Create metadata dictionary
    metadata = smile.process_file(input_file_path).to_dict()

    # Store metadata in result dictionary
    result = {
        'metadata': metadata
    }

    # Return the result dictionary
    return result


if __name__ == "__main__":
    result = openSmileExtractor("test/302_AUDIO_2.wav")
    print(result["metadata"].keys())