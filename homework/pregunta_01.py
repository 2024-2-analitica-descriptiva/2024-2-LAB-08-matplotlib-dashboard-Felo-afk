# pylint: disable=line-too-long
"""
Escriba el codigo que ejecute la accion solicitada.
"""
import glob
import os
import pandas as pd
import matplotlib.pyplot as plt


def pregunta_01():
    """
    El archivo `files//shipping-data.csv` contiene información sobre los envios
    de productos de una empresa. Cree un dashboard estático en HTML que
    permita visualizar los siguientes campos:

    * `Warehouse_block`

    * `Mode_of_Shipment`

    * `Customer_rating`

    * `Weight_in_gms`

    El dashboard generado debe ser similar a este:

    https://github.com/jdvelasq/LAB_matplotlib_dashboard/blob/main/shipping-dashboard-example.png

    Para ello, siga las instrucciones dadas en el siguiente video:

    https://youtu.be/AgbWALiAGVo

    Tenga en cuenta los siguientes cambios respecto al video:

    * El archivo de datos se encuentra en la carpeta `data`.

    * Todos los archivos debe ser creados en la carpeta `docs`.

    * Su código debe crear la carpeta `docs` si no existe.

    """

    def load_data(dir):
        for archivo in glob.glob(os.path.join(dir, "*.csv")):
            return pd.read_csv(archivo, sep=",", index_col=0)

    def create_visual_for_shipping_per_warehouse(df, output_dir):
        df = df.copy()
        plt.figure()
        counts = df.Warehouse_block.value_counts()
        counts.plot.bar(
            title="Shipping per Warehouse",
            xlabel="Warehouse block",
            ylabel="Record Count",
            color="tab:blue",
            fontsize=8,
        )
        plt.gca().spines["top"].set_visible(False)
        plt.gca().spines["right"].set_visible(False)
        plt.savefig(os.path.join(output_dir, "shipping_per_warehouse.png"))

    def create_mode_of_shipment(df, output_dir):
        plt.figure()
        plt.title("Mode of shipment", fontsize=16)
        counts = df.Mode_of_Shipment.value_counts()
        counts.plot.pie(
            wedgeprops=dict(width=0.35),
            ylabel="",
            color=["tab:blue", "tab:orange", "tab:green"],
        )
        plt.savefig(os.path.join(output_dir, "mode_of_shipment.png"))

    def create_visual_for_average_rate_customer(df, output_dir):
        df = (
            df[["Mode_of_Shipment", "Customer_rating"]]
            .groupby("Mode_of_Shipment")
            .describe()
        )
        df.columns = df.columns.droplevel()
        df = df[["mean", "min", "max"]]
        plt.figure()
        plt.title("Average customer rate", fontsize=16)
        plt.gca().spines["top"].set_visible(False)
        plt.gca().spines["right"].set_visible(False)
        plt.gca().spines["left"].set_color("dimgray")
        plt.gca().spines["bottom"].set_color("dimgray")
        plt.barh(
            y=df.index.values,
            width=df["max"] - 1,
            left=df["min"].values,
            height=0.9,
            color="lightgray",
            alpha=0.8,
        )
        colors = ["tab:green" if v >= 30 else "tab:orange" for v in df["mean"].values]
        plt.barh(
            y=df.index.values,
            width=df["mean"].values - 1,
            left=df["min"].values,
            height=0.5,
            color=colors,
            alpha=1.0,
        )

        plt.savefig(os.path.join(output_dir, "average_customer_rating.png"))

    def create_visual_for_weight_distribution(df, output_dir):
        plt.figure()
        plt.title("Distribución del peso del envío", fontsize=16)
        plt.gca().spines["top"].set_visible(False)
        plt.gca().spines["right"].set_visible(False)

        df.Weight_in_gms.plot.hist(
            color="tab:orange",
            edgecolor="white",
        )
        plt.savefig(os.path.join(output_dir, "weight_distribution.png"))

    def html_page(output_dir):
        # retorna un string con el contenido del archivo HTML
        pagina = f"""
        <!DOCTYPE html>
        <html>
            <head>
                <title>Dashboard de envios</title>
            </head>
            <body>
                <h1 style="text-align:center">Dashboard de envios</h1>
                <div style = "width:45%;float:left">
                    <img src="shipping_per_warehouse.png" alt=Fig 1>
                    <img src="create_mode_of_shipment.png" alt=Fig 2>
                </div>
                <div style = "width:45%;float:left">
                    <img src="create_visual_for_average_rate_customer.png" alt=Fig 3>
                    <img src="create_visual_for_weight_distribution.png" alt=Fig 4>
                </div>
            </body>
        </html>
        """
        with open(f"{output_dir}/index.html", "w") as archivo:
            archivo.write(pagina)

    input_dir = "files/input"
    output_dir = "docs"

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    data = load_data(input_dir)
    df = data.copy()

    create_visual_for_shipping_per_warehouse(df, output_dir)
    create_mode_of_shipment(df, output_dir)
    create_visual_for_average_rate_customer(df, output_dir)
    create_visual_for_weight_distribution(df, output_dir)
    html_page(output_dir)


pregunta_01()
