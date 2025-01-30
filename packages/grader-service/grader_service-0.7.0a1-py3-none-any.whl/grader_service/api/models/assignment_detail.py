from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from grader_service.api.models.base_model import Model
from grader_service.api.models.assignment_settings import AssignmentSettings
from grader_service.api.models.submission import Submission
from grader_service.api import util

from grader_service.api.models.assignment_settings import AssignmentSettings  # noqa: E501
from grader_service.api.models.submission import Submission  # noqa: E501

class AssignmentDetail(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, id=None, name=None, settings=None, status=None, points=None, submissions=None):  # noqa: E501
        """AssignmentDetail - a model defined in OpenAPI

        :param id: The id of this AssignmentDetail.  # noqa: E501
        :type id: int
        :param name: The name of this AssignmentDetail.  # noqa: E501
        :type name: str
        :param settings: The settings of this AssignmentDetail.  # noqa: E501
        :type settings: AssignmentSettings
        :param status: The status of this AssignmentDetail.  # noqa: E501
        :type status: str
        :param points: The points of this AssignmentDetail.  # noqa: E501
        :type points: float
        :param submissions: The submissions of this AssignmentDetail.  # noqa: E501
        :type submissions: List[Submission]
        """
        self.openapi_types = {
            'id': int,
            'name': str,
            'settings': AssignmentSettings,
            'status': str,
            'points': float,
            'submissions': List[Submission]
        }

        self.attribute_map = {
            'id': 'id',
            'name': 'name',
            'settings': 'settings',
            'status': 'status',
            'points': 'points',
            'submissions': 'submissions'
        }

        self._id = id
        self._name = name
        self._settings = settings
        self._status = status
        self._points = points
        self._submissions = submissions

    @classmethod
    def from_dict(cls, dikt) -> 'AssignmentDetail':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The AssignmentDetail of this AssignmentDetail.  # noqa: E501
        :rtype: AssignmentDetail
        """
        return util.deserialize_model(dikt, cls)

    @property
    def id(self) -> int:
        """Gets the id of this AssignmentDetail.


        :return: The id of this AssignmentDetail.
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id: int):
        """Sets the id of this AssignmentDetail.


        :param id: The id of this AssignmentDetail.
        :type id: int
        """

        self._id = id

    @property
    def name(self) -> str:
        """Gets the name of this AssignmentDetail.


        :return: The name of this AssignmentDetail.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name: str):
        """Sets the name of this AssignmentDetail.


        :param name: The name of this AssignmentDetail.
        :type name: str
        """

        self._name = name

    @property
    def settings(self) -> AssignmentSettings:
        """Gets the settings of this AssignmentDetail.


        :return: The settings of this AssignmentDetail.
        :rtype: AssignmentSettings
        """
        return self._settings

    @settings.setter
    def settings(self, settings: AssignmentSettings):
        """Sets the settings of this AssignmentDetail.


        :param settings: The settings of this AssignmentDetail.
        :type settings: AssignmentSettings
        """

        self._settings = settings

    @property
    def status(self) -> str:
        """Gets the status of this AssignmentDetail.


        :return: The status of this AssignmentDetail.
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status: str):
        """Sets the status of this AssignmentDetail.


        :param status: The status of this AssignmentDetail.
        :type status: str
        """
        allowed_values = ["created", "pushed", "released", "complete"]  # noqa: E501
        if status not in allowed_values:
            raise ValueError(
                "Invalid value for `status` ({0}), must be one of {1}"
                .format(status, allowed_values)
            )

        self._status = status

    @property
    def points(self) -> float:
        """Gets the points of this AssignmentDetail.


        :return: The points of this AssignmentDetail.
        :rtype: float
        """
        return self._points

    @points.setter
    def points(self, points: float):
        """Sets the points of this AssignmentDetail.


        :param points: The points of this AssignmentDetail.
        :type points: float
        """

        self._points = points

    @property
    def submissions(self) -> List[Submission]:
        """Gets the submissions of this AssignmentDetail.


        :return: The submissions of this AssignmentDetail.
        :rtype: List[Submission]
        """
        return self._submissions

    @submissions.setter
    def submissions(self, submissions: List[Submission]):
        """Sets the submissions of this AssignmentDetail.


        :param submissions: The submissions of this AssignmentDetail.
        :type submissions: List[Submission]
        """

        self._submissions = submissions
