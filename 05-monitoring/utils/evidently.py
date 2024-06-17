import datetime

from sklearn import datasets

from evidently.metrics import ColumnDriftMetric
from evidently.metrics import ColumnSummaryMetric
from evidently.metrics import DatasetDriftMetric
from evidently.metrics import DatasetMissingValuesMetric
from evidently.report import Report
from evidently.test_preset import DataDriftTestPreset
from evidently.test_suite import TestSuite
from evidently.ui.dashboards import CounterAgg
from evidently.ui.dashboards import DashboardPanelCounter
from evidently.ui.dashboards import DashboardPanelPlot
from evidently.ui.dashboards import PanelValue
from evidently.ui.dashboards import PlotType
from evidently.ui.dashboards import ReportFilter
from evidently.ui.remote import RemoteWorkspace
from evidently.ui.workspace import Workspace
from evidently.ui.workspace import WorkspaceBase
from evidently.ui.base import Project
from typing import Dict
import pandas as pd
import json
import requests
import numpy as np

WORKSPACE = "model_monitoring_workspace"

YOUR_PROJECT_NAME = "Ride Prediction Project"
YOUR_PROJECT_DESCRIPTION = "Monitor predictions and data quality for the ride prediction project"

def create_report(ref_data:pd.DataFrame, cur_data:pd.DataFrame) -> Report:
    ts = pd.to_datetime(cur_data['time'].dt.strftime('%Y-%m-01').values[0])

    data_drift_report = Report(
        metrics=[
            DatasetDriftMetric(),
            DatasetMissingValuesMetric(),
            ColumnDriftMetric(column_name="passenger_count", stattest="wasserstein"),
            ColumnSummaryMetric(column_name="passenger_count"),
            ColumnDriftMetric(column_name="trip_distance", stattest="wasserstein"),
            ColumnSummaryMetric(column_name="trip_distance"),
            ColumnDriftMetric(column_name="fare_amount", stattest="wasserstein"),
            ColumnSummaryMetric(column_name="fare_amount"),
            ColumnDriftMetric(column_name="total_amount", stattest="wasserstein"),
            ColumnSummaryMetric(column_name="total_amount"),
            ColumnDriftMetric(column_name="pulocationid", stattest="chisquare"),
            ColumnSummaryMetric(column_name="pulocationid"),
            ColumnDriftMetric(column_name="dolocationid", stattest="chisquare"),
            ColumnSummaryMetric(column_name="dolocationid"),
        ],
        timestamp=ts,
    )

    data_drift_report.run(reference_data=ref_data, current_data=cur_data)
    return data_drift_report


def create_test_suite(ref_data:pd.DataFrame, cur_data:pd.DataFrame) -> TestSuite:
    ts = pd.to_datetime(cur_data['time'].dt.strftime('%Y-%m-01').values[0])
    data_drift_test_suite = TestSuite(
        tests=[DataDriftTestPreset()],
        timestamp=ts,
    )

    data_drift_test_suite.run(reference_data=ref_data, current_data=cur_data)
    return data_drift_test_suite


def create_project(workspace: WorkspaceBase) -> Project:
    project = workspace.create_project(YOUR_PROJECT_NAME)
    project.description = YOUR_PROJECT_DESCRIPTION
    project.dashboard.add_panel(
        DashboardPanelCounter(
            filter=ReportFilter(metadata_values={}, tag_values=[]),
            agg=CounterAgg.NONE,
            title="Census Income Dataset (Adult)",
        )
    )
    project.dashboard.add_panel(
        DashboardPanelCounter(
            title="Model Calls",
            filter=ReportFilter(metadata_values={}, tag_values=[]),
            value=PanelValue(
                metric_id="DatasetMissingValuesMetric",
                field_path=DatasetMissingValuesMetric.fields.current.number_of_rows,
                legend="count",
            ),
            text="count",
            agg=CounterAgg.SUM,
            size=1,
        )
    )
    project.dashboard.add_panel(
        DashboardPanelCounter(
            title="Share of Drifted Features",
            filter=ReportFilter(metadata_values={}, tag_values=[]),
            value=PanelValue(
                metric_id="DatasetDriftMetric",
                field_path="share_of_drifted_columns",
                legend="share",
            ),
            text="share",
            agg=CounterAgg.LAST,
            size=1,
        )
    )
    project.dashboard.add_panel(
        DashboardPanelPlot(
            title="Dataset Quality",
            filter=ReportFilter(metadata_values={}, tag_values=[]),
            values=[
                PanelValue(metric_id="DatasetDriftMetric", field_path="share_of_drifted_columns", legend="Drift Share"),
                PanelValue(
                    metric_id="DatasetMissingValuesMetric",
                    field_path=DatasetMissingValuesMetric.fields.current.share_of_missing_values,
                    legend="Missing Values Share",
                ),
            ],
            plot_type=PlotType.LINE,
        )
    )
    project.dashboard.add_panel(
        DashboardPanelPlot(
            title="Passenger Count: Wasserstein drift distance",
            filter=ReportFilter(metadata_values={}, tag_values=[]),
            values=[
                PanelValue(
                    metric_id="ColumnDriftMetric",
                    metric_args={"column_name.name": "passenger_count"},
                    field_path=ColumnDriftMetric.fields.drift_score,
                    legend="Drift Score",
                ),
            ],
            plot_type=PlotType.BAR,
            size=1,
        )
    )
    project.dashboard.add_panel(
        DashboardPanelPlot(
            title="Trip Distance: Wasserstein drift distance",
            filter=ReportFilter(metadata_values={}, tag_values=[]),
            values=[
                PanelValue(
                    metric_id="ColumnDriftMetric",
                    metric_args={"column_name.name": "trip_distance"},
                    field_path=ColumnDriftMetric.fields.drift_score,
                    legend="Drift Score",
                ),
            ],
            plot_type=PlotType.BAR,
            size=1,
        )
    )
    project.dashboard.add_panel(
        DashboardPanelPlot(
            title="pulocationid: Wasserstein drift distance",
            filter=ReportFilter(metadata_values={}, tag_values=[]),
            values=[
                PanelValue(
                    metric_id="ColumnDriftMetric",
                    metric_args={"column_name.name": "pulocationid"},
                    field_path=ColumnDriftMetric.fields.drift_score,
                    legend="Drift Score",
                ),
            ],
            plot_type=PlotType.BAR,
            size=1,
        )
    )
    project.save()
    return project


def create_demo_project(workspace: str):
    ws = Workspace.create(workspace)
    _ = create_project(ws)

    # for i in range(0, 5):
    #     report = create_report(i=i)
    #     ws.add_report(project.id, report)

    #     test_suite = create_test_suite(i=i)
    #     ws.add_test_suite(project.id, test_suite)

def get_df_evidently_metrics(report_dict:dict) -> pd.DataFrame:
    column_name = []
    stattest_name = []
    stattest_threshold = []
    drift_score = []
    drift_detected = []
    for elem in report_dict['metrics']: # array of dicts
        if elem['metric'] == 'ColumnDriftMetric':
            column_name.append(elem['result']['column_name'])
            stattest_name.append(elem['result']['stattest_name'])
            stattest_threshold.append(elem['result']['stattest_threshold'])
            drift_score.append(elem['result']['drift_score'])
            drift_detected.append(elem['result']['drift_detected'])
    return pd.DataFrame({'column_name': column_name,
                         'stattest_name': stattest_name,
                         'stattest_threshold': stattest_threshold,
                         'drift_score': drift_score,
                         'drift_detected': drift_detected})

# the encoder helps to convert NumPy types in source data to JSON-compatible types
class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.void):
            return None

        if isinstance(obj, (np.generic, np.bool_)):
            return obj.item()

        if isinstance(obj, np.ndarray):
            return obj.tolist()

        if isinstance(obj, pd.Timestamp):
            return str(obj)
        
        return obj
    
def send_data_row(dataset_name: str, data_row: Dict) -> None:
    # print(f"Send a data item for {dataset_name}")
    # print(f"Data {data_row}")

    try:
        response = requests.post(
            f"http://evidently_service:8085/iterate/{dataset_name}",
            data=json.dumps([data_row], cls=NumpyEncoder),
            headers={"content-type": "application/json"},
        )

        if response.status_code == 200:
            print(f"Success.")

        else:
            print(
                f"Got an error code {response.status_code} for the data chunk. "
                f"Reason: {response.reason}, error text: {response.text}"
            )

    except requests.exceptions.ConnectionError as error:
        print(f"Cannot reach a metrics application, error: {error}, data: {data}")

if __name__ == "__main__":
    create_demo_project(WORKSPACE)