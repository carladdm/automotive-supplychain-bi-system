"""Automotive Parts Supply Chain ETL Pipeline.

Extracts sales, procurement, and inventory movements from relational tables,
flat CSV files, and JSON payloads. Imputes missing procurement prices via
catalog foreign-key matching, calculates margins, and exports sanitized datasets.
"""

import json
import logging
from pathlib import Path
from typing import Dict

import numpy as np
import pandas as pd

from src.config import DATA_PROCESSED_DIR, DATA_RAW_DIR

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)


class AutopartsETL:
    """Orchestrates end-to-end extraction, transformation, and staging."""

    def __init__(
        self,
        raw_dir: Path = DATA_RAW_DIR,
        processed_dir: Path = DATA_PROCESSED_DIR,
    ) -> None:
        self.raw_dir = raw_dir
        self.processed_dir = processed_dir
        self.processed_dir.mkdir(parents=True, exist_ok=True)

    def extract(self) -> Dict[str, pd.DataFrame]:
        """Ingests structured datasets from disk."""
        logging.info("Starting ingestion from %s...", self.raw_dir)
        tables = [
            "productos",
            "compras",
            "proveedores",
            "ventas",
            "clientes",
            "vendedores",
            "ubicaciones",
            "categorias",
        ]
        data: Dict[str, pd.DataFrame] = {}

        for table in tables:
            csv_path = self.raw_dir / f"{table}.csv"
            if csv_path.exists():
                data[table] = pd.read_csv(csv_path)
            else:
                data[table] = pd.DataFrame()

        json_path = self.raw_dir / "movimientosinventario.json"
        if json_path.exists():
            with open(json_path, "r", encoding="utf-8") as file:
                raw_json = json.load(file)
            data["movimientosinventario"] = pd.json_normalize(raw_json)
        else:
            data["movimientosinventario"] = pd.DataFrame()

        return data

    def transform(self, data: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
        """Resolves missing pricing and calculates analytical fields."""
        logging.info("Applying domain transformations and imputations...")
        transformed = {k: v.copy() for k, v in data.items()}

        compras = transformed.get("compras", pd.DataFrame())
        productos = transformed.get("productos", pd.DataFrame())

        if (
            not compras.empty
            and not productos.empty
            and "PrecioCompra" in compras.columns
        ):
            compras["ProductoID"] = compras["ProductoID"].astype(str)
            productos["ProductoID"] = productos["ProductoID"].astype(str)

            compras = compras.merge(
                productos[["ProductoID", "Precio_Compra"]],
                on="ProductoID",
                how="left",
            )
            compras["PrecioCompra"] = compras["PrecioCompra"].fillna(
                compras["Precio_Compra"]
            )
            compras.drop(columns=["Precio_Compra"], inplace=True)

            if "CantidadCompra" in compras.columns:
                compras["CostoTotalCompra"] = (
                    compras["CantidadCompra"] * compras["PrecioCompra"]
                )
            transformed["compras"] = compras

        if (
            not productos.empty
            and "Precio_Venta" in productos.columns
            and "Precio_Compra" in productos.columns
        ):
            productos["MargenProducto"] = (
                productos["Precio_Venta"] - productos["Precio_Compra"]
            )
            productos["MargenPct"] = (
                productos["MargenProducto"] / productos["Precio_Venta"]
            ) * 100
            productos["ClasificacionRentabilidad"] = np.where(
                productos["MargenProducto"] >= 50,
                "Alta",
                np.where(productos["MargenProducto"] >= 20, "Media", "Baja"),
            )
            transformed["productos"] = productos

        return transformed

    def load(self, data: Dict[str, pd.DataFrame]) -> None:
        """Saves clean dataframes to processed directory."""
        for name, df in data.items():
            if not df.empty:
                dest = self.processed_dir / f"{name}_clean.csv"
                df.to_csv(dest, index=False)
                logging.info("Exported clean table: %s", dest)


def main() -> None:
    pipeline = AutopartsETL()
    raw_tables = pipeline.extract()
    cleaned_tables = pipeline.transform(raw_tables)
    pipeline.load(cleaned_tables)


if __name__ == "__main__":
    main()
