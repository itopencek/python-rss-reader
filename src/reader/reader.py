class Reader:
    """
    Abstract class to read data from specific source and then returning it.
    """
    def read(self, src):
        """
        Reads data from source, which it then returns.

        :param src: source to read data from
        :return: read data
        """
        pass