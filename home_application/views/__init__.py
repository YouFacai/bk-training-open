from home_application.views.common_view import (  # noqa
    get_all_bk_users,
    get_holidays,
    get_workday_info,
    home,
)
from home_application.views.daily import (  # noqa
    check_yesterday_daily,
    daily_report,
    delete_evaluate_daily,
    evaluate_daily,
    get_prefect_dailys,
    get_reports_dates,
    list_member_daily,
    notice_non_report_users,
    report_filter,
    send_evaluate_all,
    update_daily_perfect_status,
    update_evaluate_daily,
)
from home_application.views.free_time import (  # noqa
    free_time_get_post,
    free_time_patch_delete,
    group_free_time,
    user_free_time,
)
from home_application.views.group import (  # noqa
    add_group,
    add_user,
    apply_for_group,
    check_user_in_group,
    deal_join_group,
    delete_group,
    exit_group,
    get_apply_for_group_users,
    get_available_apply_groups,
    get_group_info,
    get_group_users,
    get_user_groups,
    list_admin_group,
    list_group_admin,
    update_group,
)
from home_application.views.iam_view import get_instance_info  # noqa
from home_application.views.off_day import (  # noqa
    add_off_info,
    display_personnel_information,
    remove_off,
)
from home_application.views.user import check_user_admin, get_user  # noqa
