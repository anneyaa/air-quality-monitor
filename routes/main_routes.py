from flask import Blueprint, render_template, request, session
from datetime import date

def create_main_routes(monitor):
    main_bp = Blueprint('main', __name__)

    @main_bp.route('/')
    def index():
        return render_template('index.html', measurements=[], warnings=[])

    @main_bp.route('/refresh')
    def refresh():
        city = request.args.get('city', '').strip()
        start_date = request.args.get('start_date', '').strip()
        end_date = request.args.get('end_date', '').strip()

        if not city:
            return render_template('index.html', measurements=[], warnings=["Введите название города"])

        today_str = date.today().isoformat()
        if not start_date: start_date = today_str
        if not end_date: end_date = today_str

        success, warnings = monitor.fetch_from_api(city=city, start_date=start_date, end_date=end_date)

        return render_template('index.html',
                               measurements=monitor.data,
                               warnings=warnings,
                               city=city,
                               start_date=start_date,
                               end_date=end_date)

    return main_bp