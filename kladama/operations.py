import abc
from abc import ABC
import json


# Operations

class Operation(ABC):

    @property
    @abc.abstractmethod
    def url_path(self) -> str:
        pass


class PostOperation(Operation, ABC):

    @property
    @abc.abstractmethod
    def post_obj(self):
        pass


class PutOperation(Operation, ABC):

    @property
    @abc.abstractmethod
    def put_obj(self):
        pass


class CreateOperation(Operation, ABC):

    def __init__(self):
        Operation.__init__(self)


class DeleteOperation(Operation, ABC):
    pass


class CreateAreaOfInterestOperation(CreateOperation, PutOperation):

    def __init__(
        self,
        user,
        aoi_id,
        name,
        category,
        features
    ):
        CreateOperation.__init__(self)
        PutOperation.__init__(self)
        self._user = user
        self._aoi_id = aoi_id
        self._name = name
        self._category = category
        self._features = features

    @property
    def url_path(self):
        return "/aoi/user/{0}/{1}".format(self._user, self._aoi_id)

    @property
    def put_obj(self):
        return {
            "name": self._name,
            "category": self._category,
            "features": self._features if isinstance(self._features, str) else json.dumps(self._features)
        }


class CreatePeriodicSubscriptionOperation(CreateOperation, PostOperation):

    def __init__(
        self,
        user,
        variable_name,
        variable_source_name,
        spatial_operation_name,
        aoi_name,
    ):
        CreateOperation.__init__(self)
        PostOperation.__init__(self)
        self._user = user
        self._variable_name = variable_name
        self._variable_source_name = variable_source_name
        self._spatial_operation_name = spatial_operation_name
        self._aoi_name = aoi_name

    @property
    def url_path(self):
        return "/subsc/user/{0}".format(self._user)

    @property
    def post_obj(self):
        return {
            "type": "PERIODIC",
            "variable": {
                "name": self._variable_name,
                "source": {
                    "name": self._variable_source_name
                }
            },
            "spatialOper": {
                "name": self._spatial_operation_name
            },
            "aoi": {
                "name": self._aoi_name
            }
        }


class DeleteAreaOfInterestOperation(DeleteOperation):

    def __init__(self, user, aoi_id):
        DeleteOperation.__init__(self)
        self._user = user
        self._aoi_id = aoi_id

    @property
    def url_path(self) -> str:
        return "/aoi/user/{0}/{1}".format(self._user, self._aoi_id)


class DeleteSubscriptionOperation(DeleteOperation):

    def __init__(self, user, subscription_id):
        DeleteOperation.__init__(self)
        self._user = user
        self._subscription_id = subscription_id

    @property
    def url_path(self) -> str:
        return "/subsc/user/{0}/{1}".format(self._user, self._subscription_id)


# Builders

class OperationBuilder(ABC):

    @abc.abstractmethod
    def build(self) -> Operation:
        pass


class CreateAreaOfInterestBuilder(OperationBuilder):

    def __init__(self, user, aoi_id):
        OperationBuilder.__init__(self)
        self._user = user
        self._aoi_id = aoi_id
        self._name = ""
        self._category = ""
        self._features = {}

    def build(self) -> CreateAreaOfInterestOperation:
        return CreateAreaOfInterestOperation(
            self._user,
            self._aoi_id,
            self._name,
            self._category,
            self._features
        )

    def set_name(self, name: str):
        self._name = name
        return self

    def set_category(self, category: str):
        self._category = category
        return self

    def set_features(self, features):
        self._features = features
        return self


class CreatePeriodicSubscriptionBuilder(OperationBuilder):

    def __init__(self, user):
        OperationBuilder.__init__(self)
        self._user = user
        self._subscription_type = ""
        self._variable_name = ""
        self._variable_source_name = ""
        self._spatial_operation_name = ""
        self._aoi_name = ""

    def build(self) -> CreatePeriodicSubscriptionOperation:
        return CreatePeriodicSubscriptionOperation(
            self._user,
            self._variable_name,
            self._variable_source_name,
            self._spatial_operation_name,
            self._aoi_name,
        )

    def set_variable_name(self, variable_name: str):
        self._variable_name = variable_name
        return self

    def set_variable_source_name(self, variable_source_name: str):
        self._variable_source_name = variable_source_name
        return self

    def set_spatial_operation_name(self, spatial_operation_name: str):
        self._spatial_operation_name = spatial_operation_name
        return self

    def set_aoi_name(self, aoi_name: str):
        self._aoi_name = aoi_name
        return self


class DeleteAreaOfInterestBuilder(OperationBuilder):

    def __init__(self, user):
        OperationBuilder.__init__(self)
        self._user = user
        self._aoi_id = ""

    def build(self) -> DeleteAreaOfInterestOperation:
        return DeleteAreaOfInterestOperation(self._user, self._aoi_id)

    def set_area_of_interest_id(self, aoi_id: str):
        self._aoi_id = aoi_id
        return self


class DeleteSubscriptionBuilder(OperationBuilder):

    def __init__(self, user):
        OperationBuilder.__init__(self)
        self._user = user
        self._subscription_id = ""

    def build(self) -> DeleteSubscriptionOperation:
        return DeleteSubscriptionOperation(self._user, self._subscription_id)

    def set_subscription_id(self, subscription_id: str):
        self._subscription_id = subscription_id
        return self
