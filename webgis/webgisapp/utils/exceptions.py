class IncorrectOptionException(Exception):
    "Exception for incorrect option introduction"

    def __init__(self, message="Option invalid"):
        super().__init__(self, message)


class EmptyVarException(Exception):
    "Exception for an empty variable"

    def __init__(self, message="Empty value"):
        super().__init__(self, message)


class InstanceTypeException(Exception):
    "Exception for an object with different type of instance"

    def __init__(self, message="Instance is incorrect"):
        super().__init__(self, message)


class EmptySpecieException(Exception):
    "Exception for an empty specie"

    def __init__(self, message="Empty Specie"):
        super().__init__(self, message)


class QueryTypeException(Exception):
    "Exception for an different query set type"

    def __init__(self, message="Different query type"):
        super().__init__(self, message)


class DateRangeException(Exception):
    "Exception when there is no range of dates"

    def __init__(self, message="There is no range of dates"):
        super().__init__(self, message)
