from pyecharts import options as opts
from pyecharts.charts import Pie, Bar
from pyecharts.commons.utils import JsCode
from pyecharts.faker import Faker



c = (
    Pie(init_opts=opts.InitOpts(width='1000px', height='800px', js_host="./"))
    .add("", [list(z) for z in zip(Faker.choose(), Faker.values())],
         label_opts=opts.LabelOpts(formatter="{b}: {c}"),
         center=["30%", "20%"], radius=[0, 100])
    .add("", [list(z) for z in zip(Faker.choose(), Faker.values())],
             label_opts=opts.LabelOpts(formatter="{b}: {c}"),
             center=["30%", "50%"], radius=[0, 100])
    .add("", [list(z) for z in zip(Faker.choose(), Faker.values())],
             label_opts=opts.LabelOpts(formatter="{b}: {c}"),
             center=["30%", "80%"], radius=[0, 100])
    .set_global_opts(
        title_opts=opts.TitleOpts(title="Pie-多饼图基本示例"),
        legend_opts=opts.LegendOpts(
            type_="scroll", pos_top="20%", pos_left="80%", orient="vertical"
        ),
    )
    .render("multiple_pie.html")
)
