"""
file_faker.py
=============

Holds the FileFaker class for building example files.

"""


class FileFaker(object):
    """

    """

    def __init__(self, project, dataset_id, constraints=None, base_dir="fakedata"):
        """

        :param project:
        :param dataset_id:
        :param constraints:
        :param base_dir:
        """

    def _load_options(self):
        """

        :return:
        """
        # Check constraints and options

    def generate(self, constraints=None, max_num=None, randomise=False):
        """
        Generator to return the next file path based on an optional set of `constraints`.
        Specifying `max_num` will return after yielding the number given.
        Setting `randomise` to True will return them in a random order.

        :param constraints:
        :param max_num:
        :param randomise:
        :return:
        """
        self._update_constraints(constraints)

    def _update_constraints(self, constraints):
        """

        :param constraints:
        :return:
        """

    def _get_next_path(self):
        """

        :return:
        """
        # Yields next path
        # use itertools.product here