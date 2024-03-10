from flask import Blueprint, request, jsonify
from provider.stats.parent_stats import ReportServiceParent
from provider.stats.child_stats import ReportServiceChild

report_router = Blueprint("/reports", __name__)


@report_router.route("/reports", methods=["GET"])
def get_report():
    pid = request.args.get("pid")

    # 부모 통계 불러오기 #
    pd_Report = ReportServiceParent(pid)
    pd_day1_report = pd_Report.get_day1_report(pid)
    pd_day7_report = pd_Report.get_day7_report(pid)
    pd_day30_report = pd_Report.get_day30_report(pid)

    # 아이 통계 불러오기 #
    cd_Report = ReportServiceChild(pid)
    cd_day1_report = cd_Report.get_day1_report(pid)
    cd_day7_report = cd_Report.get_day7_report(pid)
    cd_day30_report = cd_Report.get_day30_report(pid)

    return jsonify(
        {
            "pd_day1_report": pd_day1_report,
            "pd_day7_report": pd_day7_report,
            "pd_day30_report": pd_day30_report,
            "cd_day1_report": cd_day1_report,
            "cd_day7_report": cd_day7_report,
            "cd_day30_report": cd_day30_report,
        }
    )
