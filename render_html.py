# https://gallery.pyecharts.org/#/Pie/pie_base
import os
import numpy as np
import pandas as pd

from pyecharts import options
from pyecharts.charts import Pie, Bar
from pyecharts.faker import Faker

from database import DBField
#
# c = (
#     Pie(init_opts=opts.InitOpts(js_host="./"))
#     .add("", [list(z) for z in zip(Faker.choose(), Faker.values())])
#     .set_global_opts(title_opts=opts.TitleOpts(title="Pie-基本示例"))
#     .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
#     .render("pie_base.html")
# )


def render_df_html(df: pd.DataFrame, js_path="./js/"):
    if df.shape[0] == 0:
        return
    # 收入\支出
    df1 = df.groupby(DBField.inOutClassifier, as_index=False).sum()
    labels_inOut = df1.inOutClassifier.tolist()
    values_inout = df1.inOut.tolist()
    print(labels_inOut, values_inout)
    # 支出
    df0 = df[df[DBField.inOutClassifier] == DBField.inOutSelect[0]]
    df0 = df0.groupby(DBField.firstClassifier, as_index=False).sum()
    labels = df0.firstClassifier.tolist()
    values = df0.inOut.tolist()

    # 收入
    df2 = df[df[DBField.inOutClassifier] == DBField.inOutSelect[1]]
    df2 = df2.groupby(DBField.firstClassifier, as_index=False).sum()
    labels_in = df2.firstClassifier.tolist()
    values_in = df2.inOut.tolist()


    label_size = 20
    title_size = 25

    c = (
        Pie(init_opts=options.InitOpts(width='1000px', height='800px', js_host=js_path))
            .add("", [list(z) for z in zip(labels_inOut, values_inout)],
                 center=["20%", "20%"],
                 radius=[0, 50],
                 tooltip_opts=options.TooltipOpts(textstyle_opts=options.TextStyleOpts(font_size=label_size)))
            .add("", [list(z) for z in zip(labels, values)],
                             center=["50%", "50%"],
                             radius=[0, 200],
                             tooltip_opts=options.TooltipOpts(textstyle_opts=options.TextStyleOpts(font_size=label_size)))
            .add("", [list(z) for z in zip(labels_in, values_in)],
                 center=["20%", "80%"],
                 radius=[0, 50],
                 tooltip_opts=options.TooltipOpts(textstyle_opts=options.TextStyleOpts(font_size=label_size)))
            .set_global_opts(title_opts=options.TitleOpts(title="消费总览",
                                                          title_textstyle_opts=options.TextStyleOpts(font_size=title_size)),
                             legend_opts=options.LegendOpts(textstyle_opts=options.TextStyleOpts(font_size=label_size)))
            .set_series_opts(label_opts=options.LabelOpts(font_size=label_size))
            .render("pie_base.html")
    )


if __name__ == '__main__':
    df = pd.read_csv("./data/out.csv")
    print(df)
    render_df_html(df)