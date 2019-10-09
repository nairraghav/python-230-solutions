

class StreamProcessor(object):
    """
    The StreamProcess class takes in a stream and has a process method that
    will analyze the numbers every 2 digits.
    """

    def __init__(self, stream):
        self._stream = stream

    def process(self):
        """
        This function reads the numbers from the stream for every 2 digits and
        adds them to a sum. If the sum is greater than 200, we return how many
        numbers were added. We max out at a count of 10.
        :return: int
        """

        count = 0  # How many two-digit numbers `process` method has added
        total = 0  # The running total of sums.

        # we keep looping until we hit 10 additions or a total > 200
        while (count < 10) and (total < 200):
            # read in the two digit stream
            digits = self._stream.read(2)
            # this case occurs when we are at the end of the stream
            if len(digits) < 2:
                break

            # we check to make sure can convert to an int
            try:
                digits = int(digits)
            except ValueError:
                break

            total += int(digits)
            count += 1

        # after the loop ends, we return the count
        return count
