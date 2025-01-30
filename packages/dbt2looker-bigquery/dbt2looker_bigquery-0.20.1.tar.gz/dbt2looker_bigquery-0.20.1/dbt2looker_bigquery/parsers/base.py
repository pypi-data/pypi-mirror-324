"""Base DBT parser functionality."""

from typing import Dict, List
import logging
from dbt2looker_bigquery.models.dbt import DbtCatalog, DbtManifest, DbtModel
from dbt2looker_bigquery.parsers.catalog import CatalogParser
from dbt2looker_bigquery.parsers.exposure import ExposureParser
from dbt2looker_bigquery.parsers.model import ModelParser


class DbtParser:
    """Main DBT parser that coordinates parsing of manifest and catalog files."""

    def __init__(self, raw_manifest: Dict, raw_catalog: Dict):
        """Initialize the parser with raw manifest and catalog data."""
        # self._raw_manifest = raw_manifest
        self._catalog = DbtCatalog(**raw_catalog)
        self._manifest = DbtManifest(**raw_manifest)
        self._model_parser = ModelParser(self._manifest)
        self._catalog_parser = CatalogParser(self._catalog)
        self._exposure_parser = ExposureParser(self._manifest)

    def get_models(self, args) -> List[DbtModel]:
        """Parse dbt models from manifest and filter by criteria."""

        all_models = self._model_parser.get_all_models()

        # Get exposed models if needed
        exposed_names = None
        if (hasattr(args, "exposures_only") and args.exposures_only) or (
            hasattr(args, "exposures_tag") and args.exposures_tag
        ):
            exposed_names = self._exposure_parser.get_exposures(
                args.exposures_tag if hasattr(args, "exposures_tag") else None
            )
        if exposed_names:
            logging.debug(f"Exposures found: {len(exposed_names)}")

        # Filter models based on criteria
        filtered_models = self._model_parser.filter_models(
            all_models,
            select_model=args.select if hasattr(args, "select") else None,
            tag=args.tag if hasattr(args, "tag") else None,
            exposed_names=exposed_names,
        )

        # Process models (update with catalog info)
        processed_models = []
        nodes_without_catalogue = []
        for model in filtered_models:
            if processed_model := self._catalog_parser.process_model(model):
                processed_models.append(processed_model)
            else:
                nodes_without_catalogue.append(model.unique_id)
        logging.debug(f"Models after catalog {len(processed_models)}")
        if nodes_without_catalogue:
            logging.debug(
                f"Models without catalog information: {len(nodes_without_catalogue)}"
            )
        return processed_models
