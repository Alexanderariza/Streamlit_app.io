"""
Heatmap world map
=================

Plot a heatmap of worldwide temperature data.
"""
import cdstoolbox as ct


# Plot a worldwide heatmap of temperature gridded data
@ct.application(title='Heatmap world map')
@ct.output.livefigure()
def application():
    # Retrieve surface temperature data
    data = ct.catalogue.retrieve(
        'reanalysis-era5-single-levels',
        {
            'variable': '2m_temperature',
            'grid': ['1', '1'],
            'product_type': 'reanalysis',
            'year': '2017',
            'month': '01',
            'day': '01',
            'time': '00:00',
        }
    )

    # Plot heatmap
    fig = ct.chart.heatmap(
        data,
        colorscale="viridis",
        layout_kwargs={
            'width': 1000,
            'height': 500,
            'autosize': False,
            'title': '2m air temperature',
            'xaxis': {
                'title': 'latitude',
                'tickvals': [-180., 0., 179.],
                'ticktext': ['-180.', '0.', '180.'],
                'constrain': 'domain',
                'zeroline': False
            },
            'yaxis': {
                'title': 'longitude',
                'tickvals': [-90., 0., 90.],
                'ticktext': ['-90.', '0.', '90.'],
                'scaleanchor': 'x'
            }
        },
    )

    return fig
