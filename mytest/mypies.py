# https://gallery.pyecharts.org/#/Pie/pie_base
import os
import numpy as np
import pandas as pd

from pyecharts import options
from pyecharts.charts import Pie, Bar
from pyecharts.faker import Faker
#
# c = (
#     Pie(init_opts=opts.InitOpts(js_host="./"))
#     .add("", [list(z) for z in zip(Faker.choose(), Faker.values())])
#     .set_global_opts(title_opts=opts.TitleOpts(title="Pie-基本示例"))
#     .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
#     .render("pie_base.html")
# )


def render_df_html(df: pd.DataFrame, js_path="./js/"):
    labels = df.firstClassifier.tolist()
    values = df.inOut.tolist()
    print("render_df_html")

    c = (
        Pie(init_opts=options.InitOpts(width='1000px', height='800px', js_host=js_path))
             #.add("", [list(z) for z in zip(Faker.choose(), Faker.values())])
            .add("", [list(z) for z in zip(labels, values)])
            .set_global_opts(title_opts=options.TitleOpts(title="消费总览"))
            .set_series_opts(label_opts=options.LabelOpts(),
                             center=["50%", "50%"], radius=[0, 200])
            .render("pie_base.html")
    )


if __name__ == '__main__':
    df = pd.read_csv("../data/out.csv")
    print(df)
    render_df_html(df)