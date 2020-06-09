#!/usr/bin/env python3
# thoth-metrics
# Copyright(C) 2018, 2019, 2020 Christoph Görn, Francesco Murdaca, Fridolin Pokorny
#
# This program is free software: you can redistribute it and / or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""Qeb-Hwt metrics."""

import logging
import os
from datetime import datetime

import thoth.metrics_exporter.metrics as metrics

from prometheus_api_client import PrometheusConnect

from .base import register_metric_job
from .base import MetricsBase
from .argo_workflows import ArgoWorkflowsMetrics
from ..configuration import Configuration

_LOGGER = logging.getLogger(__name__)


class QebHwtMetrics(MetricsBase):
    """Class to evaluate Metrics for Qeb-Hwt Outer Workflow."""

    @classmethod
    @register_metric_job
    def get_workflow_status(cls) -> None:
        """Get the workflow status for each workflow."""
        ArgoWorkflowsMetrics().get_thoth_workflows_status_per_namespace_per_label(
            label_selector="component=qeb-hwt", namespace=Configuration.THOTH_BACKEND_NAMESPACE
        )

    @classmethod
    @register_metric_job
    def get_qebhwt_quality(cls) -> None:
        """Get the quality for thamos advise workflows."""
        ArgoWorkflowsMetrics().get_workflow_quality(
            service_name="qeb-hwt",
            prometheus=Configuration.PROM,
            instance=Configuration.WORKFLOW_CONTROLLER_INSTANCE_BACKEND_NAMESPACE,
            namespace=Configuration.THOTH_BACKEND_NAMESPACE,
            metric_type=metrics.workflow_qebhwt_quality,
        )
