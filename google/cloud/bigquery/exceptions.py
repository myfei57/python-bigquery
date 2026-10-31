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


class JsonBatchLoadError(BigQueryError):
    """Raised when a single batch fails in a batched JSON load.

    Raised by
    :meth:`~google.cloud.bigquery.client.Client.load_table_from_json_iterator`
    when the load job of a batch could not be started or did not finish
    successfully. The batch metadata allows the caller to replay just the
    affected batch using the rows it retained for that batch.

    Args:
        batch_number (int):
            Zero-based number of the failing batch.
        input_row_range (range):
            Half-open ``range`` of the global input row indices contained in
            the failing batch, e.g. ``range(100, 200)`` means global input
            rows 100 through 199.
        job_id (str):
            The deterministic job ID used for the batch. Replaying the batch
            with the same job ID does not create a duplicate job on the server.
        message (Optional[str]):
            Optional explicit error message. If not given, one is generated
            from the other arguments.

    Attributes:
        batch_number (int): Zero-based number of the failing batch.
        input_row_range (range): Global input row range of the failing batch.
        job_id (str): Job ID used for the failing batch.
    """

    def __init__(self, batch_number, input_row_range, job_id, message=None):
        self.batch_number = batch_number
        self.input_row_range = input_row_range
        self.job_id = job_id

        if message is None:
            message = (
                "Load job {!r} for batch {} (global input rows {}..{}) failed. "
                "Replay this single batch with the retained rows and the same "
                "job ID to retry it.".format(
                    job_id,
                    batch_number,
                    input_row_range.start,
                    input_row_range.stop - 1,
                )
            )

        super().__init__(message)
