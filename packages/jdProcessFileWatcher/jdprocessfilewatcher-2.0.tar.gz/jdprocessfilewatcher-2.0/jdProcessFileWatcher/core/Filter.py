from ..Types import FileChangedData
from ..FileAction import FileAction
import collections


class FilterBase:
    def check_data(self, data: FileChangedData) -> bool:
        raise NotImplementedError()


class PathFilter(FilterBase):
    def __init__(self, path: str) -> None:
        super().__init__()

        self._path = path

    def check_data(self, data: FileChangedData) -> bool:
        return self._path.lower() in data.path.lower()


class ActionFilter(FilterBase):
    def __init__(self, action: FileAction) -> None:
        super().__init__()

        self._action = action

    def check_data(self, data: FileChangedData) -> bool:
        return data.action == self._action


class ProcessFilter(FilterBase):
    def __init__(self, pid: int | None) -> None:
        super().__init__()

        self._pid = pid

    def check_data(self, data: FileChangedData) -> bool:
        return data.pid == self._pid


class FilterList(collections.UserList[FilterBase]):
    def __init__(self) -> None:
        super().__init__()

    def check_data(self, data: FileChangedData) -> bool:
        for filter in self:
            if not filter.check_data(data):
                return False
        return True

    def filter_list(self, data_list: list[FileChangedData]) -> list[FileChangedData]:
        if len(self) == 0:
            return data_list

        filtered_list: list[FileChangedData] = []

        for data in data_list:
            for filter in self:
                if not filter.check_data(data):
                    break
            else:
                filtered_list.append(data)

        return filtered_list
