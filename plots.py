import pandas as pd
import altair as alt

alt.data_transformers.enable("vegafusion")


def spectra_plot(df, x, y, color, ruler=False):
    """Plot spectra viewer"""

    selection = alt.selection_point(fields=[color], bind='legend')
    specView = alt.Chart(df).mark_line(interpolate='basis').encode(
        x=x,
        y=y,
        color=color,
        opacity=alt.condition(selection, alt.value(1), alt.value(0.1)),
        tooltip=[x, y] if ruler else df.columns.tolist()
    ).add_params(
        selection
    )

    if ruler:
        reduced_df = pd.DataFrame(df[x].unique(), columns=[x])

        # Create a selection that chooses the nearest point & selects based on x-value
        nearest = alt.selection_point(nearest=True, on='mouseover',
                                fields=[x], empty=False)
        
        # Transparent selectors across the chart. This is what tells us
        # the x-value of the cursor
        selectors = alt.Chart(reduced_df).mark_point().encode(
            x=x,
            opacity=alt.value(0),
        ).add_params(
            nearest
        )

        # Draw points on the line, and highlight based on selection
        points = specView.mark_point().encode(
            opacity=alt.condition(nearest, alt.value(1), alt.value(0))
        )

        # # Draw text labels near the points, and highlight based on selection
        # text = specView.mark_text(align='left', dx=5, dy=-5).encode(
        #     text=alt.condition(nearest, y, alt.value(' '))
        # )

        # Draw a rule at the location of the selection
        rule = alt.Chart(reduced_df).mark_rule(color='gray').encode(
            x=x,
        ).transform_filter(
            nearest
        )

    # Put the five layers into a chart and bind the data
    plot = alt.layer(
        # possible to add text as last layer to show y value per line:
        specView, selectors, points, rule  # type: ignore
        ) if ruler else specView
    return plot.configure_legend(
        # orient='bottom',
        labelLimit=0,
    ).interactive(
    # ).properties(
    #     width=1400, height=600
    )


def metadata_viewer(df, analysis='Raman', treatment='bio', region='VLFR'):
    """Display metadata in a heatmap"""
    df = df.loc[(df.Region == region)]
    col_name = analysis + ' ' + treatment

    highlight = alt.selection_point()
    
    base = alt.Chart(df.reset_index()).encode(
        x=alt.X('Exposure_days:N', scale=alt.Scale(paddingInner=0.2), axis=alt.Axis(tickSize=0, domain=False)),
        y=alt.Y('Polymer:N', scale=alt.Scale(paddingInner=0.2), axis=alt.Axis(tickSize=0, domain=False, title=None)),
    )

    heatmap = base.mark_square(size=300, opacity=0.6).encode(
        color=alt.Color(col_name, type='quantitative', scale=alt.Scale(scheme='yellowgreen')),
        opacity=alt.condition(highlight, alt.value(0.8), alt.value(0.2)),
        tooltip=['count(Polymer_ID)', 'Supplier', 'Product_ID', 'Specifications'],
    )

    numbers = base.mark_text(baseline='middle', dy=1, fontSize=14, font='sans'
    ).encode(
        text=col_name,
        opacity=alt.condition(highlight, alt.value(0.8), alt.value(0.2)),
    )

    chart = alt.layer(heatmap, numbers).interactive().facet(
        column=alt.Column('Campaign:N', sort=['Summer', 'Autumn', 'Winter', 'Spring', 'Longterm', 'Insitu']),
        row='State:N'
    ).configure_facet(
        spacing=20
    ).configure_view(
        stroke=None
    ).add_params(
        highlight
    )
    return chart
