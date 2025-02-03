import os
from data_reader.sample import Sample
import polars as pl


class SampleRepository:
    """
    Acts as a repository for samples. It scans a base folder for sample folders,
    creates Sample objects, and provides querying methods.
    """

    def __init__(self, base_path: str, thresholded_subfolder: str = "thresholded_images"):
        """
        :param base_path: Absolute path to the folder that contains sample folders.
        :param thresholded_subfolder: Name of the image subfolder inside each sample folder.
        """
        self.base_path = base_path
        self.thresholded_subfolder = thresholded_subfolder
        self._all_samples = []  # a list of Sample objects for each found sample folder
        self._active_samples = []  # a filtered list (by default, all samples)
        self._load_samples()

    def _load_samples(self):
        """
        Scans the base directory for subfolders that contain a parquet file
        following the convention "<sample_name>_results.parquet".
        """
        for entry in os.listdir(self.base_path):
            sample_folder = os.path.join(self.base_path, entry)
            if os.path.isdir(sample_folder):
                parquet_file = os.path.join(sample_folder, f"{entry}_results.parquet")
                if os.path.exists(parquet_file):
                    sample = Sample(self.base_path, entry, self.thresholded_subfolder)
                    self._all_samples.append(sample)
        self._active_samples = list(self._all_samples)

    def limit_to(self, *sample_names):
        """
        Limits the repository to only samples whose name is in the specified list.
        Returns self to allow method chaining.

        :param sample_names: List of sample names (strings) to keep active.
        """
        sample_names_set = set(sample_names)
        self._active_samples = [s for s in self._all_samples if s.sample_name in sample_names_set]
        return self

    def reset_filter(self):
        """
        Resets any filtering so that all samples become active again.
        Returns self to allow method chaining.
        """
        self._active_samples = list(self._all_samples)
        return self

    def contour_for_temperature(self, temperature: float):
        """
        Iterates over the active samples and returns a dictionary with
        sample names as keys and contour coordinates (list of (x,y) points)
        as values for samples with Temperature > threshold.

        :param temperature: Temperature threshold.
        :return: dict {sample_name: contour_coordinates}
        """
        contours = {}
        for sample in self._active_samples:
            contour = sample.get_contour_for_temperature(temperature)
            if contour is not None:
                contours[sample.sample_name] = contour
        return contours

    def dataframes(self) -> dict:
        """
        Returns a dictionary with keys as sample names and values as
        the corresponding Polars DataFrame.

        :return: dict {sample_name: DataFrame}
        """
        dfs = {}
        for sample in self._active_samples:
            dfs[sample.sample_name] = sample.get_dataframe()
        return dfs