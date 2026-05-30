from flask import Blueprint, render_template, request, session, redirect

def create_sort_routes(monitor):
    sort_bp = Blueprint('sort', __name__)

    @sort_bp.route('/sort')
    def sort_page():
        if 'user' not in session:
            return redirect('/login')

        city = request.args.get('city', '').strip()
        start_d = request.args.get('start_date', '').strip()
        end_d = request.args.get('end_date', '').strip()

        f_type = request.args.get('f_type', 'pm10')
        f_min = request.args.get('f_min', '').strip()
        f_max = request.args.get('f_max', '').strip()
        s_by = request.args.get('s_by', 'date')
        s_order = request.args.get('s_order', 'desc')

        measurements, warnings = [], []

        if city and start_d and end_d:
            measurements, warnings = monitor.fetch_and_analyze(
                city, start_d, end_d, f_type, f_min, f_max, s_by, s_order
            )

        return render_template('sort.html',
                               measurements=measurements,
                               warnings=warnings,
                               city=city,
                               start_date=start_d,
                               end_date=end_d,
                               f_type=f_type,
                               f_min=f_min,
                               f_max=f_max,
                               s_by=s_by,
                               s_order=s_order)

    return sort_bp