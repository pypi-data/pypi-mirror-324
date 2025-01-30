from PyQt6.QtCore import QCoreApplication
from ..FileAction import FileAction
from ..Types import FileChangedData
import xml.etree.ElementTree as ET
import json
import csv


class ExporterBase:
    def get_id(self) -> str:
        raise NotImplementedError()

    def get_name(self) -> str:
        raise NotImplementedError()

    def get_file_filter(self) -> str:
        raise NotImplementedError()

    def export_data(path: str, data_list: list[FileChangedData]) -> None:
        raise NotImplementedError()


class CsvExporter(ExporterBase):
    def get_id(self) -> str:
        return "csv"

    def get_name(self) -> str:
        return "CSV"

    def get_file_filter(self) -> str:
        return QCoreApplication.translate("Exporter", "CSV files") + " (*.csv)"

    def export_data(self, path: str, data_list: list[FileChangedData]) -> None:
        with open(path, "w", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames = ["Action", "Time", "Path", "PID", "Process"])
            writer.writeheader()

            for current_data in data_list:
                writer.writerow({
                    "Action": FileAction.get_internal_name(current_data.action),
                    "Time": current_data.time.isoformat(),
                    "Path": current_data.path,
                    "PID": current_data.pid,
                    "Process": current_data.process_name
                })


class JsonExporter(ExporterBase):
    def get_id(self) -> str:
        return "json"

    def get_name(self) -> str:
        return "JSON"

    def get_file_filter(self) -> str:
        return QCoreApplication.translate("Exporter", "JSON files") + " (*.json)"

    def export_data(self, path: str, data_list: list[FileChangedData]) -> None:
        json_data = []

        for current_data in data_list:
            json_data.append({
                "action": FileAction.get_internal_name(current_data.action),
                "time": current_data.time.isoformat(),
                "path": current_data.path,
                "pid": current_data.pid,
                "process_name": current_data.process_name
            })

        with open(path, "w", encoding="utf-8") as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)


class XmlExporter(ExporterBase):
    def get_id(self) -> str:
        return "xml"

    def get_name(self) -> str:
        return "XML"

    def get_file_filter(self) -> str:
        return QCoreApplication.translate("Exporter", "XML files") + " (*.xml)"

    def export_data(self, path: str, data_list: list[FileChangedData]) -> None:
        root = ET.Element("actions")

        for current_data in data_list:
            action_element = ET.SubElement(root, "action")

            name_element = ET.SubElement(action_element, "name")
            name_element.text = FileAction.get_internal_name(current_data.action)

            time_element = ET.SubElement(action_element, "time")
            time_element.text = current_data.time.isoformat()

            path_element = ET.SubElement(action_element, "path")
            path_element.text = current_data.path

            pid_element = ET.SubElement(action_element, "name")
            pid_element.text = str(current_data.pid)

            process_name_element = ET.SubElement(action_element, "process_name")
            process_name_element.text = current_data.process_name

        tree = ET.ElementTree(root)
        ET.indent(tree, space="\t", level=0)
        tree.write(path)


def get_all_exporter() -> list[ExporterBase]:
    return [
        CsvExporter(),
        JsonExporter(),
        XmlExporter(),
    ]
