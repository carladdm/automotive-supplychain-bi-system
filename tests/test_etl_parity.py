"""Parity tests for data transformations."""

import numpy as np
import pandas as pd
from src.etl import AutopartsETL


def test_precio_compra_imputation() -> None:
    """Verifica que el merge e imputación de compras emule a Power Query."""
    raw_compras = pd.DataFrame(
        {
            "ProductoID": [1, 2],
            "CantidadCompra": [10, 5],
            "PrecioCompra": [np.nan, 20.0],
        }
    )
    raw_productos = pd.DataFrame(
        {
            "ProductoID": [1, 2],
            "Precio_Compra": [15.0, 20.0],
            "Precio_Venta": [30.0, 40.0],
        }
    )

    pipeline = AutopartsETL()
    data = {"compras": raw_compras, "productos": raw_productos}
    transformed = pipeline.transform(data)

    clean_compras = transformed["compras"]
    clean_productos = transformed["productos"]

    # Imputación de nulo
    assert (
        clean_compras.loc[clean_compras["ProductoID"] == "1", "PrecioCompra"].values[0]
        == 15.0
    )
    # Costo total calculado
    assert (
        clean_compras.loc[
            clean_compras["ProductoID"] == "1", "CostoTotalCompra"
        ].values[0]
        == 150.0
    )
    # Clasificación de margen
    assert (
        clean_productos.loc[
            clean_productos["ProductoID"] == "1", "ClasificacionRentabilidad"
        ].values[0]
        == "Baja"
    )
