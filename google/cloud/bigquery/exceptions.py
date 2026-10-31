# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


class BigQueryError(Exception):
    """Base class for all custom exceptions defined by the BigQuery client."""


class LegacyBigQueryStorageError(BigQueryError):
    """Raised when too old a version of BigQuery Storage extra is detected at runtime."""


class LegacyPyarrowError(BigQueryError):
    """Raised when too old a version of pyarrow package is detected at runtime."""


class BigQueryStorageNotFoundError(BigQueryError):
    """Raised when BigQuery Storage extra is not installed when trying to
    import it.
    """


class LegacyPandasError(BigQueryError):
    """Raised when too old a version of pandas package is detected at runtime."""


class RowCheckpointError(BigQueryError):
    """Raised when a row iterator checkpoint cannot be created.

    This is raised before any checkpoint data is produced, for example when
    the iterator does not correspond to a query job, when rows are consumed
    page-by-page rather than row-by-row, or when results are downloaded with
    the BigQuery Storage API in parallel mode.
    """


class RowCheckpointRestoreError(BigQueryError):
    """Raised when iteration cannot be resumed from a row checkpoint.

    The original, unmodified checkpoint is preserved on the ``checkpoint``
    attribute so that callers can inspect it, persist it again or retry
    after fixing the underlying problem.

    Args:
        message: Description of the restore failure.
        checkpoint: The original checkpoint value (a
            :class:`~google.cloud.bigquery.table.RowCheckpoint`, dict or JSON
            string), as passed by the caller. Never modified.
    """

    def __init__(self, message, checkpoint=None):
        super().__init__(message)
        self.checkpoint = checkpoint


class RowCheckpointSchemaMismatchError(RowCheckpointRestoreError):
    """Raised when the current result schema does not match the checkpoint."""


class RowCheckpointResultsUnavailableError(RowCheckpointRestoreError):
    """Raised when the referenced job or its cached results cannot be read.

    This covers jobs that no longer exist as well as query results that have
    expired or whose destination table has been deleted.
    """


class RowCheckpointUnsupportedModeError(RowCheckpointRestoreError):
    """Raised when a checkpoint cannot be used with the requested read mode.

    Examples include checkpoints produced from a ``tabledata.list`` iteration
    (i.e. without a corresponding query job) and attempts to resume with the
    BigQuery Storage API parallel reader.
    """
