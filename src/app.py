from flask import Flask, render_template
from controllers import chart_controller
from models.data_model import ProcesaDatawarehouse
import pandas as pd

""" Crea datawarehouse """
ProcesaDatawarehouse()


app = Flask(__name__)
server = app.server

@app.route('/')
def index():
    return render_template('index.html', plot_div='')

@app.route('/line')
def line():
    plot_div = chart_controller.line_chart()
    return render_template('index.html', plot_div=plot_div)

@app.route('/bar')
def bar():
    plot_div = chart_controller.bar_chart()
    return render_template('index.html', plot_div=plot_div)

@app.route('/pie')
def pie():
    plot_div = chart_controller.pie_chart()
    return render_template('index.html', plot_div=plot_div)

@app.route('/map')
def map_view():
    plot_div = chart_controller.map_chart()
    return render_template('index.html', plot_div=plot_div)

@app.route('/tabla')
def tabla_view():
    table_html = chart_controller.tabla()
    return render_template('index.html', plot_div=table_html)

@app.route('/hist')
def hist_view():
    plot_div = chart_controller.histograma()
    return render_template('index.html', plot_div=plot_div)

@app.route('/bar_api')
def bar_api():
    plot_div = chart_controller.bar_api()
    return render_template('index.html', plot_div=plot_div)

if __name__ == '__main__':
    app.run_server(debug=True)