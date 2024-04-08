from dash import html
import dash_ag_grid as dag
from configs.server_conf import logger, results_df, metrics_df, trades_df, full_trade_df
def dmcTableComponent(id):
    rowModelType = "infinite"
    dashGridOptions = {
        # The number of rows rendered outside the viewable area the grid renders.
        "rowBuffer": 10,
        # How many blocks to keep in the store. Default is no limit, so every requested block is kept.
        "maxBlocksInCache": 1,
        "rowSelection": "multiple",
    }
    if id == "analysis-page-infinite-grid-full-trades":
        columnDefs = [{"field": col} for col in full_trade_df.columns]
    elif id == "infinite-grid-trade":
        columnDefs = [{"field": col} for col in trades_df.columns]
    elif id == "analysis-page-infinite-grid-metrics":
        columnDefs = [{"field": col} for col in metrics_df.columns]
        rowModelType = "clientSide"
        dashGridOptions = {}
    elif id == "analysis-page-infinite-grid-results":
        columnDefs = [{"field": col} for col in results_df.columns]
    else:
        logger.error("Invalid id for dmcTableComponent", id)
        raise ValueError("Invalid id for dmcTableComponent")
    AgGridConfig = {
        "id": id,
        "columnSize": "sizeToFit",
        "className": "ag-theme-alpine",
        "columnDefs": columnDefs,
        "defaultColDef": {"sortable": True},
        "rowModelType": rowModelType,
        "dashGridOptions": dashGridOptions,
    }
    if id == "analysis-page-infinite-grid-metrics":
        AgGridConfig["rowData"] = metrics_df.to_dict("records")
    return html.Div(
        [
            dag.AgGrid(style={"width": "100%", "height": "100%"}, **AgGridConfig),
            html.Div(id=f"{id}-infinite-output"),
        ],
        className="w-full h-full animate-fade-in animate-400",
    )
