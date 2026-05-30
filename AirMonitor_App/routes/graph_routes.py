from flask import Blueprint, render_template, request, session, redirect
from AirMonitor_App.models.network import get_coordinates, get_air_data


def create_graph_routes(monitor):
    graph_bp = Blueprint('graph', __name__)

    @graph_bp.route('/graph')
    def graph_page():

        if 'user' not in session:
            return redirect('/login')

        city = request.args.get('city', '').strip()
        start_date = request.args.get('start_date', '').strip()
        end_date = request.args.get('end_date', '').strip()
        selected_params = request.args.getlist('params') or ['pm10', 'pm25']

        data = []
        city_name = city

        if city:
            coords = get_coordinates(city)
            if coords:
                lat, lon, city_name = coords
                data = get_air_data(lat, lon, start_date, end_date)

        return render_template('graph.html',
                               data=data,
                               city=city_name,
                               selected_params=selected_params,
                               start_date=start_date,
                               end_date=end_date)

    return graph_bp