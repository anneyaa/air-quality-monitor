from flask import Blueprint, render_template, request, session, redirect

def create_compare_routes(monitor):
    compare_bp = Blueprint('compare', __name__)

    @compare_bp.route('/compare')
    def compare_page():

        if 'user' not in session:
            return redirect('/login')

        city1 = request.args.get('city1', '').strip()
        city2 = request.args.get('city2', '').strip()
        city3 = request.args.get('city3', '').strip()
        target_date = request.args.get('date', '').strip()

        results = {}
        if target_date and (city1 or city2 or city3):
            cities_to_fetch = [c for c in [city1, city2, city3] if c]
            results = monitor.fetch_for_comparison(cities_to_fetch, target_date)

        return render_template('compare.html',
                               results=results,
                               city1=city1, city2=city2, city3=city3,
                               target_date=target_date)

    return compare_bp