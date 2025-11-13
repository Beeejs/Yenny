from flask import Blueprint, render_template, request, flash, current_app
from data.repositories.report_repository import ReportRepository
from datetime import datetime, timedelta
from presentation.middlewares.web.login_required import login_required

web_report_bp = Blueprint("web_report", __name__)


@web_report_bp.get("/reportes")
@login_required
def list_reports():
    repo = ReportRepository()

    # Obtener parámetros de filtro
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    # Si no hay fechas, usar últimos 30 días
    if not end_date:
        end_date = datetime.now().strftime("%Y-%m-%d")
    if not start_date:
        start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

    try:
        reports = repo.get_daily_sales_report(start_date, end_date)

        # Calcular totales
        total_ventas = sum(r['ventas'] for r in reports)
        total_unidades = sum(r['unidades'] for r in reports)
        total_monto = sum(r['monto'] for r in reports)

        return render_template(
            "reports/list.html",
            reports=reports,
            start_date=start_date,
            end_date=end_date,
            total_ventas=total_ventas,
            total_unidades=total_unidades,
            total_monto=total_monto
        )
    except Exception as e:
        current_app.logger.exception(e)
        flash("No se pudieron obtener los reportes.", "danger")
        return render_template(
            "reports/list.html",
            reports=[],
            start_date=start_date,
            end_date=end_date,
            total_ventas=0,
            total_unidades=0,
            total_monto=0
        )