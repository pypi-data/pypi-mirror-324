import numpy as np
import pandas as pd
import anndata as ad
import logging
import pickle
from zarr.errors import PathNotFoundError

import fractal_tasks_core
from pydantic import validate_call

from operetta_compose import io


__OME_NGFF_VERSION__ = fractal_tasks_core.__OME_NGFF_VERSION__

logger = logging.getLogger(__name__)


@validate_call
def feature_classification(
    *,
    zarr_url: str,
    classifier_path: str,
    table_name: str = "regionprops",
    label_name: str = "nuclei",
) -> None:
    """Classify cells using the [napari-feature-classifier](https://github.com/fractal-napari-plugins-collection/napari-feature-classifier) and write them to the OME-ZARR

    Args:
        zarr_url: Path to an OME-ZARR Image
        classifier_path: Path to the pickled scikit-learn classifier
        table_name: Folder name of the measured regionprobs features
        label_name: Name of the labels to use for feature measurements
    """
    with open(classifier_path, "rb") as f:
        clf = pd.read_pickle(f)

    try:
        ann_tbl = ad.read_zarr(f"{zarr_url}/tables/{table_name}")
    except PathNotFoundError:
        raise FileNotFoundError(
            f"No measurements exist at the specified zarr URL in the table {table_name}."
        )
    features = ann_tbl.to_df()
    roi_id_cols = ann_tbl.obs.drop(
        columns=["roi_id", "label", "prediction"], errors="ignore"
    )
    if "roi_id" not in ann_tbl.obs.columns:
        ann_tbl.obs["roi_id"] = f"{zarr_url}:" + roi_id_cols.astype(str).agg(
            ":".join, axis=1
        )

    # Select feature subset in expected order
    features = features[clf.get_feature_names()]

    # Add index columns
    features_with_annotations = pd.concat(
        (ann_tbl.obs[["roi_id", "label"]], features), axis=1
    )
    predictions = clf.predict(features_with_annotations).reset_index()
    ann_tbl.obs = pd.concat((roi_id_cols.reset_index(drop=True), predictions), axis=1)
    ann_tbl.obs_names = ann_tbl.obs.index.map(str)
    ann_tbl.write_zarr(f"{zarr_url}/tables/{table_name}")
    io.write_table_metadata(zarr_url, "feature_table", table_name, label_name)


if __name__ == "__main__":
    from fractal_tasks_core.tasks._utils import run_fractal_task

    run_fractal_task(
        task_function=feature_classification,
        logger_name=logger.name,
    )
