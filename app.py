# https://shiny.posit.co/py/docs/debug.html
# https://shiny.posit.co/py/docs/user-interfaces.html#all-together-now
# https://github.com/posit-dev/py-shiny-templates/blob/main/dashboard-tips/app-core.py
# https://www.appsilon.com/post/great-tables

import faicons as fa
import great_tables as gt
from great_tables import html, style, google_font, loc

# Load data and compute static values
from shared import app_dir, df
from shiny import App, reactive, render, ui

years = df['estimate_year'].unique().tolist()

icons = {
    "households": fa.icon_svg("house-user"),
    "housing_unit": fa.icon_svg("house"),
    "people": fa.icon_svg("people-group")
    }

# ui ----

ui.tags.link(
    rel="stylesheet",
    href="https://fonts.googleapis.com/css?family=Poppins"
),

app_ui = ui.page_sidebar(
    ui.sidebar(
        ui.input_select("year", "Select Year", years),
        ui.input_action_button("go", "Enter"),
        open="desktop",
    ),
    ui.layout_columns(
        ui.value_box(
            title = "Total Population",
            value = ui.output_ui("tot_pop"), 
            showcase = icons["people"]
        ),
         ui.value_box(
            title = "Housing Units",
            value = ui.output_ui("hu"),
            showcase = icons["housing_unit"]
        ),
        ui.value_box(
            title = "Households",
            value = ui.output_ui("hh"),
            showcase = icons["households"]
        )       
    ),
    ui.layout_columns(
        ui.card(
            ui.card_header("Estimates at a Glance"), 
            ui.output_ui("table"),
            full_screen=True
        )
    ),
    ui.include_css(app_dir / "styles.css"),
    title="OFM Estimates for the Central Puget Sound",
    fillable=True,
)

# server ----

def server(input, output, session):
    @reactive.calc
    @reactive.event(input.go)
    def select_ofm_data():
        # filter data for value boxes
        
        rec = df[df['estimate_year'] == int(input.year())].reset_index()      
        # breakpoint()
        return rec

    @render.ui
    def tot_pop():
        # extract total population value for value box

        val = select_ofm_data().loc[0, 'HHPOP'] + select_ofm_data().loc[0, 'GQPOP']
        val = "{:,}".format(round(val))
        return val

    @render.ui
    def hh():
        # extract households value for value box

        val = select_ofm_data().loc[0, 'OHU']
        val = "{:,}".format(round(val))
        return val

    @render.ui
    def hu():
        # extract housing units value for value box

        val = select_ofm_data().loc[0, 'HU']
        val = "{:,}".format(round(val))
        return val

    @reactive.calc
    def prep_table():
        # munge table before render
               
        df_clean = df

        df_clean["group"] = df_clean["publication_dim_id"].case_when([
            (df_clean["publication_dim_id"] == 11, "Intercensal"), 
            (df_clean["publication_dim_id"] == 10, "Post-censal")])

        return df_clean

    @reactive.event(input.go)
    def select_year_row():
        # identify index of row based on selected year

        df = prep_table()
        
        row = df[df["estimate_year"] == int(input.year())]
        index = row.index.item()

        return index
    
    @reactive.calc
    def gt_table():
        # prep GT table

        table = (
            gt.GT(data = prep_table())
            .cols_label(
                estimate_year = "Estimate Year",
                HU = 'Housing Unit',
                OHU = "Households",
                GQPOP = html("Group Quarters<br>Population"),
                HHPOP = html("Household<br>Population")
                )
            .fmt_number(columns=["HU", "OHU", "GQPOP", "HHPOP"], decimals=0)
            .cols_align(align="left", columns=["publication_dim_id", "estimate_year"])
            .cols_align(align="center", columns=[x for x in df.columns if x not in ["group", "publication_dim_id", "estimate_year"]])
            .tab_options(table_width="75%")
            .tab_stub(rowname_col = "estimate_year", groupname_col = "group")
            .cols_hide(columns="publication_dim_id")
            .opt_table_font(font=[google_font(name="Poppins"), "Cochin", "Serif"])
        )
        return table

    @render.ui
    def table():
        # render table. Styling based on whether 'Enter' has been clicked        

        if(input.go() >= 1):
           return gt_table().tab_style(style = style.fill(color="#E3C9E3"),
                       locations = loc.body(columns = ["HU", "OHU", "GQPOP", "HHPOP"], rows=[select_year_row()]))
        else:
            return gt_table()


app = App(app_ui, server)
