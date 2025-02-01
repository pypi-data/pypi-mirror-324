import logging
from dataclasses import dataclass
from typing import Generator, NamedTuple, Self

import numpy as np

log = logging.getLogger(__name__)


class Searcher(NamedTuple):
    """
    A class used to represent searching result
    """
    status: str
    """Search status ('tracking' or 'match')."""
    twd_min: float
    """The minimum time warping distance."""
    t_start: int
    """The start time index (0-based)."""
    t_end: int
    """The end time index (0-based)."""
    t: int
    """The time index of status (0-based)."""


@dataclass
class Spring:
    """
    A class used to represent a Spring object for time series analysis based on Time Warping Distance.
    """

    query_vector: np.ndarray
    """The query vector used for distance calculations."""
    epsilon: float
    """The epsilon value used for thresholding."""
    alpha: float = None
    """The smoothing factor for moving average calculations. If value is None aplpha will be equal 2 / (k + 1) where k is the number of past time steps in consideration of moving average. Defaults to None."""  # noqa: E501
    ddof: int = 0
    """The delta degrees of freedom for variance calculations. Defaults to 0."""
    distance_type: str = 'quadratic'
    """The type of distance calculation ('quadratic' or 'absolute'). Defaults to 'quadratic'."""
    use_z_norm: bool = False
    """Flag to indicate if z-score normalization should be used. Defaults to False."""

    def __post_init__(self):
        if self.query_vector.ndim != 1:
            raise ValueError("Query vector must be 1-dimensional.")

        self.query_vector_z_norm = (self.query_vector - np.mean(self.query_vector)) / np.std(self.query_vector)
        self.D = np.full((self.query_vector.shape[0]+1, 1), np.inf, dtype=np.float64)
        self.S = np.ones_like(self.D, dtype=np.int64)

        self.__t = 0
        self.d_min = np.inf
        self.t_start, self.t_end = self.__t, self.__t
        self.mean, self.variance = 0.0, 0.0
        self.M2 = 0.0
        self.__status = None
        self.__d_min_status = self.d_min
        self.__t_start_status = self.t_start
        self.__t_end_status = self.t_end

    @property
    def t(self) -> int:
        """
        The internal time step counter.

        Returns:
            int: The current time step.
        """
        return self.__t


    def distance(self, x: float) -> float:
        """
        Calculates the distance between the input value x and the query vector.

        The distance calculation method depends on the `distance_type` attribute of the Spring object.
        It can be either 'quadratic' or 'absolute'.

        Parameters:
            x (float): The input value for which the distance is calculated.

        Returns:
            float: The calculated distance.

        Raises:
            ValueError: If the `distance_type` is not 'quadratic' or 'absolute'.
        """
        query_vector = self.query_vector_z_norm if self.use_z_norm else self.query_vector

        match self.distance_type:
            case 'quadratic':
                return (x - query_vector) ** 2
            case 'absolute':
                return np.abs(x - query_vector)
            case _:
                raise ValueError("Invalid distance type.")

    def update_tick(self):
        """
        Increments the internal time step counter.
        """
        self.__t += 1

    def moving_average(self, x: float):
        """
        Updates the moving average of the input value x.

        Parameters:
            x (float): The input value used to update the moving average.
        """
        # 2 / (n + 1) for n-th element. Because self.update_trick() running before.
        alpha = self.alpha if self.alpha is not None else 2 / self.__t

        match self.__t:
            case 1:
                self.mean = x
            case _:
                self.mean = (1 - alpha) * self.mean + alpha * x

    def moving_variance(self, x: float) -> float:
        """
        Updates the online variance based on the input value x.

        Parameters:
            x (float): The input value used to update the variance.

        Returns:
            float: The updated variance.
        """
        delta = x - self.mean
        self.moving_average(x)
        delta2 = x - self.mean
        self.M2 += delta*delta2
        self.variance = self.M2 / (self.__t - self.ddof)

    def z_norm(self, x: float) -> float:
        """
        Normalizes the input value x using z-score normalization if enabled.

        Parameters:
            x (float): The input value to be normalized.

        Returns:
            float: The normalized value or NaN if variance is zero.
        """
        self.update_tick()
        if self.use_z_norm:
            self.moving_variance(x)
            return (x - self.mean) / np.sqrt(self.variance) if self.variance != 0 else np.nan
        return x

    def update_state(self, x: float) -> Self:
        """
        Updates the state of the Spring object based on the input value x.

        Parameters:
            x (float): The input value used to update the state.

        Returns:
            Spring: The updated Spring object.
        """
        match not np.isnan(x):
            case np.True_:
                new_column = np.hstack((0, self.distance(x)))[..., np.newaxis]
            case _:
                new_column = self.D[:, self.D.shape[1] - 1:]

        self.D = np.hstack((self.D, new_column))
        self.S = np.hstack((self.S, np.zeros_like(new_column, dtype=np.int64)))
        self.S[0, -1] = self.__t

        if np.isnan(x):
            return self

        for i in range(1, self.D.shape[0]):
            sub_d = np.copy(self.D[i-1:i+1, -2:])
            sub_d[1,1] = np.inf
            d_best = sub_d.min()
            self.D[i, -1] = self.D[i, -1] + d_best
            match sub_d[0, 1] == d_best, sub_d[1, 0] == d_best, sub_d[0, 0] == d_best:
                case np.True_, *_:
                    self.S[i, -1] = self.S[i-1, -1]
                case _, np.True_, _:
                    self.S[i, -1] = self.S[i, -2]
                case _, _, np.True_:
                    self.S[i, -1] = self.S[i - 1, -2]
        return self

    def search(self) -> Generator[Searcher, float, None]:
        """
        A generator method that yields a Searcher object and updates the state based on the input value.

        Yields:
            Searcher: An object containing the current status, minimum twd, start time index, end time index, and current time index of 'tracking' or 'match' status (All indexes are 0-based). 

        The method continues to update the state and yields Searcher objects until the generator is closed.
        """  # noqa: E501
        while True:
            x: float = yield Searcher(self.__status, float(self.__d_min_status), int(self.__t_start_status - 1),
                                      int(self.__t_end_status + 1), self.__t_end_status)
            self.update_state(self.z_norm(x))

            if self.d_min <= self.epsilon:
                if ((self.D[:, -1] >= self.d_min) | (self.S[:, -1] > self.t_end))[1:].all():
                    self.__status = 'match'
                    self.__d_min_status = self.d_min
                    self.__t_start_status = self.t_start
                    self.__t_end_status = self.t_end

                    self.d_min = np.inf
                    self.D[1:, -1] = np.where(self.S[1:, -1] <= self.t_end, np.inf, self.D[1:, -1])
            if self.D[-1, -1] <= self.epsilon and self.D[-1, -1] < self.d_min:
                self.d_min = self.D[-1, -1]
                self.t_start, self.t_end = int(self.S[-1, -1]), self.__t

                self.__status = 'tracking'
                self.__d_min_status = self.d_min
                self.__t_start_status = self.t_start
                self.__t_end_status = self.t_end

            self.D[0, -1] = np.inf
            self.D[:, -2] = self.D[:, -1]
            self.D = self.D[:, 0:self.D.shape[1] - 1]  # for column vector return
            self.S[:, -2] = self.S[:, -1]
            self.S = self.S[:, 0:self.S.shape[1] - 1]  # for column vector return
