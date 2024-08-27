
from administrator.models import Grievance, DownloadCategory


def notification_processor(request):
    if request.user.is_authenticated:
        user_type = request.user.user_type
        recipient_id = request.user.id

        if user_type == "DISTRICT":
            grievances = Grievance.objects.filter(is_deleted=False, status='Pending', recipient_id=recipient_id)
        else:
            grievances = Grievance.objects.filter(is_deleted=False, status='Pending')

        count = grievances.count()
        return {
            'count': count,
            'notification': grievances
        }
    else:
        return {
            'download_category_list':  DownloadCategory.objects.filter(is_deleted=False)
        }
   